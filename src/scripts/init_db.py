from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import hashlib
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models import Base, Block, Transaction

# Database connection
DATABASE_URL = "postgresql://adac:adac@localhost:5432/adac"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def create_genesis_block():
    session = SessionLocal()
    try:
        # Check if genesis block exists
        if session.query(Block).first() is not None:
            print("Database already initialized")
            return

        # Create genesis block
        genesis_block = Block(
            hash=hashlib.sha256(b'genesis').hexdigest(),
            previous_hash='0' * 64,
            nonce=0,
            difficulty=4,
            timestamp=datetime.utcnow()
        )
        session.add(genesis_block)
        session.commit()

        # Create initial transaction
        genesis_transaction = Transaction(
            hash=hashlib.sha256(b'genesis_transaction').hexdigest(),
            from_address='0' * 40,  # System address
            to_address='1' * 40,    # Initial holder
            amount=1000000.0,       # Initial supply
            block_id=genesis_block.id
        )
        session.add(genesis_transaction)
        session.commit()

        print("Genesis block and initial transaction created successfully")

    except Exception as e:
        print(f"Error initializing database: {e}")
        session.rollback()
    finally:
        session.close()

def list_blocks_and_transactions():
    session = SessionLocal()
    try:
        print("\nBlocks:")
        blocks = session.query(Block).all()
        for block in blocks:
            print(f"Block {block.id}:")
            print(f"  Hash: {block.hash}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Nonce: {block.nonce}")
            print(f"  Difficulty: {block.difficulty}")
            
            print("  Transactions:")
            for tx in block.transactions:
                print(f"    From: {tx.from_address}")
                print(f"    To: {tx.to_address}")
                print(f"    Amount: {tx.amount}")
                print(f"    Hash: {tx.hash}")
            print()

    finally:
        session.close()

if __name__ == "__main__":
    create_genesis_block()
    list_blocks_and_transactions()