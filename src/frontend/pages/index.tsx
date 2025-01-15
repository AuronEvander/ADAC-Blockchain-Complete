import React from 'react';
import { useState, useEffect } from 'react';
import { Container, Grid, Card, Typography } from '@mui/material';
import { BlockList } from '../components/BlockList';
import { TransactionList } from '../components/TransactionList';

export default function Dashboard() {
  const [stats, setStats] = useState({
    latestBlock: 0,
    transactions: 0,
    activeValidators: 0,
    totalStaked: 0
  });

  useEffect(() => {
    fetchStats();
  }, []);

  async function fetchStats() {
    const response = await fetch('/api/stats');
    const data = await response.json();
    setStats(data);
  }

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom>ADAC Blockchain Dashboard</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <BlockList />
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <TransactionList />
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}