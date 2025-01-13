from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Block(Base):
    __tablename__ = 'blocks'
    
    id = Column(Integer, primary_key=True)
    hash = Column(String, unique=True, nullable=False)
    previous_hash = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    nonce = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)
    transactions = relationship('Transaction', back_populates='block')

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    hash = Column(String, unique=True, nullable=False)
    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    block_id = Column(Integer, ForeignKey('blocks.id'))
    block = relationship('Block', back_populates='transactions')

class Account(Base):
    __tablename__ = 'accounts'
    
    address = Column(String, primary_key=True)
    balance = Column(Float, default=0.0)
    nonce = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_validator = Column(Boolean, default=False)
    stake_amount = Column(Float, default=0.0)

class StakingPosition(Base):
    __tablename__ = 'staking_positions'
    
    id = Column(Integer, primary_key=True)
    staker_address = Column(String, ForeignKey('accounts.address'))
    amount = Column(Float, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    rewards_claimed = Column(Float, default=0.0)

class LiquidityPool(Base):
    __tablename__ = 'liquidity_pools'
    
    id = Column(Integer, primary_key=True)
    token_a = Column(String, nullable=False)
    token_b = Column(String, nullable=False)
    reserve_a = Column(Float, default=0.0)
    reserve_b = Column(Float, default=0.0)
    total_shares = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)