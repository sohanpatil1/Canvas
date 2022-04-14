import datetime
from datetime import date
import pytz
from canvasapi import Canvas

def readcourse(course,datetoday,timenow):   
    for assignment in course.get_assignments():
        duedate = assignment.due_at
        if duedate is not None:
            duedate = convertime(duedate)
            print("Date: ",assignment.due_at)
            print("PST Date: ",duedate)
            print(course.name," : ",assignment," ",duedate)

def convertime(duedate):    
    #Convert ISO 8601 to PST Credit: https://remembertheview.com/2020/01/07/date-time-conversion-in-python-iso-8601-utc-to-pacific-standard-time/
    
    pst = pytz.timezone('US/Pacific')
    #create the time variable date_time that will be used throughout, the data is coming from an api request and I am getting back json data.
    date_time = duedate
    #set the format for the date time
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ")
    #tell python the current timezone is UTC
    date_time = pytz.timezone('UTC').localize(date_time)
    #tell python to change the timezone to Pacific
    date_time = date_time.astimezone(pst)
    #update the variable with the new time and date in the new format
    date_time = date_time.strftime('%m-%d-%y %H:%M:%S')
    return date_time


API_URL = "https://canvas.ucdavis.edu"
API_KEY = "3438~WmzXhpREXRr3EuTB7dkCHAQIJfbxcWLKihHMAQLXDnF2jqa0D6AqKiV1Cl4f8ZED"
canvas = Canvas(API_URL, API_KEY)
ECS152 = 682756
ECS162A = 678782
SAS25V = 663974
STA106 = 678534
# courselist = [ECS152,ECS162A,SAS25V,STA106]
courselist = [ECS152,ECS162A]
for i in courselist:
    course = canvas.get_course(i)
    datetoday = date.today().strftime('%d-%m-%Y')
    timenow = datetime.datetime.now() 
    current_time_date = str(datetoday) + " "+timenow.strftime("%H:%M:%S")
    print("The current time and date is : ",current_time_date)
    readcourse(course,datetoday, timenow)
    