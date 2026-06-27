import streamlit as st
from llm import analyze_text
from pdf_utils import extract_pdf
import time

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------
# SESSION STATE
# ----------------------------------

defaults = {
    "messages": [],
    "summary": "",
    "document": "",
    "mode": "home",
    "show_uploader": False,
    "chat_history": [],
    "active_chat_id": None,
    "pending_prompt": "",
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ----------------------------------
# HELPERS
# ----------------------------------

def generate_summary(text):
    with st.spinner("🤖 Generating summary..."):
        return analyze_text(text)

def ask_ai(question):
    history = "".join(f"{m['role']}: {m['content']}\n" for m in st.session_state.messages)
    prompt = f"""You are an AI Study Assistant.

Study Material:
{st.session_state.document}

Conversation:
{history}

User Question: {question}

Answer in a simple and detailed way."""
    with st.spinner("Thinking..."):
        return analyze_text(prompt)

def get_chat_title():
    """Title = first user message (truncated)."""
    for m in st.session_state.messages:
        if m["role"] == "user":
            return m["content"][:42].replace("\n", " ") + ("…" if len(m["content"]) > 42 else "")
    # Fallback: first line of document
    first = st.session_state.document.strip().split("\n")[0][:42]
    return first or "Untitled"

def save_current_chat():
    if not st.session_state.summary:
        return
    cid = st.session_state.active_chat_id
    if not cid:
        return
    entry = {
        "id": cid,
        "title": get_chat_title(),
        "messages": list(st.session_state.messages),
        "summary": st.session_state.summary,
        "document": st.session_state.document,
    }
    for i, c in enumerate(st.session_state.chat_history):
        if c["id"] == cid:
            st.session_state.chat_history[i] = entry
            return
    st.session_state.chat_history.insert(0, entry)

def load_chat(cid):
    for c in st.session_state.chat_history:
        if c["id"] == cid:
            st.session_state.active_chat_id = cid
            st.session_state.messages  = list(c["messages"])
            st.session_state.summary   = c["summary"]
            st.session_state.document  = c["document"]
            st.session_state.mode      = "chat"
            st.rerun()

def delete_chat(cid):
    st.session_state.chat_history = [c for c in st.session_state.chat_history if c["id"] != cid]
    if st.session_state.active_chat_id == cid:
        st.session_state.update({
            "messages": [], "summary": "", "document": "",
            "active_chat_id": None, "mode": "home",
        })

def do_submit(text, pdf):
    if not text.strip() and pdf is None:
        st.warning("Please paste some notes or upload a PDF.")
        return
    if pdf is not None:
        with st.spinner("Extracting PDF…"):
            extracted = extract_pdf(pdf)
        if not extracted.strip():
            st.error("No readable text found in this PDF.")
            return
        content = extracted
    else:
        content = text

    save_current_chat()
    new_id = str(int(time.time()))
    summary = generate_summary(content)

    st.session_state.update({
        "document": content,
        "summary": summary,
        "messages": [],
        "show_uploader": False,
        "mode": "chat",
        "active_chat_id": new_id,
    })
    st.session_state.chat_history.insert(0, {
        "id": new_id,
        "title": content.strip().split("\n")[0][:42] or "New Chat",
        "messages": [],
        "summary": summary,
        "document": content,
    })
    st.toast("Summary Generated ✅")
    st.balloons()
    st.rerun()

# ----------------------------------
# CSS
# ----------------------------------

st.markdown("""
<style>
.block-container{ padding-top:1.5rem; padding-bottom:2rem; max-width:860px; }
.main{ background:#0f172a; }
h1,h2,h3{ color:white; }

.hero{
    text-align:center; padding:26px 20px; border-radius:20px; margin-bottom:24px;
    background:linear-gradient(135deg,#4F46E5,#7C3AED); color:white;
}
.hero h1{ font-size:36px; margin-bottom:4px; }
.hero p{ font-size:15px; opacity:.85; margin:0; }

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#0d1117 !important;
    border-right:1px solid rgba(255,255,255,.07) !important;
}

/* New chat button */
section[data-testid="stSidebar"] [data-testid="stButton"]:first-of-type button {
    background:rgba(99,102,241,.15) !important;
    border:1px solid rgba(99,102,241,.4) !important;
    color:#a5b4fc !important;
    border-radius:10px !important;
    height:40px !important;
    font-size:13px !important;
    font-weight:500 !important;
    width:100% !important;
    margin-bottom:4px !important;
    text-align:center !important;
}
section[data-testid="stSidebar"] [data-testid="stButton"]:first-of-type button:hover{
    background:rgba(99,102,241,.3) !important; color:white !important; transform:none !important;
}

/* History item buttons */
section[data-testid="stSidebar"] .stButton > button {
    width:100% !important;
    height:auto !important;
    min-height:36px !important;
    border-radius:8px !important;
    font-size:13px !important;
    font-weight:400 !important;
    border:none !important;
    background:transparent !important;
    color:rgba(255,255,255,.7) !important;
    text-align:left !important;
    padding:7px 10px !important;
    transition:background .15s !important;
    overflow:hidden !important;
    white-space:nowrap !important;
    text-overflow:ellipsis !important;
}
section[data-testid="stSidebar"] .stButton > button:hover{
    background:rgba(255,255,255,.07) !important;
    color:white !important; transform:none !important;
}

/* Main area buttons */
section:not([data-testid="stSidebar"]) .stButton > button {
    width:100%; height:44px; border-radius:10px;
    font-weight:500; font-size:14px;
    border:1px solid rgba(255,255,255,.12);
    background:rgba(255,255,255,.06);
    color:rgba(255,255,255,.85);
    transition:all .2s ease;
}
section:not([data-testid="stSidebar"]) .stButton > button:hover{
    background:rgba(255,255,255,.11); border-color:rgba(255,255,255,.22);
    color:white; transform:none;
}
[data-testid="stDownloadButton"] button{
    background:#4F46E5 !important; border:none !important;
    color:white !important; font-weight:600 !important;
}
[data-testid="stDownloadButton"] button:hover{ background:#4338CA !important; }

/* Input box */
[data-testid="stForm"]{
    border:1.5px solid rgba(255,255,255,.18) !important;
    border-radius:20px !important;
    background:rgba(255,255,255,.05) !important;
    padding:14px 18px 12px 18px !important;
}
[data-testid="stForm"] [data-testid="stTextArea"] label{ display:none !important; }
[data-testid="stForm"] [data-baseweb="textarea"],
[data-testid="stForm"] [data-baseweb="base-input"]{
    background:transparent !important; border:none !important; box-shadow:none !important;
}
[data-testid="stForm"] textarea{
    background:transparent !important; border:none !important;
    box-shadow:none !important; color:white !important;
    font-size:16px !important; resize:none !important;
}
[data-testid="stForm"] hr{ border-color:rgba(255,255,255,.08) !important; margin:8px 0 !important; }

/* + and send inside form */
[data-testid="stForm"] [data-testid="stFormSubmitButton"]:nth-of-type(1) button{
    width:34px !important; height:34px !important; min-height:34px !important;
    border-radius:50% !important; padding:0 !important; font-size:20px !important;
    background:rgba(255,255,255,.08) !important;
    border:1px solid rgba(255,255,255,.2) !important; color:white !important;
}
[data-testid="stForm"] [data-testid="stFormSubmitButton"]:nth-of-type(2) button{
    width:38px !important; height:38px !important; min-height:38px !important;
    border-radius:50% !important; padding:0 !important; font-size:18px !important;
    background:#4F46E5 !important; border:none !important; color:white !important;
}
[data-testid="stForm"] [data-testid="stFormSubmitButton"]:nth-of-type(2) button:hover{
    background:#6366f1 !important; transform:none !important;
}

/* File uploader */
div[data-testid="stFileUploader"]{
    border:1px dashed rgba(255,255,255,.2); border-radius:12px;
    background:rgba(255,255,255,.03); padding:4px 12px; margin-top:-4px;
}
div[data-testid="stFileUploader"] label{ display:none !important; }
div[data-testid="stFileUploaderDropzone"] svg{ display:none !important; }
div[data-testid="stFileUploaderDropzone"] p,
div[data-testid="stFileUploaderDropzone"] span{
    font-size:13px !important; color:rgba(255,255,255,.4) !important;
}

.summary-box{
    border-left:4px solid #6366f1; background:rgba(99,102,241,.08);
    padding:16px 20px; border-radius:12px; margin-bottom:8px;
}
[data-testid="stChatMessage"]{ border-radius:12px; padding:10px; }
footer{ visibility:hidden; }
[data-testid="collapsedControl"]{ display:flex !important; visibility:visible !important; }
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# SIDEBAR
# ----------------------------------

with st.sidebar:
    st.markdown("### 📚 Study Assistant")

    if st.button("＋  New Chat", key="sidebar_new", use_container_width=True):
        save_current_chat()
        st.session_state.update({
            "messages": [], "summary": "", "document": "",
            "show_uploader": False, "active_chat_id": None, "mode": "home",
        })
        st.rerun()

    st.markdown("---")

    history = st.session_state.chat_history
    if not history:
        st.caption("No chats yet")
    else:
        st.markdown('<p style="font-size:11px;color:rgba(255,255,255,.3);margin:0 0 6px 2px;letter-spacing:.7px;">RECENT</p>', unsafe_allow_html=True)
        for chat in history:
            is_active = chat["id"] == st.session_state.active_chat_id
            col_t, col_d = st.columns([10, 1])
            with col_t:
                label = ("● " if is_active else "  ") + chat["title"]
                if st.button(label, key=f"h_{chat['id']}", use_container_width=True):
                    save_current_chat()
                    load_chat(chat["id"])
            with col_d:
                if st.button("✕", key=f"d_{chat['id']}"):
                    delete_chat(chat["id"])
                    st.rerun()

# ----------------------------------
# HEADER
# ----------------------------------

st.markdown("""
<div class="hero">
    <h1>📚 AI Study Assistant</h1>
    <p>Summarize Notes • Analyze PDFs • Ask Unlimited Questions</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# HOME SCREEN
# ----------------------------------

if st.session_state.mode == "home":

    with st.form("input_form", clear_on_submit=False, border=False):
        user_text = st.text_area(
            "notes",
            placeholder="Paste your study notes here…",
            label_visibility="collapsed",
            height=80,
            key="home_textarea",
        )
        st.divider()
        col_plus, col_gap, col_send = st.columns([1, 18, 1])
        with col_plus:
            toggle = st.form_submit_button("＋", help="Attach PDF")
        with col_send:
            send = st.form_submit_button("➤", help="Generate Summary")

    pdf = None
    if st.session_state.show_uploader:
        pdf = st.file_uploader("pdf", type=["pdf"], label_visibility="collapsed", key="home_pdf")
        if pdf:
            st.caption(f"📎 **{pdf.name}** selected — press ➤ to analyze")

    if toggle:
        st.session_state.show_uploader = not st.session_state.show_uploader
        st.rerun()
    if send:
        do_submit(user_text, pdf)

# ----------------------------------
# CHAT SCREEN
# ----------------------------------

elif st.session_state.mode == "chat":

    st.markdown('<div class="summary-box"><p style="margin:0;font-size:13px;color:#a5b4fc;font-weight:600;">📄 SUMMARY</p></div>', unsafe_allow_html=True)
    st.markdown(st.session_state.summary)
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Download Summary", data=st.session_state.summary,
                           file_name="summary.txt", mime="text/plain", use_container_width=True)
    with col2:
        if st.button("📄 New Document", use_container_width=True):
            save_current_chat()
            st.session_state.update({
                "summary": "", "document": "", "messages": [],
                "show_uploader": False, "active_chat_id": None, "mode": "home",
            })
            st.rerun()

    st.divider()

    # ── Chat messages ──
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── Chat input — Enter sends, no button needed ──
    # st.chat_input natively handles Enter key
    prompt = st.chat_input("Ask anything about your document…")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = ask_ai(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        save_current_chat()