"""
E-Commerce Insights Agent - Main Streamlit Application
A GenAI-powered agentic system for analyzing e-commerce data
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path
import time
from datetime import datetime

# Must be first Streamlit command
st.set_page_config(
    page_title="E-Commerce Insights Agent",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.config import config, validate_config
from src.database import DatabaseManager
from src.memory import MemoryManager
from src.agents import AgentSystem
from src.utils import VisualizationGenerator, KnowledgeBase
from src.logger import get_logger

logger = get_logger(__name__)


# Custom CSS for modern UI with Dark Mode
def load_custom_css():
    # Get dark mode state
    is_dark = st.session_state.get('dark_mode', False)
    
    # Build CSS dynamically based on theme
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    """
    
    if is_dark:
        css += """
        /* Dark Mode Colors */
        :root {
            --primary-color: #818cf8;
            --primary-dark: #6366f1;
            --secondary-color: #a78bfa;
            --accent-color: #f472b6;
            --success-color: #34d399;
            --warning-color: #fbbf24;
            --error-color: #f87171;
            --background-color: #111827;
            --surface-color: #1f2937;
            --text-color: #f9fafb;
            --text-secondary: #d1d5db;
            --border-color: #374151;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
            border-right: 1px solid var(--border-color);
        }
        
        .user-message::before {
            background: #1f2937 !important;
        }
        """
    else:
        css += """
        /* Light Mode Colors */
        :root {
            --primary-color: #6366f1;
            --primary-dark: #4f46e5;
            --secondary-color: #8b5cf6;
            --accent-color: #ec4899;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --background-color: #f9fafb;
            --surface-color: #ffffff;
            --text-color: #111827;
            --text-secondary: #6b7280;
            --border-color: #e5e7eb;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
            border-right: 1px solid var(--border-color);
        }
        
        .user-message::before {
            background: white !important;
        }
        """
    
    css += """
    /* Global font */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main container */
    .main {
        background-color: var(--background-color);
    }
    
    /* Streamlit specific overrides */
    .stApp {
        background-color: var(--background-color);
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: transparent;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Chat message styling - User */
    .user-message {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 1.25rem 1.5rem;
        border-radius: 1.25rem 1.25rem 0.25rem 1.25rem;
        margin: 1rem 0;
        margin-left: 2rem;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2), 0 2px 4px -1px rgba(99, 102, 241, 0.1);
        animation: slideInRight 0.3s ease-out;
        position: relative;
    }
    
    .user-message::before {
        content: "👤";
        position: absolute;
        left: -2.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Chat message styling - Assistant */
    .assistant-message {
        background: var(--surface-color);
        color: var(--text-color);
        padding: 1.25rem 1.5rem;
        border-radius: 1.25rem 1.25rem 1.25rem 0.25rem;
        margin: 1rem 0;
        margin-right: 2rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        animation: slideInLeft 0.3s ease-out;
        position: relative;
    }
    
    .assistant-message::before {
        content: "🤖";
        position: absolute;
        right: -2.5rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Metric cards */
    .metric-card {
        background: var(--surface-color);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border-left: 4px solid var(--primary-color);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3), 0 4px 6px -2px rgba(99, 102, 241, 0.2);
        animation: fadeIn 0.5s ease-out;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: white;
    }
    
    .main-header p {
        font-size: 1.125rem;
        opacity: 0.95;
        margin-top: 0.5rem;
        color: white;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 0.75rem;
        padding: 0.625rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        border: none;
        background: var(--primary-color);
        color: white;
    }
    
    .stButton>button:hover {
        background: var(--primary-dark);
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3), 0 2px 4px -1px rgba(99, 102, 241, 0.2);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 0.75rem;
        border: 2px solid var(--border-color);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.2s ease;
        background-color: var(--surface-color);
        color: var(--text-color);
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Sidebar text colors */
    [data-testid="stSidebar"] * {
        color: var(--text-color);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        padding: 0.5rem 0;
    }
    
    /* Data table styling */
    .dataframe {
        border-radius: 0.75rem;
        overflow: hidden;
        border: 1px solid var(--border-color);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--surface-color);
        border-radius: 0.75rem;
        border: 1px solid var(--border-color);
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: var(--background-color);
        border-color: var(--primary-color);
    }
    
    /* Success/Error/Warning messages */
    .success-message {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        padding: 1rem 1.25rem;
        border-radius: 0.75rem;
        border-left: 4px solid var(--success-color);
        box-shadow: 0 1px 3px 0 rgba(16, 185, 129, 0.1);
        animation: fadeIn 0.3s ease-out;
    }
    
    .error-message {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        padding: 1rem 1.25rem;
        border-radius: 0.75rem;
        border-left: 4px solid var(--error-color);
        box-shadow: 0 1px 3px 0 rgba(239, 68, 68, 0.1);
        animation: fadeIn 0.3s ease-out;
    }
    
    .warning-message {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        padding: 1rem 1.25rem;
        border-radius: 0.75rem;
        border-left: 4px solid var(--warning-color);
        box-shadow: 0 1px 3px 0 rgba(245, 158, 11, 0.1);
        animation: fadeIn 0.3s ease-out;
    }
    
    /* Code blocks */
    code {
        background: var(--surface-color);
        padding: 0.125rem 0.375rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
        color: var(--primary-color);
        font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-color);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.5rem 0.5rem 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: var(--text-color);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
    }
    
    /* Dark mode toggle button */
    .dark-mode-toggle {
        background: var(--surface-color);
        border: 2px solid var(--border-color);
        border-radius: 2rem;
        padding: 0.5rem 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .dark-mode-toggle:hover {
        border-color: var(--primary-color);
        transform: scale(1.05);
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.db_manager = None
        st.session_state.memory_manager = None
        st.session_state.agent_system = None
        st.session_state.knowledge_base = None
        st.session_state.chat_history = []
        st.session_state.data_loaded = False
        st.session_state.current_data = None
        st.session_state.dark_mode = False  # Dark mode toggle


def check_api_key():
    """Check if API key is configured"""
    if not config.llm.gemini_api_key or config.llm.gemini_api_key == "your_gemini_api_key_here":
        st.error("⚠️ Gemini API Key not configured!")
        st.info("Please set your GEMINI_API_KEY in the .env file")
        st.markdown("""
        **To get your free API key:**
        1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Create a new API key
        3. Add it to your `.env` file as `GEMINI_API_KEY=your_key_here`
        4. Restart the application
        """)
        st.stop()


def initialize_system():
    """Initialize the agent system"""
    if not st.session_state.initialized:
        try:
            with st.spinner("🚀 Initializing E-Commerce Insights Agent..."):
                # Initialize components
                st.session_state.db_manager = DatabaseManager()
                st.session_state.memory_manager = MemoryManager()
                st.session_state.agent_system = AgentSystem(
                    st.session_state.db_manager,
                    st.session_state.memory_manager
                )
                st.session_state.knowledge_base = KnowledgeBase()
                st.session_state.initialized = True
                logger.info("System initialized successfully")
        except Exception as e:
            st.error(f"❌ Initialization failed: {e}")
            logger.error(f"Initialization error: {e}")
            st.stop()


def render_sidebar():
    """Render sidebar with professional controls and information"""
    with st.sidebar:
        # Logo/Brand area
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); border-radius: 1rem; margin-bottom: 1.5rem;">
            <h2 style="color: white; margin: 0; font-size: 1.5rem;">🛒 ECommerce AI</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 0.25rem 0 0 0; font-size: 0.85rem;">Powered by Google Gemini</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Dark Mode Toggle
        st.markdown("### 🎨 Appearance")
        col_theme1, col_theme2 = st.columns(2)
        with col_theme1:
            if st.button("☀️ Light Mode", use_container_width=True, disabled=not st.session_state.dark_mode):
                st.session_state.dark_mode = False
                st.rerun()
        with col_theme2:
            if st.button("🌙 Dark Mode", use_container_width=True, disabled=st.session_state.dark_mode):
                st.session_state.dark_mode = True
                st.rerun()
        
        st.markdown("---")
        
        # System Status Section
        st.markdown("### 🎯 System Status")
        
        status_col1, status_col2 = st.columns(2)
        with status_col1:
            if st.session_state.initialized:
                st.markdown("""
                <div style="background: #d1fae5; padding: 0.5rem; border-radius: 0.5rem; text-align: center;">
                    <div style="font-size: 1.5rem;">✅</div>
                    <div style="font-size: 0.75rem; color: #065f46;">System</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #fef3c7; padding: 0.5rem; border-radius: 0.5rem; text-align: center;">
                    <div style="font-size: 1.5rem;">⏳</div>
                    <div style="font-size: 0.75rem; color: #92400e;">System</div>
                </div>
                """, unsafe_allow_html=True)
        
        with status_col2:
            if st.session_state.data_loaded:
                st.markdown("""
                <div style="background: #d1fae5; padding: 0.5rem; border-radius: 0.5rem; text-align: center;">
                    <div style="font-size: 1.5rem;">✅</div>
                    <div style="font-size: 0.75rem; color: #065f46;">Data</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #dbeafe; padding: 0.5rem; border-radius: 0.5rem; text-align: center;">
                    <div style="font-size: 1.5rem;">📊</div>
                    <div style="font-size: 0.75rem; color: #1e40af;">No Data</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Data Management Section
        st.markdown("### 📂 Data Management")
        
        data_dir = st.text_input(
            "Data Directory",
            value="data",
            help="Path to directory containing CSV files",
            label_visibility="collapsed"
        )
        
        if st.button("🔄 Load/Reload Data", use_container_width=True, type="primary"):
            load_data(Path(data_dir))
        
        if st.session_state.data_loaded and st.session_state.db_manager:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📋 Loaded Tables", expanded=True):
                tables = st.session_state.db_manager.get_table_list()
                for idx, table in enumerate(tables):
                    stats = st.session_state.db_manager.get_table_stats(table)
                    row_count = stats.get('row_count', 0)
                    col_count = stats.get('column_count', 0)
                    
                    st.markdown(f"""
                    <div style="background: var(--surface-color); padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 3px solid #6366f1;">
                        <div style="font-weight: 600;">{table}</div>
                        <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem;">
                            {row_count:,} rows · {col_count} columns
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Conversation Management
        st.markdown("### 💬 Conversation")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.memory_manager.clear_history() if st.session_state.memory_manager else None
                st.rerun()
        
        with col2:
            if st.button("💾 Export", use_container_width=True):
                if st.session_state.chat_history:
                    chat_df = pd.DataFrame(st.session_state.chat_history)
                    st.download_button(
                        "📥 Download",
                        chat_df.to_csv(index=False),
                        "chat_history.csv",
                        "text/csv",
                        use_container_width=True
                    )
        
        # Chat statistics
        if st.session_state.chat_history:
            msg_count = len(st.session_state.chat_history)
            st.caption(f"💬 {msg_count} messages in conversation")
        
        st.markdown("---")
        
        # API Rate Limit Info
        st.markdown("### ℹ️ API Usage")
        st.info("""
**Free Tier Limits:**
- ~15 queries/minute
- Wait 1-2 min if rate limited
- Auto-retry enabled (3 attempts)
        """)
        
        st.markdown("---")
        
        # Example queries
        st.markdown("### 💡 Example Queries")
        
        examples = [
            "Top 10 products by revenue",
            "Customer distribution by state",
            "Average review scores",
            "Sales trends over time",
            "Payment method analysis"
        ]
        
        for example in examples:
            if st.button(f"▸ {example}", key=f"example_{example}", use_container_width=True):
                st.session_state.current_query = example
                st.rerun()


def load_data(data_dir: Path):
    """Load CSV data into database with professional feedback"""
    try:
        with st.spinner("📊 Loading data... Please wait"):
            if not data_dir.exists():
                st.markdown(f"""
                <div class="error-message">
                    <strong>❌ Directory not found</strong>
                    <p style="margin: 0.5rem 0 0 0;">The path <code>{data_dir}</code> does not exist.</p>
                </div>
                """, unsafe_allow_html=True)
                return
            
            loaded_tables = st.session_state.db_manager.load_csv_data(data_dir)
            
            if loaded_tables:
                st.session_state.data_loaded = True
                
                # Success message
                st.markdown(f"""
                <div class="success-message">
                    <strong>✅ Data loaded successfully!</strong>
                    <p style="margin: 0.5rem 0 0 0;">Successfully loaded {len(loaded_tables)} tables with a total of {sum(loaded_tables.values()):,} rows.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show detailed summary
                with st.expander("📋 View Details", expanded=False):
                    for idx, (table, count) in enumerate(loaded_tables.items()):
                        st.markdown(f"""
                        <div style="background: var(--surface-color); padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 3px solid #10b981;">
                            <div style="font-weight: 600;">{table}</div>
                            <div style="color: var(--text-secondary); font-size: 0.875rem;">{count:,} rows loaded</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                logger.info(f"Data loaded successfully: {loaded_tables}")
            else:
                st.markdown("""
                <div class="warning-message">
                    <strong>⚠️ No data files found</strong>
                    <p style="margin: 0.5rem 0 0 0;">Please check if CSV files exist in the specified directory.</p>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            <strong>❌ Error loading data</strong>
            <p style="margin: 0.5rem 0 0 0;">{str(e)}</p>
        </div>
        """, unsafe_allow_html=True)
        logger.error(f"Data loading error: {e}")


def render_chat_interface():
    """Render chat interface with professional styling"""
    # Show welcome message if no chat history
    if not st.session_state.chat_history:
        theme_gradient = "#667eea 0%, #764ba2 100%" if not st.session_state.dark_mode else "#4f46e5 0%, #7c3aed 100%"
        st.markdown(f"""
        <div style="text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, {theme_gradient}); border-radius: 1.5rem; margin: 2rem 0; box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.3);">
            <h1 style="color: white; font-size: 2.5rem; margin: 0;">🛒 E-Commerce Insights Agent</h1>
            <p style="color: rgba(255,255,255,0.95); font-size: 1.2rem; margin: 1rem 0;">Your AI-powered assistant for intelligent data analysis and business insights</p>
        </div>
        
        <div style="background: var(--surface-color); padding: 2rem; border-radius: 1rem; margin: 1.5rem 0; border: 1px solid var(--border-color);">
            <h3 style="margin: 0 0 1rem 0;">✨ What can I help you with today?</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1.5rem;">
                <div style="background: var(--background-color); padding: 1.25rem; border-radius: 0.75rem; border-left: 3px solid #6366f1;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">Sales Analysis</div>
                    <div style="color: var(--text-secondary); font-size: 0.875rem;">Analyze revenue, top products, and sales trends</div>
                </div>
                <div style="background: var(--background-color); padding: 1.25rem; border-radius: 0.75rem; border-left: 3px solid #8b5cf6;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">👥</div>
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">Customer Insights</div>
                    <div style="color: var(--text-secondary); font-size: 0.875rem;">Understand customer behavior and demographics</div>
                </div>
                <div style="background: var(--background-color); padding: 1.25rem; border-radius: 0.75rem; border-left: 3px solid #ec4899;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">⭐</div>
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">Review Analysis</div>
                    <div style="color: var(--text-secondary); font-size: 0.875rem;">Explore ratings and customer feedback</div>
                </div>
                <div style="background: var(--background-color); padding: 1.25rem; border-radius: 0.75rem; border-left: 3px solid #f59e0b;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🗺️</div>
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">Geographic Distribution</div>
                    <div style="color: var(--text-secondary); font-size: 0.875rem;">Visualize sales across regions</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            render_message(message)
    
    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input area with enhanced styling
    st.markdown("""
    <div style="position: sticky; bottom: 0; background: var(--background-color); padding: 1rem 0; border-top: 2px solid var(--border-color); margin-top: 2rem;">
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask a question...",
            key="user_input",
            placeholder="💬 Ask me anything about your e-commerce data (e.g., What are the top selling products?)",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send 📤", use_container_width=True, type="primary")
    
    # Quick action buttons
    st.markdown("<div style='margin-top: 0.5rem;'>", unsafe_allow_html=True)
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    
    with quick_col1:
        if st.button("🔝 Top Products", use_container_width=True, help="Get top selling products"):
            st.session_state.current_query = "What are the top 10 best-selling products?"
            st.rerun()
    
    with quick_col2:
        if st.button("💰 Revenue Analysis", use_container_width=True, help="Analyze revenue trends"):
            st.session_state.current_query = "Show me revenue trends over time"
            st.rerun()
    
    with quick_col3:
        if st.button("⭐ Customer Reviews", use_container_width=True, help="Analyze customer reviews"):
            st.session_state.current_query = "What are the average review scores by category?"
            st.rerun()
    
    with quick_col4:
        if st.button("🗺️ Geographic", use_container_width=True, help="Geographic analysis"):
            st.session_state.current_query = "Which states have the most customers?"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Check for example query
    if 'current_query' in st.session_state and st.session_state.current_query:
        user_input = st.session_state.current_query
        st.session_state.current_query = None
        send_button = True
    
    # Process query
    if send_button and user_input:
        process_query(user_input)
        st.rerun()


def render_message(message: dict):
    """Render a chat message with professional styling"""
    role = message['role']
    content = message['content']
    timestamp = message.get('timestamp', '')
    
    if role == 'user':
        st.markdown(f"""
        <div class="user-message">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong style="font-size: 0.95rem;">You</strong>
                <span style="opacity: 0.8; font-size: 0.75rem;">{timestamp}</span>
            </div>
            <p style="margin: 0; line-height: 1.6; font-size: 0.95rem;">{content}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong style="font-size: 0.95rem;">AI Assistant</strong>
                <span style="opacity: 0.6; font-size: 0.75rem;">{timestamp}</span>
            </div>
            <div style="line-height: 1.6; font-size: 0.95rem;">
        """, unsafe_allow_html=True)
        
        # Render content with markdown support
        st.markdown(content)
        
        # Render data table if available
        if 'data' in message and message['data'] is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📊 View Data Table", expanded=False):
                st.dataframe(
                    message['data'],
                    use_container_width=True,
                    height=min(400, (len(message['data']) + 1) * 35)
                )
        
        # Render visualization if available
        if 'visualization' in message and message['visualization'] is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            st.plotly_chart(
                message['visualization'],
                use_container_width=True,
                config={'displayModeBar': True, 'displaylogo': False}
            )
        
        # Render SQL query if available
        if 'sql_query' in message and message['sql_query']:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🔍 View SQL Query", expanded=False):
                st.code(message['sql_query'], language='sql', line_numbers=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)


def process_query(user_query: str):
    """Process user query through agent system"""
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data first before querying.")
        return
    
    # Add user message
    user_message = {
        'role': 'user',
        'content': user_query,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.chat_history.append(user_message)
    
    # Process with agent system
    try:
        with st.spinner("🤔 Analyzing your query..."):
            response = st.session_state.agent_system.process_query(user_query)
            
            # Prepare assistant message
            assistant_message = {
                'role': 'assistant',
                'content': response.get('answer', response.get('response', 'I apologize, but I encountered an issue processing your request.')),
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'data': response.get('data'),
                'visualization': response.get('visualization'),
                'sql_query': response.get('sql_query')
            }
            
            st.session_state.chat_history.append(assistant_message)
            logger.info(f"Query processed: {user_query[:50]}...")
            
    except Exception as e:
        error_str = str(e)
        
        # Check if it's a rate limit error
        if "rate limit" in error_str.lower() or "429" in error_str or "resource exhausted" in error_str.lower():
            error_content = """⏳ **API Rate Limit Reached**
            
I've hit the Google Gemini API rate limit (free tier). This happens when making multiple queries quickly.

**What to do:**
- ⏰ Wait 1-2 minutes and try again
- 🔄 Your question will work once the quota resets
- 💡 Tip: Space out your queries to avoid this

Your question: "{}"

I'll be ready to answer in a moment! 😊""".format(user_query)
        else:
            error_content = f"❌ **Error:** {error_str}\n\nPlease try rephrasing your question or contact support if this persists."
        
        error_message = {
            'role': 'assistant',
            'content': error_content,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.chat_history.append(error_message)
        logger.error(f"Query processing error: {e}")


def render_metrics_dashboard():
    """Render professional metrics dashboard"""
    if not st.session_state.data_loaded:
        return
    
    st.markdown("""
    <div style="margin: 2rem 0 1.5rem 0;">
        <h3 style="margin: 0;">📈 Quick Insights</h3>
        <p style="margin: 0.25rem 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">Real-time overview of your e-commerce data</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        db = st.session_state.db_manager
        
        # Total Orders
        with col1:
            result, _ = db.execute_query("SELECT COUNT(*) as count FROM orders")
            total_orders = result['count'].iloc[0] if not result.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: var(--text-secondary); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                    Total Orders
                </div>
                <div style="color: #6366f1; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">
                    {total_orders:,}
                </div>
                <div style="color: #10b981; font-size: 0.8rem;">
                    📦 Active
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Total Customers
        with col2:
            result, _ = db.execute_query("SELECT COUNT(*) as count FROM customers")
            total_customers = result['count'].iloc[0] if not result.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: var(--text-secondary); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                    Total Customers
                </div>
                <div style="color: #8b5cf6; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">
                    {total_customers:,}
                </div>
                <div style="color: #10b981; font-size: 0.8rem;">
                    👥 Registered
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Total Products
        with col3:
            result, _ = db.execute_query("SELECT COUNT(*) as count FROM products")
            total_products = result['count'].iloc[0] if not result.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: var(--text-secondary); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                    Total Products
                </div>
                <div style="color: #ec4899; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">
                    {total_products:,}
                </div>
                <div style="color: #10b981; font-size: 0.8rem;">
                    🏷️ Listed
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Total Sellers
        with col4:
            result, _ = db.execute_query("SELECT COUNT(*) as count FROM sellers")
            total_sellers = result['count'].iloc[0] if not result.empty else 0
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: var(--text-secondary); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                    Total Sellers
                </div>
                <div style="color: #f59e0b; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">
                    {total_sellers:,}
                </div>
                <div style="color: #10b981; font-size: 0.8rem;">
                    🏪 Active
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        logger.error(f"Error rendering metrics: {e}")
        st.error("Unable to load metrics. Please ensure data is loaded correctly.")


def main():
    """Main application function"""
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Check API key
    check_api_key()
    
    # Initialize system
    initialize_system()
    
    # Render sidebar
    render_sidebar()
    
    # Render metrics dashboard
    if st.session_state.data_loaded:
        render_metrics_dashboard()
    
    # Render chat interface
    render_chat_interface()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; color: var(--text-secondary); font-size: 0.875rem; border-top: 1px solid var(--border-color); margin-top: 2rem;">
        <p style="margin: 0;">Built with ❤️ using <strong>Streamlit</strong> & <strong>Google Gemini</strong></p>
        <p style="margin: 0.25rem 0 0 0;">E-Commerce Insights Agent v1.0.0 | © 2025</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
