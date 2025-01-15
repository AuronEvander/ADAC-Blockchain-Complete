# WebSocket API Reference

## Connections

### Connect to WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

## Events

### New Block Event
```json
{
  "type": "new_block",
  "data": {
    "hash": "string",
    "index": "number",
    "transactions": []
  }
}
```

### New Transaction Event
```json
{
  "type": "new_transaction",
  "data": {
    "hash": "string",
    "sender": "string",
    "recipient": "string",
    "amount": "number"
  }
}
```