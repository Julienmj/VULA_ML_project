import streamlit as st
import cv2
import numpy as np
import pickle
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Crop Disease Detection System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS with green theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%);
        color: white;
        font-size: 16px;
        font-weight: 600;
        padding: 12px 32px;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px rgba(46, 125, 50, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        box-shadow: 0 6px 12px rgba(46, 125, 50, 0.3);
        transform: translateY(-2px);
    }
    
    h1 {
        color: #1b5e20;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        color: #2e7d32;
        font-weight: 600;
    }
    
    .header-container {
        background: linear-gradient(135deg, #2e7d32 0%, #43a047 100%);
        padding: 40px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(46, 125, 50, 0.2);
    }
    
    .header-title {
        color: white;
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        color: #e8f5e9;
        font-size: 18px;
        text-align: center;
        margin-top: 10px;
        font-weight: 400;
    }
    
    .result-card {
        background: white;
        border-left: 6px solid #2e7d32;
        padding: 24px;
        border-radius: 8px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .info-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8f4 100%);
        border-left: 6px solid #2e7d32;
        padding: 20px;
        border-radius: 8px;
        margin: 12px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    
    .info-card p, .info-card strong, .info-card li, .info-card h4, .info-card ol {
        color: #1b5e20 !important;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        border-top: 4px solid #2e7d32;
    }
    
    .progress-bar {
        background-color: #e0e0e0;
        border-radius: 4px;
        height: 10px;
        margin-top: 8px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #2e7d32 0%, #66bb6a 100%);
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .crop-name {
        color: #1b5e20;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    
    .disease-name {
        color: #c62828;
        font-size: 22px;
        font-weight: 600;
        margin: 8px 0;
    }
    
    .confidence-text {
        color: #424242;
        font-size: 18px;
        font-weight: 500;
    }
    
    .sidebar .element-container {
        background: white;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

MODEL_PATH = Path(__file__).parent.parent / 'models' / 'crop_disease_model.pkl'
LABEL_PATH = Path(__file__).parent.parent / 'models' / 'label_encoder.pkl'

@st.cache_resource
def load_model():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(LABEL_PATH, 'rb') as f:
        labels = pickle.load(f)
    return model, labels

def preprocess_image(image):
    img = cv2.resize(image, (64, 64))  # Match training size
    img = img.flatten() / 255.0
    return img.reshape(1, -1)

# Header
st.markdown("""
<div class='header-container'>
    <h1 class='header-title'>Crop Disease Detection System</h1>
    <p class='header-subtitle'>AI-Powered Diagnostics for Smallholder Farmers</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### About This System")
    st.markdown("""
    <div class='info-card'>
        <p><strong>Problem:</strong> Crop diseases cause significant yield losses due to late or incorrect diagnosis.</p>
        <p><strong>Solution:</strong> AI-powered image analysis for instant disease detection.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### System Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Crops", "14")
        st.metric("Diseases", "38")
    with col2:
        st.metric("Images", "54K")
        st.metric("Accuracy", "85%+")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Upload Crop Leaf Image")
    st.markdown("*Capture a clear photo of the affected leaf for analysis*")
    
    uploaded_file = st.file_uploader(
        "Select Image File",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of the crop leaf"
    )
    
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        st.image(image, caption="Uploaded Image")
        
        analyze_button = st.button("Analyze Disease", use_container_width=True)
    else:
        st.info("Please upload a crop leaf image to begin analysis")
        analyze_button = False

with col2:
    st.markdown("### Diagnosis Results")
    
    if uploaded_file and analyze_button:
        with st.spinner("Analyzing image..."):
            try:
                model, labels = load_model()
                processed = preprocess_image(image)
                pred_proba = model.predict_proba(processed)[0]
                class_idx = np.argmax(pred_proba)
                confidence = pred_proba[class_idx]
                
                # Parse disease name
                disease_name = labels[class_idx]
                parts = disease_name.split('___')
                crop = parts[0] if len(parts) > 0 else "Unknown"
                disease = parts[1].replace('_', ' ') if len(parts) > 1 else "Unknown"
                
                # Display results
                st.markdown(f"""
                <div class='result-card'>
                    <p class='crop-name'>{crop}</p>
                    <p class='disease-name'>{disease}</p>
                    <p class='confidence-text'>Confidence: {confidence:.1%}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Confidence indicator
                if confidence > 0.8:
                    st.success("High confidence - Diagnosis is reliable")
                elif confidence > 0.6:
                    st.warning("Moderate confidence - Consider expert consultation")
                else:
                    st.error("Low confidence - Please consult an agricultural expert")
                
                # Top predictions
                st.markdown("### Alternative Diagnoses")
                top5 = np.argsort(pred_proba)[-5:][::-1]
                
                for i, idx in enumerate(top5):
                    disease_full = labels[idx]
                    prob = pred_proba[idx]
                    parts = disease_full.split('___')
                    crop_name = parts[0] if len(parts) > 0 else "Unknown"
                    disease_name = parts[1].replace('_', ' ') if len(parts) > 1 else "Unknown"
                    
                    st.markdown(f"""
                    <div class='info-card'>
                        <strong>{i+1}. {crop_name} - {disease_name}</strong><br>
                        <span style='color: #666;'>Probability: {prob:.1%}</span>
                        <div class='progress-bar'>
                            <div class='progress-fill' style='width: {prob*100}%;'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Recommendations
                st.markdown("### Recommended Actions")
                st.markdown("""
                <div class='info-card'>
                    <ol style='margin: 0; padding-left: 20px;'>
                        <li>Confirm diagnosis with local agricultural officer</li>
                        <li>Apply appropriate treatment based on identified disease</li>
                        <li>Monitor crop progress over 7-14 days</li>
                        <li>Isolate affected plants to prevent disease spread</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please ensure the model is trained first")
    else:
        st.markdown("""
        <div class='info-card'>
            <h4 style='margin-top: 0;'>How to Use</h4>
            <ol style='margin: 0; padding-left: 20px;'>
                <li>Capture a clear photo of the affected crop leaf</li>
                <li>Upload the image using the file selector</li>
                <li>Click the "Analyze Disease" button</li>
                <li>Review diagnosis results and recommendations</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Supported Crops")
        crops = ["Apple", "Tomato", "Potato", "Corn", "Grape", "Peach", 
                 "Pepper", "Orange", "Strawberry", "Blueberry", "Cherry", "Squash"]
        
        cols = st.columns(3)
        for i, crop in enumerate(crops):
            cols[i % 3].markdown(f"• {crop}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #2e7d32; padding: 20px;'>
    <p style='font-weight: 600; margin: 0;'>Empowering Farmers Through Technology</p>
    <p style='font-size: 14px; color: #666; margin-top: 8px;'>Developed to support smallholder farmers in making informed crop management decisions</p>
</div>
""", unsafe_allow_html=True)
