import { useState } from "react";
import { motion } from "framer-motion";
import { User, Mail, Lock, Bell, Trash2, Save } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import PageTransition from "@/components/shared/PageTransition";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { useAuthStore } from "@/store/authStore";
import { useToast } from "@/hooks/use-toast";

const Settings = () => {
  const { user } = useAuthStore();
  const { toast } = useToast();
  const [name, setName] = useState(user?.name || "");
  const [email, setEmail] = useState(user?.email || "");
  const [notifications, setNotifications] = useState(true);
  const [emailAlerts, setEmailAlerts] = useState(false);

  const handleSaveProfile = () => {
    toast({ title: "Profile updated", description: "Your changes have been saved successfully." });
  };

  const handleChangePassword = () => {
    toast({ title: "Password changed", description: "Your password has been updated." });
  };

  const handleDeleteAccount = () => {
    toast({ title: "Account deleted", description: "Your account has been permanently deleted.", variant: "destructive" });
  };

  return (
    <DashboardLayout>
      <PageTransition>
        <div className="mx-auto max-w-3xl space-y-8">
          <div>
            <h1 className="font-display text-2xl font-bold text-foreground lg:text-3xl">Settings</h1>
            <p className="mt-2 text-muted-foreground">Manage your account and preferences</p>
          </div>

          {/* Profile */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl border border-border/50 bg-card p-6 shadow-sm"
          >
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl gradient-primary text-primary-foreground">
                <User className="h-5 w-5" />
              </div>
              <div>
                <h2 className="font-display text-lg font-semibold text-foreground">Profile Information</h2>
                <p className="text-sm text-muted-foreground">Update your personal details</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <Label htmlFor="name">Name</Label>
                <Input id="name" value={name} onChange={(e) => setName(e.target.value)} className="mt-1.5" />
              </div>
              <div>
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="mt-1.5" />
              </div>
              <Button onClick={handleSaveProfile} className="gradient-primary text-primary-foreground">
                <Save className="mr-2 h-4 w-4" /> Save Changes
              </Button>
            </div>
          </motion.div>

          {/* Password */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="rounded-2xl border border-border/50 bg-card p-6 shadow-sm"
          >
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-warning/10 text-warning">
                <Lock className="h-5 w-5" />
              </div>
              <div>
                <h2 className="font-display text-lg font-semibold text-foreground">Change Password</h2>
                <p className="text-sm text-muted-foreground">Update your password regularly</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <Label htmlFor="current">Current Password</Label>
                <Input id="current" type="password" className="mt-1.5" />
              </div>
              <div>
                <Label htmlFor="new">New Password</Label>
                <Input id="new" type="password" className="mt-1.5" />
              </div>
              <div>
                <Label htmlFor="confirm">Confirm Password</Label>
                <Input id="confirm" type="password" className="mt-1.5" />
              </div>
              <Button onClick={handleChangePassword} variant="outline">
                <Lock className="mr-2 h-4 w-4" /> Update Password
              </Button>
            </div>
          </motion.div>

          {/* Notifications */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="rounded-2xl border border-border/50 bg-card p-6 shadow-sm"
          >
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
                <Bell className="h-5 w-5" />
              </div>
              <div>
                <h2 className="font-display text-lg font-semibold text-foreground">Notifications</h2>
                <p className="text-sm text-muted-foreground">Manage your notification preferences</p>
              </div>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between rounded-xl bg-muted/30 p-4">
                <div>
                  <p className="font-medium text-foreground">Push Notifications</p>
                  <p className="text-sm text-muted-foreground">Receive alerts for new detections</p>
                </div>
                <Switch checked={notifications} onCheckedChange={setNotifications} />
              </div>
              <div className="flex items-center justify-between rounded-xl bg-muted/30 p-4">
                <div>
                  <p className="font-medium text-foreground">Email Alerts</p>
                  <p className="text-sm text-muted-foreground">Get weekly summary reports</p>
                </div>
                <Switch checked={emailAlerts} onCheckedChange={setEmailAlerts} />
              </div>
            </div>
          </motion.div>

          {/* Danger Zone */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="rounded-2xl border border-destructive/30 bg-destructive/5 p-6 shadow-sm"
          >
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-destructive/10 text-destructive">
                <Trash2 className="h-5 w-5" />
              </div>
              <div>
                <h2 className="font-display text-lg font-semibold text-foreground">Danger Zone</h2>
                <p className="text-sm text-muted-foreground">Irreversible actions</p>
              </div>
            </div>
            <div className="rounded-xl bg-card p-4">
              <p className="mb-3 text-sm text-foreground">
                Once you delete your account, all your data will be permanently removed. This action cannot be undone.
              </p>
              <Button onClick={handleDeleteAccount} variant="destructive">
                <Trash2 className="mr-2 h-4 w-4" /> Delete Account
              </Button>
            </div>
          </motion.div>
        </div>
      </PageTransition>
    </DashboardLayout>
  );
};

export default Settings;
