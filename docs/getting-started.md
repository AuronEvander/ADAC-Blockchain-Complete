# Getting Started with ADAC Blockchain

## Prerequisites
- Python 3.9+
- Node.js 14+
- PostgreSQL
- Docker (optional)

## Installation
```bash
# Clone repository
git clone https://github.com/BurcUnalan/ADAC-Blockchain-Complete.git
cd ADAC-Blockchain-Complete

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up frontend
cd frontend
npm install
```

## Configuration
1. Create `.env` file with required environment variables
2. Initialize database
3. Run migrations
4. Start development servers