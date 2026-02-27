import { motion } from "framer-motion";
import {
  BarChart3,
  Activity,
  Leaf,
  TrendingUp,
  Calendar,
  ArrowUpRight,
  Zap,
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell,
  PieChart,
  Pie,
} from "recharts";
import DashboardLayout from "@/components/layout/DashboardLayout";
import StatCard from "@/components/dashboard/StatCard";
import PageTransition from "@/components/shared/PageTransition";
import { useAuthStore } from "@/store/authStore";

const trendData = [
  { day: "Mon", scans: 18, healthy: 14, diseased: 4 },
  { day: "Tue", scans: 24, healthy: 18, diseased: 6 },
  { day: "Wed", scans: 12, healthy: 9, diseased: 3 },
  { day: "Thu", scans: 30, healthy: 22, diseased: 8 },
  { day: "Fri", scans: 22, healthy: 17, diseased: 5 },
  { day: "Sat", scans: 28, healthy: 20, diseased: 8 },
  { day: "Sun", scans: 32, healthy: 25, diseased: 7 },
];

const diseaseData = [
  { name: "Late Blight", count: 35, color: "hsl(0, 72%, 51%)" },
  { name: "Powdery Mildew", count: 25, color: "hsl(38, 92%, 50%)" },
  { name: "Leaf Spot", count: 20, color: "hsl(280, 65%, 60%)" },
  { name: "Early Blight", count: 12, color: "hsl(200, 70%, 50%)" },
  { name: "Healthy", count: 72, color: "hsl(158, 64%, 42%)" },
];

const pieData = [
  { name: "Healthy", value: 72, fill: "hsl(158, 64%, 42%)" },
  { name: "Diseased", value: 28, fill: "hsl(0, 72%, 51%)" },
];

const recentDetections = [
  { id: "1", disease: "Late Blight", confidence: 94, date: "2 hours ago", status: "diseased" },
  { id: "2", disease: "Healthy", confidence: 98, date: "5 hours ago", status: "healthy" },
  { id: "3", disease: "Powdery Mildew", confidence: 87, date: "1 day ago", status: "diseased" },
  { id: "4", disease: "Healthy", confidence: 96, date: "1 day ago", status: "healthy" },
  { id: "5", disease: "Leaf Spot", confidence: 79, date: "2 days ago", status: "diseased" },
];

const stagger = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};

const item = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] } },
};

