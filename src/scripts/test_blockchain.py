from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.blockchain.core import BlockchainCore
from src.models import Base

# Database connection
DATABASE_URL = "postgresql://adac:adac@localhost:5432/adac"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def test_blockchain():
    session = SessionLocal()
    try:
        # Initialize blockchain
        blockchain = BlockchainCore(session)
        
        # Create some test transactions
        miner_address = 'miner' + '1' * 35  # 40 chars total
        sender_address = 'sender' + '1' * 34
        receiver_address = 'receiver' + '1' * 32
        
        print("\nAdding transactions...")
        tx1_hash = blockchain.add_transaction(sender_address, receiver_address, 100.0)
        print(f"Transaction 1 added: {tx1_hash}")
        
        tx2_hash = blockchain.add_transaction(sender_address, receiver_address, 50.0)
        print(f"Transaction 2 added: {tx2_hash}")
        
        print("\nMining new block...")
        new_block = blockchain.create_block(miner_address)
        
        print("\nValidating block...")
        is_valid = blockchain.validate_block(new_block)
        print(f"Block is valid: {is_valid}")
        
        if is_valid:
            session.add(new_block)
            session.commit()
            print("\nBlock added to the blockchain!")
            print(f"Block hash: {new_block.hash}")
            print(f"Nonce: {new_block.nonce}")
            print("\nTransactions in block:")
            for tx in new_block.transactions:
                print(f"  From: {tx.from_address}")
                print(f"  To: {tx.to_address}")
                print(f"  Amount: {tx.amount}")
                print()
        
    finally:
        session.close()

if __name__ == "__main__":
    test_blockchain()