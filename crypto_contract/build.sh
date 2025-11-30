#!/bin/bash

# ============================================================================
# TON Smart Contract Build Script
# ============================================================================
# This script compiles the FunC smart contract into a Bag of Cells (BOC) file
# that can be deployed to the TON blockchain.
#
# Prerequisites:
#   - func (FunC compiler) installed
#   - fift (Fift interpreter) installed
#   - TON binaries in PATH or TONLIB_PATH environment variable set
#
# Usage:
#   ./build.sh
#
# Output:
#   - build/wallet.fif           - Compiled Fift assembly
#   - build/wallet_code.boc      - Compiled contract code (Bag of Cells)
#   - build/wallet_state_init.boc - State init for deployment
# ============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/build"

echo -e "${YELLOW}=== TON Smart Contract Build Script ===${NC}"
echo ""

# Create build directory if it doesn't exist
mkdir -p "${BUILD_DIR}"

# Check for required tools
check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed or not in PATH${NC}"
        echo "Please install TON development tools first."
        echo "See README.md for installation instructions."
        exit 1
    fi
}

echo "Checking for required tools..."

# Try to find func compiler
FUNC_CMD=""
if command -v func &> /dev/null; then
    FUNC_CMD="func"
elif command -v toncli &> /dev/null; then
    echo "Using toncli for compilation..."
    FUNC_CMD="toncli"
elif [ -n "${TONLIB_PATH}" ] && [ -f "${TONLIB_PATH}/func" ]; then
    FUNC_CMD="${TONLIB_PATH}/func"
else
    echo -e "${RED}Error: FunC compiler (func) not found${NC}"
    echo ""
    echo "Please install one of the following:"
    echo "  1. TON binaries: https://github.com/ton-blockchain/ton"
    echo "  2. toncli: pip install toncli"
    echo "  3. Set TONLIB_PATH environment variable"
    exit 1
fi

# Try to find fift interpreter
FIFT_CMD=""
if command -v fift &> /dev/null; then
    FIFT_CMD="fift"
elif [ -n "${TONLIB_PATH}" ] && [ -f "${TONLIB_PATH}/fift" ]; then
    FIFT_CMD="${TONLIB_PATH}/fift"
fi

echo -e "${GREEN}Found: ${FUNC_CMD}${NC}"

# Compile FunC to Fift assembly
echo ""
echo "Compiling FunC source code..."

if [ "${FUNC_CMD}" = "toncli" ]; then
    # Using toncli for compilation
    cd "${SCRIPT_DIR}"
    toncli build 2>/dev/null || {
        echo -e "${YELLOW}Note: toncli build requires project structure. Using direct func if available.${NC}"
        if command -v func &> /dev/null; then
            func -o "${BUILD_DIR}/wallet.fif" \
                 -SPA "${SCRIPT_DIR}/wallet.fc"
        else
            echo -e "${RED}Compilation failed. Please check your TON toolchain installation.${NC}"
            exit 1
        fi
    }
else
    # Using func compiler directly
    # -S: produce assembly output
    # -P: parse and check only
    # -A: asm output
    "${FUNC_CMD}" -o "${BUILD_DIR}/wallet.fif" \
                  -SPA "${SCRIPT_DIR}/wallet.fc"
fi

if [ ! -f "${BUILD_DIR}/wallet.fif" ]; then
    echo -e "${RED}Error: Compilation failed - wallet.fif not created${NC}"
    exit 1
fi

echo -e "${GREEN}✓ FunC compilation successful${NC}"

# Create Fift wrapper to generate BOC
echo ""
echo "Generating BOC file..."

# Create a Fift script to wrap the compiled code and generate BOC
cat > "${BUILD_DIR}/create_boc.fif" << 'FIFT_SCRIPT'
#!/usr/bin/env fift -s
"TonUtil.fif" include
"Asm.fif" include

// Include the compiled wallet code
"wallet.fif" include

// Get the code cell
PROGRAM{ }END>c constant code

// Create initial data cell (seqno=0, public_key=0 placeholder)
// The public key should be set during deployment
<b 0 32 u, 0 256 u, b> constant data

// Create the state init
<b b{0011} s, code ref, data ref, null dict, b> constant state_init

// Save the code BOC (just the contract code)
code "wallet_code.boc" B>file

// Create state init BOC for deployment
state_init "wallet_state_init.boc" B>file

."Contract code saved to wallet_code.boc" cr
."State init saved to wallet_state_init.boc" cr
FIFT_SCRIPT

# Run Fift to generate BOC if fift is available
if [ -n "${FIFT_CMD}" ]; then
    cd "${BUILD_DIR}"
    "${FIFT_CMD}" -s create_boc.fif 2>/dev/null || {
        echo -e "${YELLOW}Note: Fift execution requires FIFTPATH to be set.${NC}"
        echo "Skipping BOC generation. The .fif file can be used manually."
    }
    
    if [ -f "${BUILD_DIR}/wallet_code.boc" ]; then
        echo -e "${GREEN}✓ BOC file generated successfully${NC}"
    fi
else
    echo -e "${YELLOW}Note: Fift interpreter not found. BOC generation skipped.${NC}"
    echo "You can manually run the .fif file with Fift to generate BOC."
fi

# Summary
echo ""
echo -e "${GREEN}=== Build Complete ===${NC}"
echo ""
echo "Build artifacts in ${BUILD_DIR}:"
ls -la "${BUILD_DIR}/" 2>/dev/null || true
echo ""
echo "Next steps:"
echo "  1. Set your owner public key in config.json"
echo "  2. Deploy to testnet using toncli or a deployment script"
echo "  3. See README.md for detailed deployment instructions"
