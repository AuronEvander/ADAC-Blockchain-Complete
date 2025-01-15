# ADAC Blockchain Complete Implementation

A comprehensive blockchain platform with AI integration, DeFi capabilities, and cross-chain functionality.

## Project Structure
```
├── src/
│   ├── blockchain/          # Core blockchain implementation
│   │   ├── block.py
│   │   └── blockchain.py
│   ├── smart_contracts/     # Smart contract system
│   │   └── contract.py
│   ├── ai/                  # AI integration
│   │   └── predictor.py
│   ├── api/                 # REST API
│   │   └── routes.py
│   ├── database/           # Database models and connection
│   │   ├── models.py
│   │   └── connection.py
│   └── main.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js
│   │   │   ├── Wallet.js
│   │   │   └── BlockExplorer.js
│   │   └── App.js
│   └── package.json
├── tests/                  # Test suite
│   └── test_blockchain.py
├── docker-compose.yml      # Docker configuration
├── Dockerfile
├── requirements.txt
└── alembic.ini            # Database migrations
```

## Features

### Core Components
- Blockchain Core Implementation
- Smart Contract System
- AI Integration with Price Prediction
- Database Integration
- REST API

### Frontend Features
- User Dashboard
- Wallet Interface
- Block Explorer

## Prerequisites
- Docker and Docker Compose
- Node.js 14+
- Python 3.9+

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/AuronEvander/ADAC-Blockchain-Complete.git
cd ADAC-Blockchain-Complete
```

2. Start the services using Docker Compose:
```bash
docker-compose up -d
```

This will start:
- Backend API on port 8000
- PostgreSQL database on port 5432
- Redis on port 6379

## Manual Setup

### Backend Setup

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
```bash
alembic upgrade head
```

4. Start the backend server:
```bash
python -m src.main
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## API Endpoints

- GET `/chain` - Get the full blockchain
- POST `/transactions/new` - Create a new transaction
- GET `/mine` - Mine a new block
- GET `/balance/{address}` - Get balance for an address

## Testing

Run the test suite:
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

## License
MIT