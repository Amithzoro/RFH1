import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

# --- Custom CSS for better UI ---
st.markdown("""
<style>
    .stSelectbox, .stNumberInput, .stTextInput, .stDateInput, .stTimeInput {
        background-color: #111827 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5em 1em;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #1e40af;
    }
</style>
""", unsafe_allow_html=True)

st.title("💰 Smart Expense Tracker")

# --- Define categories and dynamic product options ---
category_products = {
    "Food": ["Pizza", "Burger", "Subway Lunch", "Groceries", "Snacks"],
    "Travel": ["Taxi", "Bus", "Train", "Flight", "Fuel"],
    "Entertainment": ["Movies", "Games", "Streaming", "Concerts"],
    "Bills": ["Electricity", "Internet", "Water", "Rent"],
    "Shopping": ["Clothes", "Accessories", "Shoes", "Online Purchase"],
    "Gaming": ["UC (BGMI)", "Diamonds (Free Fire)", "CP (CODM)"],
    "Other": ["Miscellaneous", "Donation", "Gift"]
}

payment_modes = ["UPI", "Cash", "Card", "Net Banking", "Wallet"]
game_currency = ["UC (BGMI)", "Diamonds (Free Fire)", "CP (CODM)", "None"]

# --- Load or initialize data ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv("expenses.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Date", "Time", "Category", "Product", "Amount",
            "Payment Mode", "Game Currency", "Notes"
        ])

df = load_data()

# --- Category selection OUTSIDE the form (for live update) ---
st.subheader("➕ Add New Expense")

col1, col2 = st.columns(2)
with col1:
    date = st.date_input("Date", datetime.now().date())
    time = st.time_input("Time", datetime.now().time().replace(microsecond=0))
    category = st.selectbox("Category", list(category_products.keys()))
    product = st.selectbox("Product / Item Name", category_products.get(category, []))
with col2:
    amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
    payment_mode = st.selectbox("Payment Mode", payment_modes)
    game_currency_choice = st.selectbox("🎮 Game Currency (only for Gaming)", game_currency)
    notes = st.text_input("Notes (optional)")

# --- Submission button (outside form to allow live updates) ---
if st.button("💾 Add Expense"):
    new_entry = {
        "Date": date.strftime("%Y-%m-%d"),
        "Time": time.strftime("%H:%M"),
        "Category": category,
        "Product": product,
        "Amount": amount,
        "Payment Mode": payment_mode,
        "Game Currency": game_currency_choice if category == "Gaming" else "None",
        "Notes": notes
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv("expenses.csv", index=False)
    st.success("✅ Expense Added Successfully!")

# --- Display and Analysis ---
st.subheader("📊 Expense Summary")

if not df.empty:
    st.dataframe(df, use_container_width=True)

    total = df["Amount"].sum()
    st.markdown(f"### 💸 Total Expenses: ₹{total:.2f}")

    chart_data = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    st.bar_chart(chart_data)
else:
    st.info("No expenses recorded yet. Start adding some!")
