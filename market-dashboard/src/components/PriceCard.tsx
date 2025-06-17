import { motion } from "framer-motion";

interface PriceCardProps {
  title: string;
  value: number | null;
  change?: number;
  gradient: string;
  delay?: number;
}

export function PriceCard({ title, value, change, gradient, delay = 0 }: PriceCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className={`relative overflow-hidden rounded-xl p-6 ${gradient}`}
    >
      <div className="relative z-10">
        <h3 className="text-sm font-medium text-white/80">{title}</h3>
        <div className="mt-2 flex items-baseline gap-2">
          <p className="text-3xl font-semibold text-white">
            {value ? `$${value.toFixed(2)}` : "N/A"}
          </p>
          {change !== undefined && (
            <span
              className={`text-sm font-medium ${
                change >= 0 ? "text-green-300" : "text-red-300"
              }`}
            >
              {change >= 0 ? "+" : ""}
              {change.toFixed(2)}%
            </span>
          )}
        </div>
      </div>
      <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
    </motion.div>
  );
} 