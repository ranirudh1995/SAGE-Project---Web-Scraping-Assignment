import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from dateutil.parser import parse

def is_leap_year(year):
    return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)

# source :- https://stackoverflow.com/questions/18325705/printing-the-number-of-days-in-a-given-month-and-year-python
def days_in_month(month, year):
    if month == 9 or month == 4 or month == 6 or month == 11:
        result=30
    elif month == 1 or month == 3 or month == 5 or month== 7 or month == 8 or month == 10 or month== 12:
        result=31
    elif month == 2 and is_leap_year(year) ==True:
        result=29
    elif month == 2 and is_leap_year(year) == False:
        result=28
    return result

year = 2019

url = 'https://en.wikipedia.org/wiki/'+str(year)+'_in_spaceflight#Orbital_launches'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find('table',["wikitable", "collapsible", "mw-collapsible" ,"mw-made-collapsible"])

dic = {}
payloadValid = False
payloadStatus = {"successful", "operational", "en route"}
date = ""
for row in table.findAll("tr"):
    cells = row.findAll("td")
    length = len(cells)
    if length==5:
        date = ""
        payloadValid = False
        date = cells[0].find('span').text
        date = sorted(date.strip().split()) # sorting to make sure that the date is [dd] [mm] [yy] format
        date.append(str(year))
        date = " ".join(date) 
        try:
            date = parse(date).isoformat()
        except Exception as e: # errors with date format (for example:- 29 August (ground test)[164])
            continue
    elif length==6:
        text = cells[5].text.strip().lower()
        if (not payloadValid) and (text in payloadStatus):
            payloadValid = True
            if date not in dic:
                dic[date] = 1
            else:
                dic[date]+=1
    
    #time.sleep(0.005) # pause the code for 0.005 seconds to avoid the possibility of being flagged as a spammer. 
        

file = open("output_"+str(year)+".csv", "w")
file.write("date, value\n")
for month in range(1,13):
    for day in range(1,days_in_month(month, year)+1):
        date = str(month)+"-"+str(day)+"-"+str(year)
        date = parse(date).isoformat()
        if date in dic:
            file.write(date+", "+str(dic[date])+"\n")
        else:
            file.write(date+", 0\n")
file.close()