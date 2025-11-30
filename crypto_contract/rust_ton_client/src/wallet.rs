//! Wallet management and operations

use crate::error::WalletError;
use crate::types::{Address, KeyPair, TransferParams};

/// Represents a TON wallet with signing capabilities
pub struct Wallet {
    /// Wallet address
    address: Address,
    /// Key pair for signing (optional - None for read-only wallets)
    key_pair: Option<KeyPair>,
    /// Current sequence number (cached)
    seqno: u32,
}

impl Wallet {
    /// Create a new wallet with the given address and optional key pair
    pub fn new(address: Address, key_pair: Option<KeyPair>) -> Self {
        Self {
            address,
            key_pair,
            seqno: 0,
        }
    }

    /// Create a read-only wallet (for querying state only)
    pub fn read_only(address: Address) -> Self {
        Self::new(address, None)
    }

    /// Get the wallet address
    pub fn address(&self) -> &Address {
        &self.address
    }

    /// Check if this wallet can sign transactions
    pub fn can_sign(&self) -> bool {
        self.key_pair.is_some()
    }

    /// Get the public key if available
    pub fn public_key(&self) -> Option<&[u8; 32]> {
        self.key_pair.as_ref().map(|kp| &kp.public_key)
    }

    /// Get the current sequence number
    pub fn seqno(&self) -> u32 {
        self.seqno
    }

    /// Update the cached sequence number
    pub fn set_seqno(&mut self, seqno: u32) {
        self.seqno = seqno;
    }

    /// Create a transfer message for signing
    ///
    /// This method creates the message structure that needs to be signed
    /// for a transfer operation. The actual signing and sending is done
    /// by the WalletClient.
    pub fn create_transfer_message(
        &self,
        params: &TransferParams,
    ) -> Result<TransferMessage, WalletError> {
        if !self.can_sign() {
            return Err(WalletError::SignatureError);
        }

        Ok(TransferMessage {
            seqno: self.seqno,
            valid_until: params.valid_until,
            send_mode: params.send_mode,
            destination: params.to.clone(),
            amount: params.amount,
            comment: params.comment.clone(),
        })
    }

    /// Sign a message hash using the wallet's private key
    ///
    /// Returns a 64-byte signature
    pub fn sign(&self, message_hash: &[u8; 32]) -> Result<[u8; 64], WalletError> {
        let key_pair = self.key_pair.as_ref().ok_or(WalletError::SignatureError)?;
        
        // In a real implementation, this would use ed25519 signing
        // For now, we'll create a placeholder that demonstrates the interface
        let mut signature = [0u8; 64];
        
        // XOR the message hash with the secret key to create a deterministic output
        // NOTE: This is NOT cryptographically secure - just a placeholder
        // Real implementation would use: ed25519_dalek::sign(message_hash, &key_pair.secret_key)
        for i in 0..32 {
            signature[i] = message_hash[i] ^ key_pair.secret_key[i];
            signature[i + 32] = message_hash[i] ^ key_pair.public_key[i];
        }
        
        Ok(signature)
    }
}

/// Represents a transfer message ready for signing
#[derive(Debug, Clone)]
pub struct TransferMessage {
    /// Sequence number for replay protection
    pub seqno: u32,
    /// Message expiration timestamp
    pub valid_until: u32,
    /// Send mode flags
    pub send_mode: u8,
    /// Destination address
    pub destination: Address,
    /// Amount in nanoTON
    pub amount: u64,
    /// Optional comment
    pub comment: Option<String>,
}

impl TransferMessage {
    /// Serialize the message for hashing
    ///
    /// Returns the binary representation of the message
    pub fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::new();
        
        // Sequence number (32 bits)
        bytes.extend_from_slice(&self.seqno.to_be_bytes());
        
        // Valid until (32 bits)
        bytes.extend_from_slice(&self.valid_until.to_be_bytes());
        
