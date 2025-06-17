import { RefreshCw } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";
import { motion } from "framer-motion";

interface NavbarProps {
  onPoll: () => void;
}

export function Navbar({ onPoll }: NavbarProps) {
  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
    >
      <div className="container flex h-16 items-center justify-between">
        <motion.h1
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-2xl font-bold"
        >
          Market Dashboard
        </motion.h1>
        <div className="flex items-center gap-4">
          <button
            onClick={onPoll}
            className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-primary-foreground hover:bg-primary/90"
          >
            <RefreshCw className="h-4 w-4" />
            Poll
          </button>
          <ThemeToggle />
        </div>
      </div>
    </motion.nav>
  );
} 