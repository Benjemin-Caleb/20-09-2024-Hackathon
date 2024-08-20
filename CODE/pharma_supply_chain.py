import json
import hashlib
import time

def hash_block(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def create_block(previous_hash, transaction):
    block = {
        'timestamp': time.time(),
        'transaction': transaction,
        'previous_hash': previous_hash,
        'hash': ""
    }
    block['hash'] = hash_block(block)
    return block

def initialize_blockchain():
    genesis_block = create_block("0", {
        "manufacturer": "Genesis",
        "drug": "N/A",
        "batch": "N/A",
        "status": "Genesis Block",
        "location": "N/A"
    })
    blockchain = [genesis_block]
    return blockchain

def add_transaction(blockchain, transaction):
    previous_hash = blockchain[-1]['hash']
    new_block = create_block(previous_hash, transaction)
    blockchain.append(new_block)

def save_blockchain(blockchain, filename="pharma_supply_chain.json"):
    with open(filename, 'w') as f:
        json.dump(blockchain, f, indent=4)

def load_blockchain(filename="pharma_supply_chain.json"):
    try:
        with open(filename, 'r') as f:
            blockchain = json.load(f)
        return blockchain
    except FileNotFoundError:
        return initialize_blockchain()

def display_all_transactions(blockchain):
    print("\nAll Transactions:")
    for block in blockchain[1:]: 
        transaction = block['transaction']
        status = transaction.get('status')
        print(f"Drug: {transaction.get('drug')} | Batch Number: {transaction.get('batch')} | Location: {transaction.get('location')} | Status: {status} | Hash: {block['hash']}")

def input_transaction():
    manufacturer = input("Enter Manufacturer Name: ")
    drug = input("Enter Drug Name: ")
    batch = input("Enter Batch Number: ")
    location = input("Enter Manufacturing Location: ")
    return {
        "manufacturer": manufacturer,
        "drug": drug,
        "batch": batch,
        "status": "Manufactured",
        "location": location
    }

def main_menu(blockchain):
    while True:
        print("\nMain Menu:")
        print("1. All Transactions")
        print("2. New Transaction")
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            display_all_transactions(blockchain)
        elif choice == "2":
            new_transaction = input_transaction()
            add_transaction(blockchain, new_transaction)
            print("\nTransaction Added:")
            display_transaction(new_transaction)

            update_status(blockchain, new_transaction, "Shipped", "Shipping Location")
            update_status(blockchain, new_transaction, "Delivered", "Delivery Location")
            save_blockchain(blockchain)
        else:
            print("Invalid choice. Please try again.")

def display_transaction(transaction):
    print(f"\nManufacturer: {transaction.get('manufacturer')}")
    print(f"Drug: {transaction.get('drug')}")
    print(f"Batch Number: {transaction.get('batch')}")
    print(f"Status: {transaction.get('status')}")
    print(f"Location: {transaction.get('location')}")

def update_status(blockchain, transaction, new_status, location_type):
    location = input(f"Enter {location_type}: ")
    updated_transaction = transaction.copy()
    updated_transaction["status"] = new_status
    updated_transaction["location"] = location
    add_transaction(blockchain, updated_transaction)
    print(f"\nStatus Updated to {new_status}:")
    display_transaction(updated_transaction)

if __name__ == "__main__":
    blockchain = load_blockchain()
    main_menu(blockchain)
