import { useState, useEffect } from "react";
import axios from "axios";
import { Navbar } from "./Navbar";
import { SearchBar } from "./SearchBar";
import { PriceCard } from "./PriceCard";
import { PriceChart } from "./PriceChart";

interface PriceData {
  symbol: string;
  price: number;
  timestamp: string;
  average: number;
  price_change?: number;
}

export function Dashboard() {
  const [symbol, setSymbol] = useState<string>("");
  const [priceData, setPriceData] = useState<PriceData | null>(null);
  const [priceHistory, setPriceHistory] = useState<PriceData[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchPrice = async (symbolToFetch: string) => {
    try {
      setIsLoading(true);
      const response = await axios.get(`/prices/latest?symbol=${symbolToFetch}`);
      const newPriceData = response.data;
      setPriceData(newPriceData);
      setPriceHistory((prev) => [...prev, newPriceData].slice(-10));
    } catch (error) {
      console.error("Error fetching price:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (searchSymbol: string) => {
    setSymbol(searchSymbol);
    fetchPrice(searchSymbol);
  };

  const handlePoll = () => {
    if (symbol) {
      fetchPrice(symbol);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar onPoll={handlePoll} />
      <main className="container space-y-8 py-8">
        <SearchBar onSearch={handleSearch} />
        
        {priceData && (
          <div className="grid gap-6 md:grid-cols-2">
            <PriceCard
              title="Latest Price"
              value={priceData.price}
              change={priceData.price_change}
              gradient="bg-gradient-to-br from-indigo-500 to-purple-600"
            />
            <PriceCard
              title="Average Price"
              value={priceData.average}
              gradient="bg-gradient-to-br from-emerald-500 to-teal-600"
              delay={0.1}
            />
          </div>
        )}

        {priceHistory.length > 0 && (
          <PriceChart
            labels={priceHistory.map((data) => new Date(data.timestamp).toLocaleTimeString())}
            latestPrices={priceHistory.map((data) => data.price)}
            averagePrices={priceHistory.map((data) => data.average)}
          />
        )}
      </main>
    </div>
  );
} 