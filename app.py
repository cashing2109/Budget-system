import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def predict_savings(income, total_expenses, savings):
    """
    Predicts future savings based on the current budget trends.
    We used a simple Linear Regression model to estimate the savings for the next month.
    The model is trained on a simulated savings trend, assuming a steady increase over time.
    """
    # Generate a simulated dataset for trend analysis
    months = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]).reshape(-1, 1)  # Last 12 months
    savings_trend = np.linspace(savings * 0.8, savings * 1.2, 12)  # Simulating a savings trend

    # Train the model on this trend
    model = LinearRegression()
    model.fit(months, savings_trend)

    # Predict next month's savings
    next_month_prediction = model.predict([[13]])[0]  # Predicting for month 13

    explanation = (
        f"We used a Linear Regression model trained on a simulated savings trend. "
        f"The model assumes savings increase steadily over time. "
        f"Based on the last 12 months' simulated savings trend, we predict next month's savings to be: ${next_month_prediction:.2f}."
    )
    return next_month_prediction, explanation

def calculate_financial_health_score(income, savings, total_expenses):
    """
    Calculates a financial health score based on savings, expenses, and income.
    Ensures a score between 0 and 100, preventing division errors.
    """
    if income == 0:
        return 0, "Income is zero, so a financial score cannot be calculated."
    
    savings_ratio = (savings / income) * 100
    expenses_ratio = (total_expenses / income) * 100

    score = savings_ratio - (expenses_ratio / 2)  # Less penalty for expenses
    score = max(0, min(100, score))  # Ensure score is between 0 and 100

    explanation = ""
    if score == 0:
        explanation = "Your financial health score is 0 because your expenses are very high compared to your income and savings. Consider reducing expenses or increasing savings."
    
    return score, explanation

# Streamlit UI
st.title("💰 Budget & Savings Prediction App")

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
    financial_health_score, score_explanation = calculate_financial_health_score(income, savings, total_expenses)

    st.subheader("📊 Budget Analysis Summary")
    st.write(f"**Total Expenses:** ${total_expenses:.2f}")
    st.write(f"**Discretionary Income:** ${discretionary_income:.2f}")
    st.write(f"**Financial Health Score:** {financial_health_score:.2f}/100")
    if score_explanation:
        st.write(f"ℹ️ {score_explanation}")

    st.subheader("📈 Future Savings Prediction")
    predicted_savings, explanation = predict_savings(income, total_expenses, savings)
    st.write(f"Predicted savings for next month: ${predicted_savings:.2f}")
    st.write(explanation)

    # Expense visualization
    labels = ["Rent/Mortgage", "Groceries", "Transportation", "Entertainment", "Debt", "Other Expenses"]
    values = [rent, groceries, transportation, entertainment, debt, other_expenses]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title("Monthly Expense Breakdown")
    st.pyplot(fig)

    # Provide recommendations
    st.subheader("💡 Recommendations")
    if financial_health_score < 50:
        st.warning("Your financial health score is below 50. Consider reducing unnecessary expenses and increasing savings.")
    elif financial_health_score < 80:
        st.info("Your financial health score is decent, but there’s room for improvement. Try saving a higher percentage of your income.")
    else:
        st.success("Great job! Your financial health is strong. Keep maintaining good budgeting habits.")

