import pandas as pd

# 1. Generate Simulated Meta Ads Export Structure
meta_data = {
    'Campaign Name': ['BOF_Retargeting_Purchase', 'TOF_Lookalike_Prospecting', 'MOF_Engagement'],
    'Amount Spent (USD)': [650.00, 450.00, 150.00],
    'Purchases': [25, 12, 0],
    'Purchase ROAS (Return on Ad Spend)': [3.8, 1.9, 0.0]
}

df_meta = pd.DataFrame(meta_data)
df_meta.to_csv('mock_meta_export.csv', index=False)
print("✅ Created mock_meta_export.csv")

# 2. Generate Simulated Google Ads Export Structure
google_data = {
    'Campaign': ['Search_Brand_Alpha', 'PerformanceMax_US', 'Display_Remarketing'],
    'Cost': [350.00, 420.00, 80.00],
    'Conversions': [45.0, 18.5, 2.0],
    'Conversion value': [1520.00, 1280.00, 90.00]
}

df_google = pd.DataFrame(google_data)
df_google.to_csv('mock_google_export.csv', index=False)
print("✅ Created mock_google_export.csv")