# TON Blockchain Smart Contract - Simple Wallet

This folder contains a minimal working example of a TON blockchain smart contract that implements a simple wallet capable of receiving and sending TON coins.

## Overview

The **SimpleWallet** contract provides:
- **Receive funds**: Accept incoming TON transfers from any address
- **Send funds**: Transfer TON to other addresses (owner authorization required)
- **Replay protection**: Uses sequence numbers to prevent transaction replay attacks
- **Signature verification**: Only the owner can authorize outgoing transfers

## Files

| File | Description |
|------|-------------|
| `wallet.fc` | FunC smart contract source code |
| `build.sh` | Build script to compile the contract |
| `config.json` | Configuration settings for deployment |
| `README.md` | This documentation file |

## Prerequisites

Before you can compile and deploy the contract, you need to install the TON development tools.

### Option 1: Install toncli (Recommended for beginners)

```bash
# Install toncli using pip
pip install toncli

# Verify installation
toncli --version
```

### Option 2: Install TON binaries directly

Download pre-built binaries from the [TON releases page](https://github.com/ton-blockchain/ton/releases) or build from source:

```bash
# Clone TON repository
git clone --recurse-submodules https://github.com/ton-blockchain/ton.git
cd ton

# Build (requires CMake, OpenSSL, and other dependencies)
mkdir build && cd build
cmake ..
cmake --build . --target func fift

# Add to PATH
export PATH=$PATH:$(pwd)
export FIFTPATH=$(pwd)/../crypto/fift/lib
```

### Option 3: Use Docker

```bash
# Pull TON development image
docker pull tonlabs/compilers

# Run compilation inside container
docker run -v $(pwd):/contract tonlabs/compilers func -o /contract/build/wallet.fif -SPA /contract/wallet.fc
```

## Compilation

### Using the build script

```bash
# Make the script executable
chmod +x build.sh

# Run the build
./build.sh
```

### Manual compilation

```bash
# Create build directory
mkdir -p build

# Compile FunC to Fift assembly
func -o build/wallet.fif -SPA wallet.fc

# Generate BOC using Fift (optional, for direct deployment)
cd build
fift -s create_boc.fif
```

### Build Output

After successful compilation, you'll find these files in the `build/` directory:

- `wallet.fif` - Fift assembly code
- `wallet_code.boc` - Compiled contract code (Bag of Cells)
- `wallet_state_init.boc` - State init for deployment

## Deployment

### Step 1: Generate a key pair

```bash
# Using toncli
toncli wallet create testnet

# Or using Fift
fift -s new-wallet.fif 0 wallet
```

### Step 2: Update configuration

Edit `config.json` and set your public key:

```json
{
    "owner": {
        "public_key": "0xYOUR_256_BIT_PUBLIC_KEY_HERE"
    }
}
```

### Step 3: Get testnet TON

1. Open Telegram and find [@testgiver_ton_bot](https://t.me/testgiver_ton_bot)
2. Send your wallet address to receive free testnet TON

### Step 4: Deploy to testnet

```bash
# Using toncli
toncli deploy -n testnet

# Or using tonweb (JavaScript)
npm install tonweb
node deploy.js
```

### Step 5: Verify deployment

Check your contract on the testnet explorer:
- https://testnet.tonscan.org/address/YOUR_CONTRACT_ADDRESS

## Interacting with the Contract

### Sending TON to the wallet

Simply send TON to the contract address. The contract will automatically accept and store the funds.

### Sending TON from the wallet

To send funds from the wallet, you need to:

1. Create an external message with:
   - Signature (512 bits)
   - Sequence number (32 bits)
   - Valid until timestamp (32 bits)
   - Send mode (8 bits)
   - Message cell reference

2. Sign the message with your private key
3. Send the external message to the contract

Example using tonweb:

```javascript
const TonWeb = require('tonweb');

const tonweb = new TonWeb(new TonWeb.HttpProvider('https://testnet.toncenter.com/api/v2/jsonRPC'));

// Load your wallet
const wallet = tonweb.wallet.create({
    publicKey: yourPublicKey,
    wc: 0
});

// Send TON
await wallet.methods.transfer({
    secretKey: yourSecretKey,
    toAddress: recipientAddress,
    amount: TonWeb.utils.toNano('0.1'), // 0.1 TON
    seqno: await wallet.methods.seqno().call(),
    sendMode: 3,
}).send();
```

### Querying contract state

```javascript
// Get current sequence number
const seqno = await wallet.methods.seqno().call();
console.log('Current seqno:', seqno);

// Get owner's public key
const publicKey = await wallet.methods.get_public_key().call();
console.log('Owner public key:', publicKey);
```

## Contract Structure

### Storage Layout

| Field | Size | Description |
|-------|------|-------------|
| seqno | 32 bits | Sequence number for replay protection |
| public_key | 256 bits | Owner's public key for signature verification |

### Message Handlers

| Handler | Type | Description |
|---------|------|-------------|
| `recv_internal` | Internal | Handles incoming messages from other contracts |
| `recv_external` | External | Handles signed messages from outside the blockchain |

### Get Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `seqno()` | int | Current sequence number |
| `get_public_key()` | int | Owner's public key |

## Security Considerations

1. **Keep your private key secure** - Never share your private key or commit it to version control
2. **Verify sequence numbers** - Always fetch the current seqno before sending transactions
3. **Set reasonable expiration** - Use valid_until to prevent old transactions from being executed
4. **Test on testnet first** - Always test your contract on testnet before deploying to mainnet

## Troubleshooting

### "func: command not found"

The FunC compiler is not installed or not in PATH. See the Prerequisites section.

### "FIFTPATH not set"

Set the FIFTPATH environment variable to point to the Fift library directory:

```bash
export FIFTPATH=/path/to/ton/crypto/fift/lib
```

### "Compilation error in wallet.fc"

Make sure you have the `stdlib.fc` file available. It's included with the TON compiler installation.

### Contract deployment fails

1. Ensure you have enough TON for gas fees
2. Verify your public key is correctly set in the state init
3. Check that you're using the correct network (testnet vs mainnet)

## Resources

- [TON Documentation](https://ton.org/docs/)
- [FunC Documentation](https://ton.org/docs/develop/func/overview)
- [TON Developers Community](https://t.me/tondev)
- [TON Testnet Faucet](https://t.me/testgiver_ton_bot)
- [TON Smart Contract Best Practices](https://ton.org/docs/develop/smart-contracts/guidelines)

## License

This code is provided as a minimal working example for educational purposes. Use at your own risk.
