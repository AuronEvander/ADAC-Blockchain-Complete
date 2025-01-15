import React from 'react';
import { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Typography } from '@mui/material';

export function BlockList() {
  const [blocks, setBlocks] = useState([]);

  useEffect(() => {
    fetchBlocks();
  }, []);

  async function fetchBlocks() {
    const response = await fetch('/api/blocks');
    const data = await response.json();
    setBlocks(data);
  }

  return (
    <>
      <Typography variant="h6">Latest Blocks</Typography>
      <List>
        {blocks.map((block) => (
          <ListItem key={block.hash}>
            <ListItemText
              primary={`Block #${block.index}`}
              secondary={`Hash: ${block.hash.substring(0, 10)}...`}
            />
          </ListItem>
        ))}
      </List>
    </>
  );
}