import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("💰 Smart Expense Tracker")

# --- Define categories and products ---
category_products = {
    "Food": ["Pizza", "Burger", "Sandwich", "Groceries", "Snacks"],
    "Travel": ["Taxi", "Bus", "Train", "Flight", "Fuel"],
    "Entertainment": ["Movies", "Games", "Streaming", "Concerts"],
    "Bills": ["Electricity", "Internet", "Water", "Rent"],
    "Shopping": ["Clothes", "Accessories", "Shoes", "Online Purchase"],
    "Other": ["Miscellaneous", "Donation", "Gift"]
}

# --- Load or initialize data ---
try:
    df = pd.read_csv("expenses.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Product", "Amount", "Notes"])

# --- Entry form ---
with st.form("expense_entry", clear_on_submit=True):
    st.subheader("➕ Add New Expense")

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", list(category_products.keys()))
    with col2:
        product = st.selectbox("Product", category_products[category])

    amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
    notes = st.text_input("Notes (optional)")
    submit = st.form_submit_button("Add Expense")

    if submit:
        new_entry = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Category": category,
            "Product": product,
            "Amount": amount,
            "Notes": notes
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv("expenses.csv", index=False)
        st.success("✅ Expense Added Successfully!")

# --- Display and analysis ---
st.subheader("📊 Expense Summary")
if not df.empty:
    st.dataframe(df)

    total = df["Amount"].sum()
    st.write(f"### 💸 Total Expenses: ₹{total:.2f}")

    fig, ax = plt.subplots()
    df.groupby("Category")["Amount"].sum().plot(kind="bar", ax=ax)
    ax.set_title("Expenses by Category")
    st.pyplot(fig)
else:
    st.info("No expenses recorded yet. Start adding some!")