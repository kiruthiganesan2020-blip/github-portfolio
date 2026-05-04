"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Search, Sliders, MapPin, Utensils } from "lucide-react";

interface PreferenceFormProps {
  onSubmit: (data: any) => void;
  isLoading: boolean;
}

export default function PreferenceForm({ onSubmit, isLoading }: PreferenceFormProps) {
  const [formData, setFormData] = useState({
    location: "Bellandur",
    budget: 1500,
    cuisine: "Any",
    min_rating: 4.0,
    additional_preferences: ""
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      ...formData,
      cuisine: formData.cuisine.toLowerCase() === "any" ? "" : formData.cuisine,
      additional_preferences: formData.additional_preferences.split(",").map(s => s.trim()).filter(s => s !== "")
    });
  };

  const cuisineChips = ["Italian", "Spicy", "Japanese", "Healthy", "Desserts"];

  const handleCuisineChip = (chip: string) => {
    setFormData(prev => {
      const cuisines = prev.cuisine.split(",").map(c => c.trim()).filter(c => c && c.toLowerCase() !== "any");
      if (cuisines.includes(chip)) {
        return { ...prev, cuisine: cuisines.filter(c => c !== chip).join(", ") || "Any" };
      } else {
        return { ...prev, cuisine: [...cuisines, chip].join(", ") };
      }
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-600 flex items-center gap-2">
          <MapPin size={16} /> Location
        </label>
        <input
          type="text"
          value={formData.location}
          onChange={(e) => setFormData({ ...formData, location: e.target.value })}
          className="w-full p-3 rounded-xl border border-gray-200 focus:border-zomato-red focus:ring-1 focus:ring-zomato-red outline-none transition-all"
          placeholder="e.g. Bellandur, Bangalore"
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-600 flex justify-between">
          <span className="flex items-center gap-2"><Sliders size={16} /> Max Budget</span>
          <span className="text-zomato-red font-bold">₹{formData.budget}</span>
        </label>
        <input
          type="range"
          min="200"
          max="5000"
          step="100"
          value={formData.budget}
          onChange={(e) => setFormData({ ...formData, budget: parseInt(e.target.value) })}
          className="w-full accent-zomato-red"
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-600 flex items-center gap-2">
          <Utensils size={16} /> Cuisine
        </label>
        <input
          type="text"
          value={formData.cuisine}
          onChange={(e) => setFormData({ ...formData, cuisine: e.target.value })}
          className="w-full p-3 rounded-xl border border-gray-200 focus:border-zomato-red focus:ring-1 focus:ring-zomato-red outline-none transition-all"
          placeholder="e.g. Italian, North Indian"
        />
        <div className="flex flex-wrap gap-2 mt-2">
          {cuisineChips.map(chip => {
            const isSelected = formData.cuisine.split(",").map(c => c.trim()).includes(chip);
            return (
              <button
                key={chip}
                type="button"
                onClick={() => handleCuisineChip(chip)}
                className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                  isSelected 
                    ? "bg-zomato-red text-white border-zomato-red" 
                    : "bg-gray-100 text-gray-600 border-gray-200 hover:border-zomato-red/50"
                }`}
              >
                {chip}
              </button>
            );
          })}
        </div>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-600 flex justify-between">
          <span>Minimum Rating</span>
          <span className="text-zomato-red font-bold">{formData.min_rating} ★</span>
        </label>
        <div className="flex gap-2 mb-2">
          <button 
            type="button" 
            onClick={() => setFormData({ ...formData, min_rating: 3.5 })}
            className={`px-3 py-1 text-xs rounded-full border transition-colors ${formData.min_rating === 3.5 ? 'bg-zomato-red text-white border-zomato-red' : 'bg-gray-50 border-gray-200'}`}
          >
            3.5 ★
          </button>
          <button 
            type="button" 
            onClick={() => setFormData({ ...formData, min_rating: 4.5 })}
            className={`px-3 py-1 text-xs rounded-full border transition-colors ${formData.min_rating === 4.5 ? 'bg-zomato-red text-white border-zomato-red' : 'bg-gray-50 border-gray-200'}`}
          >
            4.5 ★
          </button>
        </div>
        <input
          type="range"
          min="3.0"
          max="5.0"
          step="0.1"
          value={formData.min_rating}
          onChange={(e) => setFormData({ ...formData, min_rating: parseFloat(e.target.value) })}
          className="w-full accent-zomato-red"
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-600">Additional Preferences</label>
        <textarea
          value={formData.additional_preferences}
          onChange={(e) => setFormData({ ...formData, additional_preferences: e.target.value })}
          className="w-full p-3 rounded-xl border border-gray-200 focus:border-zomato-red focus:ring-1 focus:ring-zomato-red outline-none transition-all"
          placeholder="e.g. rooftop, family-friendly"
          rows={3}
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-zomato-red text-white p-4 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-red-700 transition-colors shadow-lg disabled:bg-gray-400"
      >
        {isLoading ? (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
            className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
          />
        ) : (
          <><Search size={20} /> Get Recommendations</>
        )}
      </button>
    </form>
  );
}
