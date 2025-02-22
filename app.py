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
    Also compares user spending to global recommended budget allocations.
    """
    if income == 0 or (savings == 0 and total_expenses == 0):
        return None, "Enter more data to get results.", None, None
    
    savings_ratio = (savings / income) * 100
    expenses_ratio = (total_expenses / income) * 100
    
    # Adjusted score calculation to ensure it is never 0
    score = (savings_ratio * 0.5) - (expenses_ratio * 0.3) + 50
    score = max(1, min(100, score))  # Ensure score is between 1 and 100 to avoid 0
    
    formula_used = f"Score = (Savings Ratio * 0.5) - (Expenses Ratio * 0.3) + 50"
    explanation = f"Formula Used: {formula_used}. Calculated as ({savings_ratio:.2f} * 0.5) - ({expenses_ratio:.2f} * 0.3) + 50 = {score:.2f}"
    
    # Global budget recommendations (based on financial guidelines)
    recommended_budget = {
        "Rent/Mortgage": 30,
        "Groceries": 15,
        "Transportation": 10,
        "Entertainment": 5,
        "Savings": 20,
        "Debt": 10,
        "Other Expenses": 10,
    }
    
    user_budget = {
        "Rent/Mortgage": (rent / income) * 100,
        "Groceries": (groceries / income) * 100,
        "Transportation": (transportation / income) * 100,
        "Entertainment": (entertainment / income) * 100,
        "Savings": (savings / income) * 100,
        "Debt": (debt / income) * 100,
        "Other Expenses": (other_expenses / income) * 100,
    }
    
    return score, explanation, recommended_budget, user_budget

# Streamlit UI
st.markdown(
    """
    <div style="text-align: center;">
        <h1>💰 Budget & Financial Goal Recommendation App</h1>
        <h3>Made by MD H. Rahman</h3>
        <p><a href="https://www.linkedin.com/in/habib-rahmann/" target="_blank">LinkedIn Profile</a></p>
    </div>
    """,
    unsafe_allow_html=True
)

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
    financial_health_score, score_explanation, recommended_budget, user_budget = calculate_financial_health_score(income, savings, total_expenses)

    if financial_health_score is None:
        st.error(score_explanation)
    else:
        st.subheader("📊 Budget Analysis Summary")
        st.write(f"**Total Expenses:** ${total_expenses:.2f}")
        st.write(f"**Discretionary Income:** ${discretionary_income:.2f}")
        st.write(f"**Financial Health Score:** {financial_health_score:.2f}/100")
        st.write(f"📌 {score_explanation}")
        
        # Display recommended vs actual budget allocations
        st.subheader("🌍 Recommended vs Your Budget Allocations")
        for category, percentage in recommended_budget.items():
            user_percentage = user_budget.get(category, 0)
            st.write(f"- **{category}**: Recommended - {percentage}% | Your Spending - {user_percentage:.2f}%")
        
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


