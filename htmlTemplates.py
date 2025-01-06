css = '''
<style>
/* General styling for the chat container */
.chat-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 1rem;
    background-color: #1e1e2f;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* Styling for chat messages */
.chat-message {
    padding: 1rem;
    border-radius: 20px;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    animation: fadeIn 0.5s ease-in-out;
    position: relative;
}

/* User message styling */
.chat-message.user {
    background: linear-gradient(135deg, #6c5ce7, #5a3ea3);
    margin-left: auto;
    margin-right: 0;
    color: #fff;
    border-bottom-right-radius: 0;
}

/* Bot message styling */
.chat-message.bot {
    background: linear-gradient(135deg, #4e54c8, #8f94fb);
    margin-left: 0;
    margin-right: auto;
    color: #fff;
    border-bottom-left-radius: 0;
}

/* Avatar styling */
.chat-message .avatar {
    width: 50px;
    height: 50px;
    margin-right: 1rem;
    border: 2px solid rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.chat-message .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Message text styling */
.chat-message .message {
    flex: 1;
    font-size: 1rem;
    line-height: 1.5;
}

/* Animation for chat messages */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Input box styling */
.stTextInput>div>div>input {
    background-color: #1f2937;
    color: #ffffff;
    border-radius: 10px;
    border: 1px solid #6c757d;
    padding: 0.75rem;
    font-size: 1rem;
}

.stTextInput>div>div>input:focus {
    border-color: #7c3aed;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.4);
}

/* Button styling */
.stButton>button {
    background-color: #7c3aed;
    color: #ffffff;
    border-radius: 10px;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border: none;
    transition: background-color 0.3s ease;
}

.stButton>button:hover {
    background-color: #5a3eae;
}

/* Sidebar styling */
.sidebar .sidebar-content {
    background-color: #1e1e2f;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* Header styling */
.stHeader {
    color: #ffffff;
    font-size: 2rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
}

/* Spinner styling */
.stSpinner>div {
    border-color: #7c3aed transparent transparent transparent;
}

/* Success message styling */
.stSuccess {
    color: #7c3aed;
    font-weight: bold;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/kB3qh7J/ai-icon.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/nbW9q5V/user-icon.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
