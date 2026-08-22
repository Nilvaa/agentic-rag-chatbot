import { useState } from "react";
import { loginUser } from "../services/api"

function Login() {
    const [email,setEmail]=useState("");
    const [password,setPassword]=useState("");
    const [error,setError]=useState("");
    const [loading,setLoading]=useState("");

    async function handleSubmit(event){
        event.preventDefault();
        setError("");
        setLoading(true);
        try{
            const data= await loginUser(email,password);
            console.log("login succesfull: ",data);
            localStorage.setItem("access_token",data.access_token);
            
        }catch(error){
            setError(error.message);
        }finally{
            setLoading(false);
        }
    }
    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email</label>
                    <input type="email" value={email} onChange={(event)=>setEmail(event.target.value)} 
                    required/>
                </div>
                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        required
                    />
                </div>
                {error && (
                    <p>{error}</p>
                )}
                <button type="submit" disabled={loading}>
                    {loading ? "Logging in..":"Login"}
                </button>
            </form>
        </div>
    );
}

export default Login;