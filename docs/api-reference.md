# API Reference

## REST API Endpoints

### Blockchain

#### Get Blockchain Info
```http
GET /api/blockchain/info
```
Returns general information about the blockchain.

#### Get Block
```http
GET /api/blocks/{hash}
```
Returns detailed information about a specific block.

### Transactions

#### Create Transaction
```http
POST /api/transaction/new
```
Create a new transaction.

Body:
```json
{
  "sender": "string",
  "recipient": "string",
  "amount": "number"
}
```

### Smart Contracts

#### Deploy Contract
```http
POST /api/contract/deploy
```
Deploy a new smart contract.

### Staking

#### Stake Tokens
```http
POST /api/stake
```
Stake tokens for validation.

### DeFi

#### Add Liquidity
```http
POST /api/liquidity/add
```
Add liquidity to a pool.