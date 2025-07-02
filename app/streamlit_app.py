import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import random

# Configure page
st.set_page_config(
    page_title="Personality Discovery Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: #fafbfc;
        padding: 1rem;
    }
    
    .main-header {
        font-size: 2.8rem;
        color: #1a202c;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    .welcome-container {
        background: #ffffff;
        padding: 3rem 2rem;
        border-radius: 16px;
        margin: 2rem auto;
        max-width: 800px;
        color: #2d3748;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    }
    
    .welcome-container h2 {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: #1a202c;
        text-align: center;
        line-height: 1.3;
    }
    
    .welcome-container p {
        font-size: 1.1rem;
        line-height: 1.7;
        margin-bottom: 2rem;
        color: #4a5568;
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .features-card {
        background: #ffffff;
        color: #2d3748;
        padding: 2rem 1.5rem;
        border-radius: 12px;
        margin: 1.5rem auto;
        max-width: 600px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    }
    
    .features-card h3 {
        color: #1a202c;
        font-weight: 600;
        margin-bottom: 1.5rem;
        font-size: 1.2rem;
        text-align: center;
    }
    
    .features-list {
        font-size: 1rem;
        line-height: 1.8;
        color: #4a5568;
        text-align: left;
    }
    
    .question-container {
        background: #ffffff;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin: 2rem auto;
        max-width: 900px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.03);
        border: 1px solid #e2e8f0;
    }
    
    .question-text {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1a202c;
        margin-bottom: 0.8rem;
        text-align: center;
        line-height: 1.5;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .question-subtitle {
        font-size: 1rem;
        color: #718096;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: transparent;
        padding: 0;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .stRadio > div > div > div {
        background: #ffffff;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 0.8rem 0;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    .stRadio > div > div > div:hover {
        border-color: #cbd5e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        background: #f7fafc;
    }
    
    .stRadio > div > div > div > label {
        color: #2d3748 !important;
        font-weight: 400;
        font-size: 1rem;
        cursor: pointer;
        line-height: 1.6;
        display: block;
        width: 100%;
        margin: 0;
    }
    
    /* Selected radio button styling */
    .stRadio > div > div > div[data-checked="true"] {
        background: #edf2f7;
        border-color: #a0aec0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .result-container {
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .introvert-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .extrovert-result {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .result-title {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .result-confidence {
        font-size: 1.6rem;
        font-weight: 500;
        opacity: 0.95;
    }
    
    .traits-card {
        background: linear-gradient(135deg, #ffffff 0%, #f7f9fc 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
    
    .traits-card h3 {
        color: #2c3e50;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
    }
    
    .insights-card {
        background: linear-gradient(135deg, #ffffff 0%, #f7f9fc 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
    
    .insights-card h3 {
        color: #2c3e50;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
    }
    
    .fun-fact {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 3px solid #68d391;
        margin: 1.5rem auto;
        max-width: 600px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    .fun-fact-title {
        color: #1a202c;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.8rem;
    }
    
    .fun-fact-text {
        color: #4a5568;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3498db, #2c3e50);
        border-radius: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        background: #4299e1;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        background: #3182ce;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    
    /* Chart styling */
    .js-plotly-plot {
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        overflow: hidden;
        background: white;
    }
    
    /* Trait and insight items */
    .trait-item {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        font-size: 1rem;
        color: #2d3748;
        transition: all 0.2s ease;
    }
    
    .trait-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .insight-item {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 4px solid #2c3e50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        color: #2d3748;
        line-height: 1.5;
        transition: all 0.2s ease;
    }
    
    .insight-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Animations */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
</style>
""", unsafe_allow_html=True)

# Load models and components
@st.cache_resource
def load_model_components():
    try:
        model = joblib.load('../models/naive_bayes_model.pkl')
        return model, True
    except:
        return None, False

# Questions for the quiz
def get_questions():
    return [
        {
            "id": "social_energy",
            "question": "🎊 You walk into a bustling house party with music pumping and people everywhere...",
            "subtitle": "How does your energy respond to this social storm?",
            "image": "🏠🎵👥💃🕺",
            "options": [
                "🚀 Party Mode Activated! I'm immediately scanning for new faces to meet and conversations to join",
                "😊 Cautious Explorer - I take a moment to survey the scene, then gradually join conversations",
                "🤝 Familiar Faces First - I seek out people I know and stick with smaller groups",
                "🚪 Exit Strategy Ready - I'm already calculating how long I need to stay before I can politely leave"
            ],
            "scores": [1, 2, 3, 4]
        },
        {
            "id": "alone_time",
            "question": "🌅 It's Saturday morning and you have absolutely nothing planned...",
            "subtitle": "What sounds like the perfect way to spend your free day?",
            "image": "🛏️☕📱🌳",
            "options": [
                "📞 Social Butterfly - Texting friends: 'What's everyone doing today?' Adventure awaits!",
                "🎯 Balanced Mixer - Maybe brunch with friends, then some chill time at home",
                "🏡 Cozy Controller - A few close friends over for movies, games, or just hanging out",
                "📚 Solo Sanctuary - Perfect! Time for hobbies, reading, nature walks, or creative projects"
            ],
            "scores": [1, 2, 3, 4]
        },
        {
            "id": "communication",
            "question": "💬 During a group brainstorming session, your natural style is...",
            "subtitle": "How do ideas flow from your mind to the world?",
            "image": "🧠💭✨🗣️",
            "options": [
                "🎤 Verbal Volcano - Ideas are bursting out, I love thinking out loud with everyone!",
                "⚡ Quick Contributor - I share thoughts as they come, mixing listening with spontaneous input",
                "🤔 Thoughtful Processor - I listen first, then share carefully considered ideas",
                "📝 Silent Strategist - I prefer to think deeply first, maybe jot notes before speaking"
            ],
            "scores": [1, 2, 3, 4]
        },
        {
            "id": "social_circles",
            "question": "👥 Your ideal social universe looks like...",
            "subtitle": "Quality vs quantity - what's your friendship philosophy?",
            "image": "🌐🤝💫👫",
            "options": [
                "🎪 Social Galaxy - A vast constellation of friends, acquaintances, and exciting new connections",
                "🌈 Diverse Network - Good mix of close buddies and friendly acquaintances for different vibes",
                "🏰 Trusted Circle - A solid crew of reliable friends who really 'get' me",
                "💎 Precious Few - Just a handful of incredibly deep, soul-level connections"
            ],
            "scores": [1, 2, 3, 4]
        },
        {
            "id": "public_speaking",
            "question": "🎤 Surprise! You're asked to give an impromptu speech to 50 people...",
            "subtitle": "What's your immediate reaction and how do you feel?",
            "image": "🎭🎯👥📢",
            "options": [
                "🌟 Spotlight Ready - 'This is my moment!' I thrive under attention and love the challenge",
                "💪 Nervous Excitement - Butterflies, but also kind of thrilling. I can totally do this!",
                "😬 Manageable Anxiety - Deep breaths... I'll push through and probably do okay",
                "🙈 Internal Panic - Is there a back exit? Can I fake a phone call? HELP!"
            ],
            "scores": [1, 2, 3, 4]
        },
        {
            "id": "social_media",
            "question": "📱 Your social media personality is best described as...",
            "subtitle": "How do you show up in the digital world?",
            "image": "📸💬👍❤️",
            "options": [
                "📺 Content Creator - Frequent posts, stories, live updates. Sharing life in real-time!",
                "🎯 Selective Sharer - Regular posts about meaningful moments and interests",
                "👀 Thoughtful Observer - Occasional posts, but I love seeing what others are up to",
                "🕵️ Digital Ghost - Mostly lurking. I read everything but rarely post anything"
            ],
            "scores": [1, 2, 3, 4]
        },
        {
            "id": "weekend_plans",
            "question": "🌈 Your ideal weekend adventure would be...",
            "subtitle": "What fills your cup and energizes your soul?",
            "image": "🎨🎪🌲🛋️",
            "options": [
                "🎢 Action Packed - Festivals, concerts, parties. Jam-pack it with people and activities!",
                "⚖️ Best of Both - Mix of social events and personal time. Variety is the spice of life",
                "🎯 Selective Social - One meaningful hangout plus plenty of downtime to recharge",
                "🧘 Peaceful Retreat - Nature walks, creative hobbies, meditation. Pure tranquility"
            ],
            "scores": [1, 2, 3, 4]
        },
        {
            "id": "energy_levels",
            "question": "🔋 After 4 hours at a lively social gathering, you typically feel...",
            "subtitle": "How do extended social interactions affect your inner battery?",
            "image": "⚡🔋😴💪",
            "options": [
                "🚀 Supercharged - Buzzing with energy. Where's the after-party?!",
                "😌 Pleasantly Satisfied - Good times, but ready to start winding down",
                "😮‍💨 Socially Spent - That was nice, but I definitely need some quiet time now",
                "🛌 Completely Drained - Social battery at 0%. Must find solitude immediately!"
            ],
            "scores": [1, 2, 3, 4]
        }
    ]

def calculate_personality(answers):
    """Calculate personality based on quiz answers"""
    total_score = sum(answers.values())
    max_score = len(answers) * 4
    introversion_percentage = (total_score / max_score) * 100
    
    if introversion_percentage >= 60:
        return "Introvert", introversion_percentage
    else:
        return "Extrovert", 100 - introversion_percentage

def create_personality_chart(personality, confidence):
    """Create a visual chart for personality results"""
    if personality == "Introvert":
        intro_val = confidence
        extro_val = 100 - confidence
    else:
        extro_val = confidence  
        intro_val = 100 - confidence
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Extrovert', 'Introvert'],
        y=[extro_val, intro_val],
        marker_color=['#ff7f0e', '#9467bd'],
        text=[f'{extro_val:.1f}%', f'{intro_val:.1f}%'],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Your Personality Profile",
        yaxis_title="Percentage",
        showlegend=False,
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def main():
    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'show_quiz' not in st.session_state:
        st.session_state.show_quiz = False

    # Header
    st.markdown('<h1 class="main-header">🧠 Personality Discovery Hub</h1>', unsafe_allow_html=True)
    
    questions = get_questions()
    
    # Welcome Screen
    if not st.session_state.show_quiz and not st.session_state.quiz_completed:
        st.markdown("""
        <div class="welcome-container fade-in">
            <h2>🎯 Discover Your True Personality!</h2>
            <p>Take our interactive quiz to find out whether you're more of an Introvert or Extrovert.
               This scientifically-designed assessment analyzes your behavioral patterns and preferences.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="features-card fade-in">
                <h3>✨ What You'll Get:</h3>
                <div class="features-list">
                    🔬 <strong>AI-powered personality analysis</strong><br>
                    📊 <strong>Visual breakdown of your traits</strong><br>
                    🧭 <strong>Detailed insights about your personality type</strong><br>
                    💡 <strong>Personalized tips and recommendations</strong><br>
                    ⏱️ <strong>Takes only 3-5 minutes to complete</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Fun facts
            fun_facts = [
                "Personality traits exist on a spectrum - most people show both introverted and extroverted qualities!",
                "Introversion doesn't mean shy - many introverts are confident public speakers!",
                "Extroverts get energy from social interaction, while introverts recharge through solitude.",
                "Both personality types have unique strengths and contribute valuable perspectives!",
                "Your personality type can influence your career preferences, learning style, and relationships."
            ]
            
            selected_fact = random.choice(fun_facts)
            st.markdown(f"""
            <div class="fun-fact fade-in">
                <div class="fun-fact-title">💡 Did You Know?</div>
                <div class="fun-fact-text">{selected_fact}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Start Personality Quiz", type="primary", use_container_width=True):
                st.session_state.show_quiz = True
                st.rerun()
    
    # Quiz Interface
    elif st.session_state.show_quiz and not st.session_state.quiz_completed:
        progress = st.session_state.current_question / len(questions)
        st.progress(progress, text=f"Question {st.session_state.current_question + 1} of {len(questions)}")
        
        current_q = questions[st.session_state.current_question]
        
        st.markdown(f"""
        <div class="question-container fade-in">
            <div class="question-text">{current_q['question']}</div>
            <div class="question-subtitle">{current_q['subtitle']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display visual elements
        if 'image' in current_q:
            st.markdown(f"""
            <div style="text-align: center; font-size: 2.5rem; margin: 1.5rem auto; padding: 1.5rem; 
                        background: #f7fafc; border-radius: 12px; max-width: 300px;">
                {current_q['image']}
            </div>
            """, unsafe_allow_html=True)
        
        # Answer options with simplified styling
        st.markdown("""
        <div style="margin: 2rem auto; max-width: 800px;">
            <h4 style="color: #4a5568; font-weight: 500; margin-bottom: 1.5rem; text-align: center; font-size: 1.1rem;">
                Choose the option that best describes you:
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        answer = st.radio(
            "",
            current_q['options'],
            key=f"q_{st.session_state.current_question}",
            index=None,
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.current_question > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col3:
            if answer is not None:
                if st.button("Next ➡️" if st.session_state.current_question < len(questions) - 1 else "🏁 Get Results!", 
                           type="primary", use_container_width=True):
                    # Save answer
                    score_index = current_q['options'].index(answer)
                    st.session_state.answers[current_q['id']] = current_q['scores'][score_index]
                    
                    if st.session_state.current_question < len(questions) - 1:
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.session_state.quiz_completed = True
                        st.rerun()
    
    # Results Screen
    elif st.session_state.quiz_completed:
        personality, confidence = calculate_personality(st.session_state.answers)
        
        # Results header
        if personality == "Introvert":
            result_class = "introvert-result"
            emoji = "🧘‍♀️"
            color = "#9467bd"
        else:
            result_class = "extrovert-result" 
            emoji = "🌟"
            color = "#ff7f0e"
        
        st.markdown(f"""
        <div class="result-container {result_class} fade-in">
            <div class="result-title">{emoji} You're an {personality.upper()}! {emoji}</div>
            <div class="result-confidence">Confidence: {confidence:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Personality chart
        fig = create_personality_chart(personality, confidence)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="traits-card fade-in">
                <h3>🎯 Your Personality Traits</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if personality == "Introvert":
                traits = [
                    "🧠 Thoughtful and reflective",
                    "💭 Prefer deep conversations",
                    "🌱 Recharge through solitude", 
                    "🎯 Think before speaking",
                    "🤝 Value close relationships",
                    "📚 Enjoy quiet activities"
                ]
            else:
                traits = [
                    "⚡ Outgoing and social",
                    "🗣️ Love meeting new people",
                    "🎉 Energized by interaction",
                    "🎯 Think out loud",
                    "🌐 Enjoy large social networks",
                    "🎭 Comfortable being center of attention"
                ]
            
            for trait in traits:
                st.markdown(f'<div class="trait-item">{trait}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insights-card fade-in">
                <h3>💡 Insights & Tips</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if personality == "Introvert":
                insights = [
                    "🏠 **Recharge Time**: Schedule regular alone time to recharge your energy",
                    "💬 **Communication**: You excel in one-on-one conversations and written communication", 
                    "🎯 **Work Style**: You likely prefer focused, deep work over multitasking",
                    "🤝 **Relationships**: You form fewer but deeper, more meaningful connections",
                    "📈 **Growth**: Challenge yourself to step out of your comfort zone gradually"
                ]
            else:
                insights = [
                    "👥 **Social Energy**: You thrive in collaborative and social environments",
                    "💬 **Communication**: You excel at verbal communication and group discussions",
                    "🎯 **Work Style**: You likely prefer variety and interaction in your work",
                    "🤝 **Relationships**: You enjoy meeting new people and building broad networks", 
                    "📈 **Growth**: Remember to take quiet time for reflection and deep thinking"
                ]
                
            for insight in insights:
                st.markdown(f'<div class="insight-item">{insight}</div>', unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔄 Retake Quiz", use_container_width=True):
                # Reset all session state
                st.session_state.current_question = 0
                st.session_state.answers = {}
                st.session_state.quiz_completed = False
                st.session_state.show_quiz = True
                st.rerun()
        
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                # Reset to welcome screen
                st.session_state.current_question = 0
                st.session_state.answers = {}
                st.session_state.quiz_completed = False
                st.session_state.show_quiz = False
                st.rerun()
        
        with col3:
            # Create a downloadable summary
            summary = f"""
Personality Assessment Results
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Result: {personality}
Confidence: {confidence:.1f}%

Your responses:
"""
            for q_id, score in st.session_state.answers.items():
                summary += f"- {q_id}: {score}/4\n"
            
            st.download_button(
                label="📄 Download Results",
                data=summary,
                file_name=f"personality_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
