import React, { useState } from "react";
import "./App.css";
import { login, deposit, withdraw, getTransactions } from "./api";

function App() {
  // auth state
  const [username, setUsername] = useState("");
  const [pin, setPin] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  // atm state
  const [balance, setBalance] = useState(0);
  const [amount, setAmount] = useState("");
  const [view, setView] = useState("menu"); // menu | deposit | withdraw | history
  const [transactions, setTransactions] = useState([]);
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await login(username, pin);
      setBalance(res.data.balance);
      setLoggedIn(true);
      setMessage(res.data.message);
    } catch (err) {
      setMessage(err.response?.data?.message || "Login failed");
    }
  };

  const handleDeposit = async () => {
    try {
      const res = await deposit(username, Number(amount));
      setBalance(res.data.balance);
      setMessage(res.data.message);
      setAmount("");
      setView("menu");
    } catch (err) {
      setMessage(err.response?.data?.message || "Deposit failed");
    }
  };

  const handleWithdraw = async () => {
    try {
      const res = await withdraw(username, Number(amount));
      setBalance(res.data.balance);
      setMessage(res.data.message);
      setAmount("");
      setView("menu");
    } catch (err) {
      setMessage(err.response?.data?.message || "Withdrawal failed");
    }
  };

  const handleHistory = async () => {
    try {
      const res = await getTransactions(username);
      setTransactions(res.data.transactions);
      setView("history");
    } catch (err) {
      setMessage(err.response?.data?.message || "Could not load history");
    }
  };

  const handleExit = () => {
    setLoggedIn(false);
    setUsername("");
    setPin("");
    setBalance(0);
    setMessage("Thank you for using our ATM System! Visit Again!");
    setView("menu");
  };

  // ---------- LOGIN SCREEN ----------
  if (!loggedIn) {
    return (
      <div className="atm-container">
        <div className="atm-screen">
          <h1>ATM SYSTEM</h1>
          <form onSubmit={handleLogin} className="atm-form">
            <input
              type="text"
              placeholder="Username (try user1)"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="PIN (try 1234)"
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              required
            />
            <button type="submit">Login</button>
          </form>
          {message && <p className="atm-message">{message}</p>}
        </div>
      </div>
    );
  }

  // ---------- MAIN ATM SCREEN ----------
  return (
    <div className="atm-container">
      <div className="atm-screen">
        <h1>ATM SYSTEM</h1>
        <p className="balance">Current Balance: ₹{balance}</p>
        {message && <p className="atm-message">{message}</p>}

        {view === "menu" && (
          <div className="menu">
            <button onClick={() => setView("menu")}>Check Balance</button>
            <button onClick={() => setView("deposit")}>Deposit Money</button>
            <button onClick={() => setView("withdraw")}>Withdraw Money</button>
            <button onClick={handleHistory}>Transaction History</button>
            <button className="exit-btn" onClick={handleExit}>
              Exit
            </button>
          </div>
        )}

        {view === "deposit" && (
          <div className="action-box">
            <input
              type="number"
              placeholder="Enter amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
            <button onClick={handleDeposit}>Confirm Deposit</button>
            <button onClick={() => setView("menu")}>Back</button>
          </div>
        )}

        {view === "withdraw" && (
          <div className="action-box">
            <input
              type="number"
              placeholder="Enter amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
            <button onClick={handleWithdraw}>Confirm Withdraw</button>
            <button onClick={() => setView("menu")}>Back</button>
          </div>
        )}

        {view === "history" && (
          <div className="action-box">
            <h3>Transaction History</h3>
            {transactions.length === 0 && <p>No transactions yet.</p>}
            <ul className="txn-list">
              {transactions.map((t, i) => (
                <li key={i}>
                  {t.timestamp} — {t.type}: ₹{t.amount} (Balance: ₹{t.balance_after})
                </li>
              ))}
            </ul>
            <button onClick={() => setView("menu")}>Back</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
