import datetime
from dateutil import parser
from canvasapi import Canvas

def readcourse(course):   
    for assignment in course.get_assignments():
        duedate = assignment.due_at
        if duedate is not None:
            print(course.name," : ",assignment," ",duedate)


API_URL = "https://canvas.ucdavis.edu"
API_KEY = "3438~WmzXhpREXRr3EuTB7dkCHAQIJfbxcWLKihHMAQLXDnF2jqa0D6AqKiV1Cl4f8ZED"
canvas = Canvas(API_URL, API_KEY)
ECS152 = 682756
ECS162A = 678782
SAS25V = 663974
STA106 = 678534
courselist = [ECS152,ECS162A,SAS25V,STA106]
for i in courselist:
    course = canvas.get_course(i)
    readcourse(course)
    