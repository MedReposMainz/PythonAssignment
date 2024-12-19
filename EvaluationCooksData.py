# This program is to evaluate the data of 100 cooks and output the results as a diagramm 
# Programmer: Angela Sterk
# 16.12.2024

#-----Import Libraries--------------------------
import random as rn 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime 

#----------------------------------------------------------------------
#                          Main Program
#----------------------------------------------------------------------

# Import Dataset
CookDat = pd.read_excel("cooks_data.xlsx")

# Since there is no column for sex, I will add this radomly using a loop, by first initializing the "Sex" column with empty values
# I will set a random seed to ensures the random choices are the same every time the code is excuted
rn.seed(42)  

# Here it will be checked if the 'Sex' column is already in the dataset and only generate values if column doesn't exist
if "Sex" not in CookDat.columns or CookDat["Sex"].isnull().all():  
    sex_options = ["Male", "Female"]
    # Generate random 'Sex' values for each cook in the dataset
    CookDat["Sex"] = [rn.choice(sex_options) for _ in range(len(CookDat))]

# Calculate Age using a defined function
def calculated_age(dob, doi):
    return (doi - dob).days // 365

CookDat["InterviewDate"] = pd.to_datetime(CookDat["InterviewDate"])
CookDat["DateOfBirth"] = pd.to_datetime(CookDat["DateOfBirth"])
CookDat["Age"] = CookDat.apply(lambda row: calculated_age(row["DateOfBirth"], row["InterviewDate"]), axis=1)

# Calculate BMI using: BMI = weight (kg) / height (m)^2, I will roundup to 2 decimal places
CookDat["BMI"] = (CookDat["Weight"] / (CookDat["Height"] ** 2)).round(2)

# Define a function to categorize BMI
def BMIGroup(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25.0 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"
    
# Apply the function to the BMI column
CookDat["BMICategory"] = CookDat["BMI"].apply(BMIGroup)

# Assign risk levels
for j, row in CookDat.iterrows():
    if row["BMICategory"] == "Obese" and row["PhysicalActivity"] == "No":
        CookDat.at[j, "Risk Level"] = "High Risk"
    elif row["BMICategory"] == "Obese" and row["PhysicalActivity"] == "Yes":
        CookDat.at[j, "Risk Level"] = "Moderate Risk"
    elif row["BMICategory"] != "Obese" and row["PhysicalActivity"] == "No":
        CookDat.at[j, "Risk Level"] = "Low Risk"
    elif row["BMICategory"] != "Obese" and row["PhysicalActivity"] == "Yes":
        CookDat.at[j, "Risk Level"] = "No Risk"

# Now am going to randomly add the work location of each cook using an array
#WorkingField = ["Restaurant", "Hotel", "Catering", "Food Truck", "Private Chef"]

# Assign random working field
#CookDat["Working Field"] = np.random.choice(WorkingField, size=len(CookDat))

# Check if 'Working Field' column exists and is empty
np.random.seed(42)

if "Working Field" not in CookDat.columns or CookDat["Working Field"].isnull().all():
    WorkingField = ["Restaurant", "Hotel", "Catering", "Food Truck", "Private Chef"]
    # Assign random 'Working Field' values for each cook in the dataset
    CookDat["Working Field"] = np.random.choice(WorkingField, size=len(CookDat))

# Save the updated dataset 
CookDat.to_excel("CookDat.xlsx", index=False)

#---------------- Create two diagramms --------------------------------------------

# . Bar Chart: Count the number of cooks in each working field by sex
FieldSexCounts = CookDat.groupby(['Working Field', 'Sex']).size().unstack(fill_value=0)

# 2. Pie Chart: Proportion of Working field
BmiCounts = CookDat['BMICategory'].value_counts()

# Create a figure with enough space for both charts
fig, ax = plt.subplots(1, 2, figsize=(14, 7))

# Plot the Bar Chart (on the left)
FieldSexCounts.plot(kind='bar', ax=ax[0], color=['darkred', 'darkblue'])
ax[0].set_title('Number of Cooks in Different Working fields by sex', fontsize=12, fontweight='bold')
ax[0].set_xlabel('Working Field', fontsize=12)
ax[0].set_ylabel('Number of Cooks', fontsize=12)
ax[0].tick_params(axis='x', rotation=45)
# Add gridlines to the bar chart (y-axis)
ax[0].grid(True, axis='y', linestyle='--', linewidth=0.7)

# Plot the Pie Chart (on the right)
ax[1].pie(BmiCounts, labels=BmiCounts.index, autopct='%1.1f%%', colors=['green', 'violet'])
ax[1].set_title('Proportion of cooks in each BMI Categories', fontsize=12, fontweight='bold')

# Display the chart
plt.tight_layout()  
plt.show()


