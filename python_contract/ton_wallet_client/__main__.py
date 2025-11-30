"""
TON Wallet CLI Application

A command-line interface for interacting with TON wallets.
"""

import argparse
import asyncio
import logging
import sys

from .client import WalletClient
from .error import WalletError
from .types import Address, Network, TransferParams
from .wallet import Wallet


def setup_logging(debug: bool = False):
    """Configure logging for the CLI."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def parse_network(network_str: str) -> Network:
    """Parse network from string."""
    if network_str.lower() == "mainnet":
        return Network.MAINNET
    return Network.TESTNET


async def cmd_balance(args: argparse.Namespace):
    """Handle the balance command."""
    client = WalletClient(parse_network(args.network))

    try:
        balance = await client.get_balance(args.address)
        tons = balance / 1_000_000_000.0
        print(f"Address: {args.address}")
        print(f"Balance: {balance} nanoTON ({tons:.9f} TON)")
        print(f"Explorer: {client.explorer_link(args.address)}")
    except WalletError as e:
        print(f"Error getting balance: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_state(args: argparse.Namespace):
    """Handle the state command."""
    client = WalletClient(parse_network(args.network))

    try:
        state = await client.get_wallet_state(args.address)
        tons = state.balance / 1_000_000_000.0
        print(f"Address: {args.address}")
        print(f"Balance: {state.balance} nanoTON ({tons:.9f} TON)")
        print(f"Seqno: {state.seqno}")
        print(f"Deployed: {state.is_deployed}")
        if state.last_transaction_lt is not None:
            print(f"Last TX LT: {state.last_transaction_lt}")
        print(f"Explorer: {client.explorer_link(args.address)}")
    except WalletError as e:
        print(f"Error getting state: {e}", file=sys.stderr)
        sys.exit(1)


async def cmd_send(args: argparse.Namespace):
    """Handle the send command."""
    client = WalletClient(parse_network(args.network))

    amount_nano = int(args.amount * 1_000_000_000)

    print(f"Preparing to send {args.amount} TON ({amount_nano} nanoTON)")
    print(f"From: {args.from_address}")
    print(f"To: {args.to_address}")
    print()
    print("NOTE: This is a demonstration. In production:")
    print("1. Load your secret key securely")
    print("2. Sign the transaction")
    print("3. Broadcast to the network")

    try:
        # Parse addresses
        from_addr = Address.from_friendly(args.from_address)
        to_addr = Address.from_friendly(args.to_address)

        # Create a wallet (without signing keys for demo)
        wallet = Wallet.read_only(from_addr)

        # Create transfer params
        params = TransferParams(to_addr, amount_nano)

        # In production, this would require a wallet with signing keys
        result = await client.send(wallet, params)
        print(f"Transaction: {result.hash}")
        print(f"Success: {result.success}")
    except WalletError as e:
        print(f"Expected error (no signing keys): {e}")
        print()
        print("To actually send funds, you need to:")
        print("1. Load your secret key")
        print("2. Create a Wallet with signing capability")
        print("3. Call client.send() with the wallet")


async def cmd_explorer(args: argparse.Namespace):
    """Handle the explorer command."""
    client = WalletClient(parse_network(args.network))
    print(f"Explorer link: {client.explorer_link(args.address)}")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="wallet-cli",
        description="TON Wallet CLI - Python client for SimpleWallet contract",
        epilog=(
            "NOTE: This CLI is a demonstration of the Python SDK for TON blockchain.\n"
            "The actual smart contract is written in FunC (wallet.fc).\n"
            "This Python client interacts with the deployed contract via the TON API."
        ),
    )

    parser.add_argument(
        "--network",
        choices=["mainnet", "testnet"],
        default="testnet",
        help="Network to use (default: testnet)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # balance command
    balance_parser = subparsers.add_parser("balance", help="Get wallet balance")
    balance_parser.add_argument("address", help="Wallet address")

    # state command
    state_parser = subparsers.add_parser("state", help="Get full wallet state")
    state_parser.add_argument("address", help="Wallet address")

    # send command
    send_parser = subparsers.add_parser("send", help="Send TON")
    send_parser.add_argument("from_address", help="Source wallet address")
    send_parser.add_argument("to_address", help="Destination wallet address")
    send_parser.add_argument("amount", type=float, help="Amount to send (in TON)")

    # explorer command
    explorer_parser = subparsers.add_parser("explorer", help="Get explorer link")
    explorer_parser.add_argument("address", help="Wallet address")

    return parser


async def async_main():
    """Async main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.debug)

    if not args.command:
        parser.print_help()
        return

    commands = {
        "balance": cmd_balance,
        "state": cmd_state,
        "send": cmd_send,
        "explorer": cmd_explorer,
    }

    if args.command in commands:
        await commands[args.command](args)
    else:
        parser.print_help()


def main():
    """Main entry point."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
