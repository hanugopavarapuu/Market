import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import type { ChartOptions } from "chart.js";
import { Line } from "react-chartjs-2";
import { motion } from "framer-motion";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface PriceChartProps {
  labels: string[];
  latestPrices: number[];
  averagePrices: number[];
}

export function PriceChart({ labels, latestPrices, averagePrices }: PriceChartProps) {
  const options: ChartOptions<"line"> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: "Price History",
      },
    },
    scales: {
      y: {
        beginAtZero: false,
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
        },
        ticks: {
          color: "rgba(255, 255, 255, 0.7)",
        },
      },
      x: {
        grid: {
          color: "rgba(255, 255, 255, 0.1)",
        },
        ticks: {
          color: "rgba(255, 255, 255, 0.7)",
        },
      },
    },
  };

  const data = {
    labels,
    datasets: [
      {
        label: "Latest Price",
        data: latestPrices,
        borderColor: "rgb(99, 102, 241)",
        backgroundColor: "rgba(99, 102, 241, 0.5)",
        tension: 0.4,
      },
      {
        label: "Average Price",
        data: averagePrices,
        borderColor: "rgb(34, 197, 94)",
        backgroundColor: "rgba(34, 197, 94, 0.5)",
        tension: 0.4,
      },
    ],
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="h-[400px] w-full rounded-xl bg-card p-4 shadow-lg"
    >
      <Line options={options} data={data} />
    </motion.div>
  );
} 