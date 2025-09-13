#!/usr/bin/env python3
import os
import uuid
import logging
from pybit.unified_trading import HTTP

# ====== CONFIG ======
API_KEY = os.getenv("BYBIT_API_KEY")      # or hardcode your API key here
API_SECRET = os.getenv("BYBIT_API_SECRET")  # or hardcode your API secret here

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("BybitTransfer")

# Initialize session
session = HTTP(
    testnet=False,  # True for testnet, False for live
    api_key=API_KEY,
    api_secret=API_SECRET,
)

def transfer_usdt(amount=0.1):
    transfer_id = f"transfer_{uuid.uuid4().hex[:8]}"
    try:
        resp = session.asset_transfer(
            transferId=transfer_id,
            coin="USDT",
            amount=str(amount),
            from_account_type="UNIFIED",   # Futures/Unified Trading Account
            to_account_type="FUND"         # Funding Wallet
        )
        logger.info("Transfer request sent: %s", transfer_id)
        logger.info("Response: %s", resp)
    except Exception as e:
        logger.exception("Error during transfer")

if __name__ == "__main__":
    transfer_usdt(0.1)
