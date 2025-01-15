from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Block(Base):
    __tablename__ = 'blocks'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    previous_hash = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    nonce = Column(Integer, nullable=False)
    transactions = relationship('Transaction', back_populates='block')

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    block_id = Column(Integer, ForeignKey('blocks.id'))
    block = relationship('Block', back_populates='transactions')