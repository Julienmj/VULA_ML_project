import { useState } from "react";
import { motion } from "framer-motion";
import { Search, Grid3X3, List, Sprout, Calendar, ArrowUpRight } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import PageTransition from "@/components/shared/PageTransition";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const mockHistory = Array.from({ length: 12 }, (_, i) => ({
  id: String(i + 1),
  disease: ["Late Blight", "Healthy", "Powdery Mildew", "Leaf Spot", "Early Blight", "Healthy"][i % 6],
  confidence: Math.round(70 + Math.random() * 28),
  date: `${25 - i} Feb 2026`,
  status: i % 3 === 1 ? "healthy" : "diseased",
}));

const HistoryPage = () => {
  const [view, setView] = useState<"grid" | "list">("grid");
  const [search, setSearch] = useState("");

  const filtered = mockHistory.filter((d) =>
    d.disease.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <DashboardLayout>
      <PageTransition>
        <div className="space-y-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h1 className="font-display text-2xl font-bold text-foreground lg:text-3xl">
                Detection History
              </h1>
              <p className="mt-1 text-muted-foreground">{mockHistory.length} total detections this month</p>
            </div>
            <div className="flex items-center gap-2">
              <div className="input-glow relative flex-1 rounded-xl sm:w-64 sm:flex-initial">
                <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Search diseases..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="h-10 rounded-xl pl-10 bg-muted/30 border-border/60"
                />
              </div>
              <div className="flex rounded-xl border border-border/60 bg-card p-1">
                <button
                  onClick={() => setView("grid")}
                  className={`rounded-lg p-2 transition-all ${
                    view === "grid"
                      ? "gradient-primary text-primary-foreground shadow-sm"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Grid3X3 className="h-4 w-4" />
                </button>
                <button
                  onClick={() => setView("list")}
                  className={`rounded-lg p-2 transition-all ${
                    view === "list"
                      ? "gradient-primary text-primary-foreground shadow-sm"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <List className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>

          {filtered.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col items-center justify-center rounded-3xl border-2 border-dashed border-border/40 bg-card/30 p-20"
            >
              <div className="flex h-16 w-16 items-center justify-center rounded-3xl bg-muted/50">
                <Sprout className="h-8 w-8 text-muted-foreground/40" />
              </div>
              <p className="mt-5 font-display text-lg font-semibold text-foreground">
                No detections found
              </p>
              <p className="mt-1.5 text-sm text-muted-foreground">
                Start by analyzing your first crop image
              </p>
              <Button
                className="mt-5 gradient-primary text-primary-foreground rounded-xl shadow-lg shadow-primary/20"
                onClick={() => window.location.href = "/detect"}
              >
                Go to Detection <ArrowUpRight className="ml-1.5 h-3.5 w-3.5" />
              </Button>
            </motion.div>
          ) : view === "grid" ? (
            <motion.div
              initial="hidden"
              animate="show"
              variants={{ show: { transition: { staggerChildren: 0.04 } } }}
              className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
            >
              {filtered.map((d) => (
                <motion.div
                  key={d.id}
                  variants={{ hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0 } }}
                  whileHover={{ y: -4, transition: { duration: 0.2 } }}
                  className="group cursor-pointer rounded-2xl border border-border/50 bg-card p-5 shadow-sm transition-shadow hover:shadow-xl hover:shadow-primary/5"
                >
                  <div className="mb-4 flex h-36 items-center justify-center rounded-2xl bg-muted/30">
                    <Sprout className="h-10 w-10 text-muted-foreground/20 group-hover:text-primary/20 transition-colors" />
                  </div>
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-display font-semibold text-foreground">{d.disease}</h3>
                      <p className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
                        <Calendar className="h-3 w-3" /> {d.date}
                      </p>
                    </div>
                    <span
                      className={`rounded-lg px-2.5 py-1 text-xs font-semibold ${
                        d.status === "healthy"
                          ? "bg-primary/10 text-primary"
                          : "bg-destructive/10 text-destructive"
                      }`}
                    >
                      {d.confidence}%
                    </span>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          ) : (
            <div className="rounded-2xl border border-border/50 bg-card shadow-sm overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border/30 text-left text-xs font-medium uppercase tracking-wider text-muted-foreground">
                    <th className="px-6 py-3">Disease</th>
                    <th className="px-6 py-3">Confidence</th>
                    <th className="px-6 py-3">Date</th>
                    <th className="px-6 py-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((d) => (
                    <tr key={d.id} className="border-b border-border/20 last:border-0 hover:bg-muted/30 transition-colors">
                      <td className="px-6 py-4 text-sm font-medium text-foreground">{d.disease}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <div className="h-1.5 w-16 overflow-hidden rounded-full bg-muted">
                            <div className="h-full rounded-full bg-primary" style={{ width: `${d.confidence}%` }} />
                          </div>
                          <span className="text-sm text-foreground">{d.confidence}%</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-muted-foreground">{d.date}</td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex rounded-lg px-2.5 py-1 text-xs font-semibold ${
                          d.status === "healthy" ? "bg-primary/10 text-primary" : "bg-destructive/10 text-destructive"
                        }`}>
                          {d.status === "healthy" ? "Healthy" : "Diseased"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </PageTransition>
    </DashboardLayout>
  );
};

export default HistoryPage;
