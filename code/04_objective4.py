thresholds = [0.10, 0.15, 0.20]
print("=" * 60)
print("OBJECTIVE 4 - RESULTS")
print("=" * 60)
print("SENSITIVITY ANALYSIS - Different Contamination Thresholds")
print("-" * 60)
for threshold in thresholds:
    df[f'Recyclable_Loss_{threshold}'] = df.apply(
        lambda row: row['Nonbio_Total'] if row['CR'] > threshold else 0, axis=1
    )
    total_loss = df[f'Recyclable_Loss_{threshold}'].sum()
    days_lost = (df['CR'] > threshold).sum()
    print(f"\nThreshold: CR > {threshold}")
    print(f"  Total non-bio waste: {df['Nonbio_Total'].sum():,.0f} kg")
    print(f"  Recyclable loss: {total_loss:,.0f} kg")
    print(f"  Percentage loss: {(total_loss / df['Nonbio_Total'].sum()) * 100:.1f}%")
    print(f"  Days with contaminated non-bio: {days_lost} days")
recycling_value_per_kg = 15  
financial_loss = df['Recyclable_Loss_0.15'].sum() * recycling_value_per_kg
print("\n" + "="*60)
print("FINANCIAL IMPACT (₹15/kg recycling value)")
print("="*60)
print(f"Total estimated recyclable value lost: ₹{financial_loss:,.2f}")
print(f"Equivalent to: ₹{financial_loss/100000:.2f} Lakhs")
df['Week'] = df['Date'].dt.isocalendar().week
weekly_loss = df.groupby('Week')['Recyclable_Loss_0.15'].sum()
print("\nTop 5 weeks with highest recyclable loss:")
print(weekly_loss.nlargest(5))
plt.figure(figsize=(12,5))
plt.bar(weekly_loss.index, weekly_loss.values, color='crimson', alpha=0.7)
plt.xlabel('Week Number')
plt.ylabel('Recyclable Loss (kg)')
plt.title('Weekly Recyclable Loss Due to Contamination')
plt.axhline(y=weekly_loss.mean(), color='blue', linestyle='--', label=f'Mean: {weekly_loss.mean():.0f} kg')
plt.legend()
plt.tight_layout()
plt.savefig('Objective4_Weekly_Loss.png', dpi=300)
plt.show()
