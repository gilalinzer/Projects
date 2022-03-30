#"I hereby certify that this program is solely the result of my own work 
#and is in compliance with the Academic Integrity policy of the course syllabus
#and the academic integrity policy of the CS department.”

import datetime
from datetime import date   
import suntime
from suntime import Sun, SunTimeException
from datetime import datetime, timedelta
from dateutil import tz
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
import time
import Draw

# this function is a modified version of one sent to me by Professor broder 
# it is a textbox that only accepts and prints numbers and certain special 
# keys that are needed for this program and it returns the collected data 
def textbox(x, y, wide, high, fontSize, maxChars):
    ans = ""
    
    # Draw the rectangle where the user will type in the number
    Draw.setColor(Draw.WHITE)            
    Draw.filledRect(x, y, wide, high)
    Draw.show()
    
    done = False
    while not done:  # while the user hasn't pressed return/enter
        if Draw.hasNextKeyTyped():
            # get the next key, and process it accordingly
            newKey = Draw.nextKeyTyped()
            if newKey == "Return":  # return means they're done
                done = True
            elif newKey == "BackSpace": # backspace allows them to undo
                if len(ans) > 0:
                    ans = ans[0:len(ans)-1]
            elif len(ans) < maxChars:
                if newKey == 'period': 
                    ans += '.'
                elif newKey == 'slash': # used to write date
                    ans += '/'
                elif newKey == 'colon': # used to write time
                    ans += ':'                
                elif newKey in "1234567890":
                    ans += newKey
                
            Draw.setFontSize(fontSize) # redraw the rectangle with 
            Draw.setColor(Draw.WHITE) # the current number.          
            Draw.filledRect(x, y, wide, high)
            Draw.setColor(Draw.BLACK)
            Draw.string(ans, x, y)
        Draw.show()
        
    return ans
 

def getDate(Date): # this function gets the date from the input
# and formats it correctly, checking for errors. 
    
    # getting the month
    if len(Date)!=10:
        error('date')
    if int(Date[0])>1: # the month starts with a number not a 0 or 1
        error('date')
    elif Date[0]=="0":#the month is one digit
        month=int(Date[1])
    elif Date[0]=="1": #the month is two digits
        month=int(Date[0:2]) # slicing the correct numbers from the input
    
    # getting the day
    if int(Date[3])>=4: # the day starts with a number 4 or above
        error('date')
    elif int(Date[3])==3: # the date is in the 30s
        if int(Date[0])==0 and int(Date[1])==2: # the month is february
            error('date')
        elif int(Date[4])>1: # the day is greater than 31
            error('date')
        # if the month is april, june, september or november there is no 31
        elif int(Date[4])==1 and (int(Date[1])==4 or int(Date[1])==6\
        or int(Date[1])==9 or (int(Date[0])==1 and int(Date[1])==1)):
            error('date')        
        else:
    
            day=int(Date[3:5]) # slicing the correct numbers from the input
    else: # the day starts with a 0 1 or 2 

        day=int(Date[3:5]) # slicing the correct numbers from the input    
    
    
    year=int(Date[6:10])
    
    return (year,month,day)


# this function takes a document with US zip codes and their longitudes and
# latitudes and makes it into a dictionary 
def makezipdict(): 
    data= open("zipcodes.txt") 
    zips_dict= {} 
    
    for line in data: # zip as the key and (lat,lng) data
        columns = line.split('\t')
        key = columns[0]
        zips_dict[key]= (columns[1],columns[2])
    data.close() 
    
    return zips_dict # return the whole dictionary 
 
# using a text document that has location for each zipcode
# making a dictionary with just zip as the key and (city,state) data so we 
# can print the city,state in the results 
def makelocationdict(): 
    data= open("zipcodes.txt") # using a text document that has location for each zip
    loc_dict= {} # making a dictionary with just zip as the key and (city,state) data
    for line in data:
        columns = line.split('\t')
        key = columns[0]
        loc_dict[key]= (columns[3],columns[4]) # city and state 
    data.close() 
    return loc_dict # return the whole dictionary 


def betweenTwoTimes(Time, time1,time2):
    # this function will calculate if a time is between or at one of the two 
    # times and will be used in calculating what tefilah can be said at a time  
    
    # important slices from time 
    hour= int(Time[0:2])
    minute= int(Time[3:5])    
    
    
    if (hour == int(time1.strftime('%H')) and \
       minute >= int(time1.strftime('%M'))) or \
       (hour > int(time1.strftime('%H'))):
            if (hour == int(time2.strftime('%H')) and \
            minute <= int(time2.strftime('%M'))) or \
            hour < int(time2.strftime('%H')) :
                return True
    return False

