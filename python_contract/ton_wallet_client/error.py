"""
Error types for the TON wallet client.
"""


class WalletError(Exception):
    """Base exception for all wallet-related errors."""

    pass


class NetworkError(WalletError):
    """Network connectivity errors."""

    def __init__(self, message: str):
        super().__init__(f"Network error: {message}")


class InvalidAddressError(WalletError):
    """Invalid address format."""

    def __init__(self, message: str):
        super().__init__(f"Invalid address format: {message}")


class SignatureError(WalletError):
    """Signature verification failed."""

    def __init__(self):
        super().__init__("Signature verification failed")


class InsufficientBalanceError(WalletError):
    """Insufficient balance for transaction."""

    def __init__(self, required: int, available: int):
        self.required = required
        self.available = available
        super().__init__(
            f"Insufficient balance: required {required}, available {available}"
        )


class InvalidSeqnoError(WalletError):
    """Invalid sequence number."""

    def __init__(self, expected: int, actual: int):
        self.expected = expected
        self.actual = actual
        super().__init__(f"Invalid sequence number: expected {expected}, got {actual}")


class TransactionExpiredError(WalletError):
    """Transaction expired."""

    def __init__(self):
        super().__init__("Transaction expired")


class ContractNotDeployedError(WalletError):
    """Contract not deployed."""

    def __init__(self, address: str):
        self.address = address
        super().__init__(f"Contract not deployed at address: {address}")


class KeyGenerationError(WalletError):
    """Key generation error."""

    def __init__(self, message: str):
        super().__init__(f"Key generation error: {message}")


class SerializationError(WalletError):
    """Serialization error."""

    def __init__(self, message: str):
        super().__init__(f"Serialization error: {message}")


class TonSdkError(WalletError):
    """Generic TON SDK error."""

    def __init__(self, message: str):
        super().__init__(f"TON SDK error: {message}")


class ConfigurationError(WalletError):
    """Configuration error."""

    def __init__(self, message: str):
        super().__init__(f"Configuration error: {message}")
