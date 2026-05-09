from scipy.stats import levene, ttest_ind
df['CR'] = df['Mud_Total'] / (df['Nonbio_Total'] + 1)
high_seg = df[df['SEI'] > df['SEI'].quantile(0.75)]
low_seg = df[df['SEI'] <= df['SEI'].quantile(0.25)]
print("="*60)
print("OBJECTIVE 3 - ASSUMPTION CHECK")
print("="*60)
stat_levene, p_levene = levene(high_seg['CR'], low_seg['CR'])
print(f"Levene's test for equal variance: p={p_levene:.5f}")
if p_levene < 0.05:
    print("✓ Variances are NOT equal → Using Welch's t-test")
    t_stat, p_value = ttest_ind(high_seg['CR'], low_seg['CR'], equal_var=False)
else:
    print("✓ Variances are equal → Using standard t-test")
    t_stat, p_value = ttest_ind(high_seg['CR'], low_seg['CR'], equal_var=True)
print("\n" + "="*60)
print("OBJECTIVE 3 - RESULTS")
print("="*60)
print(f"High Segregation Days - Avg Contamination Ratio: {high_seg['CR'].mean():.4f}")
print(f"Low Segregation Days - Avg Contamination Ratio: {low_seg['CR'].mean():.4f}")
print(f"T-statistic: {t_stat:.3f}")
print(f"P-value: {p_value:.5f}")
if p_value < 0.05:
    print("\n✓ STATISTICALLY SIGNIFICANT (p<0.05)")
    print("→ Poor segregation leads to HIGHER mud contamination in non-bio waste")
    print("→ Recycling efficiency is directly impacted")
else:
    print("\n✗ Not statistically significant")
total_nonbio = df['Nonbio_Total'].sum()
estimated_clean_nonbio = total_nonbio * (1 - low_seg['CR'].mean())
print(f"\nEstimated Recyclable Non-bio waste (if segregation improved): {estimated_clean_nonbio:,.0f} kg")
print(f"Current contaminated non-bio waste: {total_nonbio:,.0f} kg")
print(f"Loss due to contamination: {total_nonbio - estimated_clean_nonbio:,.0f} kg")
