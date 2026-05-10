import pandas as pd
import numpy as np
from scipy.stats import pearsonr
df = pd.read_csv("Sustainable Waste Data (Tirunelveli District).csv") #Data was not added because it is confidential.
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])
waste_cols = [c for c in df.columns if c != 'Date']
df[waste_cols] = df[waste_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
df['SEI'] = df['Bio_Total'] / (df['Bio_Total'] + df['Nonbio_Total'] + 1)
df['NBR'] = df['Nonbio_Total'] / (df['Bio_Total'] + 1)
def classify_segregation(row):
    if row['SEI'] > 0.3:
        return "Good Segregation"
    elif row['NBR'] > 2:
        return "Poor Segregation"
    else:
        return "Moderate Segregation"
df['Segregation_Status'] = df.apply(classify_segregation, axis=1)
corr, p_value = pearsonr(df['Bio_Total'], df['Nonbio_Total'])
print("="*60)
print("OBJECTIVE 1 - ASSUMPTION CHECK")
print("="*60)
print(f"Assumption: Bio and Non-bio should be independent if segregation works")
print(f"Pearson Correlation between Bio and Non-bio: {corr:.3f}")
print(f"P-value: {p_value:.5f}")
if p_value < 0.05:
    if corr > 0:
        print("✓ Correlated (p<0.05) → Waste is MIXED → Poor Segregation Confirmed")
    else:
        print("✓ Negative correlation → Some segregation exists")
else:
    print("✓ No correlation → Segregation might be working")
print("\n" + "="*60)
print("OBJECTIVE 1 - RESULTS")
print("="*60)
print(f"Average Segregation Efficiency Index (SEI): {df['SEI'].mean():.3f}")
print(f"Average Non-bio to Bio Ratio (NBR): {df['NBR'].mean():.2f}")
print("\nSegregation Status Distribution:")
print(df['Segregation_Status'].value_counts())
print(f"\nPercentage of Days with Poor Segregation: {(df['Segregation_Status']=='Poor Segregation').mean()*100:.1f}%")
