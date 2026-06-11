import streamlit as st
from supabase import create_client, Client

# --- 1. DATABASE CONNECTION SETUP ---
SUPABASE_URL = "https://uyrfrgdjwfthmwyhvdrj.supabase.co"
SUPABASE_KEY = "sb_publishable_1EmUVN4ONUX-2dnEY-eFZg_GzYA06mw"

# Initialize the cloud database client
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


# --- 3. SIDEBAR: ADD NEW INVENTORY FORM ---
with st.sidebar:
    st.header("➕ Add New Inventory")
    
    item_name = st.text_input("Item Name", placeholder="e.g., Wireless Mouse")
    starting_stock = st.number_input("Starting Stock", min_value=0, value=0, step=1)
    price = st.number_input("Price ($)", min_value=0.0, value=0.0, step=0.01)
    
    if st.button("Add Item to Cloud", use_container_width=True):
        if item_name.strip() == "":
            st.error("Please enter a valid item name.")
        else:
            new_item = {
                "name": item_name,
                "stock": starting_stock,   # Forcing clean lowercase
                "price": price             # Forcing clean lowercase
            }
            supabase.table("Items").insert(new_item).execute()
            st.success(f"Successfully added '{item_name}'!")
            st.rerun()


# --- 4. MAIN INTERFACE: LIVE STOCK SHEETS ---
st.subheader("📊 Live Stock Sheets")

# Fetch current list from the cloud
response = supabase.table("Items").select("*").order("id", desc=False).execute()
items_list = response.data

if not items_list:
    st.info("No items in inventory yet. Use the sidebar to add your first item!")
else:
    for clean_item in items_list:
        col_id, col_name, col_price, col_counter = st.columns([1, 3, 2, 3])
        
        with col_id:
            st.markdown(f"**ID:** {clean_item['id']}")
            
        with col_name:
            st.markdown(f"**Product:** {clean_item['name']}")
            
        with col_price:
            st.markdown(f"**Price:** ${float(clean_item['price']):.2f}")
            
        with col_counter:
            # Standardizing interactive step counters to lowercase keys
            new_stock = st.number_input(
                label=f"Stock counter for {clean_item['id']}",
                min_value=0,
                value=int(clean_item['stock']),
                step=1,
                key=f"stock_{clean_item['id']}",
                label_visibility="collapsed"
            )
            
            # Instantly update cloud if a user changes values
            if new_stock != clean_item['stock']:
                supabase.table("Items").update({"stock": new_stock}).eq("id", clean_item['id']).execute()
                st.rerun()
                
        st.markdown("<hr style='border: 0; height: 1px; background: #F3F4F6; margin: 10px 0;'>", unsafe_allow_html=True)
