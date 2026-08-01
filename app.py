"""
ATM System - Flask Backend
Implements: check_balance(), deposit(), withdraw(), show_menu() logic (via routes), main()
Extra (Challenge) features: PIN Verification, Transaction History, Balance Limit Check, Multiple Users
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # allow requests from the React dev server (http://localhost:3000)

# ------------------------------------------------------------------
# In-memory "database" -> Multiple Users support
# In a real app this would be a proper database (SQLite/Postgres etc.)
# ------------------------------------------------------------------
users = {
    "user1": {"pin": "1234", "balance": 1000, "transactions": []},
    "user2": {"pin": "5678", "balance": 2000, "transactions": []},
}

MAX_BALANCE_LIMIT = 100000  # ---> Balance Limit Check


def log_transaction(username, txn_type, amount, balance_after):
    """Append a record to that user's transaction history."""
    users[username]["transactions"].append(
        {
            "type": txn_type,
            "amount": amount,
            "balance_after": balance_after,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ATM backend is running"})


@app.route("/api/login", methods=["POST"])
def login():
    """---> PIN Verification"""
    data = request.get_json(force=True)
    username = data.get("username", "").strip()
    pin = data.get("pin", "").strip()

    user = users.get(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    if user["pin"] != pin:
        return jsonify({"success": False, "message": "Incorrect PIN"}), 401

    return jsonify(
        {"success": True, "message": f"Welcome {username}!", "balance": user["balance"]}
    )


@app.route("/api/balance/<username>", methods=["GET"])
def check_balance(username):
    user = users.get(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    return jsonify({"success": True, "balance": user["balance"]})


@app.route("/api/deposit", methods=["POST"])
def deposit():
    data = request.get_json(force=True)
    username = data.get("username")
    amount = data.get("amount")

    user = users.get(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    if amount is None or amount <= 0:
        return jsonify({"success": False, "message": "Enter a valid deposit amount"}), 400

    # ---> Balance Limit Check
    if user["balance"] + amount > MAX_BALANCE_LIMIT:
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Deposit exceeds max balance limit of Rs.{MAX_BALANCE_LIMIT}",
                }
            ),
            400,
        )

    user["balance"] += amount
    log_transaction(username, "Deposit", amount, user["balance"])
    return jsonify({"success": True, "message": "Deposit successful", "balance": user["balance"]})


@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json(force=True)
    username = data.get("username")
    amount = data.get("amount")

    user = users.get(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    if amount is None or amount <= 0:
        return jsonify({"success": False, "message": "Enter a valid withdrawal amount"}), 400
    if amount > user["balance"]:
        return jsonify({"success": False, "message": "Insufficient balance"}), 400

    user["balance"] -= amount
    log_transaction(username, "Withdraw", amount, user["balance"])
    return jsonify({"success": True, "message": "Withdrawal successful", "balance": user["balance"]})


@app.route("/api/transactions/<username>", methods=["GET"])
def transactions(username):
    """---> Transaction History (JSON, used by the React app)"""
    user = users.get(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    return jsonify({"success": True, "transactions": user["transactions"]})


@app.route("/debug/transactions/<username>", methods=["GET"])
def debug_transactions_view(username):
    """
    Bookmarkable HTML debug page - shows a user's transaction history as a
    table and auto-refreshes every 3 seconds, so you never have to
    copy-paste the raw JSON URL again.

    Example: http://127.0.0.1:5000/debug/transactions/user1
    """
    if username not in users:
        return f"<h2>User '{username}' not found</h2>", 404

    html = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Transaction History - __USERNAME__</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body { font-family: monospace; background: #0a0f2c; color: #e2e8f0; padding: 30px; }
        h2 { color: #ffcc00; }
        table { border-collapse: collapse; width: 100%; max-width: 700px; }
        th, td { border: 1px solid #1e3a8a; padding: 8px 12px; text-align: left; }
        th { background: #131a3d; color: #4ade80; }
        tr:nth-child(even) { background: #10173a; }
        .balance { color: #4ade80; font-weight: bold; }
        .empty { color: #8892b0; }
        .meta { color: #8892b0; font-size: 13px; margin-bottom: 15px; }
      </style>
      <meta http-equiv="refresh" content="3">
    </head>
    <body>
      <h2>Transaction History &mdash; __USERNAME__</h2>
      <p class="meta">Current balance: <span class="balance">Rs.__BALANCE__</span> &nbsp;|&nbsp; Auto-refreshing every 3s &mdash; bookmark this page</p>
      __TABLE__
    </body>
    </html>
    """

    user = users[username]
    if not user["transactions"]:
        table = '<p class="empty">No transactions yet.</p>'
    else:
        rows = "".join(
            f"<tr><td>{t['timestamp']}</td><td>{t['type']}</td>"
            f"<td>Rs.{t['amount']}</td><td>Rs.{t['balance_after']}</td></tr>"
            for t in reversed(user["transactions"])
        )
        table = (
            "<table><tr><th>Timestamp</th><th>Type</th><th>Amount</th>"
            f"<th>Balance After</th></tr>{rows}</table>"
        )

    html = html.replace("__USERNAME__", username)
    html = html.replace("__BALANCE__", str(user["balance"]))
    html = html.replace("__TABLE__", table)
    return html


if __name__ == "__main__":
    # main() equivalent - starts the program / server
    app.run(debug=True, port=5000)
