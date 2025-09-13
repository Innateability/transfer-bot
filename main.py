import logging
import time
import os
from pybit.unified_trading import HTTP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load API credentials from environment
API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")

if not API_KEY or not API_SECRET:
    raise ValueError("API key and secret must be set in environment variables!")

session = HTTP(
    testnet=False,  # True for testnet
    api_key=API_KEY,
    api_secret=API_SECRET
)

def transfer_usdt():
    transfer_id = f"tr_{int(time.time() * 1000)}"
    logging.info("Generated transferId (CID) = %s", transfer_id)
    try:
        resp = session.create_internal_transfer(
            transferId=transfer_id,
            coin="USDT",
            amount="0.1",
            fromAccountType="UNIFIED",
            toAccountType="FUND"
        )
        logging.info("Transfer response: %s", resp)
    except Exception as e:
        logging.error("Error during transfer")
        logging.exception(e)

if __name__ == "__main__":
    transfer_usdt()
