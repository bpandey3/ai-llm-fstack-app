import streamlit as st
import json
from ice_breaker import ice_break_with

def create_list_items(items):
    if items:
        for item in items:
            st.markdown(f"- {item}")

def process(name):
    summary, profile_pic_url = ice_break_with(name=name)
    return {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url,
        }
    

def main():
# Page configuration
    st.set_page_config(
        page_title="AI Profile Search",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        /* Gradient animated header */
        .title {
            background: linear-gradient(
                to right,
                #12c2e9,
                #c471ed,
                #f64f59
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient 5s ease infinite;
            font-size: 4rem !important;
            font-weight: 800 !important;
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        
        /* Profile image styling */
        .profile-img {
            border-radius: 50%;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
            display: block;
            margin: 0 auto;
        }
        .profile-img:hover {
            transform: scale(1.05);
        }
        
        /* Input and button styling */
        .stTextInput > div > div > input {
            border-radius: 25px;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #c471ed;
            box-shadow: 0 0 10px rgba(196, 113, 237, 0.3);
        }
        .stButton > button {
            border-radius: 25px;
            padding: 15px 25px;
            font-weight: 600;
            background: linear-gradient(45deg, #12c2e9, #c471ed);
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Results container styling */
        .results-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Custom blockquote style for summary */
        blockquote {
            border-left: 4px solid #c471ed;
            padding-left: 20px;
            margin: 20px 0;
            color: #555;
        }
        
        /* Facts list styling */
        .fact-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 10px 15px;
            margin: 8px 0;
            border-left: 4px solid #12c2e9;
        }
        </style>
    """, unsafe_allow_html=True)

    # Animated Header
    st.markdown('<h1 class="title">Profile Search AI</h1>', unsafe_allow_html=True)

    # Results container (will appear at the top)
    results_container = st.container()

    # Create a spacer
    st.markdown("<br>" * 3, unsafe_allow_html=True)

    # Input section at the bottom
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            with st.form("name_form", clear_on_submit=False):
                name = st.text_input("", placeholder="✨ Enter a name to search...", 
                                   help="Enter the full name of the person you want to search for")
                submit_button = st.form_submit_button("🔍 Search Profile")

    # When form is submitted
    if submit_button and name:
        with results_container:
            with st.spinner('🔮 Magic in progress...'):
                try:
                    summary, profile_pic_url = ice_break_with(name=name)
                    
                    # Profile picture
                    if profile_pic_url:
                        st.markdown(
                            f'<img src="{profile_pic_url}" class="profile-img" width="200">',
                            unsafe_allow_html=True
                        )
                    
                    # Summary section
                    st.markdown("### 📝 Professional Summary")
                    st.markdown(f"> {summary.summary}")
                    
                    # Facts section
                    st.markdown("### 🎯 Key Insights")
                    for fact in summary.facts:
                        st.markdown(f'<div class="fact-item">• {fact}</div>', 
                                  unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"🚨 Oops! Something went wrong: {str(e)}")

if __name__ == "__main__":
    main()