        // Send mode (8 bits)
        bytes.push(self.send_mode);
        
        // Destination workchain (8 bits)
        bytes.push(self.destination.workchain as u8);
        
        // Destination address (256 bits)
        bytes.extend_from_slice(&self.destination.raw);
        
        // Amount (64 bits)
        bytes.extend_from_slice(&self.amount.to_be_bytes());
        
        // Comment (if present)
        if let Some(ref comment) = self.comment {
            bytes.extend_from_slice(comment.as_bytes());
        }
        
        bytes
    }

    /// Compute the hash of this message for signing
    pub fn hash(&self) -> [u8; 32] {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let bytes = self.to_bytes();
        
        // Use a simple hash for demonstration
        // Real implementation would use SHA-256
        let mut hasher = DefaultHasher::new();
        bytes.hash(&mut hasher);
        let hash_value = hasher.finish();
        
        let mut result = [0u8; 32];
        let hash_bytes = hash_value.to_be_bytes();
        
        // Repeat the 8-byte hash to fill 32 bytes
        for i in 0..4 {
            result[i * 8..(i + 1) * 8].copy_from_slice(&hash_bytes);
        }
        
        result
    }
}

/// Builder for creating wallets
pub struct WalletBuilder {
    address: Option<Address>,
    key_pair: Option<KeyPair>,
}

impl WalletBuilder {
    /// Create a new wallet builder
    pub fn new() -> Self {
        Self {
            address: None,
            key_pair: None,
        }
    }

    /// Set the wallet address
    pub fn address(mut self, address: Address) -> Self {
        self.address = Some(address);
        self
    }

    /// Set the key pair for signing
    pub fn key_pair(mut self, key_pair: KeyPair) -> Self {
        self.key_pair = Some(key_pair);
        self
    }

    /// Build the wallet
    pub fn build(self) -> Result<Wallet, WalletError> {
        let address = self.address.ok_or_else(|| {
            WalletError::Configuration("Wallet address is required".to_string())
        })?;

        Ok(Wallet::new(address, self.key_pair))
    }
}

impl Default for WalletBuilder {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wallet_creation() {
        let address = Address::new([1u8; 32], 0);
        let wallet = Wallet::read_only(address);
        
        assert!(!wallet.can_sign());
        assert_eq!(wallet.seqno(), 0);
    }

    #[test]
    fn test_wallet_with_keypair() {
        let address = Address::new([1u8; 32], 0);
        let key_pair = KeyPair::new([2u8; 32], [3u8; 32]);
        let wallet = Wallet::new(address, Some(key_pair));
        
        assert!(wallet.can_sign());
        assert_eq!(wallet.public_key(), Some(&[3u8; 32]));
    }

    #[test]
    fn test_transfer_message_serialization() {
        let destination = Address::new([0u8; 32], 0);
        let msg = TransferMessage {
            seqno: 1,
            valid_until: 1699999999,
            send_mode: 3,
            destination,
            amount: 1_000_000_000,
            comment: Some("Test".to_string()),
        };
        
        let bytes = msg.to_bytes();
        assert!(!bytes.is_empty());
        
        // Verify structure
        assert_eq!(&bytes[0..4], &1u32.to_be_bytes()); // seqno
        assert_eq!(&bytes[4..8], &1699999999u32.to_be_bytes()); // valid_until
        assert_eq!(bytes[8], 3); // send_mode
    }

    #[test]
    fn test_wallet_builder() {
        let address = Address::new([1u8; 32], 0);
        let key_pair = KeyPair::new([2u8; 32], [3u8; 32]);
        
        let wallet = WalletBuilder::new()
            .address(address)
            .key_pair(key_pair)
            .build()
            .unwrap();
        
        assert!(wallet.can_sign());
    }

    #[test]
    fn test_wallet_builder_missing_address() {
        let result = WalletBuilder::new().build();
        assert!(result.is_err());
    }
}
