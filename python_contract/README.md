# TON Wallet Client - Python SDK

A Python SDK client for interacting with the SimpleWallet smart contract on the TON blockchain.

## Overview

This Python library provides a high-level interface for:
- 🔍 Querying wallet balances and state
- 💸 Sending TON to other addresses
- 🔐 Transaction signing and verification
- 📦 Contract deployment

### Architecture Note

TON smart contracts run on the TON Virtual Machine (TVM) and are written in **FunC** (the native TON language). This Python library is an **SDK client** that interacts with deployed contracts via the TON API - it does not compile to TVM bytecode.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer                             │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐ │
│  │  Python SDK Client  │    │   wallet.fc (FunC Contract)     │ │
│  │   (This Library)    │    │   - Runs on TON blockchain      │ │
│  │   - Runs locally    │    │   - Handles coin transfers      │ │
│  │   - Signs txns      │    │   - Verifies signatures         │ │
│  └─────────┬───────────┘    └───────────────┬─────────────────┘ │
│            │                                │                    │
│            │  HTTP/API                      │  TVM Execution     │
│            ▼                                ▼                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    TON Blockchain                           ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Python 3.8 or later
- pip package manager

## Installation

Install from source:

```bash
cd crypto_contract/python_contract
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Quick Start

### As a Library

```python
import asyncio
from ton_wallet_client import WalletClient, Network

async def main():
    # Initialize client for testnet
    client = WalletClient(Network.TESTNET)
    
    # Check wallet balance
    address = "0:0000000000000000000000000000000000000000000000000000000000000000"
    balance = await client.get_balance(address)
    print(f"Balance: {balance} nanoTON")
    
    # Get full wallet state
    state = await client.get_wallet_state(address)
    print(f"Seqno: {state.seqno}, Deployed: {state.is_deployed}")

asyncio.run(main())
```

### Using the CLI

```bash
# Check balance
python -m ton_wallet_client balance EQD...

# Get wallet state
python -m ton_wallet_client state EQD... --network testnet

# Get explorer link
python -m ton_wallet_client explorer EQD...
```

## Sending Transactions

To send TON, you need a wallet with signing capability:

```python
import asyncio
from ton_wallet_client import (
    WalletClient, Wallet, KeyPair,
    Address, TransferParams, Network
)

async def main():
    client = WalletClient(Network.TESTNET)
    
    # Load your keys (keep secret key secure!)
    secret_key = bytes(32)  # Your secret key bytes
    public_key = bytes(32)  # Your public key bytes
    key_pair = KeyPair(secret_key, public_key)
    
    # Create wallet with signing capability
    address = Address.from_friendly("EQD...")
    wallet = Wallet(address, key_pair)
    
    # Create transfer
    destination = Address.from_friendly("EQA...")
    params = TransferParams(destination, 1_000_000_000)  # 1 TON
    params.comment = "Payment"
    
    # Send!
    result = await client.send(wallet, params)
    print(f"Transaction hash: {result.hash}")

asyncio.run(main())
```

## API Reference

### `WalletClient`

Main client for blockchain operations.

| Method | Description |
|--------|-------------|
| `__init__(network)` | Create client for mainnet or testnet |
| `get_balance(address)` | Get wallet balance in nanoTON |
| `get_wallet_state(address)` | Get full wallet state |
| `get_seqno(address)` | Get current sequence number |
| `send(wallet, params)` | Send TON from wallet |
| `deploy(wallet, balance)` | Deploy wallet contract |
| `explorer_link(address)` | Get block explorer URL |

### `Wallet`

Represents a wallet with optional signing capability.

| Method | Description |
|--------|-------------|
| `__init__(address, key_pair)` | Create wallet with keys |
| `read_only(address)` | Create read-only wallet |
| `can_sign` | Check if wallet can sign |
| `address` | Get wallet address |
| `seqno` | Get cached sequence number |

### `TransferParams`

Parameters for sending TON.

| Field | Type | Description |
|-------|------|-------------|
| `to` | `Address` | Destination address |
| `amount` | `int` | Amount in nanoTON |
| `comment` | `Optional[str]` | Optional message |
| `send_mode` | `int` | Transaction flags |
| `valid_until` | `int` | Expiration timestamp |

## Building and Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with debug logging
LOG_LEVEL=DEBUG python -m ton_wallet_client balance EQD...
```

## Project Structure

```
python_contract/
├── requirements.txt        # Package dependencies
├── setup.py               # Package setup script
├── README.md              # This file
└── ton_wallet_client/
    ├── __init__.py        # Package entry point
    ├── __main__.py        # CLI entry point
    ├── client.py          # WalletClient implementation
    ├── wallet.py          # Wallet and signing
    ├── types.py           # Type definitions
    └── error.py           # Error types
```

## Network Configuration

| Network | API Endpoint | Explorer |
|---------|--------------|----------|
| Mainnet | https://toncenter.com/api/v2 | https://tonscan.org |
| Testnet | https://testnet.toncenter.com/api/v2 | https://testnet.tonscan.org |

## Security Considerations

1. **Secret Key Security**: Never hardcode or log secret keys
2. **Testnet First**: Always test on testnet before mainnet
3. **Verify Addresses**: Double-check recipient addresses
4. **Sequence Numbers**: Always fetch fresh seqno before transactions
5. **Expiration**: Set reasonable `valid_until` values

## Comparison with FunC Contract

| Aspect | FunC (wallet.fc) | Python SDK (this library) |
|--------|------------------|--------------------------|
| **Runs on** | TON blockchain | Your machine |
| **Language** | FunC | Python |
| **Purpose** | Store/transfer funds | Interact with contract |
| **Security** | On-chain verification | Signs transactions |
| **Network** | TVM execution | HTTP API calls |

## Related Files

- `../wallet.fc` - FunC smart contract source
- `../config.json` - Deployment configuration
- `../build.sh` - FunC compilation script
- `../rust_ton_client/` - Rust SDK equivalent

## License

MIT License - see repository root for details.

## Resources

- [TON Documentation](https://ton.org/docs/)
- [tonclient Python Library](https://github.com/tonstack/tonclient)
- [TON API Reference](https://toncenter.com/api/v2/)
- [TON Testnet Faucet](https://t.me/testgiver_ton_bot)
