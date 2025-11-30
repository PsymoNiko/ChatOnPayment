//! Error types for the TON wallet client

use thiserror::Error;

/// Errors that can occur during wallet operations
#[derive(Error, Debug)]
pub enum WalletError {
    /// Network connectivity errors
    #[error("Network error: {0}")]
    Network(String),

    /// Invalid address format
    #[error("Invalid address format: {0}")]
    InvalidAddress(String),

    /// Signature verification failed
    #[error("Signature verification failed")]
    SignatureError,

    /// Insufficient balance for transaction
    #[error("Insufficient balance: required {required}, available {available}")]
    InsufficientBalance { required: u64, available: u64 },

    /// Invalid sequence number
    #[error("Invalid sequence number: expected {expected}, got {actual}")]
    InvalidSeqno { expected: u32, actual: u32 },

    /// Transaction expired
    #[error("Transaction expired")]
    TransactionExpired,

    /// Contract not deployed
    #[error("Contract not deployed at address: {0}")]
    ContractNotDeployed(String),

    /// Key generation error
    #[error("Key generation error: {0}")]
    KeyGeneration(String),

    /// Serialization error
    #[error("Serialization error: {0}")]
    Serialization(String),

    /// Generic TON SDK error
    #[error("TON SDK error: {0}")]
    TonSdk(String),

    /// Configuration error
    #[error("Configuration error: {0}")]
    Configuration(String),
}

impl From<anyhow::Error> for WalletError {
    fn from(err: anyhow::Error) -> Self {
        WalletError::TonSdk(err.to_string())
    }
}
