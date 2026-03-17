print("=" * 70)
print("STRATEGY COMPARISON: SELL & SPLIT vs HELOC vs KEEP")
print("=" * 70)
print()

# Base numbers
net_proceeds_after_tax = 157034  # From selling
annual_negative_cash_flow = -6448

# STRATEGY 1: SELL AND SPLIT (50% stocks, 50% new property)
print("STRATEGY 1: SELL & SPLIT")
print("-" * 40)
stock_investment = net_proceeds_after_tax / 2
property_down_payment = net_proceeds_after_tax / 2

# Stock returns
annual_stock_return = 0.07
stock_5yr = stock_investment * (1.07 ** 5)
stock_income_5yr = stock_5yr - stock_investment

# New property scenario
new_property_price = property_down_payment / 0.20  # 20% down
new_loan = new_property_price * 0.80
new_rate = 0.0622
new_monthly_payment = new_loan * (new_rate/12) * (1 + new_rate/12)**360 / ((1 + new_rate/12)**360 - 1)

print(f"Stock Investment: ${stock_investment:,.2f}")
print(f"5-Year Stock Value: ${stock_5yr:,.2f}")
print(f"Stock Gains: ${stock_income_5yr:,.2f}")
print()
print(f"New Property Purchase: ${new_property_price:,.2f}")
print(f"Down Payment: ${property_down_payment:,.2f}")
print(f"New Loan: ${new_loan:,.2f}")
print(f"New Monthly Payment: ${new_monthly_payment:,.2f}")
print(f"5-Year Total Gain: ${stock_income_5yr:,.2f}")
print()

# STRATEGY 2: HELOC FOR INVESTMENTS
print("STRATEGY 2: HELOC (Home Equity Line of Credit)")
print("-" * 40)
max_heloc = 230000 * 0.80 - 29157  # 80% LTV minus current mortgage
heloc_amount = 100000  # Conservative amount
heloc_rate = 0.085  # Current HELOC rates ~8.5%
heloc_monthly_payment = heloc_amount * heloc_rate / 12  # Interest-only typical

# Invest HELOC in stocks
heloc_stock_5yr = heloc_amount * (1.07 ** 5)
heloc_cost_5yr = heloc_monthly_payment * 60
heloc_net_gain = heloc_stock_5yr - heloc_amount - heloc_cost_5yr

print(f"Maximum HELOC Available: ${max_heloc:,.2f}")
print(f"HELOC Amount (conservative): ${heloc_amount:,.2f}")
print(f"HELOC Rate: {heloc_rate*100:.1f}%")
print(f"Monthly HELOC Payment: ${heloc_monthly_payment:,.2f}")
print()
print(f"Invest in Stocks: ${heloc_amount:,.2f}")
print(f"5-Year Stock Value: ${heloc_stock_5yr:,.2f}")
print(f"5-Year HELOC Cost: ${heloc_cost_5yr:,.2f}")
print(f"Net Gain After HELOC Cost: ${heloc_net_gain:,.2f}")
print(f"Keep Property Appreciation: ${230000 * 0.03 * 5:,.2f}")
print(f"Total with keeping property: ${heloc_net_gain + 34500:,.2f}")
print()

# STRATEGY 3: KEEP AS IS (Status Quo)
print("STRATEGY 3: KEEP AS IS (Continue Negative Cash Flow)")
print("-" * 40)
keep_5yr_loss = annual_negative_cash_flow * 5
keep_appreciation = 230000 * (1.03 ** 5) - 230000
keep_net = keep_appreciation + keep_5yr_loss

print(f"5-Year Cash Flow Loss: ${keep_5yr_loss:,.2f}")
print(f"Property Appreciation (3% annual): ${keep_appreciation:,.2f}")
print(f"Net Position: ${keep_net:,.2f}")
print()

# STRATEGY 4: RAISE RENT
print("STRATEGY 4: RAISE RENT TO BREAK EVEN")
print("-" * 40)
breakeven_rent = 1637.33
rent_increase_needed = breakeven_rent - 1100
percent_increase = (rent_increase_needed / 1100) * 100

print(f"Current Rent: $1,100")
print(f"Break-even Rent Needed: ${breakeven_rent:.2f}")
print(f"Increase Needed: ${rent_increase_needed:.2f} ({percent_increase:.1f}%)")
print(f"Market Rent Range: $1,400-$1,700")
print(f"Could raise to: $1,500 (market rate)")
new_cash_flow = 1500 - 1637.33
print(f"Cash flow at $1,500: ${new_cash_flow:.2f}/month")
print(f"Still negative but better: ${new_cash_flow * 12:,.2f}/year")
print()

print("=" * 70)
print("FINAL RANKING (5-YEAR NET GAIN):")
print("=" * 70)
strategies = [
    ("Sell & Invest 50/50", stock_income_5yr),
    ("HELOC + Keep Property", heloc_net_gain + 34500),
    ("Raise Rent + Keep", keep_net + (400*12*5)),  # Assuming partial rent increase
    ("Keep As Is", keep_net),
]

for i, (name, value) in enumerate(sorted(strategies, key=lambda x: x[1], reverse=True), 1):
    print(f"{i}. {name}: ${value:,.2f}")