def error(item): # this will display on the screen when there is invalid input
    Draw.setFontSize(30)
    Draw.setColor(Draw.RED)
    Draw.string("Sorry, the "+item+ " is invalid.", 200,600)
    Draw.setFontSize(40)
    Draw.setColor(Draw.GRAY)
    Draw.string('Press the spacebar to restart',150,700)
    Draw.show()
    
    while True:
        if Draw.hasNextKeyTyped():
            newKey = Draw.nextKeyTyped()
            if newKey== "space":
                Draw.clear()
                go() # restarts the program
    return False # this will allow us to see if this has been invoked

def countdownTimer(time1, time2):
    # this function draws a timer showing how much time is left before the 
    # next tefilah 
    hour= int(time1[0:2])
    minute= int(time1[3:5])
    time1= timedelta(hours = hour, minutes = minute)
    # slicing and making the time into a time delta that can 
    # be subtracted from another time
    timer = time2-time1 # the difference between the times
    second = timedelta(seconds = 1)
    Draw.setColor(Draw.BLACK)
    Draw.setFontSize(20)
    Draw.string("press 's' key to stop timer",20,550)
    while timer:
        Draw.setColor(Draw.color(255, 194, 236))
        Draw.filledRect(20, 500, 120, 35) # overlapping the time
        # drawing rectangle to cover up previous time
        Draw.setColor(Draw.RED)
        Draw.setFontSize(30)
        Draw.string(timer.strftime('%H:%M:%S'),20,500)
        time.sleep(1) # wait one second
        timer = timer - second # update time to be one second less
        Draw.show()
        if Draw.hasNextKeyTyped(): # if the user presses s it will stop
            newKey = Draw.nextKeyTyped()
            if newKey== "s":
                return None # ends the countdown function so that the program 
            # can countinue and give a restart option

def halachicHours(zipcode,Date):
    # this function calculates sunrise sunset and halachic hours for the day

# based on the zipcode and date provided by the user 
    if zipcode in makezipdict(): # the zipcode is in the dictionary 
        (lat,lng)= makezipdict()[zipcode] 
    else: # the zip is not valid 
        error("zipcode")    
    
    d = getDate(Date)
    timenow = date(d[0],d[1],d[2]) # getting the returned tuple slices 
    # of year month and day
    
    # sliced dates from the tuple we returned in the get date functino
    tf = TimezoneFinder() # finding time zone based on lat and lng 
    # using this module 
    
    
    sun= Sun(float(lat),float(lng))
    
    sunrise_today = sun.get_local_sunrise_time(timenow,\
    ZoneInfo(tf.timezone_at(lng=float(lng),lat=float(lat)))) #getting time zone for location 
    
    sunset_today = sun.get_local_sunset_time(timenow,\
    ZoneInfo(tf.timezone_at(lng=float(lng),lat=float(lat))))
    
    # I had to do this because of a bug in the suntime module that 
    # calculates sunset from the day before. See: https://github.com/SatAgro/suntime/issues/12
    if sunset_today < sunrise_today: 
        sunset_today = sunset_today + timedelta(1)
        
    # Halachic hour is calculated according the Vilna Gaon as the time between 
    # sunrise and sunset divided by 12
    return (sunrise_today, sunset_today, (sunset_today-sunrise_today)/12)
    
