import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  BarChart3,
  Search,
  History,
  Settings,
  LogOut,
  Menu,
  X,
  ChevronLeft,
  Leaf,
} from "lucide-react";
import VulaLogo from "@/components/shared/VulaLogo";
import { useAuthStore } from "@/store/authStore";

const navItems = [
  { title: "Dashboard", url: "/dashboard", icon: BarChart3 },
  { title: "Detect Disease", url: "/detect", icon: Search },
  { title: "History", url: "/history", icon: History },
  { title: "Settings", url: "/settings", icon: Settings },
];

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const SidebarContent = () => (
    <div className="flex h-screen flex-col">
      <div className="flex items-center justify-between p-5">
        <VulaLogo collapsed={collapsed} />
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="hidden rounded-xl p-1.5 text-sidebar-foreground/50 hover:bg-sidebar-accent hover:text-sidebar-foreground lg:block transition-colors"
        >
          <ChevronLeft className={`h-4 w-4 transition-transform duration-300 ${collapsed ? "rotate-180" : ""}`} />
        </button>
      </div>

      <nav className="mt-6 flex-1 space-y-1 px-3 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = location.pathname === item.url;
          return (
            <Link
              key={item.url}
              to={item.url}
              onClick={() => setMobileOpen(false)}
              className={`group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200 ${
                isActive
                  ? "bg-sidebar-primary text-sidebar-primary-foreground shadow-lg shadow-sidebar-primary/20"
                  : "text-sidebar-foreground/60 hover:bg-sidebar-accent hover:text-sidebar-foreground"
              }`}
            >
              <item.icon className="h-[18px] w-[18px] shrink-0" />
              {!collapsed && <span>{item.title}</span>}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-sidebar-border p-4">
        <div className={`flex items-center ${collapsed ? 'justify-center' : 'gap-3'}`}>
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl gradient-primary text-sm font-bold text-primary-foreground shadow-sm">
            {user?.email?.[0]?.toUpperCase() || "U"}
          </div>
          {!collapsed && (
            <>
              <div className="flex-1 truncate">
                <p className="truncate text-sm font-medium text-sidebar-foreground">
                  {user?.email || "user@vula.com"}
                </p>
                <p className="truncate text-xs text-sidebar-foreground/40">Free plan</p>
              </div>
              <button
                onClick={handleLogout}
                className="rounded-xl p-1.5 text-sidebar-foreground/40 hover:bg-sidebar-accent hover:text-destructive transition-colors"
                title="Logout"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex min-h-screen bg-background">
      {/* Desktop sidebar */}
      <aside
        className={`hidden border-r border-sidebar-border bg-sidebar transition-all duration-300 lg:block ${
          collapsed ? "w-[72px]" : "w-64"
        }`}
      >
        <SidebarContent />
      </aside>

      {/* Mobile overlay */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-40 bg-foreground/40 backdrop-blur-sm lg:hidden"
              onClick={() => setMobileOpen(false)}
            />
            <motion.aside
              initial={{ x: -280 }}
              animate={{ x: 0 }}
              exit={{ x: -280 }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="fixed inset-y-0 left-0 z-50 w-64 bg-sidebar lg:hidden"
            >
              <SidebarContent />
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* Main content */}
      <div className="flex flex-1 flex-col">
        <header className="flex h-16 items-center gap-4 border-b border-border bg-card/50 px-6 backdrop-blur-sm lg:hidden">
          <button onClick={() => setMobileOpen(true)} className="rounded-xl p-2 text-foreground hover:bg-muted">
            <Menu className="h-5 w-5" />
          </button>
          <VulaLogo />
        </header>
        <main className="flex-1 overflow-auto gradient-bg">
          <div className="p-6 lg:p-8">{children}</div>
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
