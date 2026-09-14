import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import Chat from "./components/Chat";
import { AuthProvider,useAuth } from "./components/AuthContext";


function AppContext(){
  const {user,loading}=useAuth();
  const [showRegister, setShowRegister] = useState(false);

  if(loading){
    return <p>Checking Authentication</p>
  }
  if(!user){
    return showRegister ? <Register onSwitch={() => setShowRegister(false)} /> : <Login onSwitch={() => setShowRegister(true)} />;
  }
  return <Chat/>;
}

function App(){
 return(
  <AuthProvider>
  <AppContext/>
  </AuthProvider>
 );
}

export default App;