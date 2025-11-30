"""
TON blockchain client for wallet operations.
"""

import logging
from typing import Optional

from .error import SignatureError
from .types import (
    Address,
    Network,
    TransactionResult,
    TransferParams,
    WalletState,
)
from .wallet import Wallet

logger = logging.getLogger(__name__)


class WalletClient:
    """
    Client for interacting with TON blockchain.

    This client provides high-level methods for:
    - Querying wallet state and balance
    - Sending transactions
    - Deploying contracts

    Example:
        >>> import asyncio
        >>> from ton_wallet_client import WalletClient, Network
        >>>
        >>> async def main():
        ...     client = WalletClient(Network.TESTNET)
        ...     balance = await client.get_balance("EQD...")
        ...     print(f"Balance: {balance / 1e9:.2f} TON")
        ...
        >>> asyncio.run(main())

    Attributes:
        network: Network configuration
        api_url: API endpoint URL
    """

    def __init__(self, network: Network = Network.TESTNET):
        """
        Create a new wallet client for the specified network.

        Args:
            network: The TON network to connect to (Mainnet or Testnet)
        """
        self._network = network
        self._api_url = network.api_endpoint

        logger.info("Initializing TON wallet client for %s", network.value)
        logger.debug("API endpoint: %s", self._api_url)

    @classmethod
    def with_custom_endpoint(cls, endpoint: str) -> "WalletClient":
        """
        Create a client with a custom API endpoint.

        Useful for connecting to private TON nodes.

        Args:
            endpoint: Custom API endpoint URL

        Returns:
            Configured WalletClient
        """
        logger.info("Initializing TON wallet client with custom endpoint: %s", endpoint)

        client = cls.__new__(cls)
        client._network = Network.TESTNET  # Default to testnet for custom endpoints
        client._api_url = endpoint
        return client

    @property
    def network(self) -> Network:
        """Get the current network."""
        return self._network

    @property
    def api_url(self) -> str:
        """Get the API endpoint URL."""
        return self._api_url

    async def get_balance(self, address: str) -> int:
        """
        Get the balance of a wallet address.

        Args:
            address: The wallet address to query

        Returns:
            Balance in nanoTON (1 TON = 10^9 nanoTON)

        Note:
            This is currently a mock implementation that returns 0.
            To connect to the actual TON network, integrate with the toncenter API
            or use a TON client library.

        Example:
            >>> balance = await client.get_balance("EQD...")
            >>> tons = balance / 1_000_000_000
            >>> print(f"Balance: {tons:.2f} TON")
        """
        logger.debug("Getting balance for address: %s", address)

        # Parse and validate the address
        _parsed = Address.from_friendly(address)

        # MOCK IMPLEMENTATION: Returns 0
        #
        # To implement actual balance queries, use one of these approaches:
        #
        # 1. HTTP API (simpler, requires API key for production):
        #    async with aiohttp.ClientSession() as session:
        #        url = f"{self._api_url}/getAddressBalance?address={address}"
        #        async with session.get(url) as response:
        #            data = await response.json()
        #            return int(data["result"])
        #
        # 2. tonclient library (more complex, direct node connection):
        #    from tonclient import TonClient
        #    client = TonClient(...)
        #    info = await client.get_account_state(address)
        #    return info.balance

        logger.warning("get_balance: Using mock implementation, returning 0")
        return 0

    async def get_wallet_state(self, address: str) -> WalletState:
        """
        Get the full state of a wallet.

        Returns balance, sequence number, and deployment status.

        Args:
            address: The wallet address to query

        Returns:
            WalletState with balance, seqno, and deployment status

        Note:
            This is currently a mock implementation.
            For production use, integrate with the TON API or tonclient.
        """
        logger.debug("Getting wallet state for: %s", address)

        _parsed = Address.from_friendly(address)

        # MOCK IMPLEMENTATION: Returns placeholder values
        # In production, query the actual blockchain state
        logger.warning("get_wallet_state: Using mock implementation")
        return WalletState(
            balance=0,
            seqno=0,
            is_deployed=False,
            last_transaction_lt=None,
        )

    async def get_seqno(self, address: str) -> int:
        """
        Get the current sequence number of a wallet.

        The sequence number is used for replay protection.

        Args:
            address: The wallet address to query

        Returns:
            Current sequence number
        """
        logger.debug("Getting seqno for: %s", address)
        state = await self.get_wallet_state(address)
        return state.seqno

    async def send(
        self,
        wallet: Wallet,
        params: TransferParams,
    ) -> TransactionResult:
        """
        Send TON from one wallet to another.

        Args:
            wallet: The source wallet (must have signing capability)
            params: Transfer parameters including destination and amount

        Returns:
            Transaction result with hash and status

        Raises:
            SignatureError: If wallet cannot sign transactions

        Example:
            >>> params = TransferParams(destination, 1_000_000_000)  # 1 TON
            >>> params.comment = "Payment for services"
            >>> result = await client.send(wallet, params)
            >>> print(f"Transaction hash: {result.hash}")
        """
        if not wallet.can_sign:
            raise SignatureError()

        logger.info(
            "Sending %d nanoTON from %s to %s",
            params.amount,
            wallet.address,
            params.to,
        )

        # Update the wallet's seqno from the blockchain
        current_seqno = await self.get_seqno(wallet.address.to_hex())
        wallet.seqno = current_seqno

        # Create the transfer message
        message = wallet.create_transfer_message(params)

        # Compute message hash and sign
        msg_hash = message.hash()
        _signature = wallet.sign(msg_hash)

        # In a real implementation, we would:
        # 1. Serialize the message with signature
        # 2. Create a BOC (Bag of Cells)
        # 3. Send it to the blockchain via the API
        # 4. Wait for confirmation

        logger.debug("Transaction signed and ready to broadcast")

        # Mock transaction result
        return TransactionResult(
            hash=msg_hash.hex(),
            lt=0,
            fee=0,
            success=True,
            error=None,
        )

    async def deploy(
        self,
        wallet: Wallet,
        initial_balance: int,
    ) -> TransactionResult:
        """
        Deploy a wallet contract to the blockchain.

        Args:
            wallet: The wallet to deploy
            initial_balance: Initial balance to send (must be enough for deployment)

        Returns:
            Transaction result of the deployment

        Raises:
            SignatureError: If wallet cannot sign transactions
        """
        if not wallet.can_sign:
            raise SignatureError()

        logger.info(
            "Deploying wallet %s with %d nanoTON initial balance",
            wallet.address,
            initial_balance,
        )

        # In a real implementation, this would:
        # 1. Create the state init (code + data)
        # 2. Create deployment message
        # 3. Sign and broadcast

        # Mock deployment result
        return TransactionResult(
            hash="deployment_hash_placeholder",
            lt=0,
            fee=0,
            success=True,
            error=None,
        )

    def explorer_link(self, address: str) -> str:
        """
        Get the explorer URL for an address.

        Args:
            address: Wallet address

        Returns:
            Block explorer URL for the address
        """
        return f"{self._network.explorer_url}/address/{address}"

    def transaction_link(self, tx_hash: str) -> str:
        """
        Get the explorer URL for a transaction.

        Args:
            tx_hash: Transaction hash

        Returns:
            Block explorer URL for the transaction
        """
        return f"{self._network.explorer_url}/tx/{tx_hash}"
