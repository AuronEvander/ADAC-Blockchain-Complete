import uvicorn
from api.routes import app
from blockchain.blockchain import Blockchain

blockchain = Blockchain()

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()