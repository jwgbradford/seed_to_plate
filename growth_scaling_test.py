max_temp = 21
min_temp = -2
ideal_temp = 10
current_temp =0

if current_temp > ideal_temp:
    high_growth_rate_decay = (max_temp - ideal_temp)
    print('high', high_growth_rate_decay)
    today_temp_growth = 1 - ((current_temp - ideal_temp) / high_growth_rate_decay)
    print('todays growth', today_temp_growth)
elif current_temp < ideal_temp:
    low_growth_rate_decay = (ideal_temp - min_temp)
    print('low', low_growth_rate_decay)
    today_temp_growth = 1 - ((ideal_temp - current_temp) / low_growth_rate_decay)
    print('todays growth', today_temp_growth)
else:
    temp_growth_rate = 1
