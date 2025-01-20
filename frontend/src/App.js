import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [blocks, setBlocks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchBlocks = async () => {
      try {
        const response = await axios.get('http://localhost:5001/chain');
        setBlocks(response.data.chain);
      } catch (error) {
        console.error('Error fetching blockchain:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBlocks();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ADAC Blockchain Explorer</h1>
      </header>
      <main className="App-main">
        {isLoading ? (
          <p>Loading blockchain data...</p>
        ) : (
          <div className="blocks-container">
            {blocks.map((block, index) => (
              <div key={index} className="block-card">
                <h3>Block #{block.index}</h3>
                <p><strong>Hash:</strong> <span className="hash">{block.hash}</span></p>
                <p><strong>Previous Hash:</strong> <span className="hash">{block.previous_hash}</span></p>
                <p><strong>Timestamp:</strong> {new Date(block.timestamp * 1000).toLocaleString()}</p>
                <div className="block-data">
                  <strong>Data:</strong>
                  <pre>{JSON.stringify(block.data, null, 2)}</pre>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;