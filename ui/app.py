import streamlit as st
import cv2
import numpy as np
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(
    page_title="Crop Disease Detection System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .main { background: linear-gradient(135deg, #f1f8e9 0%, #ffffff 50%, #e8f5e9 100%); }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(139, 195, 74, 0.3);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(85, 139, 47, 0.15);
        transition: all 0.4s ease;
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 1);
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(85, 139, 47, 0.25);
        border: 1px solid rgba(139, 195, 74, 0.5);
    }
    
    .metric-glass {
        background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        border: 2px solid rgba(139, 195, 74, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .metric-glass:hover {
        background: linear-gradient(135deg, #e8f5e9 0%, #c5e1a5 100%);
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(76, 175, 80, 0.3);
        border: 2px solid rgba(139, 195, 74, 0.8);
    }
    
    .metric-value {
        font-size: 38px;
        font-weight: 700;
        background: linear-gradient(135deg, #2e7d32 0%, #66bb6a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 13px;
        color: #558b2f;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    .header-glass {
        background: linear-gradient(135deg, #ffffff 0%, #e8f5e9 100%);
        border-radius: 20px;
        padding: 45px;
        text-align: center;
        border: 2px solid rgba(139, 195, 74, 0.4);
        margin-bottom: 30px;
        transition: all 0.4s ease;
    }
    
    .header-glass:hover {
        background: linear-gradient(135deg, #e8f5e9 0%, #c5e1a5 100%);
        box-shadow: 0 15px 45px rgba(85, 139, 47, 0.2);
        border: 2px solid rgba(139, 195, 74, 0.6);
    }
    
    .header-title {
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(135deg, #1b5e20 0%, #4caf50 50%, #8bc34a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 18px;
        color: #558b2f;
        margin-top: 10px;
        font-weight: 500;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #558b2f 0%, #7cb342 100%);
        color: white;
        font-weight: 600;
        padding: 14px 45px;
        border-radius: 50px;
        border: none;
        box-shadow: 0 6px 20px rgba(85, 139, 47, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #689f38 0%, #8bc34a 100%);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(85, 139, 47, 0.6);
    }
    
    .result-glass {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(139, 195, 74, 0.3);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .result-glass:hover {
        background: rgba(255, 255, 255, 1);
        transform: translateX(5px);
        border-left: 4px solid #8bc34a;
        box-shadow: 0 8px 25px rgba(85, 139, 47, 0.2);
    }
    
    .disease-title {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #2e7d32 0%, #66bb6a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .confidence-badge {
        display: inline-block;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: 600;
        margin-top: 10px;
        transition: all 0.3s ease;
    }
    
    .confidence-badge:hover { transform: scale(1.1); }
    
    .high-confidence {
        background: rgba(76, 175, 80, 0.3);
        color: #4caf50;
        border: 2px solid #4caf50;
    }
    
    .medium-confidence {
        background: rgba(255, 193, 7, 0.3);
        color: #ffc107;
        border: 2px solid #ffc107;
    }
    
    .low-confidence {
        background: rgba(244, 67, 54, 0.3);
        color: #f44336;
        border: 2px solid #f44336;
    }
    
    div[data-testid="stMetricValue"] { color: #2e7d32; }
    div[data-testid="stMetricLabel"] { color: #558b2f; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 10px;
        border: 1px solid rgba(139, 195, 74, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #558b2f;
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(139, 195, 74, 0.2);
        transform: translateY(-2px);
        color: #2e7d32;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e8f5e9 0%, #c5e1a5 100%);
        border-bottom: 3px solid #8bc34a;
        color: #1b5e20;
    }
    
    h1, h2, h3, h4 {
        background: linear-gradient(135deg, #2e7d32 0%, #66bb6a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .uploadedFile {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 1px solid rgba(139, 195, 74, 0.3);
        transition: all 0.3s ease;
    }
    
    .uploadedFile:hover {
        background: rgba(255, 255, 255, 1);
        border: 1px solid rgba(139, 195, 74, 0.6);
    }
</style>
""", unsafe_allow_html=True)

MODEL_PATH = Path(__file__).parent.parent / 'models' / 'crop_disease_model.pkl'
LABEL_PATH = Path(__file__).parent.parent / 'models' / 'label_encoder.pkl'
METADATA_PATH = Path(__file__).parent.parent / 'data' / 'processed' / 'dataset_metadata.csv'

@st.cache_resource
def load_model():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(LABEL_PATH, 'rb') as f:
        labels = pickle.load(f)
    return model, labels

@st.cache_data
def load_metadata():
    return pd.read_csv(METADATA_PATH)

def preprocess_image(image):
    img = cv2.resize(image, (64, 64))
    img = img.astype(np.float32) / 255.0
    
    # Extract color histogram features
    hist_r = cv2.calcHist([img], [0], None, [8], [0, 1]).flatten()
    hist_g = cv2.calcHist([img], [1], None, [8], [0, 1]).flatten()
    hist_b = cv2.calcHist([img], [2], None, [8], [0, 1]).flatten()
    
    # Combine features
    features = np.concatenate([img.flatten(), hist_r, hist_g, hist_b])
    return features.reshape(1, -1)

def generate_pdf_report(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, "Crop Disease Detection Report")
    c.setFont("Helvetica", 12)
    y = 700
    for key, value in data.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 30
    c.save()
    buffer.seek(0)
    return buffer

st.markdown("""
<div class='header-glass'>
    <h1 class='header-title'>Crop Disease Detection System</h1>
    <p class='header-subtitle'>AI-Powered Agricultural Diagnostics Platform</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Dashboard", "Disease Detection", "Analytics & Reports"])

with tab1:
    st.markdown("### System Overview")
    
    try:
        df = load_metadata()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-glass'>
                <div class='metric-label'>Total Images</div>
                <div class='metric-value'>{len(df):,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-glass'>
                <div class='metric-label'>Crop Types</div>
                <div class='metric-value'>{df['crop'].nunique()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-glass'>
                <div class='metric-label'>Disease Classes</div>
                <div class='metric-value'>{df['disease'].nunique()}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            healthy_count = df[df['is_healthy'] == True].shape[0]
            st.markdown(f"""
            <div class='metric-glass'>
                <div class='metric-label'>Healthy Samples</div>
                <div class='metric-value'>{healthy_count:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Crop Distribution")
            crop_counts = df['crop'].value_counts().head(10)
            fig = px.bar(x=crop_counts.values, y=crop_counts.index, orientation='h', color=crop_counts.values,
                        color_continuous_scale=['#2d5016', '#558b2f', '#7cb342', '#8bc34a'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#2e7d32'), showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Health Status Distribution")
            health_data = df['is_healthy'].value_counts()
            fig = go.Figure(data=[go.Pie(labels=['Diseased', 'Healthy'], values=health_data.values,
                                        hole=0.4, marker=dict(colors=['#d32f2f', '#558b2f']))])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#2e7d32'), height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top 10 Diseases")
            disease_counts = df[df['is_healthy'] == False]['disease'].value_counts().head(10)
            fig = px.pie(values=disease_counts.values, names=disease_counts.index,
                        color_discrete_sequence=['#2d5016', '#3d6b1f', '#558b2f', '#689f38', '#7cb342', 
                                                '#8bc34a', '#9ccc65', '#aed581', '#c5e1a5', '#dcedc8'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#2e7d32'), height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Dataset Statistics")
            st.markdown(f"""
            <div class='result-glass'>
                <p style='color: #2e7d32; margin: 10px 0;'><strong>Average Image Size:</strong> {df['file_size_kb'].mean():.2f} KB</p>
                <p style='color: #2e7d32; margin: 10px 0;'><strong>Total Dataset Size:</strong> {df['file_size_kb'].sum()/1024:.2f} MB</p>
                <p style='color: #2e7d32; margin: 10px 0;'><strong>Image Dimensions:</strong> {df['width'].mode()[0]}x{df['height'].mode()[0]} px</p>
                <p style='color: #2e7d32; margin: 10px 0;'><strong>Disease Rate:</strong> {(1 - df['is_healthy'].mean())*100:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### Model Information")
            st.markdown("""
            <div class='result-glass'>
                <p style='color: #2e7d32; margin: 10px 0;'><strong>Algorithm:</strong> Random Forest</p>
                <p style='color: #2e7d32; margin: 10px 0;'><strong>Trees:</strong> 200</p>
                <p style='color: #2e7d32; margin: 10px 0;'><strong>Max Depth:</strong> 30</p>
                <p style='color: #2e7d32; margin: 10px 0;'><strong>Training Samples:</strong> 20,000</p>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")

with tab2:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Upload Crop Image")
        st.markdown("Upload a clear image of the crop leaf for disease analysis")
        
        uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'],
                                        help="Supported formats: JPG, JPEG, PNG")
        
        if uploaded_file:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            st.image(image, caption="Uploaded Image", use_container_width=True)
            analyze_button = st.button("Analyze Disease", use_container_width=True)
        else:
            st.info("Please upload a crop leaf image to begin analysis")
            analyze_button = False
    
    with col2:
        st.markdown("### Analysis Results")
        
        if uploaded_file and analyze_button:
            with st.spinner("Analyzing image..."):
                try:
                    model, labels = load_model()
                    processed = preprocess_image(image)
                    pred_proba = model.predict_proba(processed)[0]
                    class_idx = np.argmax(pred_proba)
                    confidence = pred_proba[class_idx]
                    
                    disease_name = labels[class_idx]
                    parts = disease_name.split('___')
                    crop = parts[0] if len(parts) > 0 else "Unknown"
                    disease = parts[1].replace('_', ' ') if len(parts) > 1 else "Unknown"
                    
                    confidence_class = "high-confidence" if confidence > 0.8 else "medium-confidence" if confidence > 0.6 else "low-confidence"
                    
                    st.markdown(f"""
                    <div class='result-glass'>
                        <p style='color: #558b2f; margin: 0;'>Detected Crop</p>
                        <p class='disease-title'>{crop}</p>
                        <p style='color: #558b2f; margin-top: 15px; margin-bottom: 5px;'>Condition</p>
                        <p class='disease-title' style='font-size: 24px;'>{disease}</p>
                        <span class='confidence-badge {confidence_class}'>Confidence: {confidence:.1%}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if confidence > 0.8:
                        st.success("High confidence - Diagnosis is reliable")
                    elif confidence > 0.6:
                        st.warning("Moderate confidence - Consider expert consultation")
                    else:
                        st.error("Low confidence - Consult agricultural expert")
                    
                    st.markdown("### Alternative Diagnoses")
                    top5 = np.argsort(pred_proba)[-5:][::-1]
                    
                    for i, idx in enumerate(top5):
                        disease_full = labels[idx]
                        prob = pred_proba[idx]
                        parts = disease_full.split('___')
                        crop_name = parts[0] if len(parts) > 0 else "Unknown"
                        disease_name = parts[1].replace('_', ' ') if len(parts) > 1 else "Unknown"
                        
                        st.markdown(f"""
                        <div class='result-glass' style='padding: 15px;'>
                            <strong style='color: #2e7d32;'>{i+1}. {crop_name} - {disease_name}</strong><br>
                            <span style='color: #558b2f;'>Probability: {prob:.1%}</span>
                            <div style='background: rgba(139, 195, 74, 0.2); border-radius: 10px; height: 8px; margin-top: 8px;'>
                                <div style='background: linear-gradient(90deg, #558b2f, #8bc34a); height: 100%; width: {prob*100}%; border-radius: 10px;'></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("### Recommended Actions")
                    st.markdown("""
                    <div class='result-glass'>
                        <ol style='color: #2e7d32; margin: 0; padding-left: 20px;'>
                            <li>Verify diagnosis with local agricultural officer</li>
                            <li>Apply appropriate treatment for identified disease</li>
                            <li>Monitor crop health over 7-14 days</li>
                            <li>Isolate affected plants to prevent spread</li>
                            <li>Document treatment progress with photos</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    report_data = {
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Crop": crop,
                        "Disease": disease,
                        "Confidence": f"{confidence:.1%}"
                    }
                    pdf_buffer = generate_pdf_report(report_data)
                    st.download_button(label="Download PDF Report", data=pdf_buffer,
                                     file_name=f"disease_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                     mime="application/pdf")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Please ensure the model is trained first")
        else:
            st.markdown("""
            <div class='result-glass'>
                <h4 style='color: #2e7d32; margin-top: 0;'>How to Use</h4>
                <ol style='color: #2e7d32; margin: 0; padding-left: 20px;'>
                    <li>Capture a clear photo of the affected leaf</li>
                    <li>Ensure good lighting and focus</li>
                    <li>Upload the image using the file selector</li>
                    <li>Click "Analyze Disease" button</li>
                    <li>Review results and recommendations</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Supported Crops")
            crops = ["Apple", "Tomato", "Potato", "Corn", "Grape", "Peach", 
                     "Pepper", "Orange", "Strawberry", "Blueberry", "Cherry", "Squash"]
            
            cols = st.columns(3)
            for i, crop in enumerate(crops):
                cols[i % 3].markdown(f"<p style='color: #2e7d32;'>• {crop}</p>", unsafe_allow_html=True)

with tab3:
    st.markdown("### Advanced Analytics & Reports")
    
    try:
        df = load_metadata()
        
        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Full Dataset (CSV)", data=csv,
                             file_name=f"crop_disease_dataset_{datetime.now().strftime('%Y%m%d')}.csv",
                             mime="text/csv")
        
        with col2:
            summary_df = pd.DataFrame({
                'Metric': ['Total Images', 'Crop Types', 'Disease Classes', 'Healthy Samples', 'Disease Rate'],
                'Value': [len(df), df['crop'].nunique(), df['disease'].nunique(), 
                         df[df['is_healthy'] == True].shape[0], f"{(1 - df['is_healthy'].mean())*100:.1f}%"]
            })
            summary_csv = summary_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Summary Report (CSV)", data=summary_csv,
                             file_name=f"summary_report_{datetime.now().strftime('%Y%m%d')}.csv",
                             mime="text/csv")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Disease Frequency by Crop")
            disease_crop = df[df['is_healthy'] == False].groupby(['crop', 'disease']).size().reset_index(name='count')
            top_diseases = disease_crop.nlargest(15, 'count')
            
            fig = px.treemap(top_diseases, path=['crop', 'disease'], values='count', color='count',
                           color_continuous_scale=['#2d5016', '#558b2f', '#7cb342', '#8bc34a'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#2e7d32'), height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Image Size Distribution")
            fig = px.histogram(df, x='file_size_kb', nbins=50, color_discrete_sequence=['#558b2f'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#2e7d32'), xaxis_title="File Size (KB)",
                            yaxis_title="Count", height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Crop-wise Disease Analysis")
        crop_disease_matrix = pd.crosstab(df['crop'], df['is_healthy'])
        fig = px.bar(crop_disease_matrix, barmode='group', color_discrete_sequence=['#d32f2f', '#558b2f'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#2e7d32'), height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Detailed Dataset Statistics")
        st.dataframe(df.describe(), use_container_width=True)
        
        st.markdown("#### Disease Prevalence Table")
        disease_table = df[df['is_healthy'] == False]['disease'].value_counts().reset_index()
        disease_table.columns = ['Disease', 'Count']
        disease_table['Percentage'] = (disease_table['Count'] / disease_table['Count'].sum() * 100).round(2)
        st.dataframe(disease_table, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='font-weight: 600; margin: 0; color: #2e7d32;'>Empowering Farmers Through AI Technology</p>
    <p style='font-size: 14px; color: #558b2f; margin-top: 8px;'>Developed for smallholder farmers worldwide</p>
</div>
""", unsafe_allow_html=True)
