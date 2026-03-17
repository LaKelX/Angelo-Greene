# Comprehensive scenario analysis over 5 years

# Current situation
current_value = 230000  # Moderate estimate
equity = 213573
mortgage_payment = 252.88
hoa = 345
property_tax_monthly = 417.83
insurance = 75
total_monthly = mortgage_payment + hoa + property_tax_monthly + insurance

# Market predictions
annual_appreciation = 0.03  # 3% conservative SA growth
annual_hoa_increase = 0.026  # Historical 2.6% annual
annual_rent_increase = 0.03  # 3% annual

# Scenario 1: HOLD AND LIVE IN IT
hold_5yr_value = current_value * (1 + annual_appreciation)**5
hold_5yr_equity = hold_5yr_value - (64000 * 0.35)  # Approximate remaining balance
hold_5yr_costs = sum([total_monthly * 12 * (1 + annual_hoa_increase/4)**year for year in range(5)])

# Scenario 2: SELL NOW AND INVEST
sell_proceeds = equity - (current_value * 0.08)  # After transaction costs
invest_5yr_stocks = sell_proceeds * (1.07)**5  # 7% annual return
invest_5yr_bonds = sell_proceeds * (1.05)**5  # 5% annual return
rent_costs_5yr = sum([1600 * 12 * (1.03)**year for year in range(5)])  # Renting elsewhere

# Scenario 3: HOLD AND RENT OUT
rental_income = 1550  # Moderate rent
rent_5yr_income = sum([rental_income * 12 * (1 + annual_rent_increase)**year for year in range(5)])
rent_5yr_costs = sum([total_monthly * 12 * (1 + annual_hoa_increase/4)**year for year in range(5)])
rent_5yr_profit = rent_5yr_income - rent_5yr_costs
rent_5yr_value = current_value * (1 + annual_appreciation)**5
rent_5yr_total = rent_5yr_profit + rent_5yr_value

# Scenario 4: WAIT FOR "CRASH" AND REBUY
crash_discount = 0.10  # Assuming 10% crash (unlikely per experts)
wait_value = current_value * (1 - crash_discount)
rebuy_cost = wait_value * 1.02  # 2% buying costs
new_mortgage = rebuy_cost * 0.8 * 0.0626 / 12 / (1 - (1.0626/12)**(-360))
mortgage_increase = (new_mortgage - mortgage_payment) * 60  # 5 years of higher payments

print('=== 5-YEAR SCENARIO ANALYSIS ===')
print()
print('SCENARIO 1: HOLD AND LIVE IN IT')
print(f'Current Value: ${current_value:,}')
print(f'Value in 5 Years (3% annual): ${hold_5yr_value:,.2f}')
print(f'Equity in 5 Years: ${hold_5yr_equity:,.2f}')
print(f'Total Housing Costs (5 years): ${hold_5yr_costs:,.2f}')
print(f'Net Position: ${hold_5yr_equity - hold_5yr_costs:,.2f}')
print()
print('SCENARIO 2: SELL NOW AND INVEST')
print(f'Sale Proceeds (after costs): ${sell_proceeds:,.2f}')
print(f'Stock Portfolio (7% annual): ${invest_5yr_stocks:,.2f}')
print(f'Bond Portfolio (5% annual): ${invest_5yr_bonds:,.2f}')
print(f'Rent Costs (5 years): ${rent_costs_5yr:,.2f}')
print(f'Net Position (Stocks): ${invest_5yr_stocks - rent_costs_5yr:,.2f}')
print()
print('SCENARIO 3: HOLD AND RENT OUT')
print(f'Rental Income (5 years): ${rent_5yr_income:,.2f}')
print(f'Operating Costs (5 years): ${rent_5yr_costs:,.2f}')
print(f'Cash Flow Profit: ${rent_5yr_profit:,.2f}')
print(f'Property Value in 5 Years: ${rent_5yr_value:,.2f}')
print(f'Total Return: ${rent_5yr_profit + (rent_5yr_value - current_value):,.2f}')
print()
print('SCENARIO 4: TRY TO TIME THE MARKET')
print(f'Hoped-for Crash Price (-10%): ${wait_value:,}')
print(f'Transaction Costs Round-Trip: ${current_value * 0.08 + wait_value * 0.02:,.2f}')
print(f'New Mortgage Payment (6.26%): ${new_mortgage:.2f}')
print(f'Additional Interest Cost (5 years): ${mortgage_increase:,.2f}')
print(f'Net Loss from Timing Attempt: ${-(current_value * 0.08 + wait_value * 0.02 + mortgage_increase):,.2f}')
print()
print('=== RECOMMENDATION RANKING ===')
scenarios = [
    ('Hold & Rent Out', rent_5yr_profit + (rent_5yr_value - current_value)),
    ('Hold & Live In', hold_5yr_equity - hold_5yr_costs),
    ('Sell & Invest (Stocks)', invest_5yr_stocks - rent_costs_5yr),
    ('Try to Time Market', -(current_value * 0.08 + wait_value * 0.02 + mortgage_increase))
]
for i, (name, value) in enumerate(sorted(scenarios, key=lambda x: x[1], reverse=True), 1):
    print(f'{i}. {name}: ${value:,.2f}')
