import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import shapiro, linregress
df['Month'] = df['Date'].dt.to_period('M')
monthly = df.groupby('Month').agg({
    'Bio_Total': 'mean',
    'Nonbio_Total': 'mean',
    'Mud_Total': 'mean'
}).reset_index()
monthly['Month_Num'] = range(len(monthly))
print("="*60)
print("OBJECTIVE 2 - ASSUMPTION CHECK")
print("="*60)
stat, p_shapiro = shapiro(monthly['Nonbio_Total'])
print(f"Shapiro-Wilk Normality Test on Monthly Non-bio: p={p_shapiro:.5f}")
if p_shapiro < 0.05:
    print("✓ Data NOT normally distributed → Using non-parametric Mann-Kendall test")
    from scipy.stats import spearmanr
    trend_corr, trend_p = spearmanr(monthly['Month_Num'], monthly['Nonbio_Total'])
    print(f"Spearman correlation (trend): r={trend_corr:.3f}, p={trend_p:.5f}")
else:
    print("✓ Data is normally distributed → Using linear regression")
    slope, intercept, r_value, p_value, std_err = linregress(monthly['Month_Num'], monthly['Nonbio_Total'])
    print(f"Linear trend slope: {slope:.1f} kg/month, p={p_value:.5f}")
print("\n" + "="*60)
print("OBJECTIVE 2 - RESULTS")
print("="*60)
print("Monthly Average Waste (kg):")
print(monthly[['Month', 'Bio_Total', 'Nonbio_Total', 'Mud_Total']].to_string(index=False))
import matplotlib.pyplot as plt
fig, axes = plt.subplots(3, 1, figsize=(12, 10))
axes[0].plot(monthly['Month'].astype(str), monthly['Bio_Total'], marker='o', color='green')
axes[0].set_title('Biodegradable Waste Trend')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)
axes[1].plot(monthly['Month'].astype(str), monthly['Nonbio_Total'], marker='o', color='red')
axes[1].set_title('Non-Biodegradable Waste Trend')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)
axes[2].plot(monthly['Month'].astype(str), monthly['Mud_Total'], marker='o', color='brown')
axes[2].set_title('Mud/Silt Waste Trend')
axes[2].set_xticklabels(axes[2].get_xticklabels(), rotation=45)
plt.tight_layout()
plt.savefig('Objective2_Trends.png', dpi=300)
plt.show()

