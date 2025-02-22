import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import random

def financial_goal_recommendation(income, savings, total_expenses):
    """
    Suggests a personalized financial goal based on income, savings, and spending habits.
    """
    goals = [
        "Save an extra $500 this month by reducing discretionary spending!",
        "Invest 10% of your income into a retirement account for long-term growth.",
        "Try a no-spend challenge for a week to boost savings!",
        "Increase your emergency fund to cover at least 6 months of expenses.",
        "Explore passive income opportunities to boost your financial security!",
    ]
    
    if savings / income < 0.1:
        return "Your savings rate is low! " + random.choice(goals)
    elif total_expenses / income > 0.7:
        return "You're spending a high percentage of your income! " + random.choice(goals)
    else:
        return "You're on a great track! Consider this goal: " + random.choice(goals)

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
st.title("💰 Budget & Financial Goal Recommendation App")

income = st.number_input("Enter your monthly income ($)", min_value=0.0, step=100.0)
rent = st.number_input("Enter your rent or mortgage ($)", min_value=0.0, step=50.0)
groceries = st.number_input("Enter your grocery expenses ($)", min_value=0.0, step=10.0)
transportation = st.number_input("Enter your transportation costs ($)", min_value=0.0, step=10.0)
entertainment = st.number_input("Enter your entertainment expenses ($)", min_value=0.0, step=10.0)
savings = st.number_input("Enter your current monthly savings ($)", min_value=0.0, step=10.0)
debt = st.number_input("Enter your monthly debt payments ($)", min_value=0.0, step=10.0)
other_expenses = st.number_input("Enter any other monthly expenses ($)", min_value=0.0, step=10.0)

if st.button("Analyze Budget & Get Financial Goal"):
    total_expenses = rent + groceries + transportation + entertainment + debt + other_expenses
    discretionary_income = income - total_expenses - savings
    financial_health_score, score_explanation = calculate_financial_health_score(income, savings, total_expenses)

    st.subheader("📊 Budget Analysis Summary")
    st.write(f"**Total Expenses:** ${total_expenses:.2f}")
    st.write(f"**Discretionary Income:** ${discretionary_income:.2f}")
    st.write(f"**Financial Health Score:** {financial_health_score:.2f}/100")
    if score_explanation:
        st.write(f"ℹ️ {score_explanation}")

    st.subheader("🎯 Personalized Financial Goal")
    goal_recommendation = financial_goal_recommendation(income, savings, total_expenses)
    st.write(goal_recommendation)

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


