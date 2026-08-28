import { useEffect, useState } from "react";

import {
    sendMessage,
    getConversations,
    getConversation,
    deleteConversations,
    logoutUser
} from "../services/api";


function Chat() {

    const [question, setQuestion] = useState("");

    // Stores the complete chat history displayed on screen
    const [messages, setMessages] = useState([]);

    // Current conversation ID
    const [conversationId, setConversationId] = useState(null);

    // Sidebar conversations
    const [conversations, setConversations] = useState([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");


    // ==================================================
    // SEND MESSAGE
    // ==================================================

    async function handleSubmit(event) {

        event.preventDefault();

        if (!question.trim()) {
            return;
        }

        const currentQuestion = question.trim();

        setLoading(true);
        setError("");

        try {

            // ------------------------------------------
            // SHOW USER MESSAGE IMMEDIATELY
            // ------------------------------------------

            setMessages((prev) => [
                ...prev,
                {
                    role: "user",
                    content: currentQuestion,
                    sources: []
                }
            ]);


            // ------------------------------------------
            // SEND QUESTION TO BACKEND
            // ------------------------------------------

            const data = await sendMessage(
                currentQuestion,
                conversationId
            );

            console.log("chat response:", data);


            // ------------------------------------------
            // ADD ASSISTANT RESPONSE
            // ------------------------------------------

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: data.answer,
                    sources: data.sources || []
                }
            ]);


            // ------------------------------------------
            // SAVE CONVERSATION ID
            // ------------------------------------------

            setConversationId(data.conversation_id);


            // Clear input
            setQuestion("");


            // ------------------------------------------
            // REFRESH CONVERSATION LIST
            // ------------------------------------------

            const updatedConversations =
                await getConversations();

            setConversations(updatedConversations);


        } catch (error) {

            console.error("Chat error:", error);

            setError(error.message);

        } finally {

            setLoading(false);

        }
    }


    // ==================================================
    // LOAD CONVERSATIONS
    // ==================================================

    useEffect(() => {

        async function loadConversations() {

            try {

                const data = await getConversations();

                console.log(
                    "conversations:",
                    data
                );

                setConversations(data);

            } catch (error) {

                console.error(
                    "Conversation loading error:",
                    error
                );

                setError(error.message);

            }
        }

        loadConversations();

    }, []);


    // ==================================================
    // LOAD ONE CONVERSATION
    // ==================================================

    async function handleConversationClick(id) {

        setError("");
        setLoading(true);

        try {

            const data = await getConversation(id);

            console.log(
                "selected conversation:",
                data
            );


            // ------------------------------------------
            // SET CURRENT CONVERSATION
            // ------------------------------------------

            setConversationId(id);


            // ------------------------------------------
            // LOAD ALL MESSAGES
            // ------------------------------------------

            if (
    data.messages &&
    data.messages.length > 0
) {
    const loadedMessages =
        data.messages.map((message) => ({
            id: message.id,
            role: message.role,
            content: message.content,
            sources: message.sources || []
        }));

    setMessages(loadedMessages);

} else {
    setMessages([]);
}


            setQuestion("");


        } catch (error) {

            console.error(
                "Conversation loading error:",
                error
            );

            setError(error.message);

        } finally {

            setLoading(false);

        }
    }

    async function handleDeleteConversation(id) {

    const confirmed = window.confirm(
        "Are you sure you want to delete this conversation?"
    );

    if (!confirmed) {
        return;
    }

    setError("");

    try {

        await deleteConversations(id);

        setConversations((prev) =>
            prev.filter(
                (conversation) =>
                    conversation.id !== id
            )
        );

        if (conversationId === id) {
            setConversationId(null);
            setAnswer("");
            setSources([]);
            setQuestion("");
        }

    } catch (error) {
        setError(error.message);
    }
}

    // ==================================================
    // NEW CHAT
    // ==================================================

    function handleNewChat() {

        // IMPORTANT:
        // null means the next question creates
        // a completely new conversation.

        setConversationId(null);

        setMessages([]);

        setQuestion("");

        setError("");
    }




    // ==================================================
    // LOGOUT
    // ==================================================

    function handleLogout() {

        logoutUser();

    }


    // ==================================================
    // UI
    // ==================================================

    return (

        <div className="chat-app">


            {/* ==================================================
                SIDEBAR
            ================================================== */}

            <aside className="sidebar">


                <div className="sidebar-header">

                    <h2>
                        AI ChatBot
                    </h2>

                </div>


                {/* NEW CHAT */}

                <button
                    className="new-chat-button"
                    onClick={handleNewChat}
                >
                    + New Chat
                </button>


                {/* CONVERSATIONS */}

                <div className="conversation-section">

                    <h3>
                        Conversations
                    </h3>


                    {conversations.map(
                        (conversation) => (

                           <div
    className={`conversation-wrapper ${
        conversationId === conversation.id
            ? "active"
            : ""
    }`}
    key={conversation.id}
>

    <button
        className="conversation-item"
        onClick={() =>
            handleConversationClick(
                conversation.id
            )
        }
    >
        {conversation.title ||
            `Conversation ${conversation.id}`}
    </button>

    <button
        className="delete-conversation-button"
        onClick={() =>
            handleDeleteConversation(
                conversation.id
            )
        }
        title="Delete conversation"
    >
        🗑️
    </button>

</div>

                        )
                    )}

                </div>


                {/* LOGOUT */}

                <div className="sidebar-bottom">

                    <button
                        className="logout-button"
                        onClick={handleLogout}
                    >
                        Logout
                    </button>

                </div>

            </aside>


            {/* ==================================================
                MAIN CHAT
            ================================================== */}

            <main className="chat-main">


                {/* HEADER */}

                <header className="chat-header">

                    <h1>
                        AI Assistant
                    </h1>

                </header>


                {/* ==================================================
                    CHAT CONTENT
                ================================================== */}

                <div className="chat-content">


                    {/* WELCOME MESSAGE */}

                    {messages.length === 0 && (

                        <div className="welcome">

                            <h2>
                                How can I help you?
                            </h2>

                            <p>
                                Ask a question about the
                                Apple Business Conduct Policy
                                or Human Rights Policy.
                            </p>

                        </div>

                    )}


                    {/* ==================================================
                        MESSAGES
                    ================================================== */}

                    {messages.length > 0 && (

                        <div className="messages">

                            {messages.map(
                                (message, index) => (

                                    <div
                                        className={`message ${message.role}`}
                                        key={index}
                                    >


                                        {/* MESSAGE LABEL */}

                                        <div className="message-label">

                                            {message.role === "user"
                                                ? "You"
                                                : "Assistant"
                                            }

                                        </div>


                                        {/* MESSAGE CONTENT */}

                                        <div className="message-bubble">

                                            {message.content}

                                        </div>


                                        {/* ==================================================
                                            SOURCES
                                        ================================================== */}

                                        {message.role === "assistant" &&
                                            message.sources &&
                                            message.sources.length > 0 && (

                                                <div className="sources">

                                                    <h3>
                                                        Sources
                                                    </h3>


                                                    {message.sources.map(
                                                        (
                                                            source,
                                                            sourceIndex
                                                        ) => (

                                                            <div
                                                                className="source-item"
                                                                key={sourceIndex}
                                                            >


                                                                {/* DOCUMENT SOURCE */}

                                                                {source.type === "document" && (

                                                                    <>

                                                                        <strong>
                                                                            📄{" "}
                                                                            {source.filename}
                                                                        </strong>

                                                                        <p>
                                                                            Page:{" "}
                                                                            {source.page}
                                                                            {" | "}
                                                                            Chunk:{" "}
                                                                            {source.chunk}
                                                                        </p>

                                                                    </>

                                                                )}


                                                                {/* WEB SOURCE */}

                                                                {source.type === "web" && (

                                                                    <>

                                                                        <strong>
                                                                            🌐{" "}
                                                                            {source.title}
                                                                        </strong>

                                                                        <p>
                                                                            Web search result
                                                                        </p>


                                                                        {source.url && (

                                                                            <a
                                                                                href={source.url}
                                                                                target="_blank"
                                                                                rel="noopener noreferrer"
                                                                            >
                                                                                Open source ↗
                                                                            </a>

                                                                        )}

                                                                    </>

                                                                )}

                                                            </div>

                                                        )
                                                    )}

                                                </div>

                                            )}

                                    </div>

                                )
                            )}

                        </div>

                    )}


                    {/* ==================================================
                        ERROR
                    ================================================== */}

                    {error && (

                        <div className="error-message">

                            {error}

                        </div>

                    )}

                </div>


                {/* ==================================================
                    INPUT
                ================================================== */}

                <div className="chat-input-container">


                    <form
                        className="chat-form"
                        onSubmit={handleSubmit}
                    >


                        <input
                            type="text"
                            value={question}
                            onChange={(event) =>
                                setQuestion(
                                    event.target.value
                                )
                            }
                            placeholder="Ask a question..."
                            disabled={loading}
                        />


                        <button
                            type="submit"
                            disabled={loading}
                        >

                            {loading
                                ? "Thinking..."
                                : "Send"
                            }

                        </button>


                    </form>

                </div>


            </main>

        </div>

    );
}


export default Chat;