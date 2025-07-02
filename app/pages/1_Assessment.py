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
    page_title="🎭 Personality Assessment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add navigation back to home
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("← Home", help="Back to Main Hub"):
        st.switch_page("main_hub.py")

# Enhanced styling for scenario-based assessment
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        min-height: 100vh;
    }
    
    .assessment-header {
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

# Load models and components
@st.cache_resource
def load_model_components():
    try:
        model = joblib.load('../../models/naive_bayes_model.pkl')
        return model, True
    except:
        return None, False

def get_assessment_scenarios():
    """Comprehensive scenario-based assessment questions"""
    return [
        {
            "id": "weekend_plans",
            "title": "🌅 Saturday Morning Choice",
            "story": "It's a beautiful Saturday morning, and you have no specific plans. Your phone buzzes with various invitations and opportunities...",
            "emoji": "☀️📱🛋️🌳",
            "choices": [
                {
                    "text": "🎪 'Let's organize a group hangout at the park - I'll text everyone!'",
                    "score": 4
                },
                {
                    "text": "☕ 'Coffee with my closest friend sounds perfect'",
                    "score": 3
                },
                {
                    "text": "🛋️ 'Actually, a quiet morning at home with a book sounds amazing'",
                    "score": 2
                },
                {
                    "text": "🌳 'Solo nature walk to recharge - exactly what I need'",
                    "score": 1
                }
            ]
        },
        {
            "id": "work_meeting",
            "title": "💼 The Big Meeting",
            "story": "Your manager announces a crucial client presentation next week and asks for a volunteer to lead it. The room falls silent as everyone considers the opportunity...",
            "emoji": "🎤💼📊👥",
            "choices": [
                {
                    "text": "🙋‍♀️ 'I'd love to take the lead on this - count me in!'",
                    "score": 4
                },
                {
                    "text": "🤝 'I'm interested, but could I co-present with someone?'",
                    "score": 3
                },
                {
                    "text": "📋 'I'd prefer to support with research and preparation'",
                    "score": 2
                },
                {
                    "text": "👂 'I'll help however needed, but presenting isn't my strength'",
                    "score": 1
                }
            ]
        },
        {
            "id": "party_invitation",
            "title": "🎉 The Last-Minute Party",
            "story": "Your friend calls at 7 PM: 'Hey! I'm throwing a spontaneous house party tonight - lots of people, great music, starts in an hour! You in?'",
            "emoji": "🏠🎵🕺💃",
            "choices": [
                {
                    "text": "🚀 'Absolutely! Who else is coming? Should I bring anything?'",
                    "score": 4
                },
                {
                    "text": "😊 'Sounds fun! I'll be there, might not stay super late though'",
                    "score": 3
                },
                {
                    "text": "🤔 'Maybe I'll stop by for a bit, but I'm pretty tired'",
                    "score": 2
                },
                {
                    "text": "😴 'Thanks for thinking of me, but I think I'll pass tonight'",
                    "score": 1
                }
            ]
        },
        {
            "id": "networking_event",
            "title": "🤝 Professional Networking",
            "story": "You're at a large professional conference with 200+ attendees. There are industry leaders, potential mentors, and career opportunities everywhere...",
            "emoji": "👔🌐🎯💼",
            "choices": [
                {
                    "text": "🌟 'Time to work the room - I'll try to meet as many people as possible'",
                    "score": 4
                },
                {
                    "text": "🎯 'I'll focus on having meaningful conversations with key people'",
                    "score": 3
                },
                {
                    "text": "👥 'I'll stick with colleagues and meet a few new contacts'",
                    "score": 2
                },
                {
                    "text": "📚 'I'll attend the sessions but minimize the social mingling'",
                    "score": 1
                }
            ]
        },
        {
            "id": "team_conflict",
            "title": "⚡ Team Tension",
            "story": "Two of your teammates are in a heated disagreement that's affecting the whole project. The atmosphere is tense and productivity is dropping...",
            "emoji": "😤🤝🕊️💼",
            "choices": [
                {
                    "text": "🗣️ 'Let's call a team meeting and address this head-on'",
                    "score": 4
                },
                {
                    "text": "👥 'I'll speak with each person individually first'",
                    "score": 3
                },
                {
                    "text": "📧 'Maybe we should focus on solutions via email'",
                    "score": 2
                },
                {
                    "text": "🤐 'I'll hope others handle it while I focus on my tasks'",
                    "score": 1
                }
            ]
        },
        {
            "id": "energy_source",
            "title": "⚡ Weekend Recharge",
            "story": "After a demanding week at work, you're feeling mentally drained. You have a free weekend to recharge however you want...",
            "emoji": "🔋🌱🎭🏖️",
            "choices": [
                {
                    "text": "🎭 'Time for concerts, events, and social adventures!'",
                    "score": 4
                },
                {
                    "text": "🎲 'Mix of social activities and some downtime'",
                    "score": 3
                },
                {
                    "text": "☕ 'Quiet activities with one or two close friends'",
                    "score": 2
                },
                {
                    "text": "🌱 'Solo time in nature or with a good book'",
                    "score": 1
                }
            ]
        },
        {
            "id": "social_battery",
            "title": "🔋 After the Conference",
            "story": "You've just finished a full day at a work conference - presentations, networking lunch, group discussions, and team meetings. It's 6 PM...",
            "emoji": "🏢💼🍽️💬",
            "choices": [
                {
                    "text": "🍻 'Perfect! Now let's hit the after-conference happy hour!'",
                    "score": 4
                },
                {
                    "text": "🍽️ 'Dinner with a few colleagues sounds good'",
                    "score": 3
                },
                {
                    "text": "🚗 'I'll head home but might video call friends later'",
                    "score": 2
                },
                {
                    "text": "🛀 'Home, bath, silence - I need complete solitude to recharge'",
                    "score": 1
                }
            ]
        },
        {
            "id": "decision_making",
            "title": "🤔 The Group Decision",
            "story": "Your friend group is trying to decide where to go for vacation. Everyone has different opinions and the discussion is getting lengthy...",
            "emoji": "✈️🗺️👥💭",
            "choices": [
                {
                    "text": "🗣️ 'Let me facilitate this discussion and help us reach consensus'",
                    "score": 4
                },
                {
                    "text": "💡 'I'll share my thoughts and help with the planning'",
                    "score": 3
                },
                {
                    "text": "👂 'I'll listen to options and vote when asked'",
                    "score": 2
                },
                {
                    "text": "🤷 'I'm flexible - whatever the group decides is fine with me'",
                    "score": 1
                }
            ]
        }
    ]

def calculate_personality(answers):
    """Calculate personality based on scenario answers"""
    total_score = sum(answers.values())
    max_score = len(answers) * 4
    extroversion_percentage = (total_score / max_score) * 100
    
    if extroversion_percentage >= 65:
        return "Extrovert", extroversion_percentage
    elif extroversion_percentage <= 45:
        return "Introvert", 100 - extroversion_percentage
    else:
        return "Ambivert", max(extroversion_percentage, 100 - extroversion_percentage)

def create_detailed_analysis_chart(answers):
    """Create comprehensive personality analysis chart"""
    scenarios = get_assessment_scenarios()
    
    fig = go.Figure()
    
    # Bar chart of individual scenario scores
    scenario_names = [s['title'].split(' ', 1)[1] for s in scenarios]  # Remove emoji
    scores = [answers.get(s['id'], 0) for s in scenarios]
    
    colors = ['#ff6b6b' if score >= 3 else '#4ecdc4' if score >= 2 else '#45b7d1' for score in scores]
    
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=scores,
        marker_color=colors,
        text=[f"{score}/4" for score in scores],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Your Response Pattern Across Scenarios",
        xaxis_title="Scenarios",
        yaxis_title="Extroversion Score",
        yaxis=dict(range=[0, 4.5]),
        height=400,
        showlegend=False
    )
    
    return fig

