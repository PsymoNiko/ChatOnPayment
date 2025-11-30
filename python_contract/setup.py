"""
TON Wallet Client - Python SDK

A Python SDK for interacting with the SimpleWallet smart contract on the TON blockchain.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ton-wallet-client",
    version="0.1.0",
    author="ChatOnPayment",
    author_email="",
    description="Python TON SDK client for SimpleWallet contract interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PsymoNiko/ChatOnPayment",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wallet-cli=ton_wallet_client.__main__:main",
        ],
    },
    keywords=["ton", "blockchain", "wallet", "crypto"],
)
