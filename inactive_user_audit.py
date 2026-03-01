import pandas as pd
from datetime import datetime

# 1. Load the CSV file
df = pd.read_csv("sap_user_logon_export.csv")

# 2. Convert LastLogon column to datetime
df["LastLogon"] = pd.to_datetime(df["LastLogon"])

# 3. Calculate inactivity days
today = datetime.today()
df["DaysInactive"] = (today - df["LastLogon"]).dt.days

# 4. Remove System and Communication users
df = df[~df["UserType"].isin(["System", "Communication"])]

# 5. Remove already locked users
df = df[df["Locked"] == "No"]

# 6. Flag users inactive more than 90 days
df["InactiveFlag"] = df["DaysInactive"] > 90

# 7. Flag high-risk roles
df["HighRiskRole"] = df["Role"].str.contains("SAP_ALL|ADMIN", case=False, na=False)

# 8. Keep only users needing review
review_df = df[(df["InactiveFlag"] == True) | (df["HighRiskRole"] == True)]

# 9. Export the report
review_df.to_excel("lock_recommendation_report.xlsx", index=False)

print("Lock Recommendation Report Generated Successfully.")