def calculate_zmanim(zipcode,Date, Time): 
    # this function calculates and draws all the zmanim and other info 
    # such as the location, date, and what tefilah to say 
    
    Draw.setColor(Draw.BLACK)
    Draw.setFontFamily("Chalkboard")    
    
    halachic_hour = halachicHours(zipcode,Date)[2] #getting halachic hours function
    
    sunrise_today = halachicHours(zipcode,Date)[0] #sunrise from halachic hours function
    sunset_today = halachicHours(zipcode,Date)[1]
    
    # these slices from location dictionary will be used to print the location 
    # in the program 
    city = makelocationdict()[zipcode][0] 
    state = makelocationdict()[zipcode][1]
    
    # title of the zmanim slide will show the date and location user entered
    Draw.setFontSize(35)
    # formatting of %A gives the weekday, %B is the month %d is day and %y is year
    Draw.string("Zmanim for " +sunrise_today.strftime('%A, %B %d, %Y'),70,40) # centered
    Draw.string('in ' + city+ ', '+ state,290, 80) # centered
    
    Draw.setFontSize(20)
    X=20 # X value for all zmanim
    Y=150 # starting y value that will be incremented by 20 for each zman
    
    #this formatting of %I tells it to write the hour in 12 hour clock and 
    # %M is minutes and %p is AM or PM    
    Draw.string('Sunrise is at: ' + sunrise_today.strftime('%I:%M %p'),X,Y)
   
    
    # Sof Zman Kriyat Shema is 3 halachic hours after sunrise- see mishnah brachot 1:2
    sofZmanKriyatShema= sunrise_today + (halachic_hour*3)
    Draw.string('Sof Zman Kriyat Shema: '+ sofZmanKriyatShema.strftime('%I:%M %p'),X,Y+20)
    
    # Sof zman tefila is 4 halachic hours after sunrise 
    sofZmanTefilah = sunrise_today + (halachic_hour*4)
    Draw.string('Sof Zman Tefilah: '+ sofZmanTefilah.strftime('%I:%M %p'),X,Y+40)
    
    # Chazot is halfway between sunset and sunrise and since there are 12 
    # halachic hours sunrise+6hours is chazot
    chazot= sunrise_today + (halachic_hour*6)
    Draw.string('Chazot: ' +chazot.strftime('%I:%M %p'),X,Y+60)
    
    # Mincha Gedolah is defined by the Gra as a half halachic hour after Chazot 
    # and it is the earliest time one can daven mincha
    minchaGedolah = chazot + (halachic_hour/2)
    Draw.string('Earliest Mincha: ' +minchaGedolah.strftime('%I:%M %p'),X,Y+80)
    
    # mincha ketanah is two and a half halachic hours before sunset 
    minchaKetanah = sunset_today - halachic_hour*2.5
    Draw.string('Mincha Ketanah: ' +minchaKetanah.strftime('%I:%M %p'),X,Y+100)
    plagHamincha = sunset_today - halachic_hour*1.25
    Draw.string('Plag Hamincha is at ' + plagHamincha.strftime('%I:%M %p'),X,Y+120)
    
    # it is customary to light shabbos candles 18 mintes before sunset
    # as said previously the %A gets the day of the week string 
    if sunset_today.strftime('%A')=='Friday' or sunset_today.strftime('%A')=='Saturday': # %A is day of week
        if sunset_today.strftime('%A')=='Friday':
            Candlelighting = sunset_today-timedelta(minutes=18)
            Draw.string('Candlelighting is at: '+Candlelighting.strftime('%I:%M %p'),X,Y+160)
        Draw.setFontSize(30)
        Draw.string('Shabbat Shalom!',20,Y+180)
        Draw.picture('shabbat shalom.gif', 475,150)
        Draw.setFontSize(20)            
    
    Draw.string ('Sunset is at: '+ sunset_today.strftime('%I:%M %p'),X,Y+140)
    
    # Tzeis hachochavim is when there are three stars out. 
    # This is the shabbos ending time. This is when the sun is 8.5 degrees below 
    # the horizon. This is hard to calculate and Rav Moshe Feinstein rules that 
    # in America this is never later than 50 regular minutes after sunset (in Israel
    #it's more like 20) see https://www.myzmanim.com/read/sources.aspx
    tzeis= sunset_today+(timedelta(minutes=50))
    Draw.string ('Tzeis is at: '+ tzeis.strftime('%I:%M %p'),X,Y+220) 
    # larger incrementation here because the shabbat shalom was a bigger font

    Draw.show()
    
    
    # now we will calculate what tefilah the person can say based on the 
    # time they inputted 
    # first we need to make sure the time is a valid time
    if len(Time)<5:
        error("time")
    if int(Time[0])>2:# the first number in the hour is above 2:
        error("time")
    elif int(Time[0])==2 and int(Time[1])>4: # time greater than 24
        error("time")
    elif int(Time[3])>5:# minutes are greater than 59
        error("time")
    
    # now lets change color and font size for this next string to seperate it 
    # from the zmanim
    Draw.setFontSize(30)
    Draw.setColor(Draw.RED)    
    
    
    # if the time is between sunrise and sof zman kriyat shema 
    if betweenTwoTimes(Time,sunrise_today,sofZmanKriyatShema):   
        Draw.string('You can say Shema and Shacharit now!',X,Y+250)
        Draw.string('Time left to say shema:',X,Y+300)
        countdownTimer(Time,sofZmanKriyatShema)
    
    # if the time is between sof zman kriyat shema and sof zman tefilah
    if betweenTwoTimes(Time,sofZmanKriyatShema,sofZmanTefilah):        
        Draw.string('You can say Shacharit now!',X,Y+250)
        Draw.string('Time left to daven shacharit:',X,Y+300)
        countdownTimer(Time,sofZmanTefilah)
              
    
    # if the time is between sof zman tefilah and mincha gedolah
    # there is nothing you can daven 
    if betweenTwoTimes(Time,sofZmanTefilah,minchaGedolah):
        Draw.string('Nothing to daven right now!',X,Y+250)
        Draw.string('Time until you can daven mincha:',X,Y+300)
        countdownTimer(Time,minchaGedolah)
        
   
    # if the time is between mincha gedolah and sunset - you can say mincha
    if betweenTwoTimes(Time,minchaGedolah,sunset_today):    
                Draw.string('You can daven mincha now!',X,Y+250)
                Draw.string('Time left to daven mincha:',X,Y+300) 
                countdownTimer(Time,sunset_today)               
    
    # important slices from time 
    hour= int(Time[0:2])
    minute= int(Time[3:5])   
    
    # if the time is between sunset and sunrise you can say maariv
    # if its any time later than sunset or any time earlier than 
    # sunrise - this is different because it goes back to 0 at midnight
    if (hour == int(sunset_today.strftime('%H')) and \
       minute >= int(sunset_today.strftime('%M'))) or \
       (hour > int(sunset_today.strftime('%H'))):    
        Draw.string('You can daven maariv now!',X,Y+250)
        Draw.string('Approximate time left to daven maariv:',X,Y+300)
        # since the time will be based on today's sunrise and not tommorow's 
        # it won't be entirely accurate- but as with any zman should not be 
        # relied on to the last minute anyways
        countdownTimer(Time,sunrise_today)        
    if hour <= int(sunrise_today.strftime('%H')) or \
    (hour <= int(sunrise_today.strftime('%H')) and \
    minute <= int(sunrise_today.strftime('%M'))):      
        Draw.string('You can daven maariv now!',X,Y+250)
        Draw.string('Approximate time left to daven maariv:',X,Y+300)
        countdownTimer(Time,sunrise_today)

    
   
