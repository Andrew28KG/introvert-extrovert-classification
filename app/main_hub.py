import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Personality Discovery Hub",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .app-card {
        background: white;
        padding: 3rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        border: 1px solid #e1e5e9;
        transition: all 0.3s ease;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .app-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        border-color: #2c3e50;
    }
    
    .app-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .app-description {
        color: #555;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        font-size: 1rem;
        flex-grow: 1;
    }
    
    .header-section {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #666;
        font-weight: 400;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Clean header
    st.markdown("""
    <div class="header-section">
        <h1 class="main-title">🧠 Personality Discovery Hub</h1>
        <p class="subtitle">Discover your personality through interactive experiences and creative expression</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two main apps
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="app-card">
            <div class="app-title">🎭 Scenario-Based Assessment</div>
            <div class="app-description">
                Navigate through realistic life situations and make authentic choices that reveal your personality. 
                Experience immersive storytelling with detailed behavioral analysis and comprehensive insights.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Assessment", key="assessment", use_container_width=True):
            st.switch_page("pages/1_Assessment.py")
    
    with col2:
        st.markdown("""
        <div class="app-card">
            <div class="app-title">🎨 AI Art Generator</div>
            <div class="app-description">
                Transform your personality into stunning artwork using OpenAI's DALL-E 3! Answer thoughtful questions 
                about your preferences and generate beautiful, personalized AI art that reflects your unique traits.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎨 Create Art", key="art", use_container_width=True):
            st.switch_page("pages/2_Art_Generator.py")
    
    # Simple comparison
    st.markdown("---")
    st.markdown("### 🔍 App Comparison")
    
    comparison_data = {
        'Feature': ['Assessment Type', 'Duration', 'Interaction Style', 'Visual Output', 'Best For', 'Technology'],
        '🎭 Scenario Assessment': [
            'Real-life scenarios',
            '5-8 minutes',
            'Story-driven choices',
            'Charts & detailed insights',
            'Accurate personality analysis',
            'ML-powered analysis'
        ],
        '🎨 AI Art Generator': [
            'Personality questionnaire',
            '3-5 minutes',
            'Interactive questions',
            'AI-generated artwork',
            'Creative self-expression',
            'OpenAI DALL-E 3'
        ]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Simple instructions
    st.markdown("---")
    st.info("**How to use:** Choose an app above to begin your personality discovery journey. Each offers a unique perspective on understanding yourself!")

if __name__ == "__main__":
    main() 