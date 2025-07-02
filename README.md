# 🧠 Personality Discovery Hub

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-DALL--E--3-green.svg)](https://openai.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange.svg)](https://scikit-learn.org/)

## 📄 Project Overview

**Discover Your Personality Through Interactive Experiences and AI-Generated Art**

The Personality Discovery Hub is an innovative platform that combines machine learning, psychology, and cutting-edge AI technology to offer two distinct approaches to personality assessment. Experience scenario-based behavioral analysis and transform your personality traits into beautiful, AI-generated artwork using OpenAI's DALL-E 3.

## 🎯 Features

### 🎭 Scenario-Based Assessment
- **8 Realistic Life Situations**: Navigate through immersive scenarios that reveal your authentic personality
- **ML-Powered Analysis**: Advanced machine learning models trained on behavioral patterns
- **Comprehensive Reports**: Detailed personality insights with downloadable PDF reports
- **Interactive Visualizations**: Beautiful radar charts and statistical breakdowns

### 🎨 AI Art Generator  
- **Personality Questionnaire**: 5 thoughtful questions about your artistic preferences
- **OpenAI DALL-E 3 Integration**: Transform your traits into stunning AI-generated artwork
- **Personalized Art**: Each piece reflects your unique personality characteristics
- **High-Quality Output**: Download 1024x1024 professional artwork

## 🗂️ Project Structure

```
personality-discovery-hub/
│
├── app/                             # Main application directory
│   ├── 0_main_hub.py              # Enhanced main hub with full UI
│   ├── main_hub.py                # Simplified main hub
│   ├── pages/                      # Streamlit pages
│   │   ├── 1_Assessment.py        # Scenario-based personality assessment
│   │   └── 2_Art_Generator.py     # AI art generation application
│   ├── streamlit_app.py           # Original personality quiz
│   ├── scenario_quiz_app.py       # Standalone scenario quiz
│   └── README.md                   # App-specific documentation
│
├── data/
│   ├── raw/                        # Original datasets
│   │   └── personality_dataset.csv # Raw personality data
│   └── processed/                  # Cleaned and transformed data
│       ├── personality_dataset_cleaned.csv
│       ├── feature_metadata.csv
│       └── data_preparation_summary.json
│
├── models/                         # Trained ML models
│   ├── logistic_regression_model.pkl
│   ├── naive_bayes_model.pkl
│   ├── random_forest_model.pkl
│   ├── standard_scaler.pkl
│   ├── label_encoder.pkl
│   └── API_Documentation.md
│
├── notebooks/                      # Jupyter notebooks for development
│   ├── 01_Data_Retrieval.ipynb
│   ├── 02_Data_Preparation.ipynb
│   ├── 03_Data_Exploration.ipynb
│   ├── 04_Data_Modelling.ipynb
│   ├── 05_Presentation_and_Automation.ipynb
│   └── gui.py                      # Tkinter desktop application
│
├── visuals/                        # Generated visualizations
│   └── performance_dashboard.png
│
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** 
- **OpenAI API Key** (for AI art generation)
- **pip package manager**

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/personality-discovery-hub.git
cd personality-discovery-hub
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Get OpenAI API Key** (for AI Art Generator):
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create an account and generate an API key
   - Keep your key secure (starts with `sk-`)

### Running the Application

#### 🌐 Main Hub (Recommended)
```bash
cd app
streamlit run 0_main_hub.py
```

#### 🌐 Simplified Hub
```bash
cd app  
streamlit run main_hub.py
```

#### 🖥️ Desktop GUI (Tkinter)
```bash
cd notebooks
python gui.py
```

The application will open in your browser at `http://localhost:8501`

## 🎮 How to Use

### 1. Choose Your Adventure
- **Scenario Assessment**: For accurate personality analysis through realistic situations
- **AI Art Generator**: For creative self-expression through AI-generated artwork

### 2. Scenario-Based Assessment
1. Navigate through 8 immersive life scenarios
2. Make authentic choices that feel natural to you
3. Receive detailed personality analysis with ML insights
4. Download comprehensive PDF report

### 3. AI Art Generator
1. Enter your OpenAI API key
2. Answer 5 questions about artistic preferences
3. Generate beautiful AI artwork reflecting your personality
4. Download high-quality 1024x1024 artwork

## 🧠 The Science Behind It

### Machine Learning Models
- **Naive Bayes**: Primary classification model for personality prediction
- **Logistic Regression**: Baseline comparison model  
- **Random Forest**: Ensemble method for robust predictions
- **Feature Engineering**: Comprehensive behavioral pattern analysis

### Personality Framework
Based on established personality psychology research:
- **Behavioral Patterns**: Social preferences and activities
- **Situational Responses**: How you react in various scenarios
- **Communication Styles**: Interaction patterns and preferences
- **Artistic Expression**: Creative preferences and aesthetic choices

## 🎨 AI Art Generation

### Technology Stack
- **OpenAI DALL-E 3**: State-of-the-art AI image generation
- **Personality Mapping**: Traits translated to artistic elements
- **Dynamic Prompts**: Customized based on your responses
- **Error Handling**: Robust fallback systems for API issues

### Art Style Mapping
Your personality traits influence:
- **Color Palettes**: Warm vs cool color preferences
- **Composition**: Geometric vs organic shapes
- **Complexity**: Detailed vs minimalist styles
- **Energy**: Dynamic vs peaceful aesthetics

## 📊 Dataset Information

### Features (7 behavioral indicators):
- **Time_spent_Alone**: Daily solitude preferences (0-10 scale)
- **Social_event_attendance**: Frequency of social participation (0-10 scale)
- **Going_outside**: Outdoor activity frequency (0-10 scale)
- **Friends_circle_size**: Close friendship network size (0-15 scale)
- **Post_frequency**: Social media activity level (0-10 scale)
- **Stage_fear**: Public speaking comfort (Yes/No)
- **Drained_after_socializing**: Post-social energy levels (Yes/No)

### Target:
- **Personality**: Classification (Extrovert/Introvert)

## 🛠️ Technologies Used

### Core Technologies
- **Python**: Primary programming language
- **Streamlit**: Interactive web applications
- **OpenAI API**: DALL-E 3 for AI art generation
- **scikit-learn**: Machine learning algorithms

### Data & Visualization
- **Pandas & NumPy**: Data manipulation and analysis
- **Plotly**: Interactive visualizations and charts
- **Matplotlib & Seaborn**: Statistical plotting
- **PIL/Pillow**: Image processing and handling

### Machine Learning
- **Joblib**: Model persistence and loading
- **XGBoost**: Advanced gradient boosting
- **Imbalanced-learn**: Handling class imbalance

## 🔧 Configuration

### OpenAI API Setup
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create account and verify payment method
3. Generate API key (keep secure!)
4. Enter key in the Art Generator application

### Model Configuration
Models are pre-trained and included in the `models/` directory:
- No additional training required
- Models automatically loaded on application start
- See `models/API_Documentation.md` for technical details

## 📈 Performance

### Model Accuracy
- **Overall Accuracy**: 85%+ on test dataset
- **Precision**: High confidence in predictions
- **Recall**: Comprehensive pattern recognition
- **F1-Score**: Balanced performance metrics

### Features
- **Real-time Analysis**: Instant personality assessment
- **Robust Error Handling**: Graceful API failure management
- **Responsive Design**: Works on desktop and mobile
- **Offline Capability**: Assessment works without internet

## 🔍 App Comparison

| Feature | 🎭 Scenario Assessment | 🎨 AI Art Generator |
|---------|----------------------|-------------------|
| **Duration** | 5-8 minutes | 3-5 minutes |
| **Method** | Story-driven scenarios | Artistic questionnaire |
| **Output** | Detailed analysis & charts | AI-generated artwork |
| **Technology** | ML-powered analysis | OpenAI DALL-E 3 |
| **Best For** | Accurate personality insights | Creative self-expression |
| **Requirements** | None | OpenAI API key |

## 🚧 Troubleshooting

### Common Issues

**OpenAI API Errors:**
- `401 Error`: Check API key format (starts with `sk-`)
- `400 Error`: Content policy triggered - try regenerating
- `Quota Error`: Check OpenAI account billing
- `Rate Limit`: Wait and try again

**Model Loading Issues:**
- Ensure you're in the correct directory (`app/`)
- Check that `models/` directory exists in project root
- Verify all `.pkl` files are present

**Streamlit Issues:**
- Update Streamlit: `pip install --upgrade streamlit`
- Clear cache: `streamlit cache clear`
- Check port conflicts (default: 8501)

## 📝 Future Enhancements

- [ ] **Additional Personality Models**: Big Five traits integration
- [ ] **Advanced AI Features**: Custom art styles and themes  
- [ ] **Social Features**: Share and compare results
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Multi-language Support**: Internationalization
- [ ] **Real-time Chat**: Live personality analysis through conversation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit a pull request with detailed description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Andre** 
- GitHub: [@andreusername](https://github.com/andreusername)
- Project: Personality Discovery Hub

## 🙏 Acknowledgments

- **OpenAI**: For DALL-E 3 API and AI capabilities
- **Streamlit Team**: For the excellent web framework
- **Scikit-learn**: For machine learning tools
- **Personality Psychology Research**: For scientific foundations
- **Open Source Community**: For inspiration and tools

---

**⭐ Star this repository if you found it helpful!**

**🚀 Ready to discover your personality? [Get started now!](#-quick-start)**
