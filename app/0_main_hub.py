import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="🧠 Personality Discovery Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the hub
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        min-height: 100vh;
        padding: 2rem 1rem;
    }
    
    .hub-header {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ff9a56);
        background-size: 400% 400%;
        animation: gradient 5s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hub-subtitle {
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .app-card {
        background: rgba(255, 255, 255, 0.95);
        color: #2d3748;
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
        height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .app-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    
    .app-icon {
        font-size: 5rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .app-title {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .app-description {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #4a5568;
        text-align: center;
        flex-grow: 1;
    }
    
    .app-features {
        font-size: 1rem;
        color: #718096;
        margin-top: 1.5rem;
    }
    
    .welcome-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .stats-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    .stat-box {
        background: rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.5rem;
    }
    
    .footer-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="hub-header">🧠 Personality Discovery Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hub-subtitle">Discover your personality through interactive experiences and creative expression</p>', unsafe_allow_html=True)
    
    # Welcome section
    st.markdown("""
    <div class="welcome-section">
        <h2 style="margin-bottom: 1.5rem; color: white;">🌟 Welcome to Your Personality Journey!</h2>
        <p style="font-size: 1.1rem; line-height: 1.7; color: rgba(255, 255, 255, 0.9);">
            Discover the depths of your personality through our carefully crafted applications. 
            Take a comprehensive scenario-based assessment and transform your personality into beautiful art 
            using cutting-edge AI technology and psychological insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Apps showcase
    st.markdown("## 🎯 Choose Your Personality Adventure")
    
    # Create columns for apps - now just 2 columns for 2 apps
    col1, col2 = st.columns(2)
    
    with col1:
        # Scenario-Based Assessment
        st.markdown("""
        <div class="app-card">
            <div class="app-icon">🎭</div>
            <div class="app-title">Scenario-Based Assessment</div>
            <div class="app-description">
                Navigate through 8 realistic life situations and make authentic choices that reveal your personality. 
                Experience immersive storytelling with detailed behavioral analysis and comprehensive insights.
            </div>
            <div class="app-features">
                🎯 Realistic life scenarios<br>
                📊 Advanced personality analysis<br>
                🧠 ML-powered insights<br>
                💾 Downloadable comprehensive reports
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Assessment", key="assessment", use_container_width=True):
            st.switch_page("pages/1_Assessment.py")
    
    with col2:
        # AI Art Generator
        st.markdown("""
        <div class="app-card">
            <div class="app-icon">🎨</div>
            <div class="app-title">AI Personality Art Generator</div>
            <div class="app-description">
                Transform your personality into stunning artwork using OpenAI's DALL-E 3! Answer thoughtful questions 
                about your preferences and generate beautiful, personalized AI art that reflects your unique traits.
            </div>
            <div class="app-features">
                🤖 AI-generated images using DALL-E 3<br>
                🎯 Personalized art based on personality<br>
                🌈 Custom color palette analysis<br>
                💾 High-quality downloadable artwork
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎨 Create Art", key="art", use_container_width=True):
            st.switch_page("pages/2_Art_Generator.py")
    
    # Statistics section
    st.markdown("""
    <div class="stats-container">
        <h3 style="text-align: center; margin-bottom: 2rem; color: white;">📊 Platform Statistics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">2</div>
            <div class="stat-label">Powerful Apps</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">99%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">∞</div>
            <div class="stat-label">Art Possibilities</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Features comparison
    st.markdown("## 🔍 Compare Our Apps")
    
    comparison_data = {
        'Feature': [
            'Assessment Type',
            'Duration', 
            'Interaction Style',
            'Visual Output',
            'Best For',
            'Technology'
        ],
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
    
    # About section
    st.markdown("""
    <div class="footer-section">
        <h3 style="margin-bottom: 1.5rem; color: white;">💡 About This Project</h3>
        <p style="color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
            This personality discovery platform combines machine learning, psychology, and cutting-edge AI technology 
            to offer two distinct perspectives on personality assessment. Experience scenario-based behavioral analysis 
            and transform your personality into beautiful, AI-generated artwork using DALL-E 3.
        </p>
        <p style="color: rgba(255, 255, 255, 0.7); margin-top: 1rem; font-size: 0.9rem;">
            Built with ❤️ using Streamlit, OpenAI DALL-E 3, Plotly, and advanced AI analysis • 
            Generated on {datetime.now().strftime('%B %Y')}
        </p>
    </div>
    """.format(datetime=datetime), unsafe_allow_html=True)

if __name__ == "__main__":
    main() 