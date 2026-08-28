import Login from "./components/Login";
import Chat from "./components/Chat";
import { AuthProvider,useAuth } from "./components/AuthContext";


function AppContext(){
  const {user,loading}=useAuth();
  if(loading){
    return <p>Checking Authentication</p>
  }
  if(!user){
    return <Login/>;
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