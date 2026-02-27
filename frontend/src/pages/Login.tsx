import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Mail, Lock, Eye, EyeOff, Loader2, ArrowRight, Leaf } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { useToast } from "@/hooks/use-toast";
import { useAuthStore } from "@/store/authStore";
import { authAPI } from "@/lib/api";
import PageTransition from "@/components/shared/PageTransition";

const loginSchema = z.object({
  email: z.string().trim().email("Invalid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

type LoginForm = z.infer<typeof loginSchema>;

const Login = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();
  const { setAuth } = useAuthStore();

  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginForm) => {
    setLoading(true);
    try {
      await new Promise((r) => setTimeout(r, 1200));
      setAuth(
        { id: "1", email: data.email, name: "Farmer", created_at: new Date().toISOString() },
        "demo_token_123"
      );
      toast({ title: "Welcome back!", description: "Redirecting to dashboard..." });
      navigate("/dashboard");
    } catch {
      toast({ title: "Login failed", description: "Please check your credentials.", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageTransition>
      <div className="relative flex min-h-screen gradient-bg-auth">
        {/* Left: Branding panel */}
        <div className="hidden lg:flex lg:w-1/2 flex-col justify-between p-12 relative overflow-hidden">
          <div className="relative z-10">
            <Link to="/" className="flex items-center gap-2.5">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl gradient-primary shadow-lg shadow-primary/20">
                <Leaf className="h-5 w-5 text-primary-foreground" />
              </div>
              <span className="font-display text-xl font-bold tracking-tight text-foreground">VULA</span>
            </Link>
          </div>

          <div className="relative z-10 max-w-md">
            <h2 className="font-display text-4xl font-bold leading-tight text-foreground">
              Protect your crops with
              <span className="text-gradient"> AI intelligence</span>
            </h2>
            <p className="mt-4 text-muted-foreground leading-relaxed">
              Join 12,000+ farmers using VULA to detect diseases early, reduce crop loss by 40%, and make data-driven farming decisions.
            </p>

            <div className="mt-8 flex gap-8">
              {[
                { val: "98.6%", label: "Accuracy" },
                { val: "<3s", label: "Detection" },
                { val: "40%", label: "Less Loss" },
              ].map((s) => (
                <div key={s.label}>
                  <p className="font-display text-2xl font-bold text-foreground">{s.val}</p>
                  <p className="text-xs text-muted-foreground">{s.label}</p>
                </div>
              ))}
            </div>
          </div>

          <p className="relative z-10 text-xs text-muted-foreground">
            © 2026 VULA — AI Crop Intelligence
          </p>

          {/* Decorative circles */}
          <div className="absolute -bottom-32 -right-32 h-96 w-96 rounded-full bg-primary/5 blur-3xl" />
          <div className="absolute -top-16 right-16 h-64 w-64 rounded-full bg-chart-2/5 blur-3xl" />
        </div>

        {/* Right: Form */}
        <div className="flex flex-1 flex-col items-center justify-center px-6 lg:px-16">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="w-full max-w-sm"
          >
            {/* Mobile logo */}
            <Link to="/" className="mb-8 flex items-center gap-2.5 lg:hidden">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl gradient-primary shadow-lg shadow-primary/20">
                <Leaf className="h-5 w-5 text-primary-foreground" />
              </div>
              <span className="font-display text-xl font-bold tracking-tight text-foreground">VULA</span>
            </Link>

            <h1 className="font-display text-3xl font-bold text-foreground">Welcome back</h1>
            <p className="mt-2 text-muted-foreground">Enter your credentials to access your dashboard</p>

            <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-5">
              <div>
                <label className="mb-1.5 block text-sm font-medium text-foreground">Email</label>
                <div className="input-glow relative rounded-xl">
                  <Mail className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    {...register("email")}
                    type="email"
                    placeholder="you@farm.com"
                    className="h-12 rounded-xl pl-10 bg-muted/30 border-border/60 focus:bg-card"
                  />
                </div>
                {errors.email && <p className="mt-1.5 text-xs text-destructive">{errors.email.message}</p>}
              </div>

              <div>
                <label className="mb-1.5 block text-sm font-medium text-foreground">Password</label>
                <div className="input-glow relative rounded-xl">
                  <Lock className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    {...register("password")}
                    type={showPassword ? "text" : "password"}
                    placeholder="••••••••"
                    className="h-12 rounded-xl pl-10 pr-10 bg-muted/30 border-border/60 focus:bg-card"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {errors.password && <p className="mt-1.5 text-xs text-destructive">{errors.password.message}</p>}
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Checkbox id="remember" />
                  <label htmlFor="remember" className="text-sm text-muted-foreground">Remember me</label>
                </div>
                <button type="button" className="text-sm font-medium text-primary hover:underline">
                  Forgot password?
                </button>
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full h-12 gradient-primary text-primary-foreground rounded-xl shadow-lg shadow-primary/25 hover:shadow-xl transition-all text-base"
              >
                {loading ? (
                  <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Signing in...</>
                ) : (
                  <>Sign In <ArrowRight className="ml-2 h-4 w-4" /></>
                )}
              </Button>
            </form>

            <p className="mt-8 text-center text-sm text-muted-foreground">
              Don't have an account?{" "}
              <Link to="/register" className="font-semibold text-primary hover:underline">
                Create account
              </Link>
            </p>
          </motion.div>
        </div>
      </div>
    </PageTransition>
  );
};

export default Login;
