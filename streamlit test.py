import streamlit as st
from supabase import create_client, Client

# --- 1. DATABASE CONNECTION SETUP ---
SUPABASE_URL = "https://uyrfrgdjwfthmwyhvdrj.supabase.co"
SUPABASE_KEY = "sb_publishable_1EmUVN4ONUX-2dnEY-eFZg_GzYA06mw"

# Initialize the cloud database client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- 2. PROINV+ HEADER SECTION ---
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://img.icons8.com/fluent/120/000000/layers.png" width="80" style="margin-bottom: 10px;">
    </div>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style="text-align: center; font-family: 'Inter', sans-serif; font-weight: 800; color: #1E3A8A; margin-bottom: 0px;">
        ProInv<span style="color: #3B82F6;">+</span>
    </h1>
    <p style="text-align: center; color: #6B7280; font-size: 14px;">
        Local Development Dashboard • Connected to Live Cloud DB
    </p>
    <hr style="border: 0; height: 1px; background: #E5E7EB; margin-bottom: 30px;">
    """, 
    unsafe_allow_html=True
)


# --- 3. SIDEBAR: ADD NEW INVENTORY ---
with st.sidebar:
    st.header("➕ Add New Item")
    new_name = st.text_input("Item Name", placeholder="e.g., Wireless Mouse")
    
    if st.button("Add Item to Database", use_container_width=True):
        if new_name.strip() == "":
            st.error("Please enter a valid item name.")
        else:
            try:
                # Inserting only the item name is 100% safe against column casing mismatches
                supabase.table("Items").insert({"name": new_name.strip()}).execute()
                st.success(f"Added '{new_name}' successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding item: {e}")


# --- 4. MAIN INTERFACE: LIVE INVENTORY LIST ---
st.subheader("📋 Current Inventory")

try:
    # Fetch data safely from the Items table
    response = supabase.table("Items").select("*").order("id", desc=False).execute()
    items_list = response.data

    if not items_list:
        st.info("No items found in your database table.")
    else:
        # Loop through data entries and display them safely
        for item in items_list:
            # Fallback Strategy: Extracts information regardless of lower or uppercase column keys
            p_id = item.get('id', '?')
            p_name = item.get('name', 'Unnamed Item')
            p_price = item.get('price', item.get('Price', 0.0))
            p_stock = item.get('stock', item.get('Stock', 0))
            
            # Format price safely if it returns valid numerical data
            formatted_price = f"${float(p_price):.2f}" if p_price is not None else "$0.00"
            
            # Render a clean information banner for each item row
            st.info(f"**ID:** {p_id} | **Product:** {p_name} | **Price:** {formatted_price} | **In Stock:** {p_stock}")

except Exception as e:
    st.error(f"Database Fetch Error: {e}")
