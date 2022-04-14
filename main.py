import datetime
from datetime import date
import pytz
from canvasapi import Canvas
from twilio.rest import Client 


def readcourse(course,datetoday,timenow):   #object,str,str
    output=""
    for assignment in course.get_assignments():        
        duedate = assignment.due_at
        if duedate is not None:
            due = convertime(duedate)
            duedate,duetime = due.split()
            print("Date: ",assignment.due_at)
            print("PST Date: ",duedate," and time: ",duetime)
            print(course.name," : ",assignment," ",duedate)
            print("Duedate: ",duedate," and Datetoday: ",datetoday)
            if(duedate < datetoday):
                print("Passed deadline by ")
            else:
                days,hour = duesoon(duedate,duetime)
                if(days == -1):
                    if(hour == 0):
                        output = assignment.name + " due date passed"
                    else:
                        output = assignment.name+" due today in"+hour
                elif (days == 2 and hour == 0):
                    output = assignment.name+" due date in 2 days"
                elif (days == 7 and hour == 0):
                    output = assignment.name+" due date in 7 days"
    return output
           
def duesoon(duedate,duetime):
    # Due Date: 04-11-22
    print("Due time: ",duetime)
    # Current Time: 13-04-2022 19:58:13
    duedatestr = '20'+duedate[6:8]+'-'+duedate[:5]  #Format to string date
    duedate = datetime.date.fromisoformat(duedatestr)   #Convert date to datetime
    datetoday = date.today()    #Take current date in datetime
    daysleft = abs((duedate - datetoday).days)  #Difference of dates in datetime
    timenow = datetime.datetime.now()   #Take time in datetime
    duetime = duedatestr +' '+duetime
    duetime = datetime.datetime.fromisoformat(duedatestr)
    timeleft = abs((timenow - duetime))
    print("Days left for true",daysleft)
    print("Time Left for due: ",timeleft)
    if(daysleft == 7):
        return 7,timeleft
    elif(daysleft == 2):
        return 4,timeleft
    elif(daysleft == 0):
        if(timeleft<=4 and timeleft>=3):
            return -1,timeleft
        else:
            return -1,0
    

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
    date_time = fixdate(date_time)  #Remove the first two digits of the year
    return date_time

def fixdate(date_time):  #Remove the first two digits of the year
    return date_time

def sendtophone(contentformsg):
    account_sid = 'ACb42ed908ae21638215f40879f07ae965' 
    auth_token = '3c2741fb94ec782a64cd2e830183d653' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create(  
                                messaging_service_sid='MGb50838bc488cfdd79a2eb3ab55e31b42', 
                                body=contentformsg,      
                                to='+16694547233' 
                            ) 

    print(message.sid)


contentformsg = ""
API_URL = "https://canvas.ucdavis.edu"
API_KEY = "3438~WmzXhpREXRr3EuTB7dkCHAQIJfbxcWLKihHMAQLXDnF2jqa0D6AqKiV1Cl4f8ZED"
canvas = Canvas(API_URL, API_KEY)
ECS152 = 682756
ECS162A = 678782
SAS25V = 663974
STA106 = 678534
# courselist = [ECS152,ECS162A,SAS25V,STA106]
courselist = [ECS152,ECS162A,STA106]
sendmessage=[]
for i in courselist:
    course = canvas.get_course(i)
    datetoday = date.today().strftime('%m-%d-%Y')
    timenow = datetime.datetime.now() 
    current_time_date = str(datetoday) + " "+timenow.strftime("%H:%M:%S")
    print("The current time and date is : ",current_time_date)
    msg = readcourse(course,datetoday, timenow)
    if(len(msg)>0):
        contentformsg = contentformsg + "\n" + msg
    if(len(contentformsg) >5):
        sendtophone(contentformsg)
print(contentformsg)