def go(): # this is the main action that the program does 
    Rose = Draw.color(255, 194, 236)
    Draw.setBackground(Rose)
    Draw.setFontSize(40)
    Draw.setFontFamily("Chalkboard")
    Draw.setColor(Draw.BLACK)
    TextX = 20 # the text will have a different x value than text box
    Xvalue = 500
    Yvalue = 150
    width = 150
    height = 20
    font = 20
    
    Draw.string("Welcome to Py Zmanim!", 180, 40) # centered on canvas
    Draw.setFontSize(20)
    Draw.string("Times are based on the Gra. Do not rely on zmanim to the last minute", 80, 90)
    # also centered 
    
    # prompting the questions
    Draw.string("Please enter your 5 digit zip code: ", TextX, Yvalue)           
    zipcode= textbox(Xvalue,Yvalue, width , height,font, 5)
    # this has a max of 5 chars since the zip is always 5 chars 
   
    # the following lines are incremented by 80 units 
    Draw.string("Please enter the date in MM/DD/YYYY format: ", TextX,Yvalue+80)
    Date= textbox(Xvalue,Yvalue+80,width,height, font, 10) # will be prompted next
    # this has a max of 10 chars since that is what is required for date
    
    Draw.string("Please enter the 24 hour time in HH:MM format: ", TextX,Yvalue+160)
    Time= textbox(Xvalue,Yvalue+160, width, height, font, 5) # final prompt
    # max of 5 chars because the time is always 5 chars 
    
    Draw.clear()
    

    halachicHours(zipcode, Date)    
    calculate_zmanim(zipcode, Date, Time)
    
    Draw.setFontSize(40)
    Draw.setColor(Draw.GRAY)
    Draw.string('Press the spacebar to restart',150,700)
    Draw.show()    
        
    

def main(): # this is the function that controls the whole program
    Draw.setCanvasSize(800, 800)
    go() # the program will play one time
    while True: # loop forever
        if Draw.hasNextKeyTyped(): # if the user presses space it will go again
            newKey = Draw.nextKeyTyped()
            if newKey== "space":
                Draw.clear()
                go()
            
             
main()


