# # following code is used to fetch the data and store to a file
# from nsepy import get_history
# from datetime import date
# data = get_history(symbol="NIFTY", index = True, start=date(1995,11,3), end=date(2020,11,1))
# data.to_csv("Nifty_historical.csv")

import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

df = pd.read_csv('Nifty_historical.csv')
startDateList = df.iloc[0].Date.split('-')
endDateList = df.iloc[df.shape[0] - 1].Date.split('-')

startYear = int(startDateList[0])
startMonth = int(startDateList[1])
startDay = int(startDateList[2])

endYear = int(endDateList[0])
endMonth = int(endDateList[1])
endDay = int(endDateList[2])

startDate = date(startYear, startMonth, startDay)
endDate = date(endYear, endMonth, endDay)

if startDate.weekday() != 0:
    skipDays = 7 - startDate.weekday()
    startDate = startDate + timedelta(days=skipDays)

expDate = startDate + timedelta(days=11)

dateDiff = relativedelta(endDate, expDate)

location = 0
devLT3 = 0
devLT6 = 0
devGT6 = 0

while dateDiff.years > 0 or dateDiff.months > 0 or dateDiff.days > 0:
    if df.iloc[location].Date == str(startDate):
        startTrade = df.iloc[location].Open
        endTrade = df.iloc[location + 9].Close
        
        diff = startTrade - endTrade
        if diff < 0:
            diff *= -1

        deviation = (diff * 100) / startTrade

        if deviation < 3:
            devLT3 += 1
        elif deviation < 6:
            devLT6 += 1
        else:
            devGT6 += 1


        startDate = startDate + timedelta(days=7)

        while str(startDate) not in map(str, df.Date):
            startDate = startDate + timedelta(days=7)
            
        expDate = startDate + timedelta(days=11)
        dateDiff = relativedelta(endDate, expDate)
        
    location += 1

totalObs = devLT3 + devLT6 + devGT6

devLT3Per = (devLT3 / totalObs) * 100
devLT6Per = (devLT6 / totalObs) * 100
devGT6Per = (devGT6 / totalObs) * 100

print(r'Less Than 3% deviation: ' + str(devLT3Per) + '%')
print(r'Less Than 6% deviation: ' + str(devLT6Per) + '%')
print(r'Greater Than 6% deviation: ' + str(devGT6Per) + '%')

