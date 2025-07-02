import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw, ImageFilter
import io
import random
import math
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="🎨 Personality Art Generator",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for artistic interface
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
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ff9a56, #ff6b9d, #c44cff, #8b5dff);
        background-size: 400% 400%;
        animation: gradient 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .art-card {
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
    
    .palette-box {
        width: 100px;
        height: 100px;
        border-radius: 15px;
        margin: 10px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .palette-box:hover {
        transform: scale(1.1);
    }
    
    .artwork-frame {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        margin: 20px auto;
        max-width: 600px;
    }
    
    .trait-slider {
        margin: 20px 0;
        padding: 15px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b9d 100%);
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

def generate_personality_colors(traits):
    """Generate a color palette based on personality traits"""
    # Base colors for different traits
    extrovert_base = [255, 107, 107]  # Warm red
    introvert_base = [107, 152, 255]  # Cool blue
    
    # Calculate personality lean
    extrovert_traits = ['social_energy', 'confidence', 'spontaneity', 'attention_seeking']
    introvert_traits = ['reflection', 'depth', 'calm', 'focus']
    
    extrovert_score = sum(traits.get(trait, 50) for trait in extrovert_traits) / len(extrovert_traits)
    
    # Blend colors based on personality
    if extrovert_score > 60:
        primary_color = extrovert_base
        secondary_colors = [
            [255, 154, 86],   # Orange
            [255, 107, 157],  # Pink
            [255, 193, 107],  # Yellow
        ]
    else:
        primary_color = introvert_base
        secondary_colors = [
            [107, 255, 193],  # Mint
            [157, 107, 255],  # Purple
            [107, 193, 255],  # Light blue
        ]
    
    # Add some randomness based on other traits
    creativity = traits.get('creativity', 50)
    if creativity > 70:
        secondary_colors.append([random.randint(100, 255) for _ in range(3)])
    
    colors = [primary_color] + secondary_colors
    return [(f"rgb({r},{g},{b})", f"#{r:02x}{g:02x}{b:02x}") for r, g, b in colors]

def create_abstract_art(traits, width=600, height=600):
    """Generate abstract art based on personality traits"""
    # Create image
    img = Image.new('RGB', (width, height), (240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    # Get personality colors
    colors = generate_personality_colors(traits)
    hex_colors = [color[1] for color in colors]
    
    # Personality-based parameters
    extrovert_score = traits.get('social_energy', 50)
    creativity = traits.get('creativity', 50)
    organization = traits.get('organization', 50)
    
    # Number of shapes based on extroversion
    num_shapes = int(10 + (extrovert_score / 10))
    
    # Draw shapes
    for i in range(num_shapes):
        color_idx = i % len(hex_colors)
        color = hex_colors[color_idx]
        
        # Shape size based on confidence
        confidence = traits.get('confidence', 50)
        max_size = int(50 + confidence * 2)
        size = random.randint(20, max_size)
        
        # Position
        x = random.randint(0, width - size)
        y = random.randint(0, height - size)
        
        # Shape type based on organization
        if organization > 60:
            # More geometric shapes
            if random.random() > 0.5:
                draw.rectangle([x, y, x + size, y + size], fill=color)
            else:
                draw.ellipse([x, y, x + size, y + size], fill=color)
        else:
            # More organic shapes
            points = []
            center_x, center_y = x + size//2, y + size//2
            for angle in range(0, 360, 30):
                radius = random.randint(size//4, size//2)
                px = center_x + radius * math.cos(math.radians(angle))
                py = center_y + radius * math.sin(math.radians(angle))
                points.append((px, py))
            draw.polygon(points, fill=color)
    
    # Apply filters based on personality
    if traits.get('calm', 50) > 70:
        img = img.filter(ImageFilter.BLUR)
    
    return img

def personality_quiz():
    """Simple personality trait assessment"""
    st.markdown("### 🎯 Tell us about yourself!")
    st.markdown("Rate how much each trait describes you (0-100):")
    
    traits = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        traits['social_energy'] = st.slider("Social Energy 🎉", 0, 100, 50)
        traits['confidence'] = st.slider("Confidence 💪", 0, 100, 50)
        traits['creativity'] = st.slider("Creativity 🎨", 0, 100, 50)
        traits['spontaneity'] = st.slider("Spontaneity ⚡", 0, 100, 50)
    
    with col2:
        traits['organization'] = st.slider("Organization 📋", 0, 100, 50)
        traits['calm'] = st.slider("Calmness 🧘", 0, 100, 50)
        traits['reflection'] = st.slider("Reflection 🤔", 0, 100, 50)
        traits['focus'] = st.slider("Focus 🎯", 0, 100, 50)
    
    return traits

def display_color_palette(colors):
    """Display the generated color palette"""
    st.markdown("### 🎨 Your Personality Color Palette")
    
    cols = st.columns(len(colors))
    for i, (rgb_color, hex_color) in enumerate(colors):
        with cols[i]:
            st.markdown(f"""
            <div style="background: {rgb_color}; width: 100px; height: 100px; 
                       border-radius: 15px; margin: 10px auto; 
                       box-shadow: 0 8px 20px rgba(0,0,0,0.2);"></div>
            <p style="text-align: center; font-size: 0.8rem; margin-top: 10px;">
                {hex_color}
            </p>
            """, unsafe_allow_html=True)

def create_mood_chart(traits):
    """Create a mood/energy chart based on traits"""
    categories = list(traits.keys())
    values = list(traits.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Personality Profile',
        line_color='#ff6b9d',
        fillcolor='rgba(255, 107, 157, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Your Personality Mood Chart",
        font=dict(size=14),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="art-header">🎨 Personality Art Generator</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="art-card">
        <h2 style="text-align: center; color: #2c3e50; margin-bottom: 1.5rem;">
            Turn Your Personality Into Art!
        </h2>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #4a5568; text-align: center;">
            Discover how your unique personality traits translate into beautiful, abstract art. 
            Our algorithm creates personalized artwork and color palettes based on your individual characteristics.
        </p>
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 2rem 0;">
            <h4 style="color: #2c3e50; margin-bottom: 1rem;">✨ What You'll Get:</h4>
            <ul style="color: #4a5568; line-height: 1.8;">
                <li>🎨 Custom abstract artwork reflecting your personality</li>
                <li>🌈 Personalized color palette based on your traits</li>
                <li>📊 Interactive mood chart visualization</li>
                <li>💾 Downloadable artwork for your collection</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Personality assessment
    with st.container():
        st.markdown("""
        <div class="art-card">
        """, unsafe_allow_html=True)
        
        traits = personality_quiz()
        
        if st.button("🎨 Generate My Art!", type="primary", use_container_width=True):
            st.session_state.traits = traits
            st.session_state.show_results = True
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Results
    if hasattr(st.session_state, 'show_results') and st.session_state.show_results:
        traits = st.session_state.traits
        
        # Generate color palette
        colors = generate_personality_colors(traits)
        display_color_palette(colors)
        
        # Generate artwork
        st.markdown("### 🖼️ Your Personal Artwork")
        with st.spinner("Creating your unique artwork..."):
            artwork = create_abstract_art(traits)
            
            # Display artwork
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(artwork, caption="Your Personality Art", use_column_width=True)
        
        # Mood chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Personality Mood Chart")
            fig = create_mood_chart(traits)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Art Interpretation")
            
            # Determine personality type
            extrovert_score = (traits['social_energy'] + traits['confidence'] + traits['spontaneity']) / 3
            
            if extrovert_score > 60:
                personality_type = "Extrovert"
                art_style = "Dynamic and vibrant with warm colors"
                description = "Your art features bold, energetic elements that reflect your outgoing nature."
            else:
                personality_type = "Introvert"
                art_style = "Calm and harmonious with cool tones"
                description = "Your art showcases peaceful, contemplative elements that mirror your reflective personality."
            
            st.markdown(f"""
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px;">
                <p><strong>Personality Type:</strong> {personality_type}</p>
                <p><strong>Art Style:</strong> {art_style}</p>
                <p><strong>Description:</strong> {description}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Fun facts based on traits
            if traits['creativity'] > 70:
                st.success("🎨 High creativity detected! Your art features unique, experimental elements.")
            
            if traits['organization'] > 70:
                st.info("📐 Your organized nature shows in geometric, structured patterns.")
            
            if traits['calm'] > 70:
                st.success("🧘 Your calm personality creates soothing, peaceful artwork.")
        
        # Download options
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Save artwork as bytes
            img_buffer = io.BytesIO()
            artwork.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()
            
            st.download_button(
                label="🖼️ Download Artwork",
                data=img_bytes,
                file_name=f"personality_art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png",
                use_container_width=True
            )
        
        with col2:
            if st.button("🎨 Generate New Art", use_container_width=True):
                st.session_state.show_results = False
                st.rerun()
        
        with col3:
            # Create palette data
            palette_data = "\n".join([f"{i+1}. {color[1]} - {color[0]}" for i, color in enumerate(colors)])
            
            st.download_button(
                label="🌈 Download Palette",
                data=palette_data,
                file_name=f"personality_palette_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":
    main() 