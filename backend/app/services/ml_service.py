import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import pickle
import os

class CropDiseaseCNN(nn.Module):
    def __init__(self, num_classes=15):
        super(CropDiseaseCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1), nn.BatchNorm2d(256), nn.ReLU(), nn.MaxPool2d(2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 8 * 8, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

class MLService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.label_encoder = None
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        self.recommendations = {
            "Tomato___Bacterial_spot": "Apply copper-based fungicides. Remove infected leaves. Ensure proper spacing.",
            "Tomato___Early_blight": "Use fungicides containing chlorothalonil. Practice crop rotation. Remove debris.",
            "Tomato___Late_blight": "Apply fungicides immediately. Remove infected plants. Improve air circulation.",
            "Tomato___Leaf_Mold": "Reduce humidity. Improve ventilation. Apply fungicides if severe.",
            "Tomato___Septoria_leaf_spot": "Remove infected leaves. Apply fungicides. Avoid overhead watering.",
            "Tomato___Spider_mites Two-spotted_spider_mite": "Use miticides. Spray with water. Introduce predatory mites.",
            "Tomato___Target_Spot": "Apply fungicides. Remove infected leaves. Practice crop rotation.",
            "Tomato___Tomato_mosaic_virus": "Remove infected plants. Control aphids. Use resistant varieties.",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Control whiteflies. Remove infected plants. Use resistant varieties.",
            "Tomato___healthy": "Continue good practices. Monitor regularly. Maintain proper nutrition.",
            "Potato___Early_blight": "Apply fungicides. Remove infected foliage. Practice crop rotation.",
            "Potato___Late_blight": "Apply fungicides preventively. Remove infected plants. Improve drainage.",
            "Potato___healthy": "Maintain current care. Monitor for pests. Ensure adequate nutrition.",
            "Pepper,_bell___Bacterial_spot": "Use copper sprays. Remove infected leaves. Avoid overhead irrigation.",
            "Pepper,_bell___healthy": "Continue monitoring. Maintain good practices. Ensure proper fertilization."
        }
        self.load_model()
    
    def load_model(self):
        model_path = os.path.join("ml_models", "crop_disease_cnn.pth")
        encoder_path = os.path.join("ml_models", "label_encoder.pkl")
        
        self.model = CropDiseaseCNN(num_classes=15)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        
        with open(encoder_path, "rb") as f:
            self.label_encoder = pickle.load(f)
    
    async def predict(self, image: Image.Image):
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            top3_prob, top3_idx = torch.topk(probabilities, 3)
        
        top3_prob = top3_prob.cpu().numpy()[0]
        top3_idx = top3_idx.cpu().numpy()[0]
        
        predictions = []
        for idx, prob in zip(top3_idx, top3_prob):
            class_name = self.label_encoder.inverse_transform([idx])[0]
            predictions.append({"class": class_name, "confidence": float(prob)})
        
        top_class = predictions[0]["class"]
        top_confidence = predictions[0]["confidence"]
        recommendation = self.recommendations.get(top_class, "Consult an agricultural expert.")
        
        return {
            "disease_class": top_class,
            "confidence": top_confidence,
            "top_3_predictions": predictions,
            "recommendations": recommendation
        }

ml_service = MLService()
