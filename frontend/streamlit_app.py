import streamlit as st
from api_client import login_user, query_backend, get_users, add_user_api, delete_user_api

# Page Config
st.set_page_config(page_title="Company Internal Chatbot",page_icon="🏢",layout="wide")

# Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "chatbot"

if "show_add_user" not in st.session_state:
    st.session_state.show_add_user = False

if "delete_confirm_user" not in st.session_state:
    st.session_state.delete_confirm_user = None

# Role → Departments
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
        <div style="text-align:center">
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
                    st.session_state.current_page = "chatbot"
                    st.rerun()


# 👥 MANAGE USERS PAGE
def manage_users_page():
    st.title("👥 User Management")
    st.caption("Manage company users and role assignments.")

    users = get_users(st.session_state.token)

    if not users:
        st.error("Unable to fetch users.")
        return

    st.markdown("### 📋 Users")
    st.markdown("---")

    for u in users:
        col1, col2, col3 = st.columns([3, 2, 1])

        col1.markdown(f"**{u['username']}**")
        col2.markdown(f"`{u['role'].upper()}`")

        if u["username"] == st.session_state.user["username"]:
            col3.markdown("—")
        else:
            if col3.button("🗑", key=f"del_{u['username']}"):
                st.session_state.delete_confirm_user = u["username"]

    # DELETE CONFIRMATION
    if st.session_state.delete_confirm_user:
        st.warning(
            f"⚠ Are you sure you want to delete user "
            f"**{st.session_state.delete_confirm_user}**?"
        )

        c1, c2 = st.columns(2)

        if c1.button("✅ Yes, Delete"):
            delete_user_api(
                st.session_state.token,
                st.session_state.delete_confirm_user,
            )
            st.session_state.delete_confirm_user = None
            st.success("User deleted successfully.")
            st.rerun()

        if c2.button("❌ Cancel"):
            st.session_state.delete_confirm_user = None
            st.rerun()

    st.markdown("---")

    # ADD USER BUTTON
    if not st.session_state.show_add_user:
        if st.button("➕ Add New User"):
            st.session_state.show_add_user = True
            st.rerun()
    else:
        st.markdown("### ➕ Create New User")

        with st.form("add_user_form"):
            username = st.text_input("Username")
            role = st.selectbox(
                "Role",
                [
                    "finance",
                    "marketing",
                    "hr",
                    "engineering",
                    "employees",
                    "c_level",
                ],
            )
            password = st.text_input("Password", type="password")

            submit = st.form_submit_button("Create User")

            if submit:
                response = add_user_api(
                    st.session_state.token,
                    username,
                    role,
                    password,
                )

                if response.status_code == 200:
                    st.success("User created successfully.")
                else:
                    st.error("User already exists.")

                st.session_state.show_add_user = False
                st.rerun()

        if st.button("⬅ Back"):
            st.session_state.show_add_user = False
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

        # TOGGLE BUTTON
        if role == "c_level":
            if st.session_state.current_page == "chatbot":
                if st.button("👥 Manage Users"):
                    st.session_state.current_page = "manage_users"
                    st.rerun()
            else:
                if st.button("🤖 Chatbot"):
                    st.session_state.current_page = "chatbot"
                    st.rerun()

        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.messages = []
            st.session_state.welcome_shown = False
            st.session_state.current_page = "chatbot"
            st.rerun()

    if st.session_state.current_page == "manage_users":
        manage_users_page()
        return

    st.title("🏢 Company Internal Chatbot")

    st.caption(
        f"You are logged in as **{role.upper()}**. "
        "Answers are restricted to your permitted departments."
    )
    st.markdown("---")

    if not st.session_state.welcome_shown:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    "👋 **Welcome to the Company Internal Chatbot**\n\n"
                    "I help you find **role-specific information** from internal company documents.\n\n"
                    "💡 Ask clear questions with timeframe or metrics for best results."
                ),
            }
        )
        st.session_state.welcome_shown = True

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input(
        "Ask a question about company documents..."
    )

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

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

        st.rerun()


# ROUTER
if not st.session_state.authenticated:
    login_page()
else:
    chatbot_page()
