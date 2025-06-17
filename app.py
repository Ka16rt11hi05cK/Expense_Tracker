import mysql.connector
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# --------------------- MySQL Connection ---------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Karthick@2005",  # ✅ Use your MySQL password
    database="expense_traker"  # ✅ Make sure the DB name is correct
)
cursor = conn.cursor()

# --------------------- Streamlit UI ---------------------
st.set_page_config(page_title="Expense Tracker", layout="centered")

# --------------------- Title ---------------------
st.title("💸 Personal Expense Tracker")

# --------------------- Sidebar Navigation ---------------------
menu = st.sidebar.selectbox("📂 Menu", ["➕ Add Expense", "📋 View Expenses", "📊 Visualize"])

# --------------------- Session State Defaults ---------------------
if "date" not in st.session_state: st.session_state.date = datetime.now()
if "category" not in st.session_state: st.session_state.category = "Food"
if "amount" not in st.session_state: st.session_state.amount = 0.0
if "description" not in st.session_state: st.session_state.description = ""

# --------------------- Add Expense ---------------------
if menu == "➕ Add Expense":
    st.markdown("### <span style='color:#ff4b4b;'>➕ Add New Expense</span>", unsafe_allow_html=True)

    date = st.date_input("📅 Date", value=st.session_state.date, key="date")
    category = st.selectbox("📂 Category", ["Food", "Transport", "Bills", "Others"], key="category")
    amount = st.number_input("💰 Amount (₹)", min_value=0.0, format="%.2f", key="amount")
    description = st.text_input("📝 Description", key="description")

    if st.button("✅ Save"):
        cursor.execute(
            "INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)",
            (date, category, amount, description)
        )
        conn.commit()
        st.success("✅ Expense saved!")

        # Reset inputs
        st.session_state.date = datetime.now()
        st.session_state.category = "Food"
        st.session_state.amount = 0.0
        st.session_state.description = ""

# --------------------- View Expenses ---------------------
elif menu == "📋 View Expenses":
    st.markdown("### <span style='color:#1f77b4;'>📋 All Expenses</span>", unsafe_allow_html=True)

    cursor.execute("SELECT date, category, amount, description FROM expenses ORDER BY date DESC")
    data = cursor.fetchall()

    if data:
        for row in data:
            st.write(f"📅 **{row[0]}** | 📂 **{row[1]}** | 💰 ₹{row[2]:.2f} | 📝 {row[3]}")
    else:
        st.info("No expenses added yet.")

# --------------------- Visualize ---------------------
elif menu == "📊 Visualize":
    st.markdown("### <span style='color:#2ca02c;'>📊 Expense Breakdown</span>", unsafe_allow_html=True)

    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    results = cursor.fetchall()

    if results:
        labels = [row[0] for row in results]
        sizes = [row[1] for row in results]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("No data to display. Add some expenses first.")
