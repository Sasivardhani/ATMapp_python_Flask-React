# 🏧 ATM System — Flask + React (CRA)

A full-stack ATM System built with a **Flask** REST API backend and a **React (Create React App)** frontend.

## 📚 Concepts Covered
Variables · Input & Output · Operators · If-Else · While Loop · Functions

## 🎯 Project Features
1. **Check Balance** – View your current account balance instantly.
2. **Deposit Money** – Add money to your account securely.
3. **Withdraw Money** – Withdraw cash if you have sufficient balance.
4. **Exit the ATM System** – Safely log out.

### 🏆 Challenge Upgrades (included)
- ✅ **PIN Verification** — login with username + PIN
- ✅ **Transaction History** — every deposit/withdrawal is logged with a timestamp
- ✅ **Balance Limit Check** — deposits can't push balance above ₹100,000
- ✅ **Multiple Users** — two demo accounts included out of the box

## 🧠 Logic Flow
`Start` → `Display Menu` → `User Choice` → `Perform Operation` (Check / Deposit / Withdraw)
→ `Update Balance` → `Show Menu Again` → `Exit`

## ⚙️ Functions Used (backend)
```
login()            -> PIN verification
check_balance()
deposit()
withdraw()
transactions()      -> transaction history
log_transaction()
```

---

## 📁 Project Structure

```
atm-app/
├── backend/
│   ├── app.py              # Flask API
│   └── requirements.txt
└── frontend_src/            # Files to drop into a fresh CRA project
    ├── App.js
    ├── App.css
    └── api.js
```

---

## 🚀 How to Run in VS Code

### Prerequisites
- **Python 3.8+** installed
- **Node.js (v16+) and npm** installed
- **VS Code** with the Python extension (recommended)

### 1️⃣ Backend (Flask API)

Open a terminal in VS Code (`` Ctrl+` ``), then:

```bash
cd atm-app/backend

# create & activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the server
python app.py
```

The API will start at **http://localhost:5000**.
You should see Flask's debug server log in the terminal. Test it by opening
`http://localhost:5000/api/health` in a browser — you should see a JSON success message.

Leave this terminal running.

### 2️⃣ Frontend (React – Create React App)

Open a **second terminal** in VS Code (keep the backend terminal running):

```bash
cd atm-app

# create a fresh CRA app (only needed once)
npx create-react-app frontend

# install axios for API calls
cd frontend
npm install axios
```

Then start the React app:

```bash
cd frontend
npm start
```

This opens **http://localhost:3000** in your browser automatically.

### 3️⃣ Use the App

Log in with one of the demo accounts:

| Username | PIN  | Starting Balance |
|----------|------|-------------------|
| user1    | 1234 | ₹1000              |
| user2    | 5678 | ₹2000              |

Then use the on-screen menu to check balance, deposit, withdraw, or view transaction history.

---

## 🔌 API Endpoints

| Method | Endpoint                       | Description               |
|--------|---------------------------------|----------------------------|
| POST   | `/api/login`                   | Authenticate user (PIN)   |
| GET    | `/api/balance/<username>`      | Get current balance       |
| POST   | `/api/deposit`                 | `{ username, amount }`    |
| POST   | `/api/withdraw`                | `{ username, amount }`    |
| GET    | `/api/transactions/<username>` | Get transaction history (JSON) |
| GET    | `/debug/transactions/<username>` | **Bookmarkable HTML page** — shows the same history as a table, auto-refreshes every 3 seconds. e.g. `http://127.0.0.1:5000/debug/transactions/user1` |

---

## 🛠 Troubleshooting

- **CORS errors in browser console** → make sure the Flask backend is running on port 5000 and `flask-cors` is installed.
- **`npx create-react-app` fails / is slow** → ensure you have an active internet connection; it downloads packages from npm.
- **Port already in use** → change `app.run(debug=True, port=5000)` in `app.py` to a free port, and update `API_BASE` in `api.js` to match.
- **"Module not found: axios"** → run `npm install axios` inside the `frontend` folder.

---

## 🔮 Further Upgrade Ideas
- Persist data with SQLite/PostgreSQL instead of the in-memory `users` dict
- Add JWT-based session auth instead of sending the username with every request
- Add an admin view to create new users
- Add interest calculation / mini statements
