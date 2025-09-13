import logging
import time
import os
import uuid#!/usr/bin/env python3
import logging
import time
import os
import math
from datetime import datetime
from pybit.unified_trading import HTTP

# ---------------- CONFIG ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

API_KEY = os.environ.get("BYBIT_API_KEY", "")
API_SECRET = os.environ.get("BYBIT_API_SECRET", "")
ACCOUNT_TYPE = "UNIFIED"
SYMBOL = "TRXUSDT"  # used only to check open positions

siphon_level = 4.0  # siphoning starts once balance >= 4
CHECK_INTERVAL = 3600     # 1 hour in seconds

session = HTTP(testnet=False, api_key=API_KEY, api_secret=API_SECRET)

# Track last siphon baseline
state_file = "siphon_state.txt"

def load_siphon_level():
    if not os.path.exists(state_file):
        return START siphon_level
    try:
        with open(state_file, "r") as f:
            return float(f.read().strip())
    except:
        return START siphon_level

def save_siphon_level(level):
    with open(state_file, "w") as f:
        f.write(str(level))

# ---------------- HELPERS ----------------
def get_balance():
    """Fetch unified account balance in USDT."""
    out = session.get_wallet_balance(accountType=ACCOUNT_TYPE, coin="USDT")
    try:
        res = out["result"]["list"][0]["coin"]
        for c in res:
            if c.get("coin") == "USDT":
                return float(c.get("walletBalance", 0))
    except Exception as e:
        logging.error("Error fetching balance: %s", e)
    return 0.0

def has_open_positions(symbol):
    """Check if there are open positions on the symbol."""
    try:
        out = session.get_positions(category="linear", symbol=symbol)
        positions = out.get("result", {}).get("list", [])
        for p in positions:
            if float(p.get("size", 0)) > 0:
                return True
        return False
    except Exception as e:
        logging.error("Error checking positions: %s", e)
        return False

def transfer_usdt(amount):
    """Transfer USDT from Unified → Fund account."""
    transfer_id = str(uuid.uuid4())  # Bybit requires UUID
    try:
        resp = session.create_internal_transfer(
            transferId=transfer_id,
            coin="USDT",
            amount=str(amount),
            fromAccountType="UNIFIED",
            toAccountType="FUND"
        )
        logging.info("Transfer %.2f USDT → Fund | Response: %s", amount, resp)
        return True
    except Exception as e:
        logging.error("Transfer failed")
        logging.exception(e)
        return False

# ---------------- MAIN LOGIC ----------------
def siphon_loop():
    siphon_level = load_siphon_level()
    logging.info("Starting siphon bot | initial siphon level = %.2f", siphon_level)

    while True:
        try:
            balance = get_balance()
            logging.info("Current balance = %.2f USDT | siphon level = %.2f", balance, siphon_level)

            if balance < siphon_level:
                logging.info("Balance below siphon level, waiting...")
            else:
                if has_open_positions(SYMBOL):
                    logging.info("Open positions detected, skipping siphon this hour")
                else:
                    siphon_amount = round(balance * 0.25)  # nearest whole number
                    if siphon_amount > 0:
                        success = transfer_usdt(siphon_amount)
                        if success:
                            siphon_level = balance  # reset baseline to current balance
                            save_siphon_level(siphon_level)
                            logging.info("Siphoned %.2f USDT. New siphon baseline = %.2f", siphon_amount, siphon_level)
            logging.info("Next check in %d seconds (%s)", CHECK_INTERVAL, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))
        except Exception as e:
            logging.error("Error in siphon loop")
            logging.exception(e)

        time.sleep(CHECK_INTERVAL)

# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    siphon_loop()

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
    # Generate a proper UUID
    transfer_id = str(uuid.uuid4())
    logging.info("Generated transferId (UUID) = %s", transfer_id)
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
