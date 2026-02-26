'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, Loader2, CheckCircle, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import api from '@/lib/api/client';
import { Detection } from '@/types';
import Image from 'next/image';

export default function DetectPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Detection | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const { data } = await api.post<Detection>('/detect', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(data);
    } catch (error) {
      console.error('Analysis failed', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 80) return 'text-green-600';
    if (confidence > 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Detect Disease</h1>
        <p className="text-gray-600 mt-1">Upload a crop image for AI-powered analysis</p>
      </div>

      {/* Upload Section */}
      {!result && (
        <Card className="p-8">
          <div className="space-y-6">
            <div
              className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-primary-500 transition-colors cursor-pointer"
              onClick={() => document.getElementById('file-input')?.click()}
            >
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-2">Click to upload or drag image here</p>
              <p className="text-sm text-gray-400">JPG, PNG (max 5MB)</p>
              <input
                id="file-input"
                type="file"
                accept="image/jpeg,image/png,image/jpg"
                onChange={handleFileChange}
                className="hidden"
              />
            </div>

            {preview && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="relative w-full h-64 rounded-lg overflow-hidden"
              >
                <Image src={preview} alt="Preview" fill className="object-contain" />
              </motion.div>
            )}

            <Button
              onClick={handleAnalyze}
              disabled={!file || loading}
              className="w-full bg-gradient-green hover:opacity-90"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing...
                </>
              ) : (
                'Analyze Image'
              )}
            </Button>
          </div>
        </Card>
      )}

      {/* Results Section */}
      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <Card className="p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Analysis Results</h2>
              <Button onClick={handleReset} variant="outline">
                Analyze Another
              </Button>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              <div className="relative h-64 rounded-lg overflow-hidden">
                <Image src={preview!} alt="Analyzed" fill className="object-contain" />
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Disease Detected</h3>
                  <p className="text-2xl font-bold text-primary-600">{result.disease_class}</p>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">Confidence</span>
                    <span className={`text-lg font-bold ${getConfidenceColor(result.confidence * 100)}`}>
                      {(result.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <Progress value={result.confidence * 100} className="h-2" />
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-gray-900 mb-2">Top 3 Predictions</h4>
                  <div className="space-y-2">
                    {result.top_3_predictions.map((pred, idx) => (
                      <div key={idx} className="flex items-center justify-between text-sm">
                        <span className="text-gray-700">{pred.class}</span>
                        <span className="font-medium">{(pred.confidence * 100).toFixed(1)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-8 p-6 bg-primary-50 rounded-lg">
              <div className="flex items-start gap-3">
                {result.confidence > 0.8 ? (
                  <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                ) : (
                  <AlertTriangle className="w-6 h-6 text-yellow-600 flex-shrink-0 mt-1" />
                )}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Recommendations</h4>
                  <p className="text-gray-700">{result.recommendations}</p>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
