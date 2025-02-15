from substrateinterface import Keypair
from binascii import unhexlify
import argparse
import bittensor as bt
from eth_account import Account 
from eth_account.messages import encode_defunct 

def verify_proof(verify_hotkey, verify_eth):
    args = argparse.Namespace()
    args.file = input("Enter file name: ")

    file_data = open(args.file).read()
    file_split = file_data.split("\n\t")

    if verify_hotkey:
        try:
            address_line = file_split[1]
            address_prefix = "Signed by: "
            if address_line.startswith(address_prefix):
                address = address_line[len(address_prefix):]
            else:
                address = address_line

            keypair = Keypair(ss58_address=address, ss58_format=42)

            message = file_split[0]

            signature_line = file_split[3]
            signature_prefix = "Signature: "
            if signature_line.startswith(signature_prefix):
                signature = signature_line[len(signature_prefix):]
            else:
                signature = signature_line

            real_signature = unhexlify(signature.encode())

            if not keypair.verify(data=message, signature=real_signature):
                raise ValueError(f"Invalid signature for address={address}")
            else:
                subtensor_network = bt.subtensor('test')
                hotkey_line = file_split[2]
                hotkey_prefix = "Hotkey: "
                if hotkey_line.startswith(hotkey_prefix):
                    hotkey = hotkey_line[len(hotkey_prefix):]
                else:
                    hotkey = hotkey_line
                try:
                    coldkey = subtensor_network.get_hotkey_owner(hotkey)
                    if coldkey == address:
                        print(f"Signature verified, signed by {address}")
                    else:
                        print("Invalid address: Coldkey doesn't own this hotkey")
                except Exception as e:
                    print(f"Error retrieving coldkey owner for hotkey {hotkey}: {e}")
                    return
        except IndexError:
            print("File does not contain hotkey signature data.")

    if verify_eth:
        verify_eth_signature(file_data, file_split[0])


def verify_eth_signature(file_data, eth_address):
    print("About to check eth address")
    print(eth_address)
    
    eth_signature_line = file_data.split("\n\t")[-1]
    eth_signature_prefix = "Ethereum Signature: "
    if eth_signature_line.startswith(eth_signature_prefix):
        eth_signature_hex = eth_signature_line[len(eth_signature_prefix):]
    else:
        raise ValueError("Ethereum signature not found in the file.")

    eth_signature = bytes.fromhex(eth_signature_hex)
    message_without_eth_signature = file_data.rsplit("\n\t", 1)[0]
    eth_message = encode_defunct(text=message_without_eth_signature)

    eth_account = Account.recover_message(eth_message, signature=eth_signature)

    if eth_account.lower() == eth_address.lower():
        print("Ethereum signature verified successfully.")
    else:
        print("Invalid Ethereum signature.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify proof for hotkey and/or Ethereum address.")
    parser.add_argument('--hotkey', action='store_true', help="Verify hotkey/coldkey")
    parser.add_argument('--eth', action='store_true', help="Verify Ethereum address")
    args = parser.parse_args()

    if not args.hotkey and not args.eth:
        args.hotkey = True
        args.eth = True

    verify_proof(args.hotkey, args.eth)



