import React from 'react';
import { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Typography } from '@mui/material';

export function TransactionList() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    fetchTransactions();
  }, []);

  async function fetchTransactions() {
    const response = await fetch('/api/transactions');
    const data = await response.json();
    setTransactions(data);
  }

  return (
    <>
      <Typography variant="h6">Recent Transactions</Typography>
      <List>
        {transactions.map((tx) => (
          <ListItem key={tx.hash}>
            <ListItemText
              primary={`${tx.sender.substring(0, 10)}... → ${tx.recipient.substring(0, 10)}...`}
              secondary={`Amount: ${tx.amount} ADAC`}
            />
          </ListItem>
        ))}
      </List>
    </>
  );
}