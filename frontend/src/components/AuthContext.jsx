import { createContext,useContext,useEffect,useState } from "react";
import { getCurrentUser,logoutUser } from "../services/api";

const AuthContext =createContext(null);

export function AuthProvider({children}){
    const [user,setUser]=useState(null);
    const [loading,setLoading]=useState(true);

    useEffect(()=>{
        async function checkAuthentication() {
            const token=localStorage.getItem("access_token");

                //if not jwt then no user logged in
                if(!token){
                    setLoading(false);
                    return;
                }
                try{
                    const currentUser=await getCurrentUser();
                    setUser(currentUser);
                }catch(error){
                    console.log("Authentication failed:",error);
                    localStorage.removeItem("access_token");
                    setUser(null);
                }finally{
                    setLoading(false);
                }
        }checkAuthentication();
    },[]);

    function logout(){
        logoutUser();
        setUser(null);
    }

    return (
        <AuthContext.Provider
        value={{
            user,setUser,loading,logout
        }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth(){
    return useContext(AuthContext)
}
