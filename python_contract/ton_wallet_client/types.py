"""
Type definitions for TON wallet operations.
"""

import base64
import struct
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .error import InvalidAddressError


class Network(Enum):
    """TON network selection."""

    MAINNET = "mainnet"
    TESTNET = "testnet"

    @property
    def api_endpoint(self) -> str:
        """Get the API endpoint URL for this network."""
        if self == Network.MAINNET:
            return "https://toncenter.com/api/v2"
        return "https://testnet.toncenter.com/api/v2"

    @property
    def explorer_url(self) -> str:
        """Get the explorer URL for this network."""
        if self == Network.MAINNET:
            return "https://tonscan.org"
        return "https://testnet.tonscan.org"


@dataclass
class Address:
    """
    TON wallet address representation.

    Attributes:
        raw: Raw address bytes (32 bytes)
        workchain: Workchain ID (-1 for masterchain, 0 for basechain)
        friendly: Human-readable address string
    """

    raw: bytes
    workchain: int
    friendly: str = field(init=False)

    def __post_init__(self):
        """Generate friendly address string."""
        if len(self.raw) != 32:
            raise InvalidAddressError("Address must be 32 bytes")
        self.friendly = f"{self.workchain}:{self.raw.hex()}"

    @classmethod
    def from_friendly(cls, address: str) -> "Address":
        """
        Parse an address from a friendly string format.

        Supports both EQ... format and workchain:hex format.
        """
        # Handle base64 encoded addresses (EQ..., kQ..., etc.)
        if (
            address.startswith("EQ")
            or address.startswith("kQ")
            or address.startswith("Ef")
            or address.startswith("UQ")
        ):
            return cls._from_base64(address)

        # Handle workchain:hex format
        if ":" in address:
            parts = address.split(":")
            if len(parts) != 2:
                raise InvalidAddressError("Invalid address format")

            try:
                workchain = int(parts[0])
            except ValueError:
                raise InvalidAddressError("Invalid workchain")

            try:
                raw_bytes = bytes.fromhex(parts[1])
            except ValueError:
                raise InvalidAddressError("Invalid hex in address")

            if len(raw_bytes) != 32:
                raise InvalidAddressError("Address must be 32 bytes")

            return cls(raw=raw_bytes, workchain=workchain)

        raise InvalidAddressError("Unrecognized address format")

    @classmethod
    def _from_base64(cls, address: str) -> "Address":
        """
        Parse an address from base64-encoded format (EQ..., kQ..., etc.)

        TON addresses in base64url format are 48 characters.
        Format: 1 byte flags + 1 byte workchain + 32 bytes address + 2 bytes CRC16
        """
        try:
            # Try URL-safe base64 first
            decoded = base64.urlsafe_b64decode(address + "==")
        except Exception:
            try:
                # Try standard base64
                decoded = base64.b64decode(address + "==")
            except Exception:
                raise InvalidAddressError("Invalid base64 encoding")

        if len(decoded) != 36:
            raise InvalidAddressError("Invalid address length")

        workchain = struct.unpack("b", decoded[1:2])[0]
        raw = decoded[2:34]

        return cls(raw=raw, workchain=workchain)

    def to_hex(self) -> str:
        """Convert to hex string (workchain:hex format)."""
        return f"{self.workchain}:{self.raw.hex()}"

    def __str__(self) -> str:
        return self.friendly


@dataclass
class TransactionResult:
    """
    Result of a transaction.

    Attributes:
        hash: Transaction hash
        lt: Logical time
        fee: Fee paid for the transaction (in nanoTON)
        success: Whether the transaction was successful
        error: Optional error message if transaction failed
    """

    hash: str
    lt: int
    fee: int
    success: bool
    error: Optional[str] = None


@dataclass
class WalletState:
    """
    Wallet state information.

    Attributes:
        balance: Current balance in nanoTON (1 TON = 10^9 nanoTON)
        seqno: Current sequence number for replay protection
        is_deployed: Whether the wallet contract is deployed
        last_transaction_lt: Last transaction logical time
    """

    balance: int
    seqno: int
    is_deployed: bool
    last_transaction_lt: Optional[int] = None


@dataclass
class TransferParams:
    """
    Transfer parameters for sending TON.

    Attributes:
        to: Destination address
        amount: Amount to send in nanoTON
        comment: Optional comment/message
        send_mode: Send mode flags (default: 3 = pay fees separately + ignore errors)
        valid_until: Expiration time (Unix timestamp)
    """

    to: Address
    amount: int
    comment: Optional[str] = None
    send_mode: int = 3
    valid_until: int = field(default_factory=lambda: int(time.time()) + 60)

    def with_comment(self, comment: str) -> "TransferParams":
        """Set an optional comment for the transfer."""
        self.comment = comment
        return self

    def with_send_mode(self, mode: int) -> "TransferParams":
        """Set the send mode flags."""
        self.send_mode = mode
        return self

    def with_valid_until(self, valid_until: int) -> "TransferParams":
        """Set custom expiration time."""
        self.valid_until = valid_until
        return self


class KeyPair:
    """
    Key pair for wallet operations.

    Attributes:
        secret_key: 32-byte secret key
        public_key: 32-byte public key
    """

    def __init__(self, secret_key: bytes, public_key: bytes):
        """
        Create a new key pair from raw bytes.

        Args:
            secret_key: 32-byte secret key
            public_key: 32-byte public key
        """
        if len(secret_key) != 32:
            raise ValueError("Secret key must be 32 bytes")
        if len(public_key) != 32:
            raise ValueError("Public key must be 32 bytes")

        self.secret_key = secret_key
        self.public_key = public_key

    def public_key_hex(self) -> str:
        """Get the public key as a hex string."""
        return self.public_key.hex()

    def __repr__(self) -> str:
        return f"KeyPair(public_key={self.public_key.hex()}, secret_key=[REDACTED])"
