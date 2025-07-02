
# Personality Classification API Documentation

## Overview
This API provides personality classification capabilities using machine learning to determine if a person is an Extrovert or Introvert based on behavioral patterns.

## Model Information
- **Algorithm**: Naive Bayes Classifier
- **Accuracy**: 91.45%
- **Training Dataset**: 2,009 samples
- **Test Dataset**: 503 samples
- **Features**: 11 behavioral indicators

## Usage Examples

### 1. Python API Usage

```python
from personality_predictor import PersonalityPredictor

# Initialize predictor
predictor = PersonalityPredictor()

# Example input data
sample_data = {
    'Time_spent_Alone': 8,
    'Social_event_attendance': 3,
    'Going_outside': 4,
    'Friends_circle_size': 2,
    'Post_frequency': 2,
    'Has_Stage_Fear': 1,
    'Gets_Drained_Socializing': 1
}

# Make prediction
result = predictor.predict_single(sample_data)
print(f"Personality: {result['personality']}")
print(f"Confidence: {result['confidence']:.1f}%")
```

### 2. Streamlit Web App Usage

```bash
# Run the web application
streamlit run app/streamlit_app.py

# Access at: http://localhost:8501
```

### 3. Batch Prediction Usage

```python
import pandas as pd

# Load batch data
batch_data = pd.read_csv('new_personality_data.csv')

# Make batch predictions
results = predictor.predict_batch(batch_data)
print(results[['Predicted_Personality', 'Confidence']])
```

## Input Features

### Required Features (Scale 1-10):
1. **Time_spent_Alone**: Preference for solitary activities
2. **Social_event_attendance**: Frequency of social event participation
3. **Going_outside**: Tendency to engage in outdoor social activities
4. **Friends_circle_size**: Size of close social circle
5. **Post_frequency**: Social media posting frequency

### Binary Features (0/1):
6. **Has_Stage_Fear**: Experience of stage fright (0=No, 1=Yes)
7. **Gets_Drained_Socializing**: Energy drain from social activities (0=No, 1=Yes)

## Output Format

```json
{
    "personality": "Introvert",
    "confidence": 89.5,
    "probabilities": {
        "Extrovert": 10.5,
        "Introvert": 89.5
    }
}
```

## Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 91.45% |
| Precision | 87.93% |
| Recall | 93.15% |
| F1-Score | 90.47% |

## Error Handling

- Missing features will raise `ValueError`
- Invalid data types will be automatically converted
- Out-of-range values (< 1 or > 10) will be clipped

## Installation Requirements

```
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
joblib>=1.0.0
streamlit>=1.12.0
plotly>=5.0.0
```

## File Structure

```
models/
├── naive_bayes_model.pkl          # Trained Naive Bayes model
├── random_forest_model.pkl        # Backup Random Forest model
├── logistic_regression_model.pkl  # Backup Logistic Regression model
├── standard_scaler.pkl            # Feature scaler (for LR)
├── label_encoder.pkl              # Target label encoder
├── feature_names.pkl              # Feature name mapping
└── model_metadata.pkl             # Model metadata and performance
```

## Support

For technical support or questions:
- Check model metadata: `model_metadata.pkl`
- Verify feature names: `feature_names.pkl`
- Ensure all required dependencies are installed
- Validate input data format and ranges

## Personality Type Descriptions

### Extrovert Characteristics:
- High social energy and outgoing nature
- Frequent social interactions and events
- Large social circles and many acquaintances
- Comfortable with attention and public speaking
- Energized by social activities

### Introvert Characteristics:
- Prefer solitary activities and quiet environments
- Smaller, close-knit social circles
- Need alone time to recharge energy
- Think before speaking and prefer deep conversations
- Drained by excessive social interaction

---
*Model trained on behavioral dataset with 91.45% accuracy*
