import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, X, Loader2, CheckCircle, AlertTriangle, Sprout, ArrowRight, Camera, FileImage } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import PageTransition from "@/components/shared/PageTransition";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { detectionAPI } from "@/lib/api";

interface DetectionResult {
  disease: string;
  confidence: number;
  top3: Array<{ class: string; confidence: number }>;
  recommendations: string[];
}

const mockResult: DetectionResult = {
  disease: "Late Blight",
  confidence: 94.2,
  top3: [
    { class: "Late Blight", confidence: 94.2 },
    { class: "Early Blight", confidence: 3.8 },
    { class: "Healthy", confidence: 2.0 },
  ],
  recommendations: [
    "Remove and destroy affected plant parts immediately",
    "Apply copper-based fungicide as a preventive measure",
    "Ensure adequate spacing between plants for air circulation",
    "Water at the base of plants to keep foliage dry",
  ],
};

const Detect = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<DetectionResult | null>(null);
  const { toast } = useToast();

  const handleFile = useCallback((f: File) => {
    if (!f.type.startsWith("image/")) {
      toast({ title: "Invalid file type", description: "Please upload a JPG or PNG image.", variant: "destructive" });
      return;
    }
    if (f.size > 5 * 1024 * 1024) {
      toast({ title: "File too large", description: "Maximum file size is 5MB.", variant: "destructive" });
      return;
    }
    setFile(f);
    setResult(null);
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target?.result as string);
    reader.readAsDataURL(f);
  }, [toast]);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      const f = e.dataTransfer.files[0];
      if (f) handleFile(f);
    },
    [handleFile]
  );

  const analyze = async () => {
    setAnalyzing(true);
    setProgress(0);
    const interval = setInterval(() => {
      setProgress((p) => {
        if (p >= 95) { clearInterval(interval); return 95; }
        return p + Math.random() * 15;
      });
    }, 200);
    await new Promise((r) => setTimeout(r, 2500));
    clearInterval(interval);
    setProgress(100);
    await new Promise((r) => setTimeout(r, 300));
    setResult(mockResult);
    setAnalyzing(false);
  };

  const reset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setProgress(0);
  };

  const confColor = (c: number) =>
    c >= 80 ? "text-primary" : c >= 60 ? "text-warning" : "text-destructive";

  const confBg = (c: number) =>
    c >= 80 ? "bg-primary" : c >= 60 ? "bg-warning" : "bg-destructive";

  return (
    <DashboardLayout>
      <PageTransition>
        <div className="mx-auto max-w-3xl space-y-8">
          <div>
            <h1 className="font-display text-2xl font-bold text-foreground lg:text-3xl">
              AI Disease Detection
            </h1>
            <p className="mt-2 text-muted-foreground">
              Upload a photo of your crop leaf for instant AI-powered analysis
            </p>
          </div>

          {/* Upload zone */}
          {!preview && (
            <motion.div
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              className="group cursor-pointer rounded-3xl border-2 border-dashed border-border/60 bg-card/50 p-16 text-center transition-all hover:border-primary/40 hover:bg-card/80"
              onClick={() => document.getElementById("file-input")?.click()}
            >
              <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-primary/8 transition-colors group-hover:bg-primary/12">
                <Camera className="h-9 w-9 text-primary/60 transition-colors group-hover:text-primary" />
              </div>
              <p className="font-display text-lg font-semibold text-foreground">
                Drop your crop image here
              </p>
              <p className="mt-2 text-sm text-muted-foreground">
                or click to browse • JPG, PNG up to 5MB
              </p>
              <div className="mt-6 inline-flex items-center gap-2 rounded-xl bg-muted/50 px-4 py-2 text-xs text-muted-foreground">
                <FileImage className="h-3.5 w-3.5" />
                Supports 38+ disease categories
              </div>
              <input
                id="file-input"
                type="file"
                accept="image/jpeg,image/png"
                className="hidden"
                onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
              />
            </motion.div>
          )}

          {/* Preview */}
          <AnimatePresence>
            {preview && !result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <div className="relative overflow-hidden rounded-3xl border border-border/50 bg-card shadow-sm">
                  <button
                    onClick={reset}
                    className="absolute right-4 top-4 z-10 rounded-xl bg-foreground/60 p-2 text-background hover:bg-foreground/80 transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                  <img src={preview} alt="Crop preview" className="w-full object-contain max-h-96" />
                </div>

                {analyzing && (
                  <div className="rounded-2xl border border-border/50 bg-card p-6 shadow-sm">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="relative">
                        <Loader2 className="h-5 w-5 animate-spin text-primary" />
                        <div className="absolute inset-0 animate-pulse-ring rounded-full border-2 border-primary/30" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-foreground">Analyzing image...</p>
                        <p className="text-xs text-muted-foreground">Running through 38 disease models</p>
                      </div>
                    </div>
                    <div className="h-2 overflow-hidden rounded-full bg-muted">
                      <motion.div
                        className="h-full rounded-full gradient-primary"
                        animate={{ width: `${progress}%` }}
                        transition={{ duration: 0.3 }}
                      />
                    </div>
                  </div>
                )}

                {!analyzing && !result && (
                  <Button
                    onClick={analyze}
                    className="w-full h-14 gradient-primary text-primary-foreground rounded-2xl shadow-xl shadow-primary/20 hover:shadow-2xl transition-all text-base font-semibold"
                    size="lg"
                  >
                    <Sprout className="mr-2 h-5 w-5" /> Analyze Image <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                )}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Results */}
          <AnimatePresence>
            {result && (
              <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="space-y-5">
                {preview && (
                  <div className="overflow-hidden rounded-3xl border border-border/50 bg-card shadow-sm">
                    <img src={preview} alt="Analyzed crop" className="w-full object-contain max-h-56" />
                  </div>
                )}

                {/* Main result */}
                <div className="rounded-3xl border border-border/50 bg-card p-6 shadow-sm">
                  <div className="flex items-start gap-4">
                    <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-destructive/10">
                      <AlertTriangle className="h-7 w-7 text-destructive" />
                    </div>
                    <div className="flex-1">
                      <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Detected Disease</p>
                      <h2 className="mt-1 font-display text-2xl font-bold text-foreground">{result.disease}</h2>
                    </div>
                    <div className="text-right">
                      <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Confidence</p>
                      <p className={`mt-1 font-display text-3xl font-bold ${confColor(result.confidence)}`}>
                        {result.confidence.toFixed(1)}%
                      </p>
                    </div>
                  </div>
                </div>

                {/* Top predictions */}
                <div className="rounded-3xl border border-border/50 bg-card p-6 shadow-sm">
                  <h3 className="font-display text-base font-semibold text-foreground mb-4">All Predictions</h3>
                  <div className="space-y-4">
                    {result.top3.map((p, i) => (
                      <div key={i} className="flex items-center gap-4">
                        <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-muted text-xs font-bold text-muted-foreground">
                          {i + 1}
                        </span>
                        <div className="flex-1">
                          <div className="flex justify-between text-sm mb-1.5">
                            <span className="font-medium text-foreground">{p.class}</span>
                            <span className={`font-semibold ${confColor(p.confidence)}`}>{p.confidence.toFixed(1)}%</span>
                          </div>
                          <div className="h-2 rounded-full bg-muted overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${p.confidence}%` }}
                              transition={{ duration: 0.8, delay: i * 0.15, ease: [0.22, 1, 0.36, 1] }}
                              className={`h-full rounded-full ${confBg(p.confidence)}`}
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Recommendations */}
                <div className="rounded-3xl border border-border/50 bg-card p-6 shadow-sm">
                  <h3 className="font-display text-base font-semibold text-foreground flex items-center gap-2 mb-4">
                    <CheckCircle className="h-5 w-5 text-primary" /> Treatment Plan
                  </h3>
                  <div className="space-y-3">
                    {result.recommendations.map((r, i) => (
                      <div key={i} className="flex items-start gap-3 rounded-xl bg-muted/30 p-3">
                        <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg gradient-primary text-xs font-bold text-primary-foreground">
                          {i + 1}
                        </span>
                        <p className="text-sm text-foreground leading-relaxed">{r}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex gap-3">
                  <Button className="flex-1 h-12 gradient-primary text-primary-foreground rounded-xl shadow-lg shadow-primary/20 hover:shadow-xl transition-all" size="lg">
                    Save Report
                  </Button>
                  <Button onClick={reset} variant="outline" className="flex-1 h-12 rounded-xl border-border/60" size="lg">
                    Analyze Another
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </PageTransition>
    </DashboardLayout>
  );
};

export default Detect;
