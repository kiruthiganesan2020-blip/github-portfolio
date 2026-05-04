import streamlit as st
import requests

st.set_page_config(page_title="Zomato AI - Premium Recommendations", page_icon="🍽️", layout="wide")

# Custom CSS for modern Stitch-style premium look
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
        background-color: #cb202d;
        color: white;
        font-weight: 600;
        font-size: 16px;
        border: none;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #e23744;
        box-shadow: 0 4px 12px rgba(203, 32, 45, 0.2);
        color: white;
        border: none;
    }

    /* Card Layout */
    .restaurant-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 16px;
        border-left: 6px solid #cb202d;
        border-top: 1px solid #f0f0f0;
        border-right: 1px solid #f0f0f0;
        border-bottom: 1px solid #f0f0f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .restaurant-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    }
    
    /* Typography */
    .restaurant-name {
        font-size: 22px;
        font-weight: 700;
        color: #1c1c1c;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
    .restaurant-meta {
        color: #666;
        font-size: 14.5px;
        margin-bottom: 16px;
        font-weight: 500;
    }
    .restaurant-reason {
        background-color: #fcf8f8;
        padding: 16px;
        border-radius: 12px;
        color: #444;
        line-height: 1.5;
        font-size: 15px;
        border: 1px solid #fce8e8;
    }
    .rating-badge {
        background-color: #24963f;
        color: white;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.title("🍽️ Zomato AI")
st.markdown("<p style='font-size: 18px; color: #666; margin-bottom: 30px;'>Discover hyper-personalized dining experiences powered by Gemini.</p>", unsafe_allow_html=True)

# Input Section (Top Layout)
with st.container(border=True):
    st.subheader("What are you craving?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        locations = [
            "Anywhere in Bangalore", "Indiranagar", "Koramangala", "Whitefield", 
            "HSR Layout", "Marathahalli", "Jayanagar", "BTM", "Electronic City", 
            "Yelahanka", "Malleshwaram", "Rajajinagar", "Bellandur", "Sarjapur", "Hebbal"
        ]
        loc_selection = st.selectbox("📍 Location", options=locations, index=12)
        location = "" if loc_selection == "Anywhere in Bangalore" else loc_selection
        min_rating = st.slider("⭐ Minimum Rating", min_value=3.0, max_value=5.0, value=4.0, step=0.1)

    with col2:
        budget_label = st.selectbox("💰 Budget", options=["Low (₹300)", "Medium (₹800)", "High (₹1500)"], index=2)
        model_name = st.selectbox("🧠 AI Model", options=["models/gemini-3-flash-preview", "models/gemini-2.0-flash", "models/gemini-pro"], index=0)

    with col3:
        cuisine = st.text_input("🍲 Cuisine", value="", placeholder="e.g. Italian, Sushi (Optional)")
        additional = st.text_area("✨ Special Features", placeholder="e.g. rooftop, romantic, spicy", height=68)

# Process Inputs
budget_map = {"Low (₹300)": 300.0, "Medium (₹800)": 800.0, "High (₹1500)": 1500.0}
numeric_budget = budget_map.get(budget_label, 1500.0)

submit = st.button("✨ Discover Restaurants")

if submit:
    payload = {
        "location": location.strip(),
        "budget": numeric_budget,
        "cuisine": "" if cuisine.strip().lower() == "any" else cuisine.strip(),
        "min_rating": min_rating,
        "additional_preferences": [x.strip() for x in additional.split(",") if x.strip()],
        "model_name": model_name,
        "top_n": 5
    }
    
    with st.spinner("Curating your personalized recommendations..."):
        try:
            # API call with strict 30-second timeout
            response = requests.post("http://localhost:8000/recommend", json=payload, timeout=30)
            
            if response.status_code == 200:
                results = response.json()
                recommendations = results.get('recommendations', [])
                
                # Handle empty results gracefully
                if not recommendations:
                    st.warning("We couldn't find any restaurants matching your exact criteria. Try relaxing your filters!")
                else:
                    st.success(f"Found {len(recommendations)} premium recommendations just for you!")
                    
                    for i, rec in enumerate(recommendations):
                        # Safe extraction using .get()
                        name = rec.get('name', 'Unknown Restaurant')
                        rating = rec.get('rating')
                        rating_display = f"{rating} ★" if rating else "N/A ★"
                        loc = rec.get('location', 'Unknown Location')
                        cuis = rec.get('cuisine', 'Mixed Cuisine')
                        cost = rec.get('cost', 'N/A')
                        reason = rec.get('reason', 'Great choice based on your preferences.')
                        
                        st.markdown(f"""
                        <div class="restaurant-card">
                            <div class="restaurant-name">
                                {name} 
                                <span class="rating-badge">{rating_display}</span>
                            </div>
                            <div class="restaurant-meta">
                                📍 {loc} &nbsp;•&nbsp; 🍲 {cuis} &nbsp;•&nbsp; 💰 ₹{cost} approx.
                            </div>
                            <div class="restaurant-reason">
                                <b>Why we recommend this:</b><br/> {reason}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Feedback row with unique keys
                        fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 10])
                        with fb_col1:
                            if st.button("👍", key=f"up_{name}_{i}"):
                                st.toast(f"Glad you liked {name}!")
                        with fb_col2:
                            if st.button("👎", key=f"down_{name}_{i}"):
                                st.toast(f"Feedback logged for {name}.")
                        st.markdown("<br/>", unsafe_allow_html=True)

            else:
                st.error(f"Error from server (Status {response.status_code}): {response.text}")
                
        except requests.exceptions.Timeout:
            st.error("⏳ The request took too long. The backend server might be heavily loaded. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to the backend. Please make sure the API is running on http://localhost:8000.")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")
else:
    st.info("Adjust your preferences above and click 'Discover Restaurants' to explore.")
