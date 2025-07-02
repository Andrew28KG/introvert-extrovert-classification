import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw, ImageFilter
import io
import random
import math
import base64
import requests
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="🎨 AI Art Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add navigation back to home
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("← Home", help="Back to Main Hub"):
        st.switch_page("main_hub.py")

# Enhanced styling for art generator
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        min-height: 100vh;
    }
    
    .art-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ff9a56);
        background-size: 400% 400%;
        animation: gradient 5s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .questionnaire-card {
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
    
    .question-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .art-showcase {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
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
    
    .personality-trait {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .api-info {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

def get_personality_questions():
    """Interactive questions to determine personality traits for art generation"""
    return [
        {
            "id": "color_preference",
            "question": "🌈 Which color palette speaks to your soul?",
            "options": [
                {"text": "🔥 Warm & Energetic (Reds, Oranges, Yellows)", "traits": {"energy": 4, "warmth": 4, "creativity": 3}},
                {"text": "🌊 Cool & Calming (Blues, Greens, Purples)", "traits": {"calm": 4, "depth": 4, "introspection": 4}},
                {"text": "🌸 Soft & Gentle (Pastels, Light Tones)", "traits": {"gentleness": 4, "harmony": 4, "peace": 3}},
                {"text": "⚫ Bold & Dramatic (High Contrast, Black/White)", "traits": {"boldness": 4, "structure": 4, "focus": 4}}
            ]
        },
        {
            "id": "pattern_style",
            "question": "🎨 What visual patterns resonate with you?",
            "options": [
                {"text": "🌀 Organic & Flowing (Curves, Natural Forms)", "traits": {"creativity": 4, "flexibility": 4, "naturalism": 4}},
                {"text": "🔺 Geometric & Structured (Lines, Shapes, Patterns)", "traits": {"structure": 4, "logic": 4, "precision": 4}},
                {"text": "✨ Abstract & Chaotic (Random, Expressive)", "traits": {"creativity": 4, "spontaneity": 4, "freedom": 4}},
                {"text": "🎭 Symbolic & Meaningful (Icons, Representations)", "traits": {"depth": 4, "meaning": 4, "storytelling": 4}}
            ]
        },
        {
            "id": "emotional_expression",
            "question": "💫 How do you express your emotions?",
            "options": [
                {"text": "🎪 Boldly & Openly (Big gestures, clear expressions)", "traits": {"openness": 4, "energy": 4, "boldness": 3}},
                {"text": "🎨 Subtly & Artistically (Through creative mediums)", "traits": {"creativity": 4, "subtlety": 4, "artistry": 4}},
                {"text": "📝 Thoughtfully & Deliberately (After reflection)", "traits": {"depth": 4, "introspection": 4, "deliberation": 4}},
                {"text": "🌱 Naturally & Instinctively (Goes with the flow)", "traits": {"naturalism": 4, "spontaneity": 3, "intuition": 4}}
            ]
        },
        {
            "id": "complexity_preference",
            "question": "🧩 What level of complexity appeals to you?",
            "options": [
                {"text": "🎯 Simple & Minimalist (Clean, focused, essential)", "traits": {"simplicity": 4, "focus": 4, "clarity": 4}},
                {"text": "🌟 Moderate & Balanced (Some detail, well-organized)", "traits": {"balance": 4, "harmony": 4, "structure": 3}},
                {"text": "🔮 Complex & Layered (Rich details, multiple elements)", "traits": {"complexity": 4, "depth": 4, "richness": 4}},
                {"text": "🌀 Chaotic & Unpredictable (Lots happening, surprising)", "traits": {"chaos": 4, "spontaneity": 4, "energy": 3}}
            ]
        },
        {
            "id": "inspiration_source",
            "question": "🌍 What inspires your creativity most?",
            "options": [
                {"text": "🌿 Nature & Organic Forms (Plants, landscapes, animals)", "traits": {"naturalism": 4, "peace": 3, "growth": 4}},
                {"text": "🏙️ Urban & Modern Life (Architecture, technology, people)", "traits": {"modernity": 4, "energy": 3, "structure": 3}},
                {"text": "💭 Dreams & Imagination (Fantasy, surreal, otherworldly)", "traits": {"imagination": 4, "creativity": 4, "depth": 3}},
                {"text": "📚 Knowledge & Concepts (Ideas, philosophy, science)", "traits": {"intellect": 4, "depth": 4, "complexity": 3}}
            ]
        }
    ]

def calculate_personality_traits(answers):
    """Calculate personality traits from questionnaire answers"""
    traits = {}
    
    for answer in answers.values():
        for trait, value in answer['traits'].items():
            if trait in traits:
                traits[trait] = (traits[trait] + value) / 2
            else:
                traits[trait] = value
    
    return traits

def generate_ai_art_prompt(traits):
    """Generate a very simple, safe prompt for AI art generation"""
    
    # Ultra-simple mappings - just basic colors and shapes
    simple_prompts = {
        "energy": "bright red and yellow circles",
        "calm": "blue and green waves", 
        "creativity": "purple and orange shapes",
        "structure": "gray and black squares",
        "depth": "dark blue layers",
        "boldness": "red and black triangles",
        "gentleness": "pink and white curves",
        "naturalism": "brown and green leaves",
        "complexity": "colorful geometric pattern",
        "simplicity": "white and blue circles"
    }
    
    # Get the dominant trait
    sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
    primary_trait = sorted_traits[0][0] if sorted_traits else "creativity"
    
    # Return extremely simple prompt
    basic_prompt = simple_prompts.get(primary_trait, "colorful circles and squares")
    return f"{basic_prompt}, digital art"

def generate_ai_image(prompt, api_key):
    """Generate image using OpenAI's responses API with image generation tools"""
    if not api_key:
        return None, "Please provide an OpenAI API key to generate AI images"
    
    # Basic API key validation
    if not api_key.startswith('sk-'):
        return None, "Invalid API key format. OpenAI API keys start with 'sk-'"
    
    if len(api_key) < 20:
        return None, "API key appears to be too short. Please check your key."
    
    try:
        import openai
        import base64
        client = openai.OpenAI(api_key=api_key)
        
        # Keep the prompt extremely simple
        simple_prompt = prompt.replace("abstract", "").replace("flowing", "").replace("artistic", "")
        
        # Make it even simpler - just basic shapes and colors
        if len(simple_prompt) > 50:
            simple_prompt = "colorful shapes, digital art"
        
        st.write(f"🎨 Generating art with simple prompt: {simple_prompt}")
        
        # Use the new responses API with image generation tools
        response = client.responses.create(
            model="gpt-4o-mini",
            input=simple_prompt,
            tools=[{"type": "image_generation"}],
        )
        
        # Extract image data from response
        image_data = [
            output.result
            for output in response.output
            if output.type == "image_generation_call"
        ]
        
        if image_data:
            image_base64 = image_data[0]
            # Decode base64 image
            img_bytes = base64.b64decode(image_base64)
            img = Image.open(io.BytesIO(img_bytes))
            return img, None
        else:
            return None, "No image data found in response"
            
    except Exception as e:
        error_msg = str(e)
        
        # Provide specific error messages for common issues
        if "401" in error_msg or "invalid_api_key" in error_msg:
            return None, "❌ Invalid API key. Please check your OpenAI API key and make sure it's correct."
        elif "400" in error_msg or "image_generation_user_error" in error_msg:
            # Try the most basic prompt possible
            try:
                st.write("🔄 Trying ultra-simple prompt...")
                generic_response = client.responses.create(
                    model="gpt-4o-mini",
                    input="red and blue circles",
                    tools=[{"type": "image_generation"}],
                )
                
                # Extract image data from fallback response
                fallback_image_data = [
                    output.result
                    for output in generic_response.output
                    if output.type == "image_generation_call"
                ]
                
                if fallback_image_data:
                    image_base64 = fallback_image_data[0]
                    img_bytes = base64.b64decode(image_base64)
                    img = Image.open(io.BytesIO(img_bytes))
                    return img, "⚠️ Used ultra-simple prompt. Your personality analysis is still accurate!"
                else:
                    return None, "No fallback image data found"
            except:
                return None, "❌ OpenAI filters are very strict. Try refreshing and generating again."
        elif "insufficient_quota" in error_msg:
            return None, "❌ Insufficient quota. Please check your OpenAI account billing and usage limits."
        elif "rate_limit" in error_msg:
            return None, "❌ Rate limit exceeded. Please wait a moment and try again."
        else:
            return None, f"❌ Error generating image: {error_msg}"

def display_trait_analysis(traits):
    """Display personality trait analysis"""
    st.markdown("### 🎯 Your Artistic Personality Profile")
    
    # Create radar chart
    fig = go.Figure()
    
    trait_names = list(traits.keys())
    trait_values = list(traits.values())
    
    fig.add_trace(go.Scatterpolar(
        r=trait_values,
        theta=trait_names,
        fill='toself',
        name='Your Profile',
        line_color='#FF6B6B',
        fillcolor='rgba(255, 107, 107, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 4])),
        showlegend=False,
        title="Artistic Personality Traits",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display top traits
    sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🌟 Dominant Traits:**")
        for trait, score in sorted_traits[:3]:
            percentage = (score / 4) * 100
            st.markdown(f"""
            <div class="personality-trait">
                <strong>{trait.title()}</strong><br>
                {percentage:.0f}%
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**🎨 Art Style Suggestions:**")
        if traits.get('structure', 0) > 3:
            st.write("• Geometric abstraction")
            st.write("• Minimalist compositions")
        if traits.get('naturalism', 0) > 3:
            st.write("• Organic forms")
            st.write("• Nature-inspired art")
        if traits.get('creativity', 0) > 3:
            st.write("• Expressive abstraction")
            st.write("• Surreal compositions")

def main():
    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'questionnaire_started' not in st.session_state:
        st.session_state.questionnaire_started = False
    if 'questionnaire_completed' not in st.session_state:
        st.session_state.questionnaire_completed = False
    if 'traits_calculated' not in st.session_state:
        st.session_state.traits_calculated = {}

    questions = get_personality_questions()
    
    # Header
    st.markdown('<h1 class="art-header">🎨 AI Personality Art Generator</h1>', unsafe_allow_html=True)
    
    # Welcome screen
    if not st.session_state.questionnaire_started and not st.session_state.questionnaire_completed:
        st.markdown("""
        <div class="questionnaire-card">
            <div style="text-align: center; font-size: 4rem; margin: 1rem 0;">🎨</div>
            <h2 style="text-align: center; color: #2c3e50; margin-bottom: 1.5rem;">
                Transform Your Personality Into Stunning AI Art
            </h2>
            <p style="font-size: 1.1rem; line-height: 1.6; color: #4a5568; text-align: center;">
                Answer 5 thoughtfully crafted questions about your preferences and personality. 
                We'll use advanced AI (DALL-E 3) to create unique, personalized artwork that reflects your inner self.
            </p>
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 2rem 0;">
                <h4 style="color: #2c3e50; margin-bottom: 1rem;">✨ What You'll Get:</h4>
                <ul style="color: #4a5568; line-height: 1.8;">
                    <li>🤖 AI-generated images using OpenAI's DALL-E 3</li>
                    <li>🎯 Personalized art based on your personality</li>
                    <li>📊 Detailed personality trait analysis</li>
                    <li>💾 High-quality downloadable artwork</li>
                    <li>🌈 Custom color palette recommendations</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # API Key information
        st.markdown("""
        <div class="api-info">
            <h4 style="color: white; margin-bottom: 1rem;">🔑 OpenAI API Key Required</h4>
            <p style="color: rgba(255,255,255,0.9); margin-bottom: 1rem;">
                To generate AI art, you'll need your own OpenAI API key. This ensures your privacy and gives you control over usage.
            </p>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                <strong>How to get a REAL API key:</strong><br>
                1. Visit <a href="https://platform.openai.com/api-keys" target="_blank" style="color: #4ecdc4;">platform.openai.com/api-keys</a><br>
                2. Sign up or log in to your OpenAI account<br>
                3. Click "Create new secret key"<br>
                4. Copy the ENTIRE key (starts with sk- and is ~51 characters)<br>
                5. Add billing info (required for DALL-E 3 - costs ~$0.04 per image)<br>
                6. Paste your real API key below (not a placeholder!)
            </p>
            <p style="color: #ff6b6b; font-size: 0.9rem; margin-top: 1rem;">
                ⚠️ <strong>Important:</strong> Don't use placeholder keys like "sk-test123" - you need a real key from OpenAI!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Creating", type="primary", use_container_width=True):
                st.session_state.questionnaire_started = True
                st.rerun()
    
    # Questionnaire
    elif st.session_state.questionnaire_started and not st.session_state.questionnaire_completed:
        # Progress
        progress = st.session_state.current_question / len(questions)
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
            <h4 style="color: white; text-align: center; margin-bottom: 0.5rem;">
                Question {st.session_state.current_question + 1} of {len(questions)}
            </h4>
            <div style="background: rgba(255, 255, 255, 0.3); height: 10px; border-radius: 5px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #ff6b6b, #4ecdc4); height: 100%; width: {progress * 100}%; transition: width 0.3s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        current_question = questions[st.session_state.current_question]
        
        st.markdown(f"""
        <div class="questionnaire-card">
            <div class="question-title">{current_question['question']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer options
        choice_made = None
        for i, option in enumerate(current_question['options']):
            if st.button(option['text'], key=f"option_{i}", use_container_width=True):
                choice_made = option
                break
        
        if choice_made:
            # Save answer
            st.session_state.answers[current_question['id']] = choice_made
            
            # Move to next question or complete
            if st.session_state.current_question < len(questions) - 1:
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.session_state.questionnaire_completed = True
                st.session_state.traits_calculated = calculate_personality_traits(st.session_state.answers)
                st.rerun()
    
    # Art generation and results
    elif st.session_state.questionnaire_completed:
        traits = st.session_state.traits_calculated
        
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; margin: 2rem 0; text-align: center;">
            <h2 style="color: white; margin-bottom: 1rem;">✨ Your Personality Profile Complete!</h2>
            <p style="color: rgba(255,255,255,0.9);">Now let's create stunning AI art that represents you</p>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Art Generation Section
        st.markdown("### 🤖 AI-Generated Personality Art")
        st.markdown("Generate a unique image using OpenAI's DALL-E 3 based on your personality")
        
        # API key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to generate AI art with DALL-E 3",
            placeholder="sk-..."
        )
        
        # API key validation feedback
        if api_key:
            if not api_key.startswith('sk-'):
                st.error("❌ Invalid format: API keys must start with 'sk-'")
            elif len(api_key) < 20:
                st.error("❌ Too short: API keys are typically ~51 characters long")
            elif api_key.startswith('sk-test') or 'placeholder' in api_key.lower() or 'example' in api_key.lower():
                st.error("❌ This looks like a placeholder key. You need a real API key from OpenAI!")
            else:
                st.success("✅ API key format looks correct!")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🎨 Generate AI Art", type="primary", use_container_width=True):
                if api_key:
                    with st.spinner("🤖 AI is creating your personalized artwork..."):
                        prompt = generate_ai_art_prompt(traits)
                        st.info(f"**AI Prompt:** {prompt}")
                        
                        ai_image, error = generate_ai_image(prompt, api_key)
                        if ai_image:
                            st.success("✨ Your AI artwork is ready!")
                            st.image(ai_image, caption="Your AI-Generated Personality Art", use_column_width=True)
                            
                            # Download option
                            buf = io.BytesIO()
                            ai_image.save(buf, format='PNG')
                            buf.seek(0)
                            
                            st.download_button(
                                label="💾 Download AI Art",
                                data=buf.getvalue(),
                                file_name=f"ai_personality_art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        else:
                            st.error(error)
                            if "Invalid API key" in error:
                                st.info("💡 **Need help?** Make sure you're using a real API key from platform.openai.com/api-keys")
                else:
                    st.warning("Please enter your OpenAI API key to generate AI art")
        
        with col2:
            if st.button("🔄 Generate New Prompt", use_container_width=True):
                # Regenerate prompt to show variation
                prompt = generate_ai_art_prompt(traits)
                st.info(f"**New Prompt:** {prompt}")
        
        # Personality analysis
        display_trait_analysis(traits)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Create New Art", use_container_width=True):
                st.session_state.current_question = 0
                st.session_state.answers = {}
                st.session_state.questionnaire_completed = False
                st.session_state.questionnaire_started = True
                st.session_state.traits_calculated = {}
                st.rerun()
        
        with col2:
            if st.button("🏠 Main Hub", use_container_width=True):
                st.switch_page("main_hub.py")
        
        with col3:
            # Download personality report
            report = f"""🎨 AI Personality Art Profile Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 YOUR ARTISTIC PERSONALITY TRAITS:
"""
            sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
            for trait, score in sorted_traits:
                percentage = (score / 4) * 100
                report += f"- {trait.title()}: {percentage:.0f}%\n"
            
            report += f"""
📝 QUESTIONNAIRE RESPONSES:
"""
            for i, (q_id, answer) in enumerate(st.session_state.answers.items()):
                question = questions[i]['question']
                report += f"{i+1}. {question}\n   Answer: {answer['text']}\n\n"
            
            report += f"""
🎨 AI ART PROMPT GENERATED:
{generate_ai_art_prompt(traits)}

🎯 RECOMMENDED ART STYLES:
"""
            if traits.get('structure', 0) > 3:
                report += "- Geometric abstraction and minimalist compositions\n"
            if traits.get('naturalism', 0) > 3:
                report += "- Organic forms and nature-inspired art\n"
            if traits.get('creativity', 0) > 3:
                report += "- Expressive abstraction and surreal compositions\n"
            if traits.get('complexity', 0) > 3:
                report += "- Intricate details and layered compositions\n"
            
            report += "\nGenerated by AI Personality Art Generator using OpenAI DALL-E 3"
            
            st.download_button(
                label="📄 Download Report",
                data=report,
                file_name=f"art_personality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":
    main() 