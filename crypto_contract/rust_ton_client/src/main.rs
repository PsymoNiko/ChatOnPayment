//! TON Wallet CLI Application
//!
//! A command-line interface for interacting with TON wallets

use anyhow::Result;
use ton_wallet_client::{Address, Network, TransferParams, Wallet, WalletClient};

/// Print help message
fn print_help() {
    println!("TON Wallet CLI - Rust client for SimpleWallet contract");
    println!();
    println!("USAGE:");
    println!("    wallet-cli <COMMAND> [OPTIONS]");
    println!();
    println!("COMMANDS:");
    println!("    balance <address>              Get wallet balance");
    println!("    state <address>                Get full wallet state");
    println!("    send <from> <to> <amount>      Send TON (amount in TON, not nanoTON)");
    println!("    explorer <address>             Get explorer link for address");
    println!("    help                           Print this help message");
    println!();
    println!("OPTIONS:");
    println!("    --network <mainnet|testnet>    Network to use (default: testnet)");
    println!();
    println!("EXAMPLES:");
    println!("    wallet-cli balance EQD...");
    println!("    wallet-cli send EQD... EQA... 0.5 --network testnet");
    println!("    wallet-cli explorer EQD...");
    println!();
    println!("NOTE:");
    println!("    This CLI is a demonstration of the Rust SDK for TON blockchain.");
    println!("    The actual smart contract is written in FunC (wallet.fc).");
    println!("    This Rust client interacts with the deployed contract via the TON API.");
}

/// Parse network from command line arguments
fn parse_network(args: &[String]) -> Network {
    for i in 0..args.len() {
        if args[i] == "--network" && i + 1 < args.len() {
            match args[i + 1].to_lowercase().as_str() {
                "mainnet" => return Network::Mainnet,
                "testnet" => return Network::Testnet,
                _ => {}
            }
        }
    }
    Network::Testnet
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("info")).init();

    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        print_help();
        return Ok(());
    }

    let command = &args[1];
    let network = parse_network(&args);
    let client = WalletClient::new(network).await?;

    match command.as_str() {
        "help" | "--help" | "-h" => {
            print_help();
        }

        "balance" => {
            if args.len() < 3 {
                eprintln!("Error: Address required");
                eprintln!("Usage: wallet-cli balance <address>");
                std::process::exit(1);
            }
            let address = &args[2];
            match client.get_balance(address).await {
                Ok(balance) => {
                    let tons = balance as f64 / 1_000_000_000.0;
                    println!("Address: {}", address);
                    println!("Balance: {} nanoTON ({:.9} TON)", balance, tons);
                    println!("Explorer: {}", client.explorer_link(address));
                }
                Err(e) => {
                    eprintln!("Error getting balance: {}", e);
                    std::process::exit(1);
                }
            }
        }

        "state" => {
            if args.len() < 3 {
                eprintln!("Error: Address required");
                eprintln!("Usage: wallet-cli state <address>");
                std::process::exit(1);
            }
            let address = &args[2];
            match client.get_wallet_state(address).await {
                Ok(state) => {
                    let tons = state.balance as f64 / 1_000_000_000.0;
                    println!("Address: {}", address);
                    println!("Balance: {} nanoTON ({:.9} TON)", state.balance, tons);
                    println!("Seqno: {}", state.seqno);
                    println!("Deployed: {}", state.is_deployed);
                    if let Some(lt) = state.last_transaction_lt {
                        println!("Last TX LT: {}", lt);
                    }
                    println!("Explorer: {}", client.explorer_link(address));
                }
                Err(e) => {
                    eprintln!("Error getting state: {}", e);
                    std::process::exit(1);
                }
            }
        }

        "send" => {
            if args.len() < 5 {
                eprintln!("Error: From address, to address, and amount required");
                eprintln!("Usage: wallet-cli send <from> <to> <amount>");
                std::process::exit(1);
            }
            let from_address = &args[2];
            let to_address = &args[3];
            let amount_ton: f64 = args[4].parse().unwrap_or_else(|_| {
                eprintln!("Error: Invalid amount");
                std::process::exit(1);
            });
            let amount_nano = (amount_ton * 1_000_000_000.0) as u64;

            println!("Preparing to send {} TON ({} nanoTON)", amount_ton, amount_nano);
            println!("From: {}", from_address);
            println!("To: {}", to_address);
            println!();
            println!("NOTE: This is a demonstration. In production:");
            println!("1. Load your secret key securely");
            println!("2. Sign the transaction");
            println!("3. Broadcast to the network");

            // Parse addresses
            let from = Address::from_friendly(from_address)?;
            let to = Address::from_friendly(to_address)?;

            // Create a wallet (without signing keys for demo)
            let mut wallet = Wallet::read_only(from);

            // Create transfer params
            let params = TransferParams::new(to, amount_nano);

            // In production, this would require a wallet with signing keys
            match client.send(&mut wallet, &params).await {
                Ok(result) => {
                    println!("Transaction: {}", result.hash);
                    println!("Success: {}", result.success);
                }
                Err(e) => {
                    println!("Expected error (no signing keys): {}", e);
                    println!();
                    println!("To actually send funds, you need to:");
                    println!("1. Load your secret key");
                    println!("2. Create a Wallet with signing capability");
                    println!("3. Call client.send() with the wallet");
                }
            }
        }

        "explorer" => {
            if args.len() < 3 {
                eprintln!("Error: Address required");
                eprintln!("Usage: wallet-cli explorer <address>");
                std::process::exit(1);
            }
            let address = &args[2];
            println!("Explorer link: {}", client.explorer_link(address));
        }

        _ => {
            eprintln!("Unknown command: {}", command);
            eprintln!();
            print_help();
            std::process::exit(1);
        }
    }

    Ok(())
}
