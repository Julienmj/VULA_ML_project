import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Mail, Lock, Eye, EyeOff, Loader2, ArrowRight, ShieldCheck, Leaf } from "lucide-react";
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

const registerSchema = z
  .object({
    email: z.string().trim().email("Invalid email address"),
    password: z.string().min(6, "Password must be at least 6 characters"),
    confirmPassword: z.string(),
    terms: z.boolean().refine((v) => v, "You must accept the terms"),
  })
  .refine((d) => d.password === d.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"],
  });

type RegisterForm = z.infer<typeof registerSchema>;

const getStrength = (pw: string) => {
  let s = 0;
  if (pw.length >= 8) s++;
  if (/[A-Z]/.test(pw)) s++;
  if (/[0-9]/.test(pw)) s++;
  if (/[^A-Za-z0-9]/.test(pw)) s++;
  return s;
};

const strengthColors = ["bg-destructive", "bg-destructive", "bg-warning", "bg-primary", "bg-success"];
const strengthLabels = ["", "Weak", "Fair", "Good", "Strong"];

const Register = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();
  const { setAuth } = useAuthStore();

  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
    defaultValues: { terms: false },
  });

  const password = watch("password", "");
  const strength = getStrength(password);

  const onSubmit = async (data: RegisterForm) => {
    setLoading(true);
    try {
      await new Promise((r) => setTimeout(r, 1200));
      setAuth(
        { id: "1", email: data.email, name: "Farmer", created_at: new Date().toISOString() },
        "demo_token_123"
      );
      toast({ title: "Account created!", description: "Welcome to VULA." });
      navigate("/dashboard");
    } catch {
      toast({ title: "Registration failed", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageTransition>
      <div className="relative flex min-h-screen gradient-bg-auth">
        {/* Left branding */}
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
              Start your journey to
              <span className="text-gradient"> smarter farming</span>
            </h2>
            <p className="mt-4 text-muted-foreground leading-relaxed">
              Free to start. No credit card required. Get instant AI-powered disease detection for your crops.
            </p>

            <div className="mt-8 space-y-4">
              {["Unlimited disease scans", "Real-time analytics dashboard", "Export reports & recommendations"].map((f) => (
                <div key={f} className="flex items-center gap-3">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary/10">
                    <ShieldCheck className="h-3.5 w-3.5 text-primary" />
                  </div>
                  <span className="text-sm text-foreground">{f}</span>
                </div>
              ))}
            </div>
          </div>

          <p className="relative z-10 text-xs text-muted-foreground">© 2026 VULA — AI Crop Intelligence</p>

          <div className="absolute -bottom-32 -right-32 h-96 w-96 rounded-full bg-primary/5 blur-3xl" />
          <div className="absolute -top-16 right-16 h-64 w-64 rounded-full bg-chart-4/5 blur-3xl" />
        </div>

        {/* Right form */}
        <div className="flex flex-1 flex-col items-center justify-center px-6 lg:px-16">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="w-full max-w-sm"
          >
            <Link to="/" className="mb-8 flex items-center gap-2.5 lg:hidden">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl gradient-primary shadow-lg shadow-primary/20">
                <Leaf className="h-5 w-5 text-primary-foreground" />
              </div>
              <span className="font-display text-xl font-bold tracking-tight text-foreground">VULA</span>
            </Link>

            <h1 className="font-display text-3xl font-bold text-foreground">Create account</h1>
            <p className="mt-2 text-muted-foreground">Start detecting crop diseases with AI</p>

            <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-4">
              <div>
                <label className="mb-1.5 block text-sm font-medium text-foreground">Email</label>
                <div className="input-glow relative rounded-xl">
                  <Mail className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input {...register("email")} type="email" placeholder="you@farm.com" className="h-12 rounded-xl pl-10 bg-muted/30 border-border/60 focus:bg-card" />
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
                    placeholder="Min 8 characters"
                    className="h-12 rounded-xl pl-10 pr-10 bg-muted/30 border-border/60 focus:bg-card"
                  />
                  <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors">
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {password.length > 0 && (
                  <div className="mt-2 flex items-center gap-2">
                    <div className="flex flex-1 gap-1">
                      {[1, 2, 3, 4].map((i) => (
                        <div key={i} className={`h-1 flex-1 rounded-full transition-colors ${i <= strength ? strengthColors[strength] : "bg-muted"}`} />
                      ))}
                    </div>
                    <span className="text-xs text-muted-foreground">{strengthLabels[strength]}</span>
                  </div>
                )}
                {errors.password && <p className="mt-1.5 text-xs text-destructive">{errors.password.message}</p>}
              </div>

              <div>
                <label className="mb-1.5 block text-sm font-medium text-foreground">Confirm Password</label>
                <div className="input-glow relative rounded-xl">
                  <ShieldCheck className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input {...register("confirmPassword")} type="password" placeholder="Re-enter password" className="h-12 rounded-xl pl-10 bg-muted/30 border-border/60 focus:bg-card" />
                </div>
                {errors.confirmPassword && <p className="mt-1.5 text-xs text-destructive">{errors.confirmPassword.message}</p>}
              </div>

              <div className="flex items-start gap-2 pt-1">
                <Checkbox id="terms" {...register("terms")} onCheckedChange={(checked) => setValue("terms", checked === true)} />
                <label htmlFor="terms" className="text-sm text-muted-foreground leading-tight">
                  I agree to the Terms of Service and Privacy Policy
                </label>
              </div>
              {errors.terms && <p className="text-xs text-destructive">{errors.terms.message}</p>}

              <Button type="submit" disabled={loading} className="w-full h-12 gradient-primary text-primary-foreground rounded-xl shadow-lg shadow-primary/25 hover:shadow-xl transition-all text-base">
                {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Creating account...</> : <>Create Account <ArrowRight className="ml-2 h-4 w-4" /></>}
              </Button>
            </form>

            <p className="mt-8 text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link to="/login" className="font-semibold text-primary hover:underline">Sign in</Link>
            </p>
          </motion.div>
        </div>
      </div>
    </PageTransition>
  );
};

export default Register;
