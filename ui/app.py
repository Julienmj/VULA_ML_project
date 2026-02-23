import streamlit as st
import cv2
import numpy as np
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import torch
import torch.nn as nn

st.set_page_config(page_title="Crop Disease Detection", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .main { 
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 25%, #ffffff 50%, #f1f8e9 75%, #e8f5e9 100%);
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1.5px solid rgba(139, 195, 74, 0.2);
        padding: 32px;
        box-shadow: 0 10px 40px rgba(85, 139, 47, 0.12);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(139, 195, 74, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(85, 139, 47, 0.2);
        border: 1.5px solid rgba(139, 195, 74, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%);
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        border: 2px solid rgba(139, 195, 74, 0.25);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #558b2f, #8bc34a, #558b2f);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .metric-card:hover::after {
        transform: scaleX(1);
    }
    
    .metric-card:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: 0 20px 50px rgba(76, 175, 80, 0.25);
        border: 2px solid rgba(139, 195, 74, 0.6);
        background: linear-gradient(135deg, #e8f5e9 0%, #c5e1a5 100%);
    }
    
    .metric-value {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #1b5e20 0%, #4caf50 50%, #8bc34a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 12px 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .metric-label {
        font-size: 13px;
        color: #558b2f;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
    }
    
    .header-banner {
        background: linear-gradient(135deg, #2e7d32 0%, #4caf50 50%, #66bb6a 100%);
        border-radius: 28px;
        padding: 50px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 15px 50px rgba(46, 125, 50, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .header-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .header-title {
        font-size: 52px;
        font-weight: 900;
        color: white;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .header-subtitle {
        font-size: 20px;
        color: rgba(255,255,255,0.95);
        margin-top: 12px;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #558b2f 0%, #7cb342 100%);
        color: white;
        font-weight: 700;
        font-size: 16px;
        padding: 16px 48px;
        border-radius: 50px;
        border: none;
        box-shadow: 0 8px 25px rgba(85, 139, 47, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #689f38 0%, #8bc34a 100%);
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 15px 40px rgba(85, 139, 47, 0.5);
    }
    
    .result-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 28px;
        border-left: 5px solid #8bc34a;
        margin: 18px 0;
        transition: all 0.35s ease;
        box-shadow: 0 4px 15px rgba(85, 139, 47, 0.1);
    }
    
    .result-card:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 30px rgba(85, 139, 47, 0.2);
        border-left: 5px solid #558b2f;
    }
    
    .disease-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #1b5e20 0%, #4caf50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
    }
    
    .confidence-badge {
        display: inline-block;
        padding: 12px 28px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 15px;
        margin-top: 12px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .confidence-badge:hover { 
        transform: scale(1.1) rotate(-2deg); 
    }
    
    .high-confidence {
        background: linear-gradient(135deg, #4caf50, #66bb6a);
        color: white;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
    }
    
    .medium-confidence {
        background: linear-gradient(135deg, #ffa726, #ffb74d);
        color: white;
        box-shadow: 0 6px 20px rgba(255, 167, 38, 0.4);
    }
    
    .low-confidence {
        background: linear-gradient(135deg, #ef5350, #e57373);
        color: white;
        box-shadow: 0 6px 20px rgba(239, 83, 80, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 12px;
        border: 1.5px solid rgba(139, 195, 74, 0.25);
        box-shadow: 0 4px 15px rgba(85, 139, 47, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #558b2f;
        border-radius: 14px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 15px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(139, 195, 74, 0.15);
        transform: translateY(-3px);
        color: #2e7d32;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #66bb6a 0%, #81c784 100%);
        color: white !important;
        box-shadow: 0 6px 20px rgba(102, 187, 106, 0.4);
    }
    
    .uploadedFile {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        border: 2px dashed rgba(139, 195, 74, 0.4);
        transition: all 0.3s ease;
        padding: 20px;
    }
    
    .uploadedFile:hover {
        border: 2px dashed rgba(139, 195, 74, 0.8);
        background: rgba(232, 245, 233, 0.5);
    }
    
    h1, h2, h3 {
        background: linear-gradient(135deg, #1b5e20 0%, #4caf50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #558b2f, #8bc34a);
    }
</style>
""", unsafe_allow_html=True)


MODEL_PATH = Path(__file__).parent.parent / 'models' / 'crop_disease_cnn.pth'
LABEL_PATH = Path(__file__).parent.parent / 'models' / 'label_encoder.pkl'
METADATA_PATH = Path(__file__).parent.parent / 'data' / 'processed' / 'dataset_metadata.csv'

class CropDiseaseCNN(nn.Module):
    def __init__(self, num_classes):
        super(CropDiseaseCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 8 * 8, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

@st.cache_resource
def load_model():
    with open(LABEL_PATH, 'rb') as f:
        labels = pickle.load(f)
    model = CropDiseaseCNN(len(labels))
    model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
    model.eval()
    return model, labels

@st.cache_data
def load_metadata():
    return pd.read_csv(METADATA_PATH)

def preprocess_image(image):
    img = cv2.resize(image, (128, 128))
    img = img.astype(np.float32) / 255.0
    img = img.transpose(2, 0, 1)
    return torch.FloatTensor(img).unsqueeze(0)


st.markdown("""
<div class='header-banner'>
    <h1 class='header-title'>🌿 Crop Disease Detection System</h1>
    <p class='header-subtitle'>AI-Powered CNN for Precision Agriculture | Real-time Disease Diagnosis</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Disease Detection", "📈 Analytics & Insights", "📥 Export Data"])


with tab1:
    st.markdown("### 📊 System Overview & Statistics")
    
    try:
        df = load_metadata()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>🖼️ Total Images</div>
                <div class='metric-value'>{len(df):,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>🌾 Crop Types</div>
                <div class='metric-value'>{df['crop'].nunique()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>🦠 Disease Classes</div>
                <div class='metric-value'>{df['class_label'].nunique()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            healthy_pct = (df['is_healthy'].sum() / len(df) * 100)
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>✅ Healthy Rate</div>
                <div class='metric-value'>{healthy_pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌱 Top 10 Crops Distribution")
            crop_counts = df['crop'].value_counts().head(10)
            fig = px.bar(
                x=crop_counts.values, 
                y=crop_counts.index, 
                orientation='h',
                color=crop_counts.values,
                color_continuous_scale=['#1b5e20', '#2e7d32', '#388e3c', '#43a047', '#4caf50', '#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9', '#e8f5e9'],
                labels={'x': 'Number of Images', 'y': 'Crop Type'}
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2e7d32', size=12, family='Inter'),
                showlegend=False,
                height=450,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(139, 195, 74, 0.1)'),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🩺 Health Status Distribution")
            health_data = df['is_healthy'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=['Diseased', 'Healthy'], 
                values=health_data.values,
                hole=0.5,
                marker=dict(colors=['#ef5350', '#66bb6a'], line=dict(color='white', width=3)),
                textfont=dict(size=16, color='white', family='Inter'),
                pull=[0.05, 0]
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2e7d32', size=14, family='Inter'),
                height=450,
                margin=dict(l=0, r=0, t=30, b=0),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🦠 Top 12 Disease Distribution")
            disease_counts = df[df['is_healthy'] == False]['disease'].value_counts().head(12)
            fig = px.pie(
                values=disease_counts.values, 
                names=disease_counts.index,
                color_discrete_sequence=px.colors.sequential.Greens_r,
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2e7d32', size=11, family='Inter'),
                height=450,
                margin=dict(l=0, r=0, t=30, b=0),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Dataset Statistics")
            st.markdown(f"""
            <div class='glass-card'>
                <p style='color: #2e7d32; margin: 14px 0; font-size: 15px;'><strong>📏 Avg Image Size:</strong> {df['file_size_kb'].mean():.2f} KB</p>
                <p style='color: #2e7d32; margin: 14px 0; font-size: 15px;'><strong>💾 Total Dataset:</strong> {df['file_size_kb'].sum()/1024:.2f} MB</p>
                <p style='color: #2e7d32; margin: 14px 0; font-size: 15px;'><strong>📐 Image Dimensions:</strong> {df['width'].mode()[0]}x{df['height'].mode()[0]} px</p>
                <p style='color: #2e7d32; margin: 14px 0; font-size: 15px;'><strong>🦠 Disease Rate:</strong> {(1 - df['is_healthy'].mean())*100:.1f}%</p>
                <p style='color: #2e7d32; margin: 14px 0; font-size: 15px;'><strong>✅ Healthy Samples:</strong> {df['is_healthy'].sum():,}</p>
                <p style='color: #2e7d32; margin: 14px 0; font-size: 15px;'><strong>❌ Diseased Samples:</strong> {(~df['is_healthy']).sum():,}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🤖 CNN Model Info")
            st.markdown("""
            <div class='glass-card'>
                <p style='color: #2e7d32; margin: 12px 0; font-size: 15px;'><strong>🏗️ Architecture:</strong> Deep CNN (PyTorch)</p>
                <p style='color: #2e7d32; margin: 12px 0; font-size: 15px;'><strong>📚 Layers:</strong> 4 Conv + 2 Fully Connected</p>
                <p style='color: #2e7d32; margin: 12px 0; font-size: 15px;'><strong>🖼️ Input Size:</strong> 128x128x3 RGB</p>
                <p style='color: #2e7d32; margin: 12px 0; font-size: 15px;'><strong>⚙️ Parameters:</strong> ~2.5M trainable</p>
                <p style='color: #2e7d32; margin: 12px 0; font-size: 15px;'><strong>🎯 Optimizer:</strong> Adam (lr=0.001)</p>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {str(e)}")


with tab2:
    st.markdown("### 🔍 Upload & Analyze Crop Leaf Image")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #2e7d32; margin-top: 0;'>📤 Upload Image</h4>
            <p style='color: #558b2f; font-size: 14px;'>Upload a clear photo of the crop leaf for AI-powered disease analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=['jpg', 'jpeg', 'png'],
            help="Supported: JPG, JPEG, PNG | Max size: 10MB"
        )
        
        if uploaded_file:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            st.image(image, caption="📸 Uploaded Image", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            analyze_button = st.button("🔬 Analyze Disease", use_container_width=True, type="primary")
        else:
            st.info("📌 Please upload a crop leaf image to begin analysis")
            analyze_button = False
    
    with col2:
        st.markdown("### 🎯 Analysis Results")
        
        if uploaded_file and analyze_button:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Loading CNN model...")
            progress_bar.progress(20)
            
            try:
                model, labels = load_model()
                progress_bar.progress(40)
                
                status_text.text("🖼️ Preprocessing image...")
                processed = preprocess_image(image)
                progress_bar.progress(60)
                
                status_text.text("🧠 Running CNN inference...")
                with torch.no_grad():
                    outputs = model(processed)
                    probs = torch.softmax(outputs, dim=1)[0]
                
                progress_bar.progress(80)
                
                pred_proba = probs.numpy()
                class_idx = np.argmax(pred_proba)
                confidence = pred_proba[class_idx]
                
                disease_name = labels[class_idx]
                parts = disease_name.replace('___', '_').split('_')
                crop = parts[0] if len(parts) > 0 else "Unknown"
                disease = ' '.join(parts[1:]) if len(parts) > 1 else "Unknown"
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                confidence_class = "high-confidence" if confidence > 0.8 else "medium-confidence" if confidence > 0.6 else "low-confidence"
                
                st.markdown(f"""
                <div class='result-card'>
                    <p style='color: #558b2f; margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;'>🌾 Detected Crop</p>
                    <p class='disease-title'>{crop}</p>
                    <p style='color: #558b2f; margin-top: 20px; margin-bottom: 8px; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;'>🦠 Condition</p>
                    <p class='disease-title' style='font-size: 28px;'>{disease}</p>
                    <span class='confidence-badge {confidence_class}'>🎯 Confidence: {confidence:.1%}</span>
                </div>
                """, unsafe_allow_html=True)
                
                if confidence > 0.8:
                    st.success("✅ **High Confidence** - Diagnosis is highly reliable. Proceed with recommended treatment.")
                elif confidence > 0.6:
                    st.warning("⚠️ **Moderate Confidence** - Consider consulting an agricultural expert for confirmation.")
                else:
                    st.error("❌ **Low Confidence** - Please consult an agricultural expert for accurate diagnosis.")
                
                st.markdown("### 📊 Top 5 Predictions")
                top5 = np.argsort(pred_proba)[-5:][::-1]
                
                for i, idx in enumerate(top5):
                    disease_full = labels[idx]
                    prob = pred_proba[idx]
                    parts = disease_full.replace('___', '_').split('_')
                    crop_name = parts[0]
                    disease_name = ' '.join(parts[1:])
                    
                    rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
                    
                    st.markdown(f"""
                    <div class='result-card' style='padding: 18px;'>
                        <strong style='color: #1b5e20; font-size: 16px;'>{rank_emoji} {crop_name} - {disease_name}</strong><br>
                        <span style='color: #558b2f; font-size: 14px; font-weight: 600;'>Probability: {prob:.2%}</span>
                        <div style='background: rgba(139, 195, 74, 0.15); border-radius: 12px; height: 10px; margin-top: 10px; overflow: hidden;'>
                            <div style='background: linear-gradient(90deg, #2e7d32, #66bb6a); height: 100%; width: {prob*100}%; border-radius: 12px; transition: width 0.5s ease;'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("### 💡 Recommended Actions")
                st.markdown("""
                <div class='glass-card'>
                    <ol style='color: #2e7d32; margin: 0; padding-left: 24px; font-size: 15px; line-height: 2;'>
                        <li>✅ Verify diagnosis with local agricultural officer</li>
                        <li>💊 Apply appropriate treatment for identified disease</li>
                        <li>📅 Monitor crop health over 7-14 days</li>
                        <li>🚫 Isolate affected plants to prevent spread</li>
                        <li>📸 Document treatment progress with photos</li>
                        <li>📚 Research disease-specific management practices</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.info("💡 Please ensure the CNN model is trained first by running `python src/train_cnn.py`")
        else:
            st.markdown("""
            <div class='glass-card'>
                <h4 style='color: #2e7d32; margin-top: 0;'>📋 How to Use</h4>
                <ol style='color: #2e7d32; margin: 0; padding-left: 24px; font-size: 15px; line-height: 2;'>
                    <li>📸 Capture a clear, well-lit photo of the affected leaf</li>
                    <li>☀️ Ensure good lighting and sharp focus</li>
                    <li>📤 Upload the image using the file selector above</li>
                    <li>🔬 Click "Analyze Disease" button</li>
                    <li>📊 Review CNN predictions and confidence scores</li>
                    <li>💡 Follow recommended actions based on results</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🌾 Supported Crops")
            crops = ["Apple", "Tomato", "Potato", "Corn", "Grape", "Peach", "Pepper", "Orange", "Strawberry", "Blueberry", "Cherry", "Squash"]
            
            cols = st.columns(4)
            for i, crop in enumerate(crops):
                cols[i % 4].markdown(f"<p style='color: #2e7d32; font-weight: 600;'>🌱 {crop}</p>", unsafe_allow_html=True)


with tab3:
    st.markdown("### 📈 Advanced Analytics & Insights")
    
    try:
        df = load_metadata()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌳 Disease Frequency Treemap")
            disease_crop = df[df['is_healthy'] == False].groupby(['crop', 'disease']).size().reset_index(name='count')
            top_diseases = disease_crop.nlargest(20, 'count')
            
            fig = px.treemap(
                top_diseases, 
                path=['crop', 'disease'], 
                values='count', 
                color='count',
                color_continuous_scale=['#e8f5e9', '#c5e1a5', '#aed581', '#9ccc65', '#8bc34a', '#7cb342', '#689f38', '#558b2f', '#33691e']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2e7d32', size=12, family='Inter'),
                height=500,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Image Size Distribution")
            fig = px.histogram(
                df, 
                x='file_size_kb', 
                nbins=50, 
                color_discrete_sequence=['#66bb6a'],
                labels={'file_size_kb': 'File Size (KB)', 'count': 'Frequency'}
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2e7d32', size=12, family='Inter'),
                xaxis_title="File Size (KB)",
                yaxis_title="Number of Images",
                height=500,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(showgrid=True, gridcolor='rgba(139, 195, 74, 0.1)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 195, 74, 0.1)')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### 🌾 Crop-wise Health Analysis")
        crop_disease_matrix = pd.crosstab(df['crop'], df['is_healthy'])
        crop_disease_df = crop_disease_matrix.reset_index()
        crop_disease_df.columns = ['Crop', 'Diseased', 'Healthy']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Diseased', x=crop_disease_df['Crop'], y=crop_disease_df['Diseased'], marker_color='#ef5350'))
        fig.add_trace(go.Bar(name='Healthy', x=crop_disease_df['Crop'], y=crop_disease_df['Healthy'], marker_color='#66bb6a'))
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2e7d32', size=12, family='Inter'),
            height=450,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 195, 74, 0.1)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Disease Prevalence Table")
            disease_table = df[df['is_healthy'] == False]['disease'].value_counts().reset_index()
            disease_table.columns = ['Disease', 'Count']
            disease_table['Percentage'] = (disease_table['Count'] / disease_table['Count'].sum() * 100).round(2)
            disease_table['Percentage'] = disease_table['Percentage'].astype(str) + '%'
            st.dataframe(disease_table.head(15), use_container_width=True, height=400)
        
        with col2:
            st.markdown("#### 📊 Detailed Statistics")
            st.dataframe(df[['width', 'height', 'file_size_kb']].describe(), use_container_width=True, height=400)
        
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")


with tab4:
    st.markdown("### 📥 Export Dataset & Reports")
    
    try:
        df = load_metadata()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='glass-card'>
                <h4 style='color: #2e7d32; margin-top: 0;'>📊 Full Dataset Export</h4>
                <p style='color: #558b2f; font-size: 14px;'>Download complete dataset metadata with all image information</p>
            </div>
            """, unsafe_allow_html=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Full Dataset (CSV)",
                data=csv,
                file_name=f"crop_disease_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.markdown("""
            <div class='glass-card'>
                <h4 style='color: #2e7d32; margin-top: 0;'>📋 Summary Report</h4>
                <p style='color: #558b2f; font-size: 14px;'>Download executive summary with key statistics and metrics</p>
            </div>
            """, unsafe_allow_html=True)
            
            summary_df = pd.DataFrame({
                'Metric': ['Total Images', 'Crop Types', 'Disease Classes', 'Healthy Samples', 'Diseased Samples', 'Disease Rate (%)', 'Avg File Size (KB)', 'Total Dataset (MB)'],
                'Value': [
                    len(df), 
                    df['crop'].nunique(), 
                    df['class_label'].nunique(), 
                    df['is_healthy'].sum(), 
                    (~df['is_healthy']).sum(),
                    f"{(1 - df['is_healthy'].mean())*100:.2f}",
                    f"{df['file_size_kb'].mean():.2f}",
                    f"{df['file_size_kb'].sum()/1024:.2f}"
                ]
            })
            summary_csv = summary_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Summary Report (CSV)",
                data=summary_csv,
                file_name=f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🦠 Disease-Only Dataset")
            diseased_df = df[df['is_healthy'] == False]
            diseased_csv = diseased_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Diseased Samples Only",
                data=diseased_csv,
                file_name=f"diseased_samples_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### ✅ Healthy-Only Dataset")
            healthy_df = df[df['is_healthy'] == True]
            healthy_csv = healthy_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Healthy Samples Only",
                data=healthy_csv,
                file_name=f"healthy_samples_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📊 Quick Dataset Preview")
        st.dataframe(df.head(100), use_container_width=True, height=400)
        
    except Exception as e:
        st.error(f"❌ Error loading export options: {str(e)}")

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #e8f5e9 0%, #c5e1a5 100%); border-radius: 20px; margin-top: 40px;'>
    <h3 style='color: #1b5e20; margin: 0; font-weight: 800;'>🌱 Empowering Farmers Through AI Technology</h3>
    <p style='font-size: 16px; color: #2e7d32; margin-top: 12px; font-weight: 500;'>Deep Learning CNN for Precision Agriculture | Real-time Disease Detection</p>
    <p style='font-size: 14px; color: #558b2f; margin-top: 8px;'>Developed with ❤️ for smallholder farmers worldwide</p>
</div>
""", unsafe_allow_html=True)