def main():
    # Initialize session state
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'assessment_started' not in st.session_state:
        st.session_state.assessment_started = False
    if 'assessment_completed' not in st.session_state:
        st.session_state.assessment_completed = False

    scenarios = get_assessment_scenarios()
    
    # Header
    st.markdown('<h1 class="assessment-header">🎭 Personality Assessment</h1>', unsafe_allow_html=True)
    
    # Welcome screen
    if not st.session_state.assessment_started and not st.session_state.assessment_completed:
        st.markdown("""
        <div class="scenario-card">
            <div class="emoji-large">🧠</div>
            <h2 style="text-align: center; color: #2c3e50; margin-bottom: 1.5rem;">
                Discover Your Personality Through Real-Life Scenarios
            </h2>
            <p style="font-size: 1.1rem; line-height: 1.6; color: #4a5568; text-align: center;">
                Navigate through 8 realistic situations and make choices that feel authentic to you. 
                This advanced assessment uses scenario-based analysis to provide deeper insights into your personality type.
            </p>
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 2rem 0;">
                <h4 style="color: #2c3e50; margin-bottom: 1rem;">✨ What Makes This Special:</h4>
                <ul style="color: #4a5568; line-height: 1.8;">
                    <li>🎯 Scenario-based for more accurate results</li>
                    <li>📊 Detailed behavioral pattern analysis</li>
                    <li>🧠 ML-powered personality prediction</li>
                    <li>💾 Downloadable comprehensive report</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Begin Assessment", type="primary", use_container_width=True):
                st.session_state.assessment_started = True
                st.rerun()
    
    # Assessment gameplay
    elif st.session_state.assessment_started and not st.session_state.assessment_completed:
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
            🤔 How would you most likely respond?
        </div>
        """, unsafe_allow_html=True)
        
        choice_made = None
        for i, choice in enumerate(current_scenario['choices']):
            if st.button(choice['text'], key=f"choice_{i}", use_container_width=True):
                choice_made = choice
                break
        
        if choice_made:
            # Save answer
            st.session_state.answers[current_scenario['id']] = choice_made['score']
            
            # Move to next scenario or complete
            if st.session_state.current_scenario < len(scenarios) - 1:
                st.session_state.current_scenario += 1
                st.rerun()
            else:
                st.session_state.assessment_completed = True
                st.rerun()
    
    # Results screen
    elif st.session_state.assessment_completed:
        personality, confidence = calculate_personality(st.session_state.answers)
        
        st.markdown(f"""
        <div class="result-card">
            <div class="emoji-large">{'🌟' if personality == 'Extrovert' else '🧘‍♀️' if personality == 'Introvert' else '⚖️'}</div>
            <h2>You're an {personality.upper()}!</h2>
            <p style="font-size: 1.3rem; margin: 1rem 0;">
                Confidence: {confidence:.1f}%
            </p>
            <p style="font-size: 1rem; opacity: 0.9;">
                Based on your responses to {len(scenarios)} real-life scenarios
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show detailed analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Detailed Analysis")
            fig = create_detailed_analysis_chart(st.session_state.answers)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Key Insights")
            
            # Calculate insights
            total_score = sum(st.session_state.answers.values())
            avg_score = total_score / len(st.session_state.answers)
            
            high_scenarios = [scenarios[i]['title'] for i, score in enumerate(st.session_state.answers.values()) if score >= 3]
            low_scenarios = [scenarios[i]['title'] for i, score in enumerate(st.session_state.answers.values()) if score <= 2]
            
            st.markdown(f"""
            **Overall Pattern:** {personality}
            
            **Average Response Score:** {avg_score:.1f}/4.0
            
            **Social Engagement:** {"High" if avg_score >= 3 else "Moderate" if avg_score >= 2 else "Low"}
            
            **Energy Source:** {"External stimulation" if personality == "Extrovert" else "Internal reflection" if personality == "Introvert" else "Balanced approach"}
            """)
            
            if high_scenarios:
                st.markdown("**🔥 High Energy Scenarios:**")
                for scenario in high_scenarios[:3]:
                    st.write(f"• {scenario}")
            
            if low_scenarios:
                st.markdown("**🧘 Reflective Scenarios:**")
                for scenario in low_scenarios[:3]:
                    st.write(f"• {scenario}")
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Retake Assessment", use_container_width=True):
                st.session_state.current_scenario = 0
                st.session_state.answers = {}
                st.session_state.assessment_completed = False
                st.session_state.assessment_started = True
                st.rerun()
        
        with col2:
            if st.button("🏠 Main Hub", use_container_width=True):
                st.switch_page("main_hub.py")
        
        with col3:
            # Download comprehensive results
            results_summary = f"""🎭 Comprehensive Personality Assessment Results
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🧠 PERSONALITY TYPE: {personality}
📊 CONFIDENCE LEVEL: {confidence:.1f}%
⚡ AVERAGE RESPONSE: {avg_score:.2f}/4.0

📋 DETAILED SCENARIO RESPONSES:
"""
            for i, (scenario_id, score) in enumerate(st.session_state.answers.items()):
                scenario_title = scenarios[i]['title']
                results_summary += f"{i+1}. {scenario_title}: {score}/4\n"
            
            results_summary += f"""
🎯 PERSONALITY INSIGHTS:
- Energy Source: {"External interactions and stimulation" if personality == "Extrovert" else "Internal thoughts and reflection" if personality == "Introvert" else "Balanced between internal and external"}
- Social Preference: {"Large groups and dynamic environments" if avg_score >= 3 else "Small groups and intimate settings" if avg_score <= 2 else "Flexible depending on situation"}
- Communication Style: {"Expressive and outgoing" if personality == "Extrovert" else "Thoughtful and reserved" if personality == "Introvert" else "Adaptable to context"}
- Decision Making: {"Quick and collaborative" if personality == "Extrovert" else "Careful and independent" if personality == "Introvert" else "Situationally appropriate"}

Generated by AI-Powered Personality Assessment System
"""
            
            st.download_button(
                label="📄 Download Report",
                data=results_summary,
                file_name=f"personality_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
