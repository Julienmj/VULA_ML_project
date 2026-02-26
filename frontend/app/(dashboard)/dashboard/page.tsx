'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, CheckCircle, AlertCircle, TrendingUp } from 'lucide-react';
import { Card } from '@/components/ui/card';
import api from '@/lib/api/client';
import { Stats, DiseaseDistribution } from '@/types';

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [distribution, setDistribution] = useState<DiseaseDistribution[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, distRes] = await Promise.all([
          api.get<Stats>('/analytics/stats'),
          api.get<DiseaseDistribution[]>('/analytics/disease-distribution'),
        ]);
        setStats(statsRes.data);
        setDistribution(distRes.data);
      } catch (error) {
        console.error('Failed to fetch dashboard data', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const statCards = [
    {
      title: 'Total Scans',
      value: stats?.total_detections || 0,
      icon: Activity,
      color: 'text-blue-600',
      bg: 'bg-blue-50',
    },
    {
      title: 'Healthy Crops',
      value: `${stats?.healthy_percentage || 0}%`,
      icon: CheckCircle,
      color: 'text-green-600',
      bg: 'bg-green-50',
    },
    {
      title: 'Diseased Crops',
      value: `${stats?.diseased_percentage || 0}%`,
      icon: AlertCircle,
      color: 'text-red-600',
      bg: 'bg-red-50',
    },
    {
      title: 'Avg Confidence',
      value: `${stats?.avg_confidence || 0}%`,
      icon: TrendingUp,
      color: 'text-purple-600',
      bg: 'bg-purple-50',
    },
  ];

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
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Welcome back! Here's your overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.title}</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                </div>
                <div className={`${stat.bg} p-3 rounded-full`}>
                  <stat.icon className={`w-6 h-6 ${stat.color}`} />
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Disease Distribution */}
      <Card className="p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Disease Distribution</h2>
        <div className="space-y-3">
          {distribution.slice(0, 5).map((item) => (
            <div key={item.disease} className="flex items-center justify-between">
              <span className="text-sm text-gray-700">{item.disease}</span>
              <div className="flex items-center gap-3">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gradient-green h-2 rounded-full"
                    style={{ width: `${(item.count / stats!.total_detections) * 100}%` }}
                  />
                </div>
                <span className="text-sm font-medium text-gray-900 w-8">{item.count}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
