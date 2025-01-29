import pandas as pd
from sqlalchemy import create_engine
import os

DB_HOST = os.getenv("DB_HOST", "db")  # Using 'db' as defined in docker-compose
DB_NAME = os.getenv("DB_NAME", "employee_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mysecretpassword")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)
print("Database connection successful!")


# Load CSV files
df_emp = pd.read_csv("employee_details.csv")
df_salary = pd.read_csv("employee_salary.csv")

# Merge datasets on EmployeeID
df = pd.merge(df_emp, df_salary, on="EmployeeID", how="left")
print(df.head())

# Handle Missing Values
print(df.isnull().sum())  # Shows the number of missing values per column
#there is nothing nulls


# Remove duplicates
df.drop_duplicates(inplace=True)
print(df.info())
# Convert date columns to YYYY-MM-DD format
for col in ["DateOfJoining", "SalaryStartDate"]:
    df[col] =pd.to_datetime(df[col], errors="coerce") #.dt.strftime("%Y-%m-%d")



# # Calculate Salary Growth Percentage
df["SalaryGrowthPercentage"] = df.groupby("EmployeeID")["Salary"].pct_change().fillna(0) * 100
print(df)
# # Filter employees with PerformanceRating >= 3
df = df[df["PerformanceRating"] >= 3]

# # Select relevant columns
df_final = df[["EmployeeID", "Name", "DateOfJoining", "Salary", "PerformanceRating", "SalaryGrowthPercentage"]]
df_final.rename(columns={"Salary": "CurrentSalary"}, inplace=True)
# Load into PostgreSQL database
engine = create_engine(DATABASE_URL)
print("Engine creation are done")
df_final.to_sql("employees", engine, if_exists="replace", index=False)

print("Data successfully loaded into PostgreSQL!")
