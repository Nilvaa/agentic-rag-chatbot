import { useState } from "react";
import { loginUser , getCurrentUser} from "../services/api"
import { useAuth } from "./AuthContext";

function Login() {
    const [email,setEmail]=useState("");
    const [password,setPassword]=useState("");
    const [error,setError]=useState("");
    const [loading,setLoading]=useState(false);

    const { setUser } =useAuth();

    async function handleSubmit(event){
        event.preventDefault();
        console.log("LOGIN BUTTON CLICKED");
        console.log("EMAIL:", email);
        console.log("PASSWORD:", password);
        
        setError("");
        setLoading(true);
        try{
            const data= await loginUser(email,password);
            console.log("login succesfull: ",data);
            localStorage.setItem("access_token",data.access_token);
            const currentUser= await getCurrentUser();
            console.log("current user: ",currentUser);
            setUser(currentUser)
            
        }catch(error){
            console.error("LOGIN ERROR:", error);
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