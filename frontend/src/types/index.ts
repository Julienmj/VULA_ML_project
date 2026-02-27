export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface Detection {
  id: string;
  disease: string;
  confidence: number;
  top3: Array<{ class: string; confidence: number }>;
  recommendations: string;
  image_url: string;
  created_at: string;
  user_id: string;
}

export interface DetectionHistory {
  detections: Detection[];
  total: number;
}

export interface DashboardStats {
  total_scans: number;
  healthy_percentage: number;
  diseased_percentage: number;
  avg_confidence: number;
}

export interface DiseaseDistribution {
  labels: string[];
  data: number[];
}

export interface DetectionTrend {
  labels: string[];
  data: number[];
}
