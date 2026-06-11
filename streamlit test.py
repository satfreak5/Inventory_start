import streamlit as st
from supabase import create_client, Client

# --- 1. DATABASE CONNECTION SETUP ---
SUPABASE_URL = "https://uyrfrgdjwfthmwyhvdrj.supabase.co"
SUPABASE_KEY = "sb_publishable_1EmUVN4ONUX-2dnEY-eFZg_GzYA06mw"

# Initialize the cloud database client smoothly
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- 2. PREMIUM PROINV+ HEADER SECTION ---
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://img.icons8.com/fluent/120/000000/layers.png" width="100" style="margin-bottom: 10px;">
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style="text-align: center; font-family: 'Inter', sans-serif; font-weight: 800; color: #1E3A8A; letter-spacing: -1px; margin-top: 0px; margin-bottom: 0px;">
        ProInv<span style="color: #3B82F6;">+</span>
    </h1>
    <p style="text-align: center; color: #6B7280; font-size: 14px; margin-top: 5px;">
        Welcome to your live, cloud-connected inventory dashboard management console.
    </p>
    <hr style="border: 0; height: 1px; background: #E5E7EB; margin-top: 20px; margin-bottom: 30px;">
    """, 
    unsafe_allow_html=True
)


# --- 3. MAIN INTERFACE: LIVE INVENTORY LIST ---
st.subheader("📋 Current Inventory Items")

try:
    # Fetch data from the Items table
    response = supabase.table("Items").select("*").order("id", desc=False).execute()
    items_list = response.data

    if not items_list:
        st.info("No items found in your database table.")
    else:
        # Display the raw database dictionary entries safely to inspect the exact column names
        for item in items_list:
            st.json(item)

except Exception as e:
    st.error(f"Database Fetch Error: {e}")
