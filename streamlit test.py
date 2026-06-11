import streamlit as st
from supabase import create_client, Client

# 🔑 YOUR ACTUAL SUPABASE KEYS
SUPABASE_URL = "https://uyrfrgdjwfthmwyhvdrj.supabase.co"
SUPABASE_KEY = "sb_publishable_1EmUVN4ONUX-2dnEY-eFZg_GzYA06mw"

# Connect the Python brain to the cloud database memory
@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# --- WEBSITE HEADER ---
st.set_page_config(page_title="Cloud Inventory", page_icon="📦", layout="centered")
st.title("📦 Professional Cloud Inventory System")
st.write("Welcome to your live, cloud-connected inventory dashboard management console.")

st.divider()

# --- SIDEBAR: ADD NEW ITEM ---
st.sidebar.header("➕ Add New Inventory")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_name = st.text_input("Item Name")
    new_qty = st.number_input("Starting Stock", min_value=0, step=1)
    new_price = st.number_input("Price ($)", min_value=0.0, step=0.01)
    submit_button = st.form_submit_button("Add Item to Cloud")

    if submit_button:
        if new_name.strip() == "":
            st.sidebar.error("Item name cannot be blank!")
        else:
            try:
                supabase.table("Items").insert({
                    "name": new_name, "quantity": new_qty, "price": new_price
                }).execute()
                st.sidebar.success(f"Added {new_name} successfully!")
                st.rerun()  # Refresh the page to show the new item immediately
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# --- MAIN PAGE: VIEW & MANAGE INVENTORY ---
st.subheader("📊 Live Stock Sheets")

try:
    # Pull data from cloud
    response = supabase.table("Items").select("*").order("id").execute()
    items = response.data

    if not items:
        st.info("The inventory is currently empty.")
    else:
        # Loop through data and display beautiful individual interactive rows
        for item in items:
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                
                with col1:
                    st.write(f"**ID:** {item['id']}")
                with col2:
                    st.write(f"**Product:** {item['name']}")
                with col3:
                    st.write(f"**Price:** ${item['price']:.2f}")
                with col4:
                    current_stock = item['quantity']
                    new_stock = st.number_input(
                        f"Stock for ID {item['id']}", 
                        min_value=0, 
                        value=int(current_stock), 
                        key=f"stock_{item['id']}", 
                        label_visibility="collapsed"
                    )
                    
                    # If they change the number, update the cloud instantly
                    if new_stock != current_stock:
                        supabase.table("Items").update({"quantity": new_stock}).eq("id", item['id']).execute()
                        st.rerun()
                st.divider()

except Exception as e:
    st.error(f"Could not load cloud data: {e}")
