from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: float

class Block(BaseModel):
    timestamp: str
    transactions: List[Transaction]
    previous_hash: str
    hash: str

@app.get("/chain")
def get_chain():
    return {"chain": blockchain.chain}

@app.post("/transactions/new")
def new_transaction(transaction: Transaction):
    blockchain.add_transaction(
        transaction.sender,
        transaction.recipient,
        transaction.amount
    )
    return {"message": "Transaction will be added to the next block"}

@app.get("/mine")
def mine():
    blockchain.mine_pending_transactions("miner-address")
    return {"message": "New block mined!"}

@app.get("/balance/{address}")
def get_balance(address: str):
    balance = blockchain.get_balance(address)
    return {"address": address, "balance": balance}