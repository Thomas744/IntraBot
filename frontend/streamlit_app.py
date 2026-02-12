import streamlit as st
from api_client import login_user, query_backend

# Page Config
st.set_page_config(
    page_title="Company Internal Chatbot",
    page_icon="🏢",
    layout="wide",
)

# Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔑 flag to ensure welcome message shows only once
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

# Role → Departments (RBAC aligned)
ROLE_DEPARTMENTS = {
    "finance": ["finance", "general"],
    "marketing": ["marketing", "general"],
    "hr": ["hr", "general"],
    "engineering": ["engineering", "general"],
    "employees": ["general"],
    "c_level": ["finance", "marketing", "hr", "engineering", "general"],
}

# 🔐 LOGIN PAGE
def login_page():
    st.markdown(
        """
        <div style="text-align:center; padding-top:80px;">
            <h1>🏢 Company Internal Chatbot</h1>
            <p>Secure role-based access to internal documents</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            st.subheader("🔐 Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                result = login_user(username, password)
                if not result:
                    st.error("Invalid username or password.")
                else:
                    st.session_state.authenticated = True
                    st.session_state.token = result["access_token"]
                    st.session_state.user = {
                        "username": username,
                        "role": result["role"],
                    }
                    st.session_state.messages = []
                    st.session_state.welcome_shown = False
                    st.rerun()

# 🤖 CHATBOT PAGE
def chatbot_page():
    user = st.session_state.user
    role = user["role"]
    departments = ROLE_DEPARTMENTS.get(role, [])

    # Sidebar
    with st.sidebar:
        st.markdown("## 👤 User Panel")
        st.success("Logged in")

        st.markdown(f"**User:** `{user['username']}`")
        st.markdown(f"**Role:** `{role.upper()}`")

        st.markdown("### 📂 Accessible Departments")
        for d in departments:
            st.markdown(f"- {d}")

        st.markdown("---")

        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.messages = []
            st.session_state.welcome_shown = False
            st.rerun()

    # Main Chat UI
    st.title("🏢 Company Internal Chatbot")

    st.caption(
        f"You are logged in as **{role.upper()}**. "
        "Answers are restricted to your permitted departments."
    )
    st.markdown("---")

    # Welcome message (ONLY ONCE)
    if not st.session_state.welcome_shown:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    "👋 **Welcome to the Company Internal Chatbot**\n\n"
                    "I help you find **role-specific information** from internal company documents.\n\n"
                    "You can ask about reports, metrics, summaries, or comparisons related to your department.\n\n"
                    "💡 **Tip:** Ask clear questions with a *timeframe* or *metric* for best results."
                ),
            }
        )
        st.session_state.welcome_shown = True

    # Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    user_input = st.chat_input("Ask a question about company documents...")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        response = query_backend(
            st.session_state.token,
            user_input,
        )

        if not response:
            assistant_text = "❌ Error communicating with backend."
            citations = []
        else:
            assistant_text = response.get("answer", "No answer returned.")
            citations = response.get("citations", [])

        if citations:
            assistant_text += "\n\n---\n**Sources:**"
            for c in citations:
                assistant_text += (
                    f"\n- `{c['department']}` | `{c['source_path']}`"
                )

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_text}
        )

        with st.chat_message("assistant"):
            st.markdown(assistant_text)

# ROUTER
if not st.session_state.authenticated:
    login_page()
else:
    chatbot_page()
