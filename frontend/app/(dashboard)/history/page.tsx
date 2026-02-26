'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import api from '@/lib/api/client';
import { DetectionHistory } from '@/types';

export default function HistoryPage() {
  const [history, setHistory] = useState<DetectionHistory | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const { data } = await api.get<DetectionHistory>('/detect/history?skip=0&limit=20');
        setHistory(data);
      } catch (error) {
        console.error('Failed to fetch history', error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const getConfidenceBadge = (confidence: number) => {
    if (confidence > 0.8) return <Badge className="bg-green-500">High</Badge>;
    if (confidence > 0.6) return <Badge className="bg-yellow-500">Medium</Badge>;
    return <Badge className="bg-red-500">Low</Badge>;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Detection History</h1>
        <p className="text-gray-600 mt-1">View all your past disease detections</p>
      </div>

      {history?.detections.length === 0 ? (
        <Card className="p-12 text-center">
          <p className="text-gray-500">No detections yet. Start by analyzing your first crop image!</p>
        </Card>
      ) : (
        <div className="grid gap-6">
          {history?.detections.map((detection, index) => (
            <motion.div
              key={detection.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card className="p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">{detection.disease_class}</h3>
                      {getConfidenceBadge(detection.confidence)}
                    </div>
                    <p className="text-sm text-gray-600">
                      Confidence: {(detection.confidence * 100).toFixed(1)}%
                    </p>
                    <p className="text-sm text-gray-500 mt-1">
                      {format(new Date(detection.created_at), 'PPpp')}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">Top Predictions:</p>
                    <div className="text-xs text-gray-600 mt-1 space-y-1">
                      {detection.top_3_predictions.slice(0, 3).map((pred, idx) => (
                        <div key={idx}>
                          {pred.class}: {(pred.confidence * 100).toFixed(0)}%
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
