# 🌱 Crop Disease Detection System

An AI-powered machine learning system that analyzes crop leaf images to detect and classify diseases, helping smallholder farmers make timely and informed decisions.

---

## 📋 Table of Contents
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dataset Information](#-dataset-information)
- [Model Performance](#-model-performance)
- [Project Structure](#-project-structure)
- [Contributors](#-contributors)
- [License](#-license)

---

## 🎯 Problem Statement

Crop diseases cause significant yield losses among smallholder farmers due to late or incorrect diagnosis. Access to agricultural experts is limited, and farmers often rely on guesswork, which results in ineffective treatment and reduced productivity.

## 💡 Solution

A machine learning-based image classification system using Random Forest algorithm that:
- Analyzes crop leaf images in real-time
- Detects and classifies 38 different crop diseases
- Provides confidence scores and alternative diagnoses
- Offers actionable recommendations for farmers

---

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (Recommended: Python 3.12)
- **Git** (for cloning the repository)
- **pip** (Python package manager)
- **Minimum 8GB RAM** (for model training)
- **2GB free disk space**

---

## 📥 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/AIC.git
cd AIC
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Or install manually:**
```bash
pip install pandas numpy opencv-python scikit-learn streamlit matplotlib seaborn joblib pillow
```

### Step 4: Download Dataset

1. Download the PlantVillage dataset from [Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease)
2. Extract to `plantvillage dataset/` folder in the project root

### Step 5: Prepare Data

```bash
python src\data_cleaning.py
```

This creates `data/processed/dataset_metadata.csv` with 54,305 image records.

---

## 🚀 Usage

### Train the Model

```bash
python src\train_model_sklearn.py
```

**Training Details:**
- Duration: ~20-30 minutes
- Output: `models/crop_disease_model.pkl` and `models/label_encoder.pkl`
- Training samples: 20,000 images (configurable)

### Launch Web Application

```bash
streamlit run ui\app.py
```

**Access the app at:** http://localhost:8501

### Using the Application

1. **Upload Image:** Click "Browse files" and select a crop leaf image (JPG/PNG)
2. **Analyze:** Click "Analyze Disease" button
3. **Review Results:**
   - Primary diagnosis with confidence score
   - Top 5 alternative diagnoses
   - Recommended actions based on confidence level

---

## 📊 Dataset Information

| Metric | Value |
|--------|-------|
| Total Images | 54,305 |
| Crop Types | 14 |
| Disease Classes | 38 |
| Healthy Classes | 14 |
| Original Resolution | 256x256 |
| Training Resolution | 64x64 |

### Supported Crops
Apple, Tomato, Potato, Corn, Grape, Peach, Pepper, Orange, Strawberry, Blueberry, Cherry, Squash, Soybean, Raspberry

---

## 🎯 Model Performance

**Algorithm:** Random Forest Classifier

**Configuration:**
- Training samples: 16,000 (80%)
- Test samples: 4,000 (20%)
- Number of trees: 200
- Max depth: 30
- Features: Flattened pixel values (64x64x3 = 12,288)

**Confidence Interpretation:**
- **High (>80%):** Reliable diagnosis
- **Moderate (60-80%):** Consider expert consultation
- **Low (<60%):** Consult agricultural expert

---

## 📁 Project Structure

```
AIC/
├── data/
│   ├── processed/
│   │   └── dataset_metadata.csv    # Cleaned dataset metadata
│   └── raw/                         # Raw data (if any)
├── models/
│   ├── crop_disease_model.pkl      # Trained Random Forest model
│   └── label_encoder.pkl            # Disease class labels
├── notebooks/
│   ├── 01_data_cleaning.ipynb      # Data preprocessing notebook
│   ├── 02_eda.ipynb                # Exploratory data analysis
│   └── 03_model_training.ipynb     # Model training experiments
├── src/
│   ├── data_cleaning.py            # Data cleaning script
│   └── train_model_sklearn.py      # Model training script
├── ui/
│   └── app.py                      # Streamlit web interface
├── plantvillage dataset/           # Raw image dataset (not in repo)
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies
```

---

## 💡 Key Features

✅ **Instant Disease Diagnosis** - Real-time image analysis  
✅ **38 Disease Classes** - Comprehensive disease coverage  
✅ **Confidence Scoring** - Reliability indicators  
✅ **Alternative Diagnoses** - Top 5 possibilities shown  
✅ **User-Friendly Interface** - Professional agricultural theme  
✅ **No Expert Required** - Accessible to all farmers  
✅ **Actionable Recommendations** - Clear next steps provided  

---

## 🔧 Technical Stack

- **Language:** Python 3.12
- **ML Framework:** scikit-learn
- **Image Processing:** OpenCV
- **Web Framework:** Streamlit
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn

---

## 👥 Contributors

| Name | Role | Contact |
|------|------|---------|
| Pacifique Bakundukize  | Project Lead | pacitekno12@gmail.com |
| [Name 2] | ML Engineer | email@example.com |
| [Name 3] | Data Scientist | email@example.com |
| [Name 4] | Backend Developer | email@example.com |
| [Name 5] | Frontend Developer | email@example.com |
| [Name 6] | UI/UX Designer | email@example.com |
| [Name 7] | Data Analyst | email@example.com |
| [Name 8] | QA Engineer | email@example.com |
| [Name 9] | Documentation Lead | email@example.com |
| [Name 10] | DevOps Engineer | email@example.com |

---

## 🌍 Impact

**Target Users:** Smallholder farmers in developing regions

**Benefits:**
- 🌾 Reduced crop losses through early detection
- 📉 Decreased reliance on agricultural experts
- 💊 Improved treatment effectiveness
- 📈 Increased farmer productivity
- 📊 Data-driven agricultural decisions

---

## 📝 Future Enhancements

- [ ] Train on full 54K dataset
- [ ] Implement CNN for improved accuracy
- [ ] Mobile application development
- [ ] Treatment recommendations database
- [ ] Offline mode support
- [ ] Multi-language interface
- [ ] Integration with agricultural APIs
- [ ] Batch image processing

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed for educational purposes as part of an AI/ML course focusing on practical agricultural applications.

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Contact the project team
- Check documentation in `/notebooks`

---

## 🙏 Acknowledgments

- PlantVillage Dataset for providing comprehensive crop disease images
- Agricultural experts for domain knowledge validation
- Open-source community for tools and libraries

---

**Developed to empower smallholder farmers through accessible AI technology** 🌱

---

## 📚 Additional Resources

- [PlantVillage Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Project Notebooks](./notebooks/)
