# Bittensor and EVM Address Verification Script

This script is designed to verify ownership of both Bittensor hotkeys and Ethereum Virtual Machine (EVM) addresses for participants in the Alpha Token Holding incentive program.

## Description

The script facilitates bidirectional signing, where a Bittensor hotkey signs an EVM address and vice versa. It supports separate commands for hotkey and EVM signing, ensuring secure and verifiable results.

## Requirements

- Accept mnemonic input through environment variables for enhanced security.
- Use Python ETH signing library with mnemonic support.
- Store results in a verifiable format.
- Provide error handling for invalid inputs.
- Ensure secure handling of mnemonics.

## Features

- **Hotkey Signature Generation**: Generate signatures using Bittensor hotkeys.
- **EVM Address Signature Generation**: Generate signatures using EVM addresses.
- **Verification**: Verify both hotkey and EVM address signatures.
- **Error Handling**: Robust error handling for invalid inputs.

## Usage Instructions

### Environment Setup

Ensure you have the necessary Python libraries installed. You can install them using the command: pip install -r requirements.txt

### Running the Script

To generate and verify signatures, use the following commands:

#### Hotkey Signature Generation

To generate a hotkey signature, run: python signer/generate-proof.py --hotkey

#### EVM Address Signature Generation

To generate an EVM address signature, run: python signer/generate-proof.py --eth

#### Both Hotkey and EVM Address Signature Generation

To generate both hotkey and EVM address signatures, run: python signer/generate-proof.py

### Verification

To verify the generated signatures, use the following commands:

#### Verify Hotkey Signature

To verify a hotkey signature, run: python signer/verify-proof.py --hotkey

#### Verify EVM Address Signature

To verify an EVM address signature, run: python signer/verify-proof.py --eth

#### Verify Both Signatures

To verify both hotkey and EVM address signatures, run: python signer/verify-proof.py

## Input/Output Format

- **Input**: Mnemonics for both hotkey and EVM address.
- **Output**: A text file containing the signed message and signatures in a verifiable format.

## Security Considerations

- **Mnemonic Handling**: Ensure mnemonics are handled securely and not exposed in logs or error messages.
- **Environment Variables**: Use environment variables to securely pass sensitive information.

## Technical Notes

- The script uses mnemonics instead of private keys for consistency with the current system.
- It integrates with the existing Bittensor hotkey/coldkey system.
- The same signing library as the current implementation is used for consistency.

## Example Commands

- To generate proof for hotkey, run: python signer/generate-proof.py --hotkey
- To generate proof for Ethereum address, run: python signer/generate-proof.py --eth
- To verify proof for hotkey, run: python signer/verify-proof.py --hotkey
- To verify proof for Ethereum address, run: python signer/verify-proof.py --eth

Ensure you have the necessary Python libraries installed and configured to run the script successfully.