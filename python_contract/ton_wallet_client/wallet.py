"""
Wallet management and operations.
"""

import hashlib
import struct
from dataclasses import dataclass
from typing import Optional

from .error import SignatureError, ConfigurationError
from .types import Address, KeyPair, TransferParams


@dataclass
class TransferMessage:
    """
    Represents a transfer message ready for signing.

    Attributes:
        seqno: Sequence number for replay protection
        valid_until: Message expiration timestamp
        send_mode: Send mode flags
        destination: Destination address
        amount: Amount in nanoTON
        comment: Optional comment
    """

    seqno: int
    valid_until: int
    send_mode: int
    destination: Address
    amount: int
    comment: Optional[str] = None

    def to_bytes(self) -> bytes:
        """
        Serialize the message for hashing.

        Returns the binary representation of the message.
        """
        parts = []

        # Sequence number (32 bits, big-endian)
        parts.append(struct.pack(">I", self.seqno))

        # Valid until (32 bits, big-endian)
        parts.append(struct.pack(">I", self.valid_until))

        # Send mode (8 bits)
        parts.append(struct.pack("B", self.send_mode))

        # Destination workchain (8 bits, signed)
        parts.append(struct.pack("b", self.destination.workchain))

        # Destination address (256 bits)
        parts.append(self.destination.raw)

        # Amount (64 bits, big-endian)
        parts.append(struct.pack(">Q", self.amount))

        # Comment (if present)
        if self.comment:
            parts.append(self.comment.encode("utf-8"))

        return b"".join(parts)

    def hash(self) -> bytes:
        """
        Compute the hash of this message for signing.

        Uses SHA-256 as required by TON blockchain for message signing.

        Returns:
            32-byte hash
        """
        message_bytes = self.to_bytes()
        return hashlib.sha256(message_bytes).digest()


class Wallet:
    """
    Represents a TON wallet with signing capabilities.

    Attributes:
        address: Wallet address
        key_pair: Key pair for signing (optional - None for read-only wallets)
        seqno: Current sequence number (cached)
    """

    def __init__(self, address: Address, key_pair: Optional[KeyPair] = None):
        """
        Create a new wallet with the given address and optional key pair.

        Args:
            address: Wallet address
            key_pair: Optional key pair for signing
        """
        self._address = address
        self._key_pair = key_pair
        self._seqno = 0

    @classmethod
    def read_only(cls, address: Address) -> "Wallet":
        """Create a read-only wallet (for querying state only)."""
        return cls(address, None)

    @property
    def address(self) -> Address:
        """Get the wallet address."""
        return self._address

    @property
    def can_sign(self) -> bool:
        """Check if this wallet can sign transactions."""
        return self._key_pair is not None

    @property
    def public_key(self) -> Optional[bytes]:
        """Get the public key if available."""
        if self._key_pair:
            return self._key_pair.public_key
        return None

    @property
    def seqno(self) -> int:
        """Get the current sequence number."""
        return self._seqno

    @seqno.setter
    def seqno(self, value: int):
        """Update the cached sequence number."""
        self._seqno = value

    def create_transfer_message(self, params: TransferParams) -> TransferMessage:
        """
        Create a transfer message for signing.

        This method creates the message structure that needs to be signed
        for a transfer operation. The actual signing and sending is done
        by the WalletClient.

        Args:
            params: Transfer parameters

        Returns:
            TransferMessage ready for signing

        Raises:
            SignatureError: If wallet cannot sign (no key pair)
        """
        if not self.can_sign:
            raise SignatureError()

        return TransferMessage(
            seqno=self._seqno,
            valid_until=params.valid_until,
            send_mode=params.send_mode,
            destination=params.to,
            amount=params.amount,
            comment=params.comment,
        )

    def sign(self, message_hash: bytes) -> bytes:
        """
        Sign a message hash using the wallet's private key.

        Returns a 64-byte signature.

        Security Note:
            This is a PLACEHOLDER implementation for demonstration purposes.
            In production, you should use the `pynacl` or `ed25519` library
            for proper Ed25519 signing as required by TON:

            >>> from nacl.signing import SigningKey
            >>> signing_key = SigningKey(secret_key_bytes)
            >>> signed = signing_key.sign(message_hash)

        Args:
            message_hash: 32-byte message hash to sign

        Returns:
            64-byte signature

        Raises:
            SignatureError: If wallet cannot sign
        """
        if not self._key_pair:
            raise SignatureError()

        if len(message_hash) != 32:
            raise ValueError("Message hash must be 32 bytes")

        # PLACEHOLDER: In production, use pynacl for proper signing
        # Using random bytes to avoid predictable signatures
        # DO NOT USE IN PRODUCTION - this is not cryptographically secure
        import os
        signature = os.urandom(64)

        return signature


class WalletBuilder:
    """Builder for creating wallets."""

    def __init__(self):
        """Create a new wallet builder."""
        self._address: Optional[Address] = None
        self._key_pair: Optional[KeyPair] = None

    def address(self, address: Address) -> "WalletBuilder":
        """Set the wallet address."""
        self._address = address
        return self

    def key_pair(self, key_pair: KeyPair) -> "WalletBuilder":
        """Set the key pair for signing."""
        self._key_pair = key_pair
        return self

    def build(self) -> Wallet:
        """
        Build the wallet.

        Returns:
            Configured Wallet instance

        Raises:
            ConfigurationError: If address is not set
        """
        if not self._address:
            raise ConfigurationError("Wallet address is required")

        return Wallet(self._address, self._key_pair)
