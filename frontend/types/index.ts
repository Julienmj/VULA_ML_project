export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface Detection {
  id: number;
  disease_class: string;
  confidence: number;
  top_3_predictions: Array<{ class: string; confidence: number }>;
  recommendations: string;
  created_at: string;
  image_path: string;
}

export interface DetectionHistory {
  detections: Detection[];
  total: number;
}

export interface Stats {
  total_detections: number;
  healthy_count: number;
  diseased_count: number;
  healthy_percentage: number;
  diseased_percentage: number;
  avg_confidence: number;
}

export interface DiseaseDistribution {
  disease: string;
  count: number;
}
