import streamlit as st

from agent import run_agent
from tools import reserve_book

st.set_page_config(
    page_title="AI Library Assistant",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>

.stApp {
    background-color: #f8fafc;
}

.main-title {
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    color: #1e293b;
}

.subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 25px;
}

[data-testid="stChatMessage"] {
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">📚 AI Library Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask me to find or reserve books!</div>',
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to the AI Library Assistant.\n\n"
                "I can help you search for books and reserve them.\n\n"
                "What would you like to find today?"
            )
        }
    ]

if "pending_reservation" not in st.session_state:
    st.session_state.pending_reservation = None

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


user_input = st.chat_input("Type your message here...")


if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    pending = st.session_state.pending_reservation

    if pending:

        answer = user_input.strip().lower()

        if answer in ["yes", "y"]:

            result = reserve_book(
                pending["book_id"],
                pending["customer_name"],
                confirmed=True
            )

            if result["success"]:

                reservation = result["reservation"]

                response = (
                    "✅ **Reservation successful!**\n\n"
                    f"**Book:** {reservation['book_title']}\n\n"
                    f"**Customer:** {reservation['customer_name']}\n\n"
                    f"**Reservation ID:** {reservation['reservation_id']}\n\n"
                    f"**Remaining copies:** {result['remaining_copies']}"
                )

            else:

                response = f"❌ {result['message']}"

            st.session_state.pending_reservation = None

        elif answer in ["no", "n"]:

            response = "❌ No problem! Your reservation has been cancelled."

            st.session_state.pending_reservation = None

        else:

            response = (
                "Please reply **yes** to confirm the reservation "
                "or **no** to cancel it."
            )

    else:

        with st.spinner("Thinking..."):

            try:

                result = run_agent(
                    user_input,
                    ui_mode=True
                )

                response = result["response"] or "I'm sorry, I couldn't generate a response."

                st.session_state.pending_reservation = (
                    result["pending_reservation"]
                )

            except Exception as error:

                response = f"Something went wrong: {error}"
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    st.rerun()
