# TON Wallet Client - Rust SDK

A Rust SDK client for interacting with the SimpleWallet smart contract on the TON blockchain.

## Overview

This Rust library provides a high-level interface for:
- 🔍 Querying wallet balances and state
- 💸 Sending TON to other addresses
- 🔐 Transaction signing and verification
- 📦 Contract deployment

### Architecture Note

TON smart contracts run on the TON Virtual Machine (TVM) and are written in **FunC** (the native TON language). This Rust library is an **SDK client** that interacts with deployed contracts via the TON API - it does not compile to TVM bytecode.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer                             │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐ │
│  │   Rust SDK Client   │    │   wallet.fc (FunC Contract)     │ │
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

- Rust 1.70 or later
- Cargo package manager

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
ton-wallet-client = { path = "./rust_ton_client" }
```

Or build from source:

```bash
cd crypto_contract/rust_ton_client
cargo build --release
```

## Quick Start

### As a Library

```rust
use ton_wallet_client::{WalletClient, Network, Address, TransferParams};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize client for testnet
    let client = WalletClient::new(Network::Testnet).await?;
    
    // Check wallet balance
    let address = "0:0000000000000000000000000000000000000000000000000000000000000000";
    let balance = client.get_balance(address).await?;
    println!("Balance: {} nanoTON", balance);
    
    // Get full wallet state
    let state = client.get_wallet_state(address).await?;
    println!("Seqno: {}, Deployed: {}", state.seqno, state.is_deployed);
    
    Ok(())
}
```

### Using the CLI

```bash
# Build the CLI
cargo build --release

# Check balance
./target/release/wallet-cli balance EQD...

# Get wallet state
./target/release/wallet-cli state EQD... --network testnet

# Get explorer link
./target/release/wallet-cli explorer EQD...
```

## Sending Transactions

To send TON, you need a wallet with signing capability:

```rust
use ton_wallet_client::{
    WalletClient, Wallet, WalletBuilder, KeyPair, 
    Address, TransferParams, Network
};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let client = WalletClient::new(Network::Testnet).await?;
    
    // Load your keys (keep secret key secure!)
    let secret_key: [u8; 32] = [/* your secret key bytes */];
    let public_key: [u8; 32] = [/* your public key bytes */];
    let key_pair = KeyPair::new(secret_key, public_key);
    
    // Create wallet with signing capability
    let address = Address::from_friendly("EQD...")?;
    let mut wallet = WalletBuilder::new()
        .address(address)
        .key_pair(key_pair)
        .build()?;
    
    // Create transfer
    let destination = Address::from_friendly("EQA...")?;
    let params = TransferParams::new(destination, 1_000_000_000) // 1 TON
        .with_comment("Payment");
    
    // Send!
    let result = client.send(&mut wallet, &params).await?;
    println!("Transaction hash: {}", result.hash);
    
    Ok(())
}
```

## API Reference

### `WalletClient`

Main client for blockchain operations.

| Method | Description |
|--------|-------------|
| `new(network)` | Create client for mainnet or testnet |
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
| `new(address, key_pair)` | Create wallet with keys |
| `read_only(address)` | Create read-only wallet |
| `can_sign()` | Check if wallet can sign |
| `address()` | Get wallet address |
| `seqno()` | Get cached sequence number |

### `TransferParams`

Parameters for sending TON.

| Field | Type | Description |
|-------|------|-------------|
| `to` | `Address` | Destination address |
| `amount` | `u64` | Amount in nanoTON |
| `comment` | `Option<String>` | Optional message |
| `send_mode` | `u8` | Transaction flags |
| `valid_until` | `u32` | Expiration timestamp |

## Building and Testing

```bash
# Build library and CLI
cargo build

# Run tests
cargo test

# Build optimized release
cargo build --release

# Run with debug logging
RUST_LOG=debug cargo run -- balance EQD...
```

## Project Structure

```
rust_ton_client/
├── Cargo.toml          # Package manifest
├── README.md           # This file
└── src/
    ├── lib.rs          # Library entry point
    ├── main.rs         # CLI application
    ├── client.rs       # WalletClient implementation
    ├── wallet.rs       # Wallet and signing
    ├── types.rs        # Type definitions
    └── error.rs        # Error types
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

| Aspect | FunC (wallet.fc) | Rust SDK (this library) |
|--------|------------------|------------------------|
| **Runs on** | TON blockchain | Your machine |
| **Language** | FunC | Rust |
| **Purpose** | Store/transfer funds | Interact with contract |
| **Security** | On-chain verification | Signs transactions |
| **Network** | TVM execution | HTTP API calls |

## Related Files

- `../wallet.fc` - FunC smart contract source
- `../config.json` - Deployment configuration
- `../build.sh` - FunC compilation script

## License

MIT License - see repository root for details.

## Resources

- [TON Documentation](https://ton.org/docs/)
- [tonlib-rs Crate](https://crates.io/crates/tonlib)
- [TON API Reference](https://toncenter.com/api/v2/)
- [TON Testnet Faucet](https://t.me/testgiver_ton_bot)
