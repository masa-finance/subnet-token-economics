import bittensor as bt
import argparse
from eth_account import Account 
from eth_account.messages import encode_defunct 


def generate_proof(validate_hotkey, validate_eth):
    args = argparse.Namespace()

    try:
        if validate_hotkey:
            args.hotkey = input("Enter your hotkey address: ").strip()
            if not args.hotkey:
                raise ValueError("Hotkey cannot be empty.")

            args.name = input("Enter your coldkey name: ").strip()
            if not args.name:
                raise ValueError("Coldkey name cannot be empty.")
            
            wallet = bt.wallet(name=args.name)
            keypair = wallet.coldkey
            
            args.ethaddress = input("Enter your ethereum address: ").strip()
            if not args.ethaddress:
                raise ValueError("Ethereum address cannot be empty.")

            message = f"{args.ethaddress}"
            signature = keypair.sign(data=message)

            # Break the long line into multiple lines for readability
            file_contents = (
                f"{message}\n"
                f"\tSigned by: {keypair.ss58_address}\n"
                f"\tHotkey: {args.hotkey}\n"
                f"\tSignature: {signature.hex()}"
            )
            open("message_and_signature.txt", "w").write(file_contents)

            if not validate_eth:
                print("Hotkey signature generated and saved to message_and_signature.txt")

        if validate_eth:
            sign_with_eth_wallet()

    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def sign_with_eth_wallet():
    try:
        eth_mnemonic = input("Enter your Ethereum wallet mnemonic: ").strip()
        if not eth_mnemonic:
            raise ValueError("Ethereum wallet mnemonic cannot be empty.")

        Account.enable_unaudited_hdwallet_features()
        eth_account = Account.from_mnemonic(eth_mnemonic)
        try:
            with open("message_and_signature.txt", "r") as f:
                file_data = f.read()
        except FileNotFoundError:
            file_data = f"{eth_account.address}"
            with open("message_and_signature.txt", "w") as f:
                f.write(file_data)
        eth_message = encode_defunct(text=file_data)
        eth_signature = eth_account.sign_message(eth_message)

        with open("message_and_signature.txt", "a") as f:
            f.write(f"\n\tEthereum Signature: {eth_signature.signature.hex()}")

        print("Ethereum signature generated and appended to message_and_signature.txt")

    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate proof for hotkey and/or Ethereum address.")
    parser.add_argument('--hotkey', action='store_true', help="Validate hotkey/coldkey")
    parser.add_argument('--eth', action='store_true', help="Validate Ethereum address")
    args = parser.parse_args()

    if not args.hotkey and not args.eth:
        args.hotkey = True
        args.eth = True

    generate_proof(args.hotkey, args.eth)
