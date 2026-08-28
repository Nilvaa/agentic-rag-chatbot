const API_URL="http://127.0.0.1:8000"

// autheticated api helper
async function authRequest(endpoint,options={}) {
    const token=localStorage.getItem("access_token");

    const response=await fetch(`${API_URL}${endpoint}`,{
        ...options,
        headers:{
            "Content-Type": "application/json",
            ...options.headers,
            ...(token &&{
                Authorization:`Bearer ${token}`,
            }),
        },
    });

    //jwt expired/invalid

    if(response.status==401){
        localStorage.removeItem("access_token");
        window.location.href="/";
        return;
    }
    const data=await response.json()
    if(!response.ok){
        throw new Error(data.detail || "Something went wrong");
    }
    return data;
}

//login
export async function loginUser(email, password) {
    console.log("1. loginUser called");

    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email,
            password,
        }),
    });

    console.log("2. response received:", response.status);

    const data = await response.json();

    console.log("3. response data:", data);

    if (!response.ok) {
        throw new Error(data.detail || "Login failed");
    }

    return data;
}

//register

export async function registerUser(email,password) {
    const response=await fetch(`${API_URL}/auth/register`,{
        method:"POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email,password
        }),
    });

    const data=await response.json();

    if (!response.ok){
        throw new Error (data.detail || "register failed")
    }
    return data
}

//current user
export async function getCurrentUser() {   
    return authRequest("/auth/me");
}

//get conversations
export async function getConversations(){
    return authRequest("/conversations/")
}

//get one conversation
export async function getConversation(conversationId){
    return authRequest(`/conversations/${conversationId}`);
}

//delete conversation
export async function deleteConversations(conversationId){
    return authRequest(`/conversations/${conversationId}`,
        {method:"DELETE"}
    );
}

// send chat message
export async function sendMessage(question,conversationId=null) {
  return authRequest("/chat/",{
    method:"POST",
    body: JSON.stringify({
            question,conversation_id:conversationId  
        }),
  });
}

//logout
export function logoutUser(){
    localStorage.removeItem("access_token");
    window.location.href="/"
}