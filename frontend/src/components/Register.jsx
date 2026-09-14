import { useState } from "react";
import { registerUser } from "../services/api";
import "./Login.css";

function Register({ onSwitch }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();
        setError("");
        setSuccess("");
        setLoading(true);
        try {
            await registerUser(email, password);
            setSuccess("Registration successful! Please login.");
            setTimeout(() => {
                onSwitch();
            }, 2000);
        } catch (error) {
            console.error("REGISTER ERROR:", error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="login-container">
            <div className="login-card">
                <h1 className="login-title">Register</h1>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Email</label>
                        <input
                            type="email"
                            className="form-input"
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            className="form-input"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            required
                        />
                    </div>
                    {error && (
                        <p className="error-message">{error}</p>
                    )}
                    {success && (
                        <p style={{ color: "green", marginBottom: "1rem", fontSize: "0.875rem" }}>{success}</p>
                    )}
                    <button type="submit" className="submit-button" disabled={loading}>
                        {loading ? "Registering.." : "Register"}
                    </button>
                </form>
                <p style={{ marginTop: "1rem", textAlign: "center", fontSize: "0.9rem", color: "#555" }}>
                    Already have an account? <span style={{ color: "#007bff", cursor: "pointer", fontWeight: "500" }} onClick={onSwitch}>Login</span>
                </p>
            </div>
        </div>
    );
}

export default Register;
