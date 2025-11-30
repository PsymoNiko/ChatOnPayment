"""
TON Wallet Client Library

A Python SDK client for interacting with the SimpleWallet contract on the TON blockchain.

Overview
--------
This library provides a high-level interface for:
- Creating and managing TON wallets
- Sending and receiving TON coins
- Querying wallet state (balance, sequence number)
- Signing and broadcasting transactions

Architecture
------------
TON smart contracts are written in FunC (the native language for TON Virtual Machine).
This Python library serves as an SDK client to interact with those contracts, providing:
- Type-safe contract interaction
- Key management and signing
- Network communication with TON nodes

Example
-------
>>> import asyncio
>>> from ton_wallet_client import WalletClient, Network
>>>
>>> async def main():
...     client = WalletClient(Network.TESTNET)
...     balance = await client.get_balance("EQD...")
...     print(f"Balance: {balance} nanoTON")
...
>>> asyncio.run(main())
"""

from .error import WalletError
from .types import (
    Address,
    KeyPair,
    Network,
    TransactionResult,
    TransferParams,
    WalletState,
)
from .wallet import Wallet, TransferMessage
from .client import WalletClient

__all__ = [
    "WalletError",
    "Address",
    "KeyPair",
    "Network",
    "TransactionResult",
    "TransferParams",
    "WalletState",
    "Wallet",
    "TransferMessage",
    "WalletClient",
]

__version__ = "0.1.0"
