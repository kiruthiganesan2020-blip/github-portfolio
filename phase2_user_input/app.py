from __future__ import annotations

from pathlib import Path

import streamlit as st

from phase2_user_input.schema import UserPreferenceRequest
from phase2_user_input.storage import save_request_snapshot
from phase2_user_input.validators import (
    parse_additional_preferences,
    validate_preferences,
)


OUTPUT_DIR = Path("phase2_user_input/output").resolve()

AVAILABLE_LOCATIONS = [
    "BTM", "Banashankari", "Banaswadi", "Bannerghatta Road", "Basavanagudi", 
    "Basaveshwara Nagar", "Bellandur", "Bommanahalli", "Brigade Road", "Brookefield", 
    "CV Raman Nagar", "Central Bangalore", "Church Street", "City Market", 
    "Commercial Street", "Cunningham Road", "Domlur", "East Bangalore", "Ejipura", 
    "Electronic City", "Frazer Town", "HBR Layout", "HSR", "Hebbal", "Hennur", 
    "Hosur Road", "ITPL Main Road, Whitefield", "Indiranagar", "Infantry Road", 
    "JP Nagar", "Jakkur", "Jalahalli", "Jayanagar", "Jeevan Bhima Nagar", "KR Puram", 
    "Kaggadasapura", "Kalyan Nagar", "Kammanahalli", "Kanakapura Road", "Kengeri", 
    "Koramangala", "Koramangala 1st Block", "Koramangala 2nd Block", "Koramangala 3rd Block", 
    "Koramangala 4th Block", "Koramangala 5th Block", "Koramangala 6th Block", 
    "Koramangala 7th Block", "Koramangala 8th Block", "Kumaraswamy Layout", "Langford Town", 
    "Lavelle Road", "MG Road", "Magadi Road", "Majestic", "Malleshwaram", "Marathahalli", 
    "Mysore Road", "Nagarbhavi", "Nagawara", "New BEL Road", "North Bangalore", 
    "Old Airport Road", "Old Madras Road", "Peenya", "RT Nagar", "Race Course Road", 
    "Rajajinagar", "Rajarajeshwari Nagar", "Rammurthy Nagar", "Residency Road", 
    "Richmond Road", "Sadashiv Nagar", "Sahakara Nagar", "Sanjay Nagar", "Sankey Road", 
    "Sarjapur Road", "Seshadripuram", "Shanti Nagar", "Shivajinagar", "South Bangalore", 
    "St. Marks Road", "Thippasandra", "Ulsoor", "Uttarahalli", "Varthur Main Road, Whitefield", 
    "Vasanth Nagar", "Vijay Nagar", "West Bangalore", "Whitefield", "Wilson Garden", 
    "Yelahanka", "Yeshwantpur"
]


def render_form() -> None:
    st.set_page_config(page_title="Zomato AI - Phase 2 Input", page_icon="🍽️")
    st.title("Zomato AI - User Preference Collection")
    st.caption("Phase 2 input layer with validation and normalized schema output.")

    with st.form("preference_form"):
        location = st.selectbox("Location", options=AVAILABLE_LOCATIONS)
        budget = st.slider("Budget (₹)", min_value=200, max_value=5000, value=1500, step=100)
        cuisine = st.text_input("Cuisine", placeholder="Italian, Chinese")
        min_rating = st.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=3.5, step=0.1)
        additional_raw = st.text_area(
            "Additional Preferences (comma-separated)",
            placeholder="family-friendly, quick service",
        )

        submitted = st.form_submit_button("Submit Preferences")

    if not submitted:
        return

    payload = UserPreferenceRequest(
        location=location,
        budget=float(budget),
        cuisine=cuisine,
        min_rating=float(min_rating),
        additional_preferences=parse_additional_preferences(additional_raw),
    ).normalize()

    is_valid, errors = validate_preferences(payload)
    if not is_valid:
        st.error("Please fix the following issues:")
        for err in errors:
            st.write(f"- {err}")
        return

    output_path = save_request_snapshot(payload.to_dict(), OUTPUT_DIR)

    st.success("Preferences captured successfully.")
    st.write("Normalized payload:")
    st.json(payload.to_dict())
    st.info(f"Saved to: {output_path}")


if __name__ == "__main__":
    render_form()

