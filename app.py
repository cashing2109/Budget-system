import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def predict_savings(income, total_expenses, savings):
    """
    Predicts future savings based on the current budget trends.
    Uses a simple regression model without storing user data.
    """

    # Generate a simulated dataset for trend analysis
    months = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape(-1, 1)  # Last 12 months
    savings_trend = np.linspace(savings * 0.8, savings * 1.2, 12)  # Simulating a savings trend

    # Train the model on this trend
    model = LinearRegression()
    model.fit(months, savings_trend)

    # Predict next month's savings
    next_month_prediction = model.predict([[13]])[0]  # Predicting for month 13

    return f"Predicted savings for next month: ${next_month_prediction:.2f}"

# Streamlit UI
st.title("💰 Budget & Savings Prediction App (No Data Storage)")

income = st.number_input("Enter your monthly income ($)", min_value=0.0, step=100.0)
rent = st.number_input("Enter your rent or mortgage ($)", min_value=0.0, step=50.0)
groceries = st.number_input("Enter your grocery expenses ($)", min_value=0.0, step=10.0)
transportation = st.number_input("Enter your transportation costs ($)", min_value=0.0, step=10.0)
entertainment = st.number_input("Enter your entertainment expenses ($)", min_value=0.0, step=10.0)
savings = st.number_input("Enter your current monthly savings ($)", min_value=0.0, step=10.0)
debt = st.number_input("Enter your monthly debt payments ($)", min_value=0.0, step=10.0)
other_expenses = st.number_input("Enter any other monthly expenses ($)", min_value=0.0, step=10.0)

if st.button("Analyze Budget & Predict Savings"):
    total_expenses = rent + groceries + transportation + entertainment + debt + other_expenses
    discretionary_income = income - total_expenses - savings

    st.subheader("📊 Budget Analysis Summary")
    st.write(f"**Total Expenses:** ${total_expenses:.2f}")
    st.write(f"**Discretionary Income:** ${discretionary_income:.2f}")

    st.subheader("📈 Future Savings Prediction (No Data Storage)")
    st.write(predict_savings(income, total_expenses, savings))

    # Expense visualization
    labels = ["Rent/Mortgage", "Groceries", "Transportation", "Entertainment", "Debt", "Other Expenses"]
    values = [rent, groceries, transportation, entertainment, debt, other_expenses]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title("Monthly Expense Breakdown")
    st.pyplot(fig)
