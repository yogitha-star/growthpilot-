import streamlit as st
from groq import Groq
import time

# Page configuration
st.set_page_config(
    page_title="GrowthPilot - AI Startup Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design
st.markdown("""
    <style>
    /* Smooth animations */
    * {
        transition: all 0.3s ease;
    }
    
    /* Main background - Modern gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Sidebar - Premium dark theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%);
        box-shadow: 4px 0 20px rgba(0,0,0,0.2);
    }
    
    /* Sidebar text - White labels */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: white !important;
    }
    
    /* Input fields - Clear visibility */
    [data-testid="stSidebar"] input {
        color: #1a202c !important;
        background-color: #f7fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 10px !important;
    }
    
    [data-testid="stSidebar"] input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Selectbox - Clear dark text on light background */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #f7fafc !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #1a202c !important;
        background-color: #f7fafc !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        border: 2px solid #e2e8f0 !important;
    }
    
    /* Dropdown menu items */
    [data-baseweb="popover"] {
        background-color: white !important;
    }
    
    [data-baseweb="menu"] {
        background-color: white !important;
    }
    
    [data-baseweb="menu"] li {
        color: #1a202c !important;
        background-color: white !important;
        padding: 12px !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: #edf2f7 !important;
    }
    
    /* Premium buttons with gradient */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 14px 20px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        font-size: 0.95rem !important;
        text-transform: none !important;
    }
    
    .stButton button:hover {
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Header card - Modern & eye-catching */
    .header-card {
        background: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #2d3748;
        font-weight: 600;
        margin-bottom: 0.6rem;
    }
    
    .tagline {
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.8;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Chat messages - Modern cards */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 15px !important;
        padding: 1.2rem !important;
        margin: 0.8rem 0 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08) !important;
        border-left: 4px solid #667eea !important;
    }
    
    /* Chat input - Enhanced visibility */
    .stChatInputContainer input,
    .stChatInputContainer textarea {
        color: #1a202c !important;
        background-color: white !important;
        border: 3px solid #667eea !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 1rem !important;
    }
    
    .stChatInputContainer input:focus,
    .stChatInputContainer textarea:focus {
        border-color: #764ba2 !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Info cards - Simpler design */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .info-card h4 {
        color: #667eea;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .info-card p {
        color: #4a5568;
        line-height: 1.5;
        margin: 0;
        font-size: 0.95rem;
    }
    
    /* Success/Error messages - Better visibility */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
    }
    
    /* Profile summary card */
    .profile-summary {
        background: rgba(102, 126, 234, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Divider styling */
    hr {
        margin: 1.5rem 0 !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "startup_stage" not in st.session_state:
    st.session_state.startup_stage = "Idea Stage"
if "industry" not in st.session_state:
    st.session_state.industry = "Fashion & Clothing"
if "founder_type" not in st.session_state:
    st.session_state.founder_type = "First-Time Founder"
if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

# Sidebar
with st.sidebar:
    st.markdown("## 🔑 API Configuration")
    
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.groq_api_key,
        placeholder="Enter your Groq API key...",
        help="Get your free API key from console.groq.com"
    )
    
    if api_key:
        st.session_state.groq_api_key = api_key
        masked = api_key[:7] + "•" * 10 + api_key[-4:] if len(api_key) > 11 else "•" * len(api_key)
        st.success("✅ API Connected!")
        st.caption(f"🔒 {masked}")
    else:
        st.warning("⚠️ Add your API key to get started")
        st.info("👉 Visit console.groq.com to get a free API key")
    
    st.markdown("---")
    
    st.markdown("## 👤 Your Profile")
    
    founder_type = st.selectbox(
        "Founder Type:",
        [
            "First-Time Founder",
            "Student Founder", 
            "Solo Founder",
            "Rural Entrepreneur",
            "Serial Entrepreneur",
            "Technical Founder",
            "Non-Technical Founder"
        ],
        index=[
            "First-Time Founder",
            "Student Founder", 
            "Solo Founder",
            "Rural Entrepreneur",
            "Serial Entrepreneur",
            "Technical Founder",
            "Non-Technical Founder"
        ].index(st.session_state.founder_type),
        help="Your experience level helps personalize advice"
    )
    st.session_state.founder_type = founder_type
    
    startup_stage = st.selectbox(
        "Current Stage:",
        [
            "Idea Stage",
            "Market Research",
            "Validation Stage",
            "MVP Development",
            "Beta Testing",
            "First Users (0-100)",
            "Growth Stage (100-1000)",
            "Scaling (1000+)",
            "Pre-Funding",
            "Post-Funding"
        ],
        index=[
            "Idea Stage",
            "Market Research",
            "Validation Stage",
            "MVP Development",
            "Beta Testing",
            "First Users (0-100)",
            "Growth Stage (100-1000)",
            "Scaling (1000+)",
            "Pre-Funding",
            "Post-Funding"
        ].index(st.session_state.startup_stage),
        help="We'll provide stage-appropriate guidance"
    )
    st.session_state.startup_stage = startup_stage
    
    industry = st.selectbox(
        "Industry:",
        [
            "Fashion & Clothing",
            "SaaS & Tech",
            "E-commerce",
            "Food & Beverage",
            "Health & Wellness",
            "Education & EdTech",
            "FinTech",
            "Agriculture & AgriTech",
            "Real Estate",
            "Consulting & Services",
            "Media & Entertainment",
            "Travel & Hospitality",
            "Other"
        ],
        index=[
            "Fashion & Clothing",
            "SaaS & Tech",
            "E-commerce",
            "Food & Beverage",
            "Health & Wellness",
            "Education & EdTech",
            "FinTech",
            "Agriculture & AgriTech",
            "Real Estate",
            "Consulting & Services",
            "Media & Entertainment",
            "Travel & Hospitality",
            "Other"
        ].index(st.session_state.industry),
        help="Industry-specific strategies and insights"
    )
    st.session_state.industry = industry
    
    # Profile Summary
    st.markdown("---")
    st.markdown("### 📊 Profile Summary")
    st.markdown(f"""
    <div class='profile-summary'>
        <strong>👤 Type:</strong> {st.session_state.founder_type}<br>
        <strong>🚀 Stage:</strong> {st.session_state.startup_stage}<br>
        <strong>🏢 Industry:</strong> {st.session_state.industry}<br>
        <strong>💬 Chats:</strong> {st.session_state.chat_count}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## ⚡ Quick Actions")
    st.caption("Click any button for instant guidance:")
    
    if st.button("💡 Validate My Idea", use_container_width=True, key="validate"):
        if not st.session_state.groq_api_key:
            st.error("🔑 Add API key first!")
        else:
            st.session_state.messages.append({
                "role": "user", 
                "content": "I have a startup idea. Help me validate it step by step. What should I focus on?"
            })
            st.rerun()
    
    if st.button("🎯 Create Marketing Plan", use_container_width=True, key="marketing"):
        if not st.session_state.groq_api_key:
            st.error("🔑 Add API key first!")
        else:
            st.session_state.messages.append({
                "role": "user",
                "content": f"Create a simple, actionable marketing plan for my {st.session_state.startup_stage} startup in {st.session_state.industry}."
            })
            st.rerun()
    
    if st.button("💰 Build Sales Strategy", use_container_width=True, key="sales"):
        if not st.session_state.groq_api_key:
            st.error("🔑 Add API key first!")
        else:
            st.session_state.messages.append({
                "role": "user",
                "content": f"Help me build a sales strategy that works for {st.session_state.startup_stage}. Keep it simple and actionable."
            })
            st.rerun()
    
    if st.button("📝 Write Sales Pitch", use_container_width=True, key="pitch"):
        if not st.session_state.groq_api_key:
            st.error("🔑 Add API key first!")
        else:
            st.session_state.messages.append({
                "role": "user",
                "content": "Help me write a compelling sales pitch for my startup. Make it clear and persuasive."
            })
            st.rerun()
    
    if st.button("📈 Get First Customers", use_container_width=True, key="customers"):
        if not st.session_state.groq_api_key:
            st.error("🔑 Add API key first!")
        else:
            st.session_state.messages.append({
                "role": "user",
                "content": "What's the best way to get my first 10 customers? Give me specific tactics I can start today."
            })
            st.rerun()
    
    if st.button("🚀 Next Steps (This Week)", use_container_width=True, key="nextsteps"):
        if not st.session_state.groq_api_key:
            st.error("🔑 Add API key first!")
        else:
            st.session_state.messages.append({
                "role": "user",
                "content": f"I'm at {st.session_state.startup_stage}. What are the 3 most important things I should do THIS WEEK?"
            })
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Conversation", use_container_width=True, key="clear"):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.rerun()

# Main Header - Improved central design
st.markdown("""
    <div class='header-card'>
        <div class='main-title'>🚀 Startup AI Assistant</div>
        <div class='subtitle'>Learn from Real Founder Journeys</div>
        <div class='tagline'>
            Get advice based on what real founders tried, what failed, and what actually worked.<br>
            Personalized for your role, stage, and industry—without expensive consultants.
        </div>
    </div>
""", unsafe_allow_html=True)

# Enhanced System Prompt - SHORT AND CLEAR
SYSTEM_PROMPT = f"""You are a helpful AI mentor for startup founders. You're helping a {st.session_state.founder_type} in {st.session_state.industry} at {st.session_state.startup_stage}.

CRITICAL RULES - FOLLOW STRICTLY:
1. Keep responses VERY SHORT (maximum 4-5 sentences)
2. Use SIMPLE, everyday language (like talking to a friend)
3. NO jargon, NO complex terms
4. Give ONE clear point per response
5. End with ONE specific action they can take

RESPONSE FORMAT:
- First sentence: Direct answer to their question
- Next 2-3 sentences: Brief explanation
- Last sentence: One specific action to take this week

EXAMPLES OF GOOD RESPONSES:

Question: "How do I get my first customers?"
Good Answer: "Start by talking to 10 people who have the problem you're solving. Ask them about their current solution and what frustrates them. This week, make a list of 10 potential customers and reach out to 3 of them for a 15-minute chat."

Question: "How do I validate my idea?"
Good Answer: "Talk to at least 20 potential customers before building anything. Ask if they currently pay for a solution to this problem. This week, reach out to 5 people in your target audience and ask them 3 questions about their pain points."

BAD RESPONSES (Don't do this):
- Long paragraphs
- Multiple points at once
- Complex frameworks or theory
- Jargon like "MVP", "product-market fit", "CAC", "LTV"
- More than 5 sentences

Remember: They're overwhelmed. Keep it SHORT, SIMPLE, and ACTIONABLE."""

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Auto-generate AI response when last message is from user (button clicks)
if (len(st.session_state.messages) > 0 and 
    st.session_state.messages[-1]["role"] == "user" and 
    st.session_state.groq_api_key):
    
    # Count how many assistant messages we have
    assistant_count = sum(1 for msg in st.session_state.messages if msg["role"] == "assistant")
    user_count = sum(1 for msg in st.session_state.messages if msg["role"] == "user")
    
    # Debug info (remove after testing)
    # st.sidebar.write(f"DEBUG: Users={user_count}, Assistants={assistant_count}")
    
    # If user messages > assistant messages, we need to respond
    if user_count > assistant_count:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    client = Groq(api_key=st.session_state.groq_api_key)
                    
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    messages.extend(st.session_state.messages)
                    
                    full_response = ""
                    placeholder = st.empty()
                    
                    stream = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=300,
                        top_p=0.9,
                        stream=True,
                    )
                    
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            full_response += chunk.choices[0].delta.content
                            placeholder.markdown(full_response + "▌")
                    
                    placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Make sure your API key is valid (get one at console.groq.com)")
                    # Don't rerun on error so user can see the error message

# Chat input
if prompt := st.chat_input("💬 Ask me anything about building and growing your startup..."):
    if not st.session_state.groq_api_key:
        st.error("⚠️ Please add your Groq API key in the sidebar to start chatting!")
        
        st.stop()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_count += 1
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.session_state.groq_api_key)
            
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(st.session_state.messages)
            
            full_response = ""
            placeholder = st.empty()
            
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=300,  # Shorter responses - easier to read
                top_p=0.9,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"❌ Oops! Something went wrong: {str(e)}")
            st.info("💡 **Troubleshooting:**\n- Check if your API key is valid\n- Make sure you have internet connection\n- Try refreshing the page")

