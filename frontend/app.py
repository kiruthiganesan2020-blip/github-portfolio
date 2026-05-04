import streamlit as st
import requests

st.set_page_config(page_title="Zomato AI - Premium Recommendations", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for modern premium look with better fonts
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
        color: #1a1a1a;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Enhanced Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 16px;
        height: 3.5em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        transform: translateY(-2px);
        color: white;
        border: none;
    }

    /* Enhanced Card Layout */
    .restaurant-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 28px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #667eea;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .restaurant-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    .restaurant-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        background: rgba(255, 255, 255, 1);
    }
    
    /* Enhanced Typography */
    .restaurant-name {
        font-size: 24px;
        font-weight: 700;
        color: #1a1a1a;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
    }
    .restaurant-meta {
        color: #4a5568;
        font-size: 15px;
        margin-bottom: 18px;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        opacity: 0.8;
    }
    .restaurant-reason {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 18px;
        border-radius: 14px;
        color: #2d3748;
        line-height: 1.6;
        font-size: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    .rating-badge {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(72, 187, 120, 0.3);
        font-family: 'Inter', sans-serif;
    }
    
    /* Enhanced Input Styles */
    .stSelectbox > div > div > input,
    .stSlider > div > div > div {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Header Typography */
    .main-header {
        font-family: 'Playfair Display', serif;
        font-weight: 800;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Header Section with enhanced typography
st.markdown("""
<div class="main-header" style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 3.5rem; margin-bottom: 10px; font-weight: 800;">🍽️ Zomato AI</h1>
    <p style="font-size: 1.3rem; opacity: 0.9; font-weight: 300;">Discover hyper-personalized dining experiences powered by AI</p>
</div>
""", unsafe_allow_html=True)

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
        
        # Add a helpful tip instead of model selection
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 12px; border-radius: 10px; margin-top: 10px;">
            <p style="font-size: 13px; color: white; margin: 0;">💡 <strong>Tip:</strong> Our AI automatically selects the best model for your needs!</p>
        </div>
        """, unsafe_allow_html=True)

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
        "model_name": "models/gemini-3-flash-preview",
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
