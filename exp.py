import streamlit as st
from pymongo import MongoClient

# MongoDB Setup (Make sure MongoDB is running locally or use MongoDB Atlas)
client = MongoClient("mongodb://localhost:27017/")
db = client['expense_tracker']
collection = db['expenses']

# Function to add an expense
def add_expense(description, amount, category):
    expense_data = {
        'description': description,
        'amount': amount,
        'category': category
    }
    collection.insert_one(expense_data)

# Function to retrieve all expenses
def get_expenses():
    expenses = collection.find()
    return list(expenses)

# Streamlit UI
st.title("Expense Tracker")

# Sidebar Menu
menu = ["Add Expense", "View Expenses"]
choice = st.sidebar.selectbox("Menu", menu)

# Add Expense Module
if choice == "Add Expense":
    st.subheader("Add a New Expense")
    
    with st.form(key='add_expense_form'):
        description = st.text_input("Expense Description")
        amount = st.number_input("Expense Amount", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Other"])
        submit_button = st.form_submit_button(label='Add Expense')

    if submit_button:
        add_expense(description, amount, category)
        st.success(f"Expense added: {description} - ₹{amount} ({category})")

# View Expenses Module
elif choice == "View Expenses":
    st.subheader("View All Expenses")
    
    expenses = get_expenses()
    
    if len(expenses) > 0:
        total_amount = 0
        for expense in expenses:
            st.write(f"Description: {expense['description']}, Amount: ₹{expense['amount']}, Category: {expense['category']}")
            total_amount += expense['amount']
        
        st.write(f"**Total Expenses: ₹{total_amount}**")
    else:
        st.info("No expenses found!")

