from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

app = FastAPI(title="ADAC Blockchain API")

class TransactionRequest(BaseModel):
    sender: str
    recipient: str
    amount: float

class OrderRequest(BaseModel):
    trader: str
    pair: str
    side: str
    amount: float
    price: Optional[float] = None

@app.post("/transaction/new")
async def create_transaction(transaction: TransactionRequest):
    try:
        tx_hash = blockchain.add_transaction(
            transaction.sender,
            transaction.recipient,
            Decimal(str(transaction.amount))
        )
        return {"success": True, "transaction_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/stake")
async def stake_tokens(address: str, amount: float):
    try:
        success = staking.stake(address, Decimal(str(amount)))
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/balance/{address}")
async def get_balance(address: str):
    balance = blockchain.get_balance(address)
    return {"address": address, "balance": float(balance)}