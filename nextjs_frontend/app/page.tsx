"use client";

import { useState } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import PreferenceForm from "@/components/PreferenceForm";
import RecommendationCard from "@/components/RecommendationCard";
import { Sparkles, UtensilsCrossed } from "lucide-react";

export default function Home() {
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRecommendations = async (prefs: any) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post("http://localhost:8000/recommend", {
        ...prefs,
        top_n: 5
      });
      setRecommendations(response.data.recommendations);
    } catch (err: any) {
      setError("Failed to fetch recommendations. Please ensure backend is running at http://localhost:8000");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-4 md:p-8 max-w-7xl mx-auto">
      <header className="mb-12 text-center">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="inline-flex items-center gap-2 bg-red-100 text-zomato-red px-4 py-2 rounded-full font-bold mb-4"
        >
          <Sparkles size={18} /> Phase 5: Response Presentation Layer
        </motion.div>
        <h1 className="text-5xl font-extrabold text-zomato-dark mb-4 flex items-center justify-center gap-3">
          <UtensilsCrossed className="text-zomato-red" size={48} /> Zomato AI
        </h1>
        <p className="text-xl text-zomato-gray max-w-2xl mx-auto">
          Hyper-personalized restaurant recommendations using the power of Gemini 3.0.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-4">
          <div className="glass p-6 rounded-3xl sticky top-8 border-t-4 border-zomato-red">
            <h2 className="text-xl font-bold mb-6 text-zomato-dark">Find Your Perfect Meal</h2>
            <PreferenceForm onSubmit={fetchRecommendations} isLoading={isLoading} />
          </div>
        </div>

        <div className="lg:col-span-8">
          <AnimatePresence mode="wait">
            {isLoading ? (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center justify-center h-64 space-y-4"
              >
                <div className="w-12 h-12 border-4 border-zomato-red border-t-transparent rounded-full animate-spin" />
                <p className="text-zomato-gray font-medium">Analyzing restaurants and generating reasons...</p>
              </motion.div>
            ) : error ? (
              <motion.div
                key="error"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="bg-red-50 text-red-600 p-6 rounded-2xl border border-red-100 text-center"
              >
                <p className="font-bold mb-2">Oops! Something went wrong.</p>
                <p className="text-sm">{error}</p>
              </motion.div>
            ) : recommendations.length > 0 ? (
              <motion.div key="results" className="space-y-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-bold text-zomato-dark">Top Recommendations</h2>
                  <span className="text-zomato-gray text-sm">{recommendations.length} matches found</span>
                </div>
                {recommendations.map((rec) => (
                  <RecommendationCard key={rec.name} rec={rec} />
                ))}
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-col items-center justify-center h-96 text-center space-y-6 opacity-40 grayscale"
              >
                <UtensilsCrossed size={80} className="text-gray-400" />
                <div>
                  <p className="text-2xl font-bold">No results yet</p>
                  <p>Fill out the form on the left to get personalized suggestions.</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
      
      <footer className="mt-20 py-8 border-t border-gray-200 text-center text-gray-500 text-sm">
        <p>© 2026 Zomato AI Recommendation Engine. Built with Next.js & Gemini 3.0.</p>
      </footer>
    </main>
  );
}
