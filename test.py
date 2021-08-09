from datetime import datetime, timedelta

a = datetime(2020,1,1)
todays_date = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")
print(a.day, todays_date.day)
