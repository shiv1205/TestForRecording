import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

#Main title of the application
st.title("Mortgage Repayments Calculator")

#Heading for mortgage input section
st.write("### Input Data")
#Divide page into 2 columns
col1, col2 = st.columns(2) #Divide page into 2 columns
home_value = col1.number_input("Home Value ($)", min_value=0, value=500000) # Sets the default home value to $500,000.
deposit = col1.number_input("Deposit ($)", min_value=0, value=100000)
interest_rate = col2.number_input(
    "Interest Rate (%)",
    min_value=0.0,
    value=5.5,
    step=0.1
)
loan_term = col2.number_input("Loan Term (Years)", min_value=1, value=30)

#Calculate mortgage amount after subtracting the deposit
loan_amount = home_value - deposit
#Convert annual interest percentage to monthly decimal rate
monthly_interest_rate = interest_rate / 100 / 12
#Convert loan term from years to total number of monthly payments
number_of_payments = loan_term * 12
#Check calculated mortgage amount is 0 or negative
if loan_amount <= 0:
    #Set monthly payment to 0 if the loan amount is required
    monthly_payment = 0.0
#Check monthly interest rate is 0
elif monthly_interest_rate == 0:
    #Divide loan amount by number of payments to get monthly payment
    monthly_payment = loan_amount / number_of_payments
#Calculate monthly payment when interest rate is greater than 0
else:
    monthly_payment = (
        loan_amount
        * monthly_interest_rate
        * (1 + monthly_interest_rate) ** number_of_payments
        / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    )

# Calculate total payment and total interest
total_payment = monthly_payment * number_of_payments
#Calculate total interest by subtracting original loan amount
total_interest = total_payment - loan_amount
#Display heading for the payment summary
st.write("### Payments")
#Divide payment summary into 3 columns 
col1, col2, col3 = st.columns(3)
col1.metric(label = "Monthly Payments ($)", value = f"{monthly_payment:,.2f}")
col2.metric(label = "Total Payments ($)", value = f"{total_payment:,.0f}")
col3.metric(label = "Total Interest ($)", value = f"{total_interest:,.0f}")

#Create a DataFrame with the payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)
    schedule.append([i, monthly_payment, 
                     principal_payment, 
                     interest_payment, 
                     remaining_balance, 
                     year])

df = pd.DataFrame(schedule, columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],)    

#Display DataFrame as a chart
st.write("### Remaining Mortgage Balance by Year")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.bar_chart(payments_df)