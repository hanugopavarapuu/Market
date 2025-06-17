import { Search } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";

interface SearchBarProps {
  onSearch: (symbol: string) => void;
}

export function SearchBar({ onSearch }: SearchBarProps) {
  const [symbol, setSymbol] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (symbol.trim()) {
      onSearch(symbol.trim().toUpperCase());
    }
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="container max-w-2xl"
      onSubmit={handleSubmit}
    >
      <div className="flex gap-2">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Enter symbol (e.g., AAPL)"
          className="flex-1 rounded-lg border bg-background px-4 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
        <button
          type="submit"
          className="flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-primary-foreground hover:bg-primary/90"
        >
          <Search className="h-4 w-4" />
          Search
        </button>
      </div>
    </motion.form>
  );
} 