//! # TON Wallet Client Library
//!
//! A Rust SDK client for interacting with the SimpleWallet contract on the TON blockchain.
//!
//! ## Overview
//!
//! This library provides a high-level interface for:
//! - Creating and managing TON wallets
//! - Sending and receiving TON coins
//! - Querying wallet state (balance, sequence number)
//! - Signing and broadcasting transactions
//!
//! ## Architecture
//!
//! TON smart contracts are written in FunC (the native language for TON Virtual Machine).
//! This Rust library serves as an SDK client to interact with those contracts, providing:
//! - Type-safe contract interaction
//! - Key management and signing
//! - Network communication with TON nodes
//!
//! ## Example
//!
//! ```rust,ignore
//! use ton_wallet_client::{WalletClient, Network};
//!
//! #[tokio::main]
//! async fn main() -> anyhow::Result<()> {
//!     let client = WalletClient::new(Network::Testnet).await?;
//!     
//!     // Check wallet balance
//!     let balance = client.get_balance("EQD...").await?;
//!     println!("Balance: {} nanoTON", balance);
//!     
//!     Ok(())
//! }
//! ```

pub mod error;
pub mod wallet;
pub mod types;
pub mod client;

pub use error::WalletError;
pub use wallet::Wallet;
pub use types::{Address, KeyPair, Network, TransactionResult, TransferParams, WalletState};
pub use client::WalletClient;
