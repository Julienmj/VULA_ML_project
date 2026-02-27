import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Leaf, ArrowRight, Shield, Zap, BarChart3, Sparkles, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/store/authStore";

const features = [
  { icon: Zap, title: "Instant Detection", desc: "Upload a photo and get results in under 3 seconds with our cutting-edge AI model.", color: "from-primary to-emerald-light" },
  { icon: Shield, title: "98.6% Accuracy", desc: "Trained on 50M+ crop images across 38 disease categories for clinical-grade reliability.", color: "from-chart-2 to-primary" },
  { icon: BarChart3, title: "Smart Analytics", desc: "Track disease patterns, seasonal trends, and farm health with actionable intelligence.", color: "from-chart-4 to-chart-2" },
];

const stats = [
  { value: "50M+", label: "Images Analyzed" },
  { value: "38", label: "Disease Types" },
  { value: "98.6%", label: "Accuracy Rate" },
  { value: "12K+", label: "Active Farmers" },
];

const Index = () => {
  const { isAuthenticated, loadFromStorage } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => { loadFromStorage(); }, [loadFromStorage]);
  useEffect(() => { if (isAuthenticated) navigate("/dashboard"); }, [isAuthenticated, navigate]);

  return (
    <div className="min-h-screen gradient-bg-auth overflow-hidden">
      {/* Nav */}
      <nav className="relative z-10 flex items-center justify-between px-6 py-5 lg:px-16">
        <div className="flex items-center gap-2.5">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl gradient-primary shadow-lg shadow-primary/20">
            <Leaf className="h-5 w-5 text-primary-foreground" />
          </div>
          <span className="font-display text-xl font-bold tracking-tight text-foreground">VULA</span>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="ghost" onClick={() => navigate("/login")} className="text-muted-foreground hover:text-foreground">
            Sign In
          </Button>
          <Button onClick={() => navigate("/register")} className="gradient-primary text-primary-foreground rounded-xl px-6 shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/30 transition-all">
            Get Started <ArrowRight className="ml-1.5 h-4 w-4" />
          </Button>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative mx-auto max-w-6xl px-6 pt-16 pb-24 lg:pt-28">
        <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }} className="text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-2 text-sm font-medium text-primary backdrop-blur-sm"
          >
            <Sparkles className="h-3.5 w-3.5" />
            AI-Powered Crop Intelligence
            <ChevronRight className="h-3.5 w-3.5" />
          </motion.div>

          <h1 className="mt-8 font-display text-5xl font-extrabold leading-[1.1] text-foreground sm:text-6xl lg:text-7xl">
            Detect Diseases
            <br />
            <span className="text-gradient">Before They Spread</span>
          </h1>

          <p className="mx-auto mt-6 max-w-xl text-lg leading-relaxed text-muted-foreground">
            VULA uses deep learning to identify 38+ crop diseases from a single photo. 
            Protect your harvest, reduce chemical use, and farm smarter.
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Button
              onClick={() => navigate("/register")}
              size="lg"
              className="gradient-primary text-primary-foreground rounded-xl px-8 py-6 text-base shadow-xl shadow-primary/25 hover:shadow-2xl hover:shadow-primary/35 transition-all"
            >
              Start Free Trial <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button onClick={() => navigate("/login")} size="lg" variant="outline" className="rounded-xl px-8 py-6 text-base border-border/60">
              Sign In
            </Button>
          </div>
        </motion.div>

        {/* Stats bar */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
          className="mx-auto mt-20 grid max-w-3xl grid-cols-2 gap-1 rounded-3xl border border-border/50 bg-card/60 p-2 backdrop-blur-xl sm:grid-cols-4"
        >
          {stats.map((s, i) => (
            <div key={i} className="flex flex-col items-center rounded-2xl py-6 transition-colors hover:bg-muted/50">
              <span className="font-display text-2xl font-bold text-foreground">{s.value}</span>
              <span className="mt-1 text-xs font-medium text-muted-foreground">{s.label}</span>
            </div>
          ))}
        </motion.div>

        {/* Features */}
        <motion.div
          initial="hidden"
          animate="show"
          variants={{ show: { transition: { staggerChildren: 0.12, delayChildren: 0.7 } } }}
          className="mt-24 grid gap-6 sm:grid-cols-3"
        >
          {features.map((f) => (
            <motion.div
              key={f.title}
              variants={{ hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0 } }}
              whileHover={{ y: -6, transition: { duration: 0.2 } }}
              className="group relative rounded-3xl border border-border/50 bg-card/60 p-8 backdrop-blur-sm transition-shadow hover:shadow-2xl hover:shadow-primary/5"
            >
              <div className={`mb-5 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br ${f.color} shadow-lg`}>
                <f.icon className="h-6 w-6 text-primary-foreground" />
              </div>
              <h3 className="font-display text-xl font-semibold text-foreground">{f.title}</h3>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{f.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/40 py-8 text-center text-sm text-muted-foreground">
        © 2026 VULA. AI-powered crop disease detection for modern agriculture.
      </footer>
    </div>
  );
};

export default Index;
