# 🧠 Personality Discovery Hub

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)

## Overview

An interactive platform that combines machine learning and AI to help you discover your personality through two unique approaches: scenario-based assessment and AI-generated artwork.

## Features

### 🎭 Scenario-Based Assessment
- Navigate through 8 realistic life situations
- Get personality analysis using machine learning
- Download detailed reports with charts
- 5-8 minute interactive experience

### 🎨 AI Art Generator  
- Answer 5 questions about artistic preferences
- Generate personalized artwork using OpenAI DALL-E 3
- Download high-quality 1024x1024 images
- 3-5 minute creative experience

### 📊 Analytics Dashboard
- **[View Live Dashboard →](https://lookerstudio.google.com/reporting/2afa875c-2e09-428d-8554-cd73e45f72f6)**
- Interactive Looker Studio report with comprehensive data visualizations
- Real-time insights into personality patterns and behavioral trends
- Model performance metrics and feature importance analysis
- Cross-filterable charts and dynamic exploration tools

## Quick Start

### What You Need
- Python 3.8 or higher
- OpenAI API key (for art generation)

### Installation

1. **Clone and install:**
```bash
git clone https://github.com/yourusername/personality-discovery-hub.git
cd personality-discovery-hub
pip install -r requirements.txt
```

2. **Get OpenAI API Key:**
   - Visit [platform.openai.com](https://platform.openai.com/api-keys)
   - Create account and generate API key
   - Keep your key secure (starts with `sk-`)

3. **Run the app:**
```bash
cd app
streamlit run 0_main_hub.py
```

Open your browser to `http://localhost:8501`

## How to Use

1. **Choose your path:** Scenario Assessment or AI Art Generator
2. **Follow the prompts:** Answer questions authentically  
3. **Get results:** View analysis or download artwork
4. **Try both apps:** Each offers a different perspective

## Project Structure

```
personality-discovery-hub/
├── app/                    # Main applications
│   ├── 0_main_hub.py      # Enhanced main hub
│   ├── main_hub.py        # Simple hub
│   └── pages/             # Individual apps
├── data/                  # Datasets
├── models/                # Trained ML models  
├── notebooks/             # Development notebooks
└── requirements.txt       # Dependencies
```

## The Science

**Machine Learning Models:**
- Naive Bayes for personality classification
- Trained on behavioral patterns and social preferences
- 85%+ accuracy on personality prediction

**AI Art Generation:**
- OpenAI DALL-E 3 integration
- Personality traits mapped to artistic elements
- Dynamic prompts based on your responses

## Troubleshooting

**OpenAI API Issues:**
- Make sure your API key starts with `sk-`
- Check your OpenAI account has billing set up
- If you get errors, try regenerating the art

**App Won't Start:**
- Make sure you're in the `app/` directory
- Try: `pip install --upgrade streamlit`
- Check that Python 3.8+ is installed

## Technologies Used

- **Python** - Core language
- **Streamlit** - Web interface
- **OpenAI DALL-E 3** - AI art generation
- **scikit-learn** - Machine learning
- **Plotly** - Interactive charts
- **Looker Studio** - Analytics dashboard and data visualization

## What's Included

| Feature | Scenario Assessment | AI Art Generator |
|---------|-------------------|------------------|
| Duration | 5-8 minutes | 3-5 minutes |
| Method | Story scenarios | Art questions |
| Output | Analysis report | AI artwork |
| Requirements | None | OpenAI API key |

## Contributing

Feel free to submit issues and pull requests. For major changes, please open an issue first.

## Dataset

Training data from [Personality Classification Dataset on Kaggle](https://www.kaggle.com/datasets/rakeshkapilavai/extrovert-vs-introvert-behavior-data)

---

**Ready to discover your personality? [Get started now!](#quick-start)**
