import { motion } from "framer-motion";
import { LucideIcon, TrendingUp, TrendingDown } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: number;
  variant?: "default" | "success" | "destructive" | "warning";
  subtitle?: string;
}

const iconGradients = {
  default: "from-primary to-emerald-light",
  success: "from-primary to-emerald-light",
  destructive: "from-destructive to-warning",
  warning: "from-warning to-chart-3",
};

const StatCard = ({ title, value, icon: Icon, trend, variant = "default", subtitle }: StatCardProps) => (
  <motion.div
    whileHover={{ y: -4, transition: { duration: 0.2 } }}
    className="stat-card-glow group rounded-2xl border border-border/50 bg-card p-6 shadow-sm transition-shadow hover:shadow-xl hover:shadow-primary/5"
  >
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <p className="mt-2 font-display text-3xl font-bold tracking-tight text-foreground">{value}</p>
        {trend !== undefined && (
          <div className={`mt-2 inline-flex items-center gap-1 rounded-lg px-2 py-0.5 text-xs font-semibold ${
            trend >= 0
              ? "bg-primary/10 text-primary"
              : "bg-destructive/10 text-destructive"
          }`}>
            {trend >= 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
            {trend >= 0 ? "+" : ""}{trend}%
          </div>
        )}
        {subtitle && <p className="mt-1 text-xs text-muted-foreground">{subtitle}</p>}
      </div>
      <div className={`flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br ${iconGradients[variant]} shadow-lg shadow-primary/10`}>
        <Icon className="h-5 w-5 text-primary-foreground" />
      </div>
    </div>
  </motion.div>
);

export default StatCard;
