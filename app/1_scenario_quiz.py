import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import random

# Configure page
st.set_page_config(
    page_title="🎮 Personality Scenarios",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for game-like interface
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        min-height: 100vh;
    }
    
    .game-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 400% 400%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .scenario-card {
        background: rgba(255, 255, 255, 0.95);
        color: #2d3748;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem auto;
        max-width: 900px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .scenario-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .scenario-story {
        font-size: 1.2rem;
        line-height: 1.6;
        color: #4a5568;
        margin-bottom: 2rem;
        text-align: center;
        font-style: italic;
    }
    
    .result-card {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        margin: 2rem auto;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        max-width: 800px;
    }
    
    .progress-bar {
        background: rgba(255, 255, 255, 0.3);
        height: 10px;
        border-radius: 5px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        height: 100%;
        transition: width 0.3s ease;
    }
    
    .emoji-large {
        font-size: 4rem;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

def get_scenarios():
    """Define the social scenarios with personality mappings"""
    return [
        {
            "id": "weekend_party",
            "title": "🎉 The Unexpected Weekend Party",
            "story": "It's Friday evening and your friend just texted: 'Hey! I'm throwing a house party tonight, lots of people coming, starts at 8pm. You should come!' You weren't planning anything special tonight...",
            "emoji": "🏠🎵🕺💃",
            "choices": [
                {
                    "text": "🚀 'YES! I'll be there! Who else is coming? Can I bring anyone?'",
                    "traits": {"social_energy": 4, "party_preference": 4, "spontaneity": 4}
                },
                {
                    "text": "😊 'Sounds fun! Let me see how I'm feeling closer to 8pm'",
                    "traits": {"social_energy": 3, "party_preference": 3, "spontaneity": 2}
                },
                {
                    "text": "🤔 'Maybe for a bit, but I might not stay too long'",
                    "traits": {"social_energy": 2, "party_preference": 2, "spontaneity": 2}
                },
                {
                    "text": "😴 'Thanks for the invite, but I think I'll pass tonight'",
                    "traits": {"social_energy": 1, "party_preference": 1, "spontaneity": 1}
                }
            ]
        },
        {
            "id": "work_presentation",
            "title": "📊 The Big Presentation Opportunity",
            "story": "Your boss announces: 'We need someone to present our quarterly results to the entire company next week. It's a great opportunity for visibility and career growth.' Everyone looks around the room...",
            "emoji": "🎤📈👔💼",
            "choices": [
                {
                    "text": "🙋‍♀️ 'I'd love to do it! This sounds like an amazing opportunity!'",
                    "traits": {"public_speaking": 4, "attention_seeking": 4, "confidence": 4}
                },
                {
                    "text": "💪 'I'm interested, but could I maybe co-present with someone?'",
                    "traits": {"public_speaking": 3, "attention_seeking": 2, "confidence": 3}
                },
                {
                    "text": "😬 'I could do it if really needed, but I'd need time to prepare'",
                    "traits": {"public_speaking": 2, "attention_seeking": 1, "confidence": 2}
                },
                {
                    "text": "🙈 'I think someone else would be better suited for this'",
                    "traits": {"public_speaking": 1, "attention_seeking": 1, "confidence": 1}
                }
            ]
        },
        {
            "id": "lunch_break",
            "title": "🍽️ The Daily Lunch Dilemma",
            "story": "It's lunch time at work. You have a full hour break and several options for how to spend it. Your colleagues are making various plans...",
            "emoji": "🥗☕👥📚",
            "choices": [
                {
                    "text": "👥 Join the group going to that new restaurant everyone's talking about",
                    "traits": {"social_lunch": 4, "group_activity": 4, "new_experiences": 4}
                },
                {
                    "text": "☕ Grab coffee with one or two close work friends",
                    "traits": {"social_lunch": 3, "group_activity": 2, "new_experiences": 2}
                },
                {
                    "text": "🥗 Eat at my desk while catching up on personal messages",
                    "traits": {"social_lunch": 2, "group_activity": 1, "new_experiences": 1}
                },
                {
                    "text": "🌳 Take a solo walk outside and enjoy some quiet time",
                    "traits": {"social_lunch": 1, "group_activity": 1, "new_experiences": 2}
                }
            ]
        },
        {
            "id": "networking_event",
            "title": "🤝 The Professional Networking Event",
            "story": "You're at an industry networking event. The room is buzzing with professionals exchanging business cards and making connections. There's a cocktail hour, presentations, and plenty of mingling opportunities...",
            "emoji": "👔🍸💼🤝",
            "choices": [
                {
                    "text": "🌟 Work the room! Meet as many new people as possible",
                    "traits": {"networking": 4, "meeting_strangers": 4, "social_energy": 4}
                },
                {
                    "text": "🎯 Focus on having a few meaningful conversations",
                    "traits": {"networking": 3, "meeting_strangers": 3, "social_energy": 3}
                },
                {
                    "text": "😊 Stick close to colleagues I came with, maybe meet 1-2 new people",
                    "traits": {"networking": 2, "meeting_strangers": 2, "social_energy": 2}
                },
                {
                    "text": "⏰ Attend the presentations but leave before the mingling gets intense",
                    "traits": {"networking": 1, "meeting_strangers": 1, "social_energy": 1}
                }
            ]
        },
        {
            "id": "vacation_planning",
            "title": "✈️ The Dream Vacation Decision",
            "story": "You have a week off and the budget for a great vacation. Your travel agent shows you several amazing options, each offering a completely different experience...",
            "emoji": "🏖️🏔️🏛️🎪",
            "choices": [
                {
                    "text": "🎪 Group tour of European cities with 20 other travelers",
                    "traits": {"group_travel": 4, "structured_activity": 3, "meeting_strangers": 4}
                },
                {
                    "text": "🏖️ Beach resort vacation with a friend or partner",
                    "traits": {"group_travel": 2, "structured_activity": 2, "meeting_strangers": 2}
                },
                {
                    "text": "🏔️ Solo hiking adventure in a national park",
                    "traits": {"group_travel": 1, "structured_activity": 1, "meeting_strangers": 1}
                },
                {
                    "text": "🏛️ Cultural city break with museums and quiet exploration",
                    "traits": {"group_travel": 1, "structured_activity": 3, "meeting_strangers": 1}
                }
            ]
        }
    ]

def calculate_personality_from_traits(user_traits):
    """Convert trait scores to personality prediction"""
    extrovert_indicators = ['social_energy', 'party_preference', 'attention_seeking', 'networking', 'meeting_strangers', 'group_activity']
    
    extrovert_score = sum(user_traits.get(trait, 2) for trait in extrovert_indicators) / len(extrovert_indicators)
    total_score = sum(user_traits.values()) / len(user_traits)
    
    if total_score >= 3.0:
        return "Extrovert", min(95, (total_score - 2) * 40 + 60)
    else:
        return "Introvert", min(95, (4 - total_score) * 40 + 60)

def create_trait_radar_chart(user_traits):
    """Create a radar chart showing trait distribution"""
    traits = list(user_traits.keys())
    values = list(user_traits.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=traits,
        fill='toself',
        name='Your Profile',
        line_color='#ff6b6b',
        fillcolor='rgba(255, 107, 107, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 4])),
        showlegend=False,
        title="Your Behavioral Trait Profile",
        font=dict(size=14),
        height=500
    )
    
    return fig

def main():
    # Initialize session state
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = 0
    if 'user_traits' not in st.session_state:
        st.session_state.user_traits = {}
    if 'scenarios_completed' not in st.session_state:
        st.session_state.scenarios_completed = False
    if 'show_scenarios' not in st.session_state:
        st.session_state.show_scenarios = False

    scenarios = get_scenarios()
    
    # Header
    st.markdown('<h1 class="game-header">🎭 Social Scenarios Game</h1>', unsafe_allow_html=True)
    
    # Welcome screen
    if not st.session_state.show_scenarios and not st.session_state.scenarios_completed:
        st.markdown("""
        <div class="scenario-card">
            <div class="emoji-large">🎮</div>
            <h2 style="text-align: center; color: #2c3e50; margin-bottom: 1.5rem;">
                Welcome to the Personality Scenarios Game!
            </h2>
            <p style="font-size: 1.1rem; line-height: 1.6; color: #4a5568; text-align: center;">
                Navigate through realistic social situations and make choices that feel natural to you. 
                Your decisions will reveal patterns about your personality type through gamified behavioral analysis.
            </p>
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 2rem 0;">
                <h4 style="color: #2c3e50; margin-bottom: 1rem;">🎯 How It Works:</h4>
                <ul style="color: #4a5568; line-height: 1.8;">
                    <li>🎪 Experience 5 immersive social scenarios</li>
                    <li>🎯 Make choices that feel authentic to you</li>
                    <li>📊 See your behavioral traits mapped out</li>
                    <li>🧠 Discover your personality type through gameplay</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Scenarios", type="primary", use_container_width=True):
                st.session_state.show_scenarios = True
                st.rerun()
    
    # Scenarios gameplay
    elif st.session_state.show_scenarios and not st.session_state.scenarios_completed:
        # Progress indicator
        progress = st.session_state.current_scenario / len(scenarios)
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
            <h4 style="color: white; text-align: center; margin-bottom: 0.5rem;">
                Scenario {st.session_state.current_scenario + 1} of {len(scenarios)}
            </h4>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress * 100}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        current_scenario = scenarios[st.session_state.current_scenario]
        
        st.markdown(f"""
        <div class="scenario-card">
            <div class="scenario-title">{current_scenario['title']}</div>
            <div style="text-align: center; font-size: 3rem; margin: 1rem 0;">
                {current_scenario['emoji']}
            </div>
            <div class="scenario-story">{current_scenario['story']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Choice selection
        st.markdown("""
        <div style="text-align: center; color: white; font-size: 1.2rem; margin: 2rem 0;">
            🤔 What would you most likely do?
        </div>
        """, unsafe_allow_html=True)
        
        choice_made = None
        for i, choice in enumerate(current_scenario['choices']):
            if st.button(choice['text'], key=f"choice_{i}", use_container_width=True):
                choice_made = choice
                break
        
        if choice_made:
            # Update user traits
            for trait, value in choice_made['traits'].items():
                if trait in st.session_state.user_traits:
                    st.session_state.user_traits[trait] = (st.session_state.user_traits[trait] + value) / 2
                else:
                    st.session_state.user_traits[trait] = value
            
            # Move to next scenario or complete
            if st.session_state.current_scenario < len(scenarios) - 1:
                st.session_state.current_scenario += 1
                st.rerun()
            else:
                st.session_state.scenarios_completed = True
                st.rerun()
    
    # Results screen
    elif st.session_state.scenarios_completed:
        personality, confidence = calculate_personality_from_traits(st.session_state.user_traits)
        
        st.markdown(f"""
        <div class="result-card">
            <div class="emoji-large">{'🧘‍♀️' if personality == 'Introvert' else '🌟'}</div>
            <h2>You're an {personality.upper()}!</h2>
            <p style="font-size: 1.3rem; margin: 1rem 0;">
                Confidence: {confidence:.1f}%
            </p>
            <p style="font-size: 1rem; opacity: 0.9;">
                Based on your choices across {len(scenarios)} social scenarios
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show trait analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Your Behavioral Profile")
            fig = create_trait_radar_chart(st.session_state.user_traits)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Key Insights")
            sorted_traits = sorted(st.session_state.user_traits.items(), key=lambda x: x[1], reverse=True)
            
            for trait, score in sorted_traits[:6]:
                trait_name = trait.replace('_', ' ').title()
                percentage = (score / 4) * 100
                st.metric(trait_name, f"{percentage:.0f}%")
        
        # Celebrity matches
        st.markdown("### 🌟 Celebrity Personality Matches")
        if personality == "Extrovert":
            celebrities = ["🎬 Ryan Reynolds", "🎤 Taylor Swift", "🏀 LeBron James", "📺 Ellen DeGeneres"]
        else:
            celebrities = ["🎭 Emma Watson", "🔬 Bill Gates", "📚 J.K. Rowling", "🎨 Tim Burton"]
        
        cols = st.columns(len(celebrities))
        for i, celebrity in enumerate(celebrities):
            with cols[i]:
                st.info(celebrity)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Play Again", use_container_width=True):
                st.session_state.current_scenario = 0
                st.session_state.user_traits = {}
                st.session_state.scenarios_completed = False
                st.session_state.show_scenarios = True
                st.rerun()
        
        with col2:
            if st.button("🏠 Main Menu", use_container_width=True):
                st.session_state.current_scenario = 0
                st.session_state.user_traits = {}
                st.session_state.scenarios_completed = False
                st.session_state.show_scenarios = False
                st.rerun()
        
        with col3:
            # Download results
            results_summary = f"""🎮 Social Scenarios Game Results
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🧠 Personality Type: {personality}
📊 Confidence: {confidence:.1f}%

🎯 Behavioral Traits:
"""
            for trait, score in sorted_traits:
                trait_name = trait.replace('_', ' ').title()
                results_summary += f"- {trait_name}: {score:.2f}/4.0\n"
            
            st.download_button(
                label="📄 Download Results",
                data=results_summary,
                file_name=f"scenarios_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":
    main() 