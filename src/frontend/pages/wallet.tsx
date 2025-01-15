import React from 'react';
import { useState } from 'react';
import { Container, Card, TextField, Button, Typography } from '@mui/material';

export default function Wallet() {
  const [balance, setBalance] = useState('0');
  const [recipient, setRecipient] = useState('');
  const [amount, setAmount] = useState('');

  async function sendTransaction() {
    const response = await fetch('/api/transaction/new', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ recipient, amount })
    });
    if (response.ok) {
      // Handle success
    }
  }

  return (
    <Container maxWidth="md">
      <Typography variant="h4">ADAC Wallet</Typography>
      <Card>
        <Typography>Balance: {balance} ADAC</Typography>
        <TextField
          label="Recipient"
          value={recipient}
          onChange={(e) => setRecipient(e.target.value)}
        />
        <TextField
          label="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <Button onClick={sendTransaction}>Send</Button>
      </Card>
    </Container>
  );
}