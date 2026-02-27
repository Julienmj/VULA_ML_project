import { Leaf } from "lucide-react";
import { Link } from "react-router-dom";

const VulaLogo = ({ collapsed = false }: { collapsed?: boolean }) => (
  <Link to="/" className="flex items-center gap-2.5">
    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-primary shadow-md">
      <Leaf className="h-5 w-5 text-primary-foreground" />
    </div>
    {!collapsed && (
      <span className="font-display text-xl font-bold tracking-tight text-gradient">
        VULA
      </span>
    )}
  </Link>
);

export default VulaLogo;