# Welcome message (only when no messages)
if len(st.session_state.messages) == 0:
    st.markdown("### 🎯 Quick Start Prompts")
    st.caption("Click any card to ask that question:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Marketing Strategy", use_container_width=True, key="ex_marketing"):
            if not st.session_state.groq_api_key:
                st.error("Add API key first!")
            else:
                st.session_state.messages.append({
                    "role": "user",
                    "content": "How do I create a marketing strategy for my SaaS startup with zero budget?"
                })
                st.rerun()
        st.caption("Get a simple marketing plan with no budget")
    
    with col2:
        if st.button("💰 Sales Process", use_container_width=True, key="ex_sales"):
            if not st.session_state.groq_api_key:
                st.error("Add API key first!")
            else:
                st.session_state.messages.append({
                    "role": "user",
                    "content": "What's the best sales process for a B2B product with a 6-month sales cycle?"
                })
                st.rerun()
        st.caption("Build an effective sales strategy")
    
    with col3:
        if st.button("📈 First 100 Customers", use_container_width=True, key="ex_growth"):
            if not st.session_state.groq_api_key:
                st.error("Add API key first!")
            else:
                st.session_state.messages.append({
                    "role": "user",
                    "content": "What are the top 3 things I should focus on to get my first 100 customers?"
                })
                st.rerun()
        st.caption("Get your first customers quickly")
    
    st.markdown("---")
    
    st.markdown("### 🌟 What Makes This Different:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📖 Real Founder Stories", use_container_width=True, key="feature1"):
            if not st.session_state.groq_api_key:
                st.error("Add API key first!")
            else:
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Show me real examples of founders who succeeded in my industry. What did they try and what worked?"
                })
                st.rerun()
        st.markdown("""
        - Learn from actual examples
        - See what worked and what failed
        - Get honest, practical advice
        """)
    
    with col2:
        if st.button("🎯 Get Personalized Plan", use_container_width=True, key="feature2"):
            if not st.session_state.groq_api_key:
                st.error("Add API key first!")
            else:
                st.session_state.messages.append({
                    "role": "user",
                    "content": f"Based on my profile ({st.session_state.founder_type}, {st.session_state.startup_stage}, {st.session_state.industry}), what should I focus on right now?"
                })
                st.rerun()
        st.markdown("""
        - Based on your stage and industry
        - Simple language, no jargon
        - Action-focused next steps
        """)
    
    st.info("💡 **Tip:** Click any button above or use Quick Actions in the sidebar!")
