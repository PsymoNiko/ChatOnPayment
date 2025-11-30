//! Type definitions for TON wallet operations

use serde::{Deserialize, Serialize};

/// TON network selection
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Network {
    /// TON mainnet
    Mainnet,
    /// TON testnet for development
    Testnet,
}

impl Network {
    /// Get the API endpoint URL for this network
    pub fn api_endpoint(&self) -> &'static str {
        match self {
            Network::Mainnet => "https://toncenter.com/api/v2",
            Network::Testnet => "https://testnet.toncenter.com/api/v2",
        }
    }

    /// Get the explorer URL for this network
    pub fn explorer_url(&self) -> &'static str {
        match self {
            Network::Mainnet => "https://tonscan.org",
            Network::Testnet => "https://testnet.tonscan.org",
        }
    }
}

/// TON wallet address representation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Address {
    /// Raw address bytes (32 bytes)
    pub raw: [u8; 32],
    /// Workchain ID (-1 for masterchain, 0 for basechain)
    pub workchain: i8,
    /// Human-readable address string
    pub friendly: String,
}

impl Address {
    /// Create a new address from raw bytes and workchain
    pub fn new(raw: [u8; 32], workchain: i8) -> Self {
        let friendly = format!(
            "{}:{}",
            workchain,
            hex::encode(raw)
        );
        Self {
            raw,
            workchain,
            friendly,
        }
    }

    /// Parse an address from a friendly string format
    pub fn from_friendly(address: &str) -> Result<Self, crate::error::WalletError> {
        // Handle both EQ... format and workchain:hex format
        if address.starts_with("EQ") || address.starts_with("kQ") || 
           address.starts_with("Ef") || address.starts_with("UQ") {
            // Base64 encoded address - parse accordingly
            Self::from_base64(address)
        } else if address.contains(':') {
            // workchain:hex format
            let parts: Vec<&str> = address.split(':').collect();
            if parts.len() != 2 {
                return Err(crate::error::WalletError::InvalidAddress(
                    "Invalid address format".to_string(),
                ));
            }
            let workchain: i8 = parts[0].parse().map_err(|_| {
                crate::error::WalletError::InvalidAddress("Invalid workchain".to_string())
            })?;
            let raw_hex = parts[1];
            let raw_bytes = hex::decode(raw_hex).map_err(|_| {
                crate::error::WalletError::InvalidAddress("Invalid hex in address".to_string())
            })?;
            if raw_bytes.len() != 32 {
                return Err(crate::error::WalletError::InvalidAddress(
                    "Address must be 32 bytes".to_string(),
                ));
            }
            let mut raw = [0u8; 32];
            raw.copy_from_slice(&raw_bytes);
            Ok(Self::new(raw, workchain))
        } else {
            Err(crate::error::WalletError::InvalidAddress(
                "Unrecognized address format".to_string(),
            ))
        }
    }

    /// Parse an address from base64-encoded format (EQ..., kQ..., etc.)
    fn from_base64(address: &str) -> Result<Self, crate::error::WalletError> {
        // TON addresses in base64url format are 48 characters
        // Format: 1 byte flags + 1 byte workchain + 32 bytes address + 2 bytes CRC16
        let decoded = base64::Engine::decode(
            &base64::engine::general_purpose::URL_SAFE_NO_PAD,
            address,
        )
        .or_else(|_| {
            base64::Engine::decode(&base64::engine::general_purpose::STANDARD, address)
        })
        .map_err(|_| {
            crate::error::WalletError::InvalidAddress("Invalid base64 encoding".to_string())
        })?;

        if decoded.len() != 36 {
            return Err(crate::error::WalletError::InvalidAddress(
                "Invalid address length".to_string(),
            ));
        }

        let workchain = decoded[1] as i8;
        let mut raw = [0u8; 32];
        raw.copy_from_slice(&decoded[2..34]);

        Ok(Self::new(raw, workchain))
    }

    /// Convert to hex string (workchain:hex format)
    pub fn to_hex(&self) -> String {
        format!("{}:{}", self.workchain, hex::encode(self.raw))
    }
}

impl std::fmt::Display for Address {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.friendly)
    }
}

/// Result of a transaction
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TransactionResult {
    /// Transaction hash
    pub hash: String,
    /// Logical time
    pub lt: u64,
    /// Fee paid for the transaction (in nanoTON)
    pub fee: u64,
    /// Whether the transaction was successful
    pub success: bool,
    /// Optional error message if transaction failed
    pub error: Option<String>,
}

/// Wallet state information
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WalletState {
    /// Current balance in nanoTON (1 TON = 10^9 nanoTON)
    pub balance: u64,
    /// Current sequence number for replay protection
    pub seqno: u32,
    /// Whether the wallet contract is deployed
    pub is_deployed: bool,
    /// Last transaction logical time
    pub last_transaction_lt: Option<u64>,
}

/// Transfer parameters for sending TON
#[derive(Debug, Clone)]
pub struct TransferParams {
    /// Destination address
    pub to: Address,
    /// Amount to send in nanoTON
    pub amount: u64,
    /// Optional comment/message
    pub comment: Option<String>,
    /// Send mode flags (default: 3 = pay fees separately + ignore errors)
    pub send_mode: u8,
    /// Expiration time (Unix timestamp)
    pub valid_until: u32,
}

impl TransferParams {
    /// Create new transfer parameters
    pub fn new(to: Address, amount: u64) -> Self {
        Self {
            to,
            amount,
            comment: None,
            send_mode: 3,
            valid_until: (std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs() as u32)
                + 60, // Valid for 60 seconds
        }
    }

    /// Set an optional comment for the transfer
    pub fn with_comment(mut self, comment: impl Into<String>) -> Self {
        self.comment = Some(comment.into());
        self
    }

    /// Set the send mode flags
    pub fn with_send_mode(mut self, mode: u8) -> Self {
        self.send_mode = mode;
        self
    }

    /// Set custom expiration time
    pub fn with_valid_until(mut self, valid_until: u32) -> Self {
        self.valid_until = valid_until;
        self
    }
}

/// Key pair for wallet operations
#[derive(Clone)]
pub struct KeyPair {
    /// 32-byte secret key
    pub secret_key: [u8; 32],
    /// 32-byte public key
    pub public_key: [u8; 32],
}

impl KeyPair {
    /// Create a new key pair from raw bytes
    pub fn new(secret_key: [u8; 32], public_key: [u8; 32]) -> Self {
        Self {
            secret_key,
            public_key,
        }
    }

    /// Get the public key as a hex string
    pub fn public_key_hex(&self) -> String {
        hex::encode(self.public_key)
    }
}

impl std::fmt::Debug for KeyPair {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("KeyPair")
            .field("public_key", &hex::encode(self.public_key))
            .field("secret_key", &"[REDACTED]")
            .finish()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_network_endpoints() {
        assert_eq!(
            Network::Mainnet.api_endpoint(),
            "https://toncenter.com/api/v2"
        );
        assert_eq!(
            Network::Testnet.api_endpoint(),
            "https://testnet.toncenter.com/api/v2"
        );
    }

    #[test]
    fn test_address_from_hex() {
        let hex_addr = "0:0000000000000000000000000000000000000000000000000000000000000000";
        let addr = Address::from_friendly(hex_addr).unwrap();
        assert_eq!(addr.workchain, 0);
        assert_eq!(addr.raw, [0u8; 32]);
    }

    #[test]
    fn test_transfer_params() {
        let to = Address::new([0u8; 32], 0);
        let params = TransferParams::new(to, 1_000_000_000)
            .with_comment("Test transfer");
        
        assert_eq!(params.amount, 1_000_000_000);
        assert_eq!(params.comment, Some("Test transfer".to_string()));
        assert_eq!(params.send_mode, 3);
    }
}