const Dashboard = () => {
  const { user } = useAuthStore();

  return (
    <DashboardLayout>
      <PageTransition>
        <div className="space-y-8">
          {/* Header */}
          <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h1 className="font-display text-2xl font-bold text-foreground lg:text-3xl">
                Welcome back, {user?.name || "Farmer"} 👋
              </h1>
              <p className="mt-1 flex items-center gap-1.5 text-muted-foreground">
                <Calendar className="h-3.5 w-3.5" />
                {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
              </p>
            </div>
            <a
              href="/detect"
              className="inline-flex items-center gap-2 rounded-xl gradient-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow-lg shadow-primary/20 transition-all hover:shadow-xl"
            >
              <Zap className="h-4 w-4" /> New Scan
            </a>
          </div>

          {/* Stats */}
          <motion.div variants={stagger} initial="hidden" animate="show" className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <motion.div variants={item}>
              <StatCard title="Total Scans" value="1,284" icon={BarChart3} trend={12} subtitle="This month" />
            </motion.div>
            <motion.div variants={item}>
              <StatCard title="Healthy Crops" value="72%" icon={Leaf} trend={5} variant="success" subtitle="924 healthy" />
            </motion.div>
            <motion.div variants={item}>
              <StatCard title="Diseased Crops" value="28%" icon={Activity} trend={-3} variant="destructive" subtitle="360 affected" />
            </motion.div>
            <motion.div variants={item}>
              <StatCard title="Avg Confidence" value="91.4%" icon={TrendingUp} trend={2} variant="warning" subtitle="Above threshold" />
            </motion.div>
          </motion.div>

          {/* Charts Row */}
          <div className="grid gap-6 lg:grid-cols-7">
            {/* Area Chart */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="lg:col-span-4 rounded-2xl border border-border/50 bg-card p-6 shadow-sm"
            >
              <div className="mb-6 flex items-center justify-between">
                <div>
                  <h3 className="font-display text-lg font-semibold text-foreground">Detection Activity</h3>
                  <p className="text-sm text-muted-foreground">Scans over the past 7 days</p>
                </div>
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-primary" /> Healthy</span>
                  <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-destructive" /> Diseased</span>
                </div>
              </div>
              <ResponsiveContainer width="100%" height={260}>
                <AreaChart data={trendData}>
                  <defs>
                    <linearGradient id="gradHealthy" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="hsl(158, 64%, 42%)" stopOpacity={0.3} />
                      <stop offset="100%" stopColor="hsl(158, 64%, 42%)" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="gradDiseased" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="hsl(0, 72%, 51%)" stopOpacity={0.2} />
                      <stop offset="100%" stopColor="hsl(0, 72%, 51%)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(150 12% 89% / 0.5)" vertical={false} />
                  <XAxis dataKey="day" tick={{ fontSize: 12, fill: "hsl(200 8% 46%)" }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 12, fill: "hsl(200 8% 46%)" }} axisLine={false} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      background: "hsl(0 0% 100%)",
                      border: "1px solid hsl(150 12% 89%)",
                      borderRadius: "12px",
                      fontSize: "13px",
                      boxShadow: "0 8px 32px -8px rgba(0,0,0,0.12)",
                    }}
                  />
                  <Area type="monotone" dataKey="healthy" stroke="hsl(158, 64%, 42%)" strokeWidth={2.5} fill="url(#gradHealthy)" />
                  <Area type="monotone" dataKey="diseased" stroke="hsl(0, 72%, 51%)" strokeWidth={2} fill="url(#gradDiseased)" />
                </AreaChart>
              </ResponsiveContainer>
            </motion.div>

            {/* Donut + Disease breakdown */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="lg:col-span-3 rounded-2xl border border-border/50 bg-card p-6 shadow-sm"
            >
              <h3 className="font-display text-lg font-semibold text-foreground">Crop Health</h3>
              <p className="text-sm text-muted-foreground">Overall health ratio</p>

              <div className="my-6 flex justify-center">
                <ResponsiveContainer width={180} height={180}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={55}
                      outerRadius={80}
                      paddingAngle={4}
                      dataKey="value"
                      stroke="none"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={index} fill={entry.fill} />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="space-y-3">
                {diseaseData.slice(0, 4).map((d) => (
                  <div key={d.name} className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: d.color }} />
                      <span className="text-foreground">{d.name}</span>
                    </div>
                    <span className="font-medium text-muted-foreground">{d.count}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Disease Bar Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.45 }}
            className="rounded-2xl border border-border/50 bg-card p-6 shadow-sm"
          >
            <div className="mb-6">
              <h3 className="font-display text-lg font-semibold text-foreground">Disease Distribution</h3>
              <p className="text-sm text-muted-foreground">Cases by disease type this month</p>
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={diseaseData} layout="vertical" margin={{ left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(150 12% 89% / 0.5)" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 12, fill: "hsl(200 8% 46%)" }} axisLine={false} tickLine={false} />
                <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 12, fill: "hsl(200 8% 46%)" }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    background: "hsl(0 0% 100%)",
                    border: "1px solid hsl(150 12% 89%)",
                    borderRadius: "12px",
                    fontSize: "13px",
                    boxShadow: "0 8px 32px -8px rgba(0,0,0,0.12)",
                  }}
                />
                <Bar dataKey="count" radius={[0, 8, 8, 0]} barSize={24}>
                  {diseaseData.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Recent Detections */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="rounded-2xl border border-border/50 bg-card shadow-sm"
          >
            <div className="flex items-center justify-between border-b border-border/50 p-6">
              <div>
                <h3 className="font-display text-lg font-semibold text-foreground">Recent Detections</h3>
                <p className="text-sm text-muted-foreground">Latest scan results</p>
              </div>
              <a href="/history" className="flex items-center gap-1 text-sm font-medium text-primary hover:underline">
                View all <ArrowUpRight className="h-3.5 w-3.5" />
              </a>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border/30 text-left text-xs font-medium uppercase tracking-wider text-muted-foreground">
                    <th className="px-6 py-3">Disease</th>
                    <th className="px-6 py-3">Confidence</th>
                    <th className="px-6 py-3">Time</th>
                    <th className="px-6 py-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {recentDetections.map((d) => (
                    <tr key={d.id} className="border-b border-border/20 last:border-0 transition-colors hover:bg-muted/30">
                      <td className="px-6 py-4 text-sm font-medium text-foreground">{d.disease}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <div className="h-1.5 w-16 overflow-hidden rounded-full bg-muted">
                            <div
                              className="h-full rounded-full bg-primary transition-all"
                              style={{ width: `${d.confidence}%` }}
                            />
                          </div>
                          <span className="text-sm text-foreground">{d.confidence}%</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-muted-foreground">{d.date}</td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex items-center rounded-lg px-2.5 py-1 text-xs font-semibold ${
                            d.status === "healthy"
                              ? "bg-primary/10 text-primary"
                              : "bg-destructive/10 text-destructive"
                          }`}
                        >
                          {d.status === "healthy" ? "Healthy" : "Diseased"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>
        </div>
      </PageTransition>
    </DashboardLayout>
  );
};

export default Dashboard;
