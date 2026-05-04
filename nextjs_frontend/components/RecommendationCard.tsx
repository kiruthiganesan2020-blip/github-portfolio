"use client";

import { motion } from "framer-motion";
import { Star, MapPin, Utensils, IndianRupee, ThumbsUp, ThumbsDown } from "lucide-react";
import { useState } from "react";

interface Recommendation {
  rank: number;
  name: string;
  reason: string;
  rating: number | null;
  cost: number | null;
  cuisine: string;
  location: string;
}

export default function RecommendationCard({ rec }: { rec: Recommendation }) {
  const [feedback, setFeedback] = useState<"up" | "down" | null>(null);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      className="glass rounded-2xl p-6 mb-6 relative overflow-hidden group"
    >
      <div className="absolute top-0 left-0 w-1.5 h-full bg-zomato-red" />
      
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-2xl font-bold text-zomato-dark flex items-center gap-2">
            <span className="text-zomato-red">#{rec.rank}</span> {rec.name}
          </h3>
          <div className="flex items-center gap-4 text-zomato-gray text-sm mt-1">
            <span className="flex items-center gap-1"><MapPin size={14} /> {rec.location}</span>
            <span className="flex items-center gap-1"><Utensils size={14} /> {rec.cuisine}</span>
            <span className="flex items-center gap-1"><IndianRupee size={14} /> {rec.cost} approx.</span>
          </div>
        </div>
        
        <div className="flex flex-col items-end">
          <div className="bg-green-700 text-white px-2 py-1 rounded-md font-bold text-sm flex items-center gap-1">
            {rec.rating || "N/A"} <Star size={12} fill="currentColor" />
          </div>
        </div>
      </div>

      <div className="bg-red-50/50 p-4 rounded-xl border border-red-100 mb-4">
        <p className="text-sm text-gray-700 leading-relaxed italic">
          <span className="font-bold text-zomato-red not-italic mr-2">Why this?</span>
          "{rec.reason}"
        </p>
      </div>

      <div className="flex items-center gap-3">
        <button 
          onClick={() => setFeedback("up")}
          className={`p-2 rounded-full transition-colors ${feedback === "up" ? "bg-green-100 text-green-600" : "hover:bg-gray-100 text-gray-400"}`}
        >
          <ThumbsUp size={18} />
        </button>
        <button 
          onClick={() => setFeedback("down")}
          className={`p-2 rounded-full transition-colors ${feedback === "down" ? "bg-red-100 text-red-600" : "hover:bg-gray-100 text-gray-400"}`}
        >
          <ThumbsDown size={18} />
        </button>
        {feedback && (
          <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-xs text-gray-500">
            Thanks for the feedback!
          </motion.span>
        )}
      </div>
    </motion.div>
  );
}
