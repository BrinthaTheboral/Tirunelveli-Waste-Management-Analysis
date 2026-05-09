from scipy.stats import f_oneway
print("="*60)
print("OBJECTIVE 5 - ASSUMPTION CHECK")
print("="*60)
locations = ['Thachanallur', 'Town', 'Palayankottai', 'Melapalayam']
location_cr = {}
for loc in locations:
    mud_col = f'Mud_{loc}'
    nonbio_col = f'Nonbio_{loc}'
    df[f'CR_{loc}'] = df[mud_col] / (df[nonbio_col] + 1)
    location_cr[loc] = df[f'CR_{loc}'].dropna()
f_stat, p_anova = f_oneway(*location_cr.values())
print(f"ANOVA test (CR across locations): F={f_stat:.3f}, p={p_anova:.5f}")
if p_anova < 0.05:
    print("✓ Locations have SIGNIFICANTLY different contamination levels")
    print("→ Intervention should be LOCATION-SPECIFIC\n")
else:
    print("✗ No significant difference → Uniform intervention may work\n")
print("="*60)
print("OBJECTIVE 5 - LOCATION-WISE ANALYSIS")
print("="*60)
for loc in locations:
    avg_cr = df[f'CR_{loc}'].mean()
    total_nonbio = df[f'Nonbio_{loc}'].sum()
    loss = df.apply(lambda row: row[f'Nonbio_{loc}'] if row[f'CR_{loc}'] > 0.15 else 0, axis=1).sum()
    print(f"\n{loc}:")
    print(f"  Avg Contamination: {avg_cr:.3f}")
    print(f"  Total Non-bio: {total_nonbio:,.0f} kg")
    print(f"  Recyclable loss: {loss:,.0f} kg")
    print(f"  Priority: {'HIGH' if loss > 500000 else 'MEDIUM' if loss > 200000 else 'LOW'}")
print("\n" + "="*60)
print("DATA-DRIVEN RECOMMENDATIONS")
print("="*60)
df['Month_Name'] = df['Date'].dt.month_name()
monthly_loss = df.groupby('Month_Name')['Recyclable_Loss_0.15'].sum()
worst_month = monthly_loss.idxmax()
print(f"\n1. TIME-SPECIFIC:")
print(f"   → Highest contamination in: {worst_month}")
print(f"   → Intensify segregation campaigns during {worst_month}")
print(f"\n2. LOCATION-SPECIFIC:")
worst_loc = max(locations, key=lambda x: df[f'CR_{x}'].mean())
print(f"   → Most critical location: {worst_loc}")
print(f"   → Deploy additional segregation staff here")
print(f"\n3. QUANTIFIED BENEFIT:")
current_loss = df['Recyclable_Loss_0.15'].sum()
if current_loss > 0:
    potential_recovery = current_loss * 0.6  # 60% recovery if segregation improves
    print(f"   → Current recyclable loss: {current_loss:,.0f} kg")
    print(f"   → Potential recovery (60%): {potential_recovery:,.0f} kg")
    print(f"   → Financial benefit: ₹{potential_recovery * 15:,.2f}")
print(f"\n4. IMMEDIATE ACTIONS:")
print(f"   ✓ Door-to-door segregation awareness in {worst_loc}")
print(f"   ✓ Weekly contamination monitoring dashboard")
print(f"   ✓ Separate C&D waste collection to reduce mud entry")

