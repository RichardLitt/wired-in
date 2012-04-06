#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
#-*- coding: utf-8 -*-

"""

Wired In: Time tracker and Task manager
CC-Share Alike 2012 © Richard Littauer
https://github.com/RichardLitt/wired-in

"""

# Let's fedex in some packages!
# This may not be the best way to do this, actually. 
import os
import time
import datetime
import sys
import re
import dis
import random
import math
import textwrap

# These are going to have to be edited for new users.
folder_path = '/Users/richardlittauer/Github/wired-in/'
output_file_name = folder_path + 'wyred/oxygen.csv'
tasks_file = folder_path +  'wyred/tasks.csv'
shopping_list = folder_path + 'wyred/shopping_list.csv'

# These change each semester, obviously.
work_tasks = ["hiwi", "FLST", "PSR", "syntax", "CL4LRL", "stats", "research"]

# The help desk.
def help():
    print
    print "-------------------Help Desk-------------------"
    print
    print " begin/being <project> [last]/[%d | backtime]"
    print " end <project> <\"comment\">/<\"-x\">/<\"-c\"> [%d | backtime]" 
    print " fence [manual]"
    print " status"
    print " cease"
    print " topics"
    print " PID"
    print
    print " search <project> [print]"
    print " today [-][project]/[left]/[tasks] [all]"
    print " yesterday"
    print " week <%d> [days to search]"
    print " test"
    print
    print " write/w (Hours and minutes, or today optional)"
    print " projects <project>"
    print " random [today]"
    print " task [today/all]"
    print " mvim/vi <file>"
    print
    print "-----------------------------------------------"
    print


# The following is for editing files
def edit(x):
    if x == 'tasks':
        x = 'wyred/tasks.csv'
    if x == 'log':
        x =  'wyred/oxygen.csv'
    if x == 'code':
        x = 'wired_in.py'
    if x == 'list':
        x = 'wyred/shopping_list.csv'
    path = '/Users/richardlittauer/Github/wired-in/'
    command = sys.argv[1] + ' ' + path + x
    os.system(command)
    print 'Now executing: ' + command

# Shim
def print_time_labels(input_time):
    if len(input_time) == 16:
        input_time = input_time[-8:]
    input_time_split = input_time.split(':')
    hours = int(input_time_split[0])
    minutes = int(input_time_split[1])
    seconds = int(input_time_split[2])
    hour_string = "hours"
    minute_string = "minutes"
    second_string = "seconds"
    if hours == 1:
        hour_string = "hour"
    if minutes == 1:
        minute_string = "minute"
    if seconds == 1:
        second_string = "second"

    ## Removes seconds. Should remove from the function completely.
    output = "%s %s and %s %s" % (hours, hour_string, minutes, minute_string)
    if hours == 0:
        output = "%s %s" % (minutes, minute_string)
    if seconds == 0:
        output = "%s %s and %s %s" % (hours, hour_string, minutes, minute_string)
    if minutes == 0:
        output = "%s %s" % (hours, hour_string)
    if (seconds == 0) and (hours == 0):
        output = "%s %s" % (minutes, minute_string)
    if (seconds == 0) and (hours == 0) and (minutes == 0):
        output = "a while"
    return output

# How to add time together.
def time_add(x, y):
    hours = 0
    minutes = 0
    seconds = 0
    days = 0
    seconds = int(x[6:8]) + int(y[6:8])
    if seconds >= int(60):
        minutes += 1
        seconds = seconds - 60
    minutes = int(x[3:5]) + int(y[3:5]) + minutes
    if minutes >= 60:
        hours += 1
        minutes = minutes - 60
    hours = int(x[0:2]) + int(y[0:2]) + hours
    if hours >= 24:
        days += 1
        hours = hours - 24
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    if len(str(minutes)) == 1:
        minutes = "0" + str(minutes)
    if len(str(seconds)) == 1:
        seconds = "0" + str(seconds)
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)

# Shim
def day_index(x):
    months = [['nostring',0], \
    ['january', 0], \
    ['february', 31], \
    ['march', 59], \
    ['april', 90], \
    ['may', 120], \
    ['june', 151], \
    ['july', 181], \
    ['august', 212], \
    ['september', 243], \
    ['october', 273], \
    ['november', 304], \
    ['december', 334]]

    # This will find the amount of days from zero given a date
    if len(str(x)) > 4:
        days = 0
        days += int(x[8:10])
        days += months[int(x[5:7])][1]
        return str(days)

    # Given the amount of days, this will reverse into a date.
    if len(str(x)) < 4:
        date = []
        # This is going to mess up over the new year
        now = datetime.datetime.now()
        date.append(str(now)[0:4])
        # This sould be able to account for strings over the new year, staring
        # in november.
        if int(day_index(str(now)[0:10])) > 304:
            if int(x) < 200:
                date[0] = date.append(int(str(now)[0:4])+1)
        for month in range(len(months)):
            if int(x) >= months[month][1]:
                month_store = month
                date_store = int(x)-months[month][1]
                if date_store < 10:
                    date_store = '0' + str(date_store)
                if month_store < 10:
                    month_store = '0' + str(month)
        date.append(str(month_store))
        date.append(str(date_store))
        date = '-'.join(date)
        return date

# Natural language processor for numbers
# input whatever, returns string
def number_string(x):
    if x == 'one': return '01'
    if x == 'two': return '02'
    if x == 'three': return '03'
    if x == 'four': return '04'
    if x == 'five': return '05'
    if x == 'six': return '06'
    if x == 'seven': return '07'
    if x == 'eight': return '08'
    if x == 'nine': return '09'
    if x == 'ten': return '10'
    if x == 'eleven': return '11'
    if x == 'twelve': return '12'
    if x == 'dozen': return '12'
    if x == 'thirteen': return '13'
    if x == 'fourteen': return '14'
    if x == 'fifteen': return '15'
    if x == 'sixteen': return '16'
    if x == 'seventeen': return '17'
    if x == 'eighteen': return '18'
    if x == 'nineteen': return '19'
    if x == 'twenty': return '20'
    if x == 'thirty': return '30'
    if x == 'fourty': return '40'
    if x == 'fifty': return '50'
    if x == 'sixty': return '60'
    if x == 'seventy': return '70'
    if x == 'eighty': return '80'
    if x == 'ninety': return '90'
    if x == 'hundred': return '100'

    pattern = re.compile("\d+")
    match_o_time = re.search(pattern, str(x))
    if (match_o_time != None):
        return str(x)

# NLP for manual date input
def date_string(x):
    today = datetime.datetime.now()

    # Converts YYYY/MM/DD to YYYY-MM-DD
    if len(x.split('/')) == 3:
        x = x.split('/')
        x = '-'.join(x)

    # This is for non-dates. 
    if x == 'x':
        date = 'x'

    # If the string is just today
    if x == "today":
        date = str(today)[:10]

    # If it is tomorrow
    if x == "tomorrow":
        date = str(today)[:8] + str(int(str(today)[8:10])+1)
        bad_dates = ["29", "30", "31"]
        if date[8:10] in bad_dates:
            print "Check the month - there may be no tomorrow."
    pass_through = ['today', 'tomorrow', 'x']

    # If it is neither
    if x not in pass_through:
        # X must be YYYY-MM-DD
        pattern = re.compile("\d+\-\d+\-\d+")
        match_o = re.match(pattern, x)
        if (match_o != None):
            date = x
        if (match_o == None):
            x = x.split(' ')
            months = ['no month', 'January', 'February', 'March', 'April', \
                    'May',  'June', 'July', 'August', 'September', 'October',\
                    'November', 'December']
            ## Ignore case needs to be done by regex here. 
            if x[0] in months:
                month = months.index(x[0])
                if month < 10:
                    month = '0' + str(month)
            pattern = re.compile("\d\d")
            match_p = re.match(pattern, x[1])
            if (match_p != None):
                day = x[1][:2]
            if (match_p == None):
                pattern = re.compile("\d")
                match_n = re.match(pattern, x[1][:1])
                if (match_n != None):
                    day = '0' + x[1][:1]
                if (match_n == None):
                    ordinal = ['zeroth', 'first', 'second', 'third', 'fourth', \
                            'fifth', 'sixth',\
                            'seventh','eighth', 'nineth', 'tenth', 'eleventh', \
                            'twelfth', 'thirteenth','fourteenth','sixteenth',\
                            'seventeenth','eightteenth','nineteenth','twentieth',
                            'twentyfirst','twentyfirst','twentysecond',\
                            'twentythird','twentyfourth','twentyfifth',\
                            'twentysixth','twentyseventh','twentyeighth'\
                            ,'twentyninth','thirtieth','thirtyfirst']
                    day = x[1]
                    if day not in ordinal:
                        print 'ERROR'
                    if day in ordinal:
                        day = ordinal.index(day)
                        if day < int(10):
                            day = '0' + str(day)
            year = '2012'
            date = [year, month, str(day)]
            date = '-'.join(date)
    return date

# I don't actually remember what I was doing with this.
def random_navi_animal():
    animal = ["'angts\xcck", "eltungawng", "ngawng", "fpxafaw", "ikran",
            "ikranay", "kali'weya", "lenay'ga", "lonataya", "nantang",
            "pa'li", "palulukan", "riti", "talioang", "teylu", "toruk",
            "yerik", "yomh\xcc'ang", "hi'ang", "zize'"]
    return str(animal[random.randrange(len(animal)-1)])

# PIS should be field 1, but it isn't. Grevious oversight. v2 will have to
# change this.
def PID(PID):
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    for line in lineList:
        line = line.split(', ')
        line[7] = line[7].replace('\n', '')
        if line[7] == PID:
            print
            print 'Information for PID %s:' % PID
            print 'Project: ' + line[0]
            print 'Task: ' + line[1]
            print 'Expected Time: ' + print_time_labels(line[2])
            print 'Due: ' + line[3]
            print 'Weight: ' + line[4]
            print 'Days to do: ' + line[5]
            print 'Type: ' + line[6]
            print

# This function basically sorts the tasks by when they are due and how the time
# should be divided it. 

# It shims the lines into lines that are then passed to
# the today task, which means there's some room for error in reading due dates
# if you use the lines then. This isn't currently a problem, but might be
# eventually.

# Makes a minute index HHMMSS
def minutes_index(string):
    output = 0
    string = string.split(':')
    output = int(string[0])*60 + int(string[1])
    return output

def task_division(line):
    line  = line.split(', ')
    'life, Memorize the articles of the constitution, \
    03:00:00, 2012-03-21, 1, 1, hard, 28'
    time_for_task = line[2]
    date_due = line[3]
    days_to_do = line[5]
    task_type = line[6]
    PID = line[7]

    ## This is currently testing the ability to divide up time in different
    ## ways. What would be good is an output format that isn't a day string.
    ## Also, to output line by line, but recall original dates.
    task_types = ['dead', # Day of only.
            'hard', # Days before, doesn't divide.
            'soft', # Days before, divides time.
            'cont', # Repeats from start date for x days.
            'x', # Doesn't repeat or show unless asked
            'filler'] # Shouldn't appear, but does for now.

    if task_type not in task_types:
        print "Something is wrong with your formatting tasks."
        print "Look at PID: " + PID

    if task_type == 'dead':
        line = ', '.join(line)
        return line

    if task_type == 'hard':
        # Currently, the way it is set up is on hard - shows the full time, days
        # before. 
        line = ', '.join(line)
        return line
        # start_appearing = int(day_index(date_due)) - int(days_to_do)
        # date_due = day_index(start_appearing)

    if task_type == 'soft':

        start_appearing = int(day_index(date_due)) - int(days_to_do)
        time_for_task = minutes_index(line[2])

        # This checks if there has already been work done. 
        f = open(output_file_name, 'r+')
        lineList = f.readlines()

        # This checks the logs based on PIDs to see if any work has been 
        # done yet.
        for logline in lineList:
            logline = logline.split(', ')
            if len(logline) == int(7):
                logPID = logline[6]
                if logPID == PID:
                    time_done = logline[3].split(':')
                    time_taken_already = int(time_done[0])*60\
                            + int(time_done[1])
                    time_for_task = time_for_task - time_taken_already

        # Splits according to days left
        today = str(datetime.datetime.now())[0:10]
        days_left = int(days_to_do)

        # If it already should have been appearing
        if start_appearing <= int(day_index(today)):
            days_left = int(day_index(date_due))-int(day_index(today))+1
            if days_left <= 0:
                days_left = 1
            line[3] = today

        time_for_task = (time_for_task / days_left) \
                + time_for_task%days_left

        # This converts 183 into 03:03:00
        tft = []
        tft_hour = time_for_task / 60
        if tft_hour < 10:
            tft_hour = '0' + str(tft_hour)
        tft_hour = str(tft_hour)
        tft.append(tft_hour)
        tft_minute = time_for_task % 60
        if tft_minute < 10:
            tft_minute = '0' + str(tft_minute)
        tft_minute = str(tft_minute)
        tft.append(tft_minute)
        tft.append('00')
        tft = ':'.join(tft)
        line[2] = tft
        line = ', '.join(line)
        # print line.replace('\n', '')
        return line

    if task_type == 'cont':
        time_for_task = int(line[2][0:2])*60 + int(line[2][3:5])
        f = open(output_file_name, 'r+')
        lineList = f.readlines()
        for logline in lineList:
            logline = logline.split(', ')
            if len(logline) == int(7):
                logPID = logline[6].replace('\n','')
                if logPID == PID:
                    time_done = logline[3].split(':')
                    time_taken_already = int(time_done[0])*60\
                            + int(time_done[1])
                    time_for_task = time_for_task - time_taken_already
        if time_for_task <= line[2]:
            today = datetime.datetime.now()
            line[3] = day_index(str(int(day_index(str(today)[:10]))+1))
        if time_for_task > line[2]:
            line[3] = str(datetime.datetime.now())[:10]
        line = ', '.join(line)
        return line

    '''
    # For repeating tasks (cont) that differ in time too much to calculate
    if task_type == 'obj':
        # Has it been logged yet?
        f = open(output_file_name, 'r+')
        lineList = f.readlines()
        for logline in lineList:
            logline = logline.split(', ')
            if len(logline) == int(7):
                logPID = logline[6].replace('\n','')
                if logPID == PID:
                    # If so, then make the next day tomorrow. 
                    today = datetime.datetime.now()
                    line[3] = day_index(str(int(day_index(str(today)[:10]))+1))
        line = ', '.join(line)
        return line
    '''

    if task_type == 'x':
        today =datetime.datetime.now()
        line[3] = day_index(str(int(day_index(str(today)[:10]))+1))
        # Going to want to fix this so that it goes over month boundaries. 

        line = ', '.join(line)
        return line

    # Filler should never actually happen anymore - this was a retrofix.
    if task_type == 'filler':
        line[0] = '!' + line[0] 
        line = ', '.join(line)
        return line

# How to start a log line. 
def begin():
    f = open(output_file_name,'a')
    print
    print "Mask on!"
    print

    project = raw_input('project: ')

    what_time = raw_input('begin: now. ')
    time_now = datetime.datetime.now()
    if what_time != '':
        try:
            pattern = re.compile("\d+")
            match_o = re.match(pattern, what_time)
            if (match_o != None):
                today = datetime.datetime.now()
                min_change = datetime.timedelta(minutes=int(what_time))
                time_adjust = today - min_change
                print "-----------------------------------------------------------------------"
                print "You have just adjusted time backwards: " 
                print str(time_now) + " is now " + str(time_adjust) + "."
                print "-----------------------------------------------------------------------"
                time_now = time_adjust
        except: x = "There should be another option here."
        try:
            if what_time == "-l":
                f = open(output_file_name, 'r+')
                lineList = f.readlines()
                on = lineList[-1]
                pattern = re.compile("\d\d:\d\d:\d\d.\d+")
                match_o_time = re.search(pattern, on[27:])
                if (match_o_time != None):
                    time_now = str(time_now)[:10] + " " + match_o_time.group(0)
                    print "-----------------------------------------------------------------------"
                    print "You have just adjusted your start level from the last known signal, at " + time_now + "."
                    print "-----------------------------------------------------------------------"
        except: x = "This is a filler. You are in real time."
    print
    f.write(str(time_now) + ", ")
    f.write(project + ", ")
    f.close()

# How to end a logline. 
def end():
    f = open(output_file_name, 'r+')
    from datetime import datetime
    from datetime import timedelta
    lineList = f.readlines()
    on = lineList[-1]
    on_split = on.split(', ')
    off = datetime.now()
    print
    print "---------------------------------End------------------------------------"
    print 'Mask off!'
    print 

    project = raw_input('project: ' + on_split[1] + '. ')
    if project == '':
        project = on_split[1]
    if project != '':
        if project != on_split[1]:
            print
            print 'Do you know what you\'re doing?'
            print


    what_time = raw_input('end: now. ')
    if what_time != '':
        try:
            pattern = re.compile("\d+")
            match_o = re.match(pattern, what_time)
            if (match_o != None):
                today = datetime.now()
                min_change = timedelta(minutes=int(what_time))
                time_adjust = today - min_change
                print "You have just adjusted time backwards: " + str(off) + " is now " + str(time_adjust) + "."
                off = time_adjust
        except: x = "penguins"
    off = str(off)
    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(off[11:19], FMT) - datetime.strptime(on[11:19], FMT)
    total_time = str(tdelta)
    if len(total_time) == 15:
        total_time = total_time[-7:]
    if len(total_time) == 16:
        total_time = total_time[-8:]
    comment = raw_input('comment: ')
    comment = comment.replace(', ', ',')
    if comment == "x":
        comment = ""
    if comment == "c":
        comment = 'class'
    if comment == 'h':
        comment = 'homework'
    PID = raw_input('PID: - ')
    print

    print 'You were on the surface of Pandora from: ' + on[:19] + ' to ' + off[11:19] + '.'
    time_labels = print_time_labels(total_time)
    try:
        pattern = re.compile("\d+")
        match_o = re.match(pattern, comment)
        if (match_o != None):
                print "You survived for %s, and killed like %s %s." % (time_labels, match_o.group())
        if (match_o == None):
                print "You survived for %s." % time_labels
    except: x = "moose"
    print
    print 'Operation ' + project + ' is now terminated. Your activity report readout: '
    print comment
    print "------------------------------------------------------------------------"
    f.write(str(off) + ", ")
    f.write(total_time + ", ")
    f.write(project + ", ")
    f.write(comment.replace("\"", "'"))
    f.write(', ' + PID)
    f.write("\n")
    f.close()

# Wait, what project am I running now, anyway?
def status():
    f = open(output_file_name, 'r')
    from datetime import datetime
    lineList = f.readlines()
    print 
    print "---------------------------------Status---------------------------------"
    line = lineList[-1].split(', ')
    if len(line) != 3:
        f = open(output_file_name, 'r+')
        lineList = f.readlines()
        on = lineList[-1]
        # Clean this us using split()
        try:
            pattern_time = re.compile("\d\d:\d\d\:\d\d.\d+")
            match_o_time = re.search(pattern_time, on[29:])
            if (match_o_time != None):
                onn = match_o_time.group(0)
                off = str(datetime.now())
                FMT = '%H:%M:%S'
                time_since = datetime.strptime(off[11:19], FMT) - datetime.strptime(onn[:8], FMT)
                time_since = str(time_since)
        except: x = "I am a whale"
        time_labels = print_time_labels(time_since)
        print "You have not been working for %s." % time_labels
        print
        print on
        on = on.replace('\n', '').split(', ')
        print "Your last job, %s, lasted %s. Comment: \n%s" % (on[4], print_time_labels(on[3]), on[5])
        if len(time_since) >= 10:
            print "Good morning. You haven't started working yet today."
            print "Your last read out was: " + on.replace("\n","")
    if len(line) == 3:
        on = line[0]
        last_job = line[1]
        off = str(datetime.now())
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(off[11:19], FMT) - datetime.strptime(on[11:19], FMT)
        print 'You are currently on project %s in Pandora.' % last_job
        print 'Time alive: %s.' % print_time_labels(str(tdelta))
    print "------------------------------------------------------------------------"
    print ""
    f.close()

# Let's put a project on pause fast. Kind of meaningless, really.
def cease():
    f = open(output_file_name, 'r+')
    lineList = f.readlines()
    on = lineList[-1]
    from datetime import datetime
    from datetime import timedelta
    off = datetime.now()
    off = str(off)
    from datetime import datetime
    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(off[11:19], FMT) - datetime.strptime(on[11:19], FMT)
    print
    print "---------------------------------Cease----------------------------------"
    print 'Mask off!'
    print 'You were on the surface of Pandora from ' + on[:19] + ' to ' + off[:19]
    print 'You survived for ' + str(tdelta) + '.'
    print 'What ho?! A break?'
    print "------------------------------------------------------------------------"
    print
    f.write(str(off) + ", ")
    f.write(str(tdelta) + ", ")
    project = on.split(', ')[1]
    f.write(project + ", ")
    f.write("")
    f.write("\n")
    f.close()

# How long have I worked on each project?
# To do: First day, last day, amount of times.
def search():
    f = open(output_file_name, 'r+')
    lineList = f.readlines()
    from datetime import datetime
    from datetime import timedelta
    total_time = "00:00:00"
    days = 0
    day_string = 'days'
    print
    print "---------------------------------Search---------------------------------"
    for line in lineList:
        line = line.split(', ')
        if sys.argv[2] == line[1]:
                FMT = '%H:%M:%S'
                tt = datetime.strptime(line[3], FMT)
                total_time = datetime.strptime(str(total_time), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                if str(total_time)[9] == '2':
                    days += 1
                total_time = str(total_time)[11:]
                try:
                    if (sys.argv[3] == "print"):
                        line[5] = line[5].replace("\n", "")
                        print line[0][5:11] + "for " + print_time_labels(line[3]) + ": " + line[5]
                except: x = "This is a filler."
    if days == 1:
        day_string = "day"
    if days != 0:
        if sys.argv[2] == "coding":
            print "You have worked on this project for %d %s and %s." % (days, \
                    day_string, print_time_labels(total_time))
        if sys.argv[2] != "coding":
            print "You have worked on %s for %d %s and %s." % (sys.argv[2], \
                days, day_string, print_time_labels(total_time))
    if days == 0:
        if sys.argv[2] == "coding":
            print "You have worked on this project for %s." % print_time_labels(total_time)
        if sys.argv[2] != "coding":
            print "You have worked on %s for %s." % (sys.argv[2], print_time_labels(total_time))
    print "------------------------------------------------------------------------"
    print
    f.close()


# What is happening today? How much have I worked, on what, and how productive
# have I been?
def today():
    from datetime import datetime
    from datetime import timedelta
    f = open(output_file_name, 'r')
    lineList = f.readlines()
    # Will be useful when you integrate PIDs.
    oxygenList = lineList
    time_now = datetime.now()
    print
    total_time = "00:00:00"
    total_time_alt = "00:00:00"
    logged_time = "00:00:00"
    specific_job_catch = "empty"
    done_jobs = []

    for line in lineList:
        line = line.replace('\n', '').split(', ')
        if str(time_now)[:10] == line[0][:10]:

            if len(line) == 3:
                # if line[1] in work_tasks:
                on = line[0]
                off = str(time_now)
                FMT = '%H:%M:%S'
                tdelta = datetime.strptime(off[11:19], FMT) - \
                        datetime.strptime(on[11:19], FMT)
                on = lineList[-1].replace(", ", ". \
                        Your current Operation: ").replace(",", ".")
                worked = str(tdelta)
                read_out = "Ongoing..."


            if len(line) > 3:
                # if line[1] in work_tasks:
                worked = line[3]
                read_out = line[5]
            time_labels = print_time_labels(worked)
            read_out_block = "%s for %s: %s" % (line[1], time_labels, \
                    read_out)
            done_jobs.append(read_out_block)
            FMT = '%H:%M:%S'
            lt = datetime.strptime(worked, FMT)
            logged_time = datetime.strptime(str(logged_time), FMT) + \
                    timedelta(hours=lt.hour,minutes=lt.minute,seconds=lt.second)
            logged_time = str(logged_time)[11:]

            if line[1] in work_tasks:
                    tt = datetime.strptime(worked, FMT)
                    total_time = datetime.strptime(str(total_time), FMT) + \
                            timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                    total_time = str(total_time)[11:]
            try:
                if sys.argv[2][0] == "-":
                    if (line[1] != sys.argv[2]):
                        FMT = '%H:%M:%S'
                        tdelta = datetime.strptime(total_time, FMT) - \
                                datetime.strptime(line[3], FMT)
                        total_time_alt = str(tdelta)
                    specific_job = sys.argv[2][1:]
                    specific_job_catch = "except"
            except: penguins = "penguins"

            try:
                if sys.argv[2][0] != "-":
                    if (line[1] == sys.argv[2]):
                        tt = datetime.strptime(worked, FMT)
                        total_time_alt = datetime.strptime\
                                (str(total_time_alt), FMT)\
                                + timedelta(hours=tt.hour,minutes\
                                =tt.minute,seconds=tt.second)
                        total_time_alt = str(total_time_alt)[11:]
                        specific_job = line[1]
                        specific_job_catch = "only"
            except: specific_job = "essential work"

    productivity_measure =(float(total_time[:2])*60+ \
            float(total_time[3:5]))/500*100

    print "You have worked a total of %s today." % print_time_labels(total_time)
    if total_time != logged_time:
        print "(But you've logged %s.)" % print_time_labels(logged_time)
    print "So far, you have been %.2f%% productive." % productivity_measure

    try: 
        if (sys.argv[2] == "left"):
            time_left = 500-(float(total_time[:2])*60+float(total_time[3:5]))
            time_left_fmt = str(int((time_left-time_left%60)/60)) + ":" + str(int(time_left%60)) + ":00"
            print "You only have %s left to go!" % print_time_labels(time_left_fmt)
    except: daw = "d'awwwww"

    if specific_job_catch == "except":
        time_labels = print_time_labels(total_time_alt)
        print "Of that, you did everything but %s for %s." % (specific_job, time_labels)
    if specific_job_catch == "only":
        time_labels = print_time_labels(total_time_alt)
        print "Of that, you did %s for %s." % (specific_job, time_labels)

    # This loads up the tasks bit if you want to see what you need to do today.
    try:
        if sys.argv[2] == "tasks":
            tasks()
    except: jesus = "dead"
    print 
    print "----------------------------------"
    for job in done_jobs:
        dedented_text = textwrap.dedent(job).strip()
        print textwrap.fill(dedented_text, initial_indent='', subsequent_indent='    ')

# This basically shows what you need to do today. 
def tasks():
    from datetime import datetime
    from datetime import timedelta
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    f = open(output_file_name, 'r')
    oxygenList = f.readlines()

    time_left_today = "00:00:00"
    time_also_left_today = "00:00:00"
    to_do_today = []
    to_do_today_as_well = []

    # Adds the tasks to do to a list.
    for line in lineList:
        line = task_division(line)
        line = line.split(', ')
        today = datetime.now()

        # Checks based on PIDs if the task if done 
        # Subtracts time from tasks done. 
            # To do:
                # In progress tasks.
                # No way of doing this atm - should log PIDs too, I guess?
                # Would have to change from .csv to do this. :/

        for log in oxygenList:
            log = log.split(', ')

            # Ideally, this shouldn't neet to happen, but that's dependant on
            # only logging tasks to do.
            if len(log) == 6: skip = "no PID"
            if len(log) == 7:
                if log[6] == line[7]:
                    if log[0][:10] == str(today)[:10]:
                        FMT = '%H:%M:%S'

# Should be redone using minute_index()

                        tdelta = datetime.strptime(line[2], FMT) - \
                        datetime.strptime(log[3], FMT)
                        live_time = str(tdelta)
                        # Makes sure it is HH:MM:SS format
                        if len(live_time) == 7:
                            live_time = '0' + live_time
                        # Fixes a bug that puts the time into negative days
                        # when it is over the time specified
                        if len(live_time) != 8:
                            live_time = '00:00:00'

                            # Removes it from also to do, as you've done enough
                            # on it today
                            line[3] = day_index(str(int(day_index(line[3]))+1))
                            line[5] = '1'

                        # Sets the time left to do for this project.
                        line[2] = live_time


        # This is basically if it matches today or not. 
        today_index = int(day_index(str(today)[:10]))
        # If it is not one of those 'do sometime' tasks.
        if line[3] != "x":
            # If it needs to be done today today.
            if today_index >= int(day_index(line[3][:10])):
                # Because we don't need non-specific tasks in here.
                if line[2] != '00:00:00':
                    to_do_today.append(line)
                if line[2] == '00:00:00':
                    to_do_today_as_well.append(line)
            # Or if it is due tomorrow but should be done today.
            elif (int(day_index(line[3]))-int(line[5])+1) <= \
            today_index:
                to_do_today_as_well.append(line)
        # If it is one of those...
        if line[3] == 'x':
            to_do_today_as_well.append(line)

    # Prints the projects you need to do today.
    projects = []
    for item in to_do_today:
        if item[0] not in projects:
            projects.append(item[0])
    print
    print 'Jobs today: %s' % ', '.join(map(str, projects))

    print
    print "You need to:"


    # Sorts accoding to weight, and then alphabeticallyw
    from operator import itemgetter, attrgetter
    to_do_today = sorted(to_do_today, key=itemgetter(2), reverse=True)
    to_do_today = sorted(to_do_today, key=itemgetter(4), reverse=True)

    to_do_today_as_well = sorted(to_do_today_as_well, key=itemgetter(2),
            reverse=True)
    to_do_today_as_well = sorted(to_do_today_as_well, key=itemgetter(4), reverse=True)

    # Prints out what you have to do today (or yesterday...)
    for x in range(len(to_do_today)):
        line = to_do_today[x]
        PID = line[7].replace('\n', '')
        time_left_today = time_add(line[2], time_left_today)
        if print_time_labels(line[2]) != "0 minutes":
            print " %s %s : %s for %s." % (PID, line[0], line[1], \
                    print_time_labels(line[2]))
        if print_time_labels(line[2]) == "0 minutes":
            print " %s %s : %s." % (PID, line[0], line[1])

    # Prints out the rest if you want to see them. 
    try:
        if sys.argv[3] == "all":
            print
            print "Also to do today:"
            for x in range(len(to_do_today_as_well)):
                line = to_do_today_as_well[x]
                PID = line[7].replace('\n', '')
                time_also_left_today = time_add(line[2], \
                        time_also_left_today)
                # print " %s %s : %s for %s." % (PID, line[0], line[1], \
                #        print_time_labels(line[2]))
                if print_time_labels(line[2]) != "a while":
                    print " %s %s : %s for %s." % (PID, line[0], line[1], \
                            print_time_labels(line[2]))
                if print_time_labels(line[2]) == "a while":
                    print " %s %s : %s." % (PID, line[0], line[1])

    # Nonsense is good.
    except: jesus = "is he dead?"

    print
    # Prints the total time left given the tasks to do.
    print "You have roughly %s of work to do." % print_time_labels(time_left_today)
    if time_also_left_today != "00:00:00":
        print "You also have an extra %s of work after that." % \
                print_time_labels(time_also_left_today)


def vacation():
    from datetime import datetime
    from datetime import timedelta
    f = open(output_file_name, 'r')
    lineList = f.readlines()
    # Will be useful when you integrate PIDs.
    oxygenList = lineList
    time_now = datetime.now()
    print 
    total_time = "00:00:00"
    total_time_alt = "00:00:00"
    logged_time = "00:00:00"
    specific_job_catch = "empty"

    for line in lineList:
        line = task_division(line)
        line = line.replace('\n', '').split(', ')
        if str(time_now)[:10] == line[0][:10]:

            if len(line) == 3:
                # if line[1] in work_tasks:
                on = line[0]
                off = str(time_now)
                FMT = '%H:%M:%S'
                tdelta = datetime.strptime(off[11:19], FMT) - \
                        datetime.strptime(on[11:19], FMT)
                on = lineList[-1].replace(", ", ". \
                        Your current Operation: ").replace(",", ".")
                worked = str(tdelta)
                read_out = "Ongoing..."


            if len(line) > 3:
                # if line[1] in work_tasks:
                worked = line[3]
                read_out = line[5]
            time_labels = print_time_labels(worked)
            read_out_block = "%s for %s: %s" % (line[1], time_labels, \
                    read_out)
            dedented_text = textwrap.dedent(read_out_block).strip()
            print textwrap.fill(dedented_text, initial_indent='', subsequent_indent='    ')
            FMT = '%H:%M:%S'
            lt = datetime.strptime(worked, FMT)
            logged_time = datetime.strptime(str(logged_time), FMT) + \
                    timedelta(hours=lt.hour,minutes=lt.minute,seconds=lt.second)
            logged_time = str(logged_time)[11:]

            if line[1] in work_tasks:
                    tt = datetime.strptime(worked, FMT)
                    total_time = datetime.strptime(str(total_time), FMT) + \
                            timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                    total_time = str(total_time)[11:]
            try:
                if sys.argv[2][0] == "-":
                    if (line[1] != sys.argv[2]):
                        FMT = '%H:%M:%S'
                        tdelta = datetime.strptime(total_time, FMT) - \
                                datetime.strptime(line[3], FMT)
                        total_time_alt = str(tdelta)
                    specific_job = sys.argv[2][1:]
                    specific_job_catch = "except"
            except: penguins = "penguins"

            try:
                if sys.argv[2][0] != "-":
                    if (line[1] == sys.argv[2]):
                        tt = datetime.strptime(worked, FMT)
                        total_time_alt = datetime.strptime(str(total_time_alt), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                        total_time_alt = str(total_time_alt)[11:]
                        specific_job = line[1]
                        specific_job_catch = "only"
            except: specific_job = "essential work"
    
    productivity_measure =(float(total_time[:2])*60+ \
            float(total_time[3:5]))/500*100
    try: 
        if (sys.argv[2] == "left"):
            time_left = 500-(float(total_time[:2])*60+float(total_time[3:5]))
            time_left_fmt = str(int((time_left-time_left%60)/60)) + ":" + str(int(time_left%60)) + ":00"
            print "You only have %s left to go!" % print_time_labels(time_left_fmt)
    except: daw = "d'awwwww"

    if specific_job_catch == "except":
        time_labels = print_time_labels(total_time_alt)
        print "Of that, you did everything but %s for %s." % (specific_job, time_labels)
    if specific_job_catch == "only":
        time_labels = print_time_labels(total_time_alt)
        print "Of that, you did %s for %s." % (specific_job, time_labels)

    # This loads up the tasks bit if you want to see what you need to do today.
    try:
        if sys.argv[2] == "tasks":
            f = open(tasks_file, 'r+')
            lineList = f.readlines()

            print
            print "You need to:"

            time_left_today = "00:00:00"
            time_also_left_today = "00:00:00"
            to_do_today = []

            # Adds the tasks to do to a list.
            for line in lineList:
                line = line.split(', ')
                today = datetime.now()

                for log in oxygenList:
                    log = log.split(', ')
                    if len(log) == 6: skip = "should be a function"
                    if len(log) == 7:
                        if log[6] == line[7]:
                            if log[0][:10] == str(today)[:10]:
                                tdelta = datetime.strptime(line[2], FMT) - \
                                datetime.strptime(log[3], FMT)
                                live_time = str(tdelta)
                                if len(live_time) == 7:
                                    live_time = '0' + live_time
                                line[2] = live_time


                if day_index(str(today)[:10]) >= day_index(line[3][:10]):
                    to_do_today.append(line)

                elif (int(day_index(line[3]))-int(line[5])+1) <= \
                int(day_index(str(today)[:10])):
                    to_do_today.append(line)

            # Prints out what you have to do today (or yesterday...)
            for x in range(len(to_do_today)):
                line = to_do_today[x]
                try:
                    PID = line[7].replace('\n', '')
                except:
                    PID = 0
                time_left_today = time_add(line[2], time_left_today)
                if print_time_labels(line[2]) != "0 minutes":
                    print " %s %s : %s. (%s)" % (PID, line[0], line[1], line[3])
                if print_time_labels(line[2]) == "0 minutes":
                    print " %s %s : %s. (%s)" % (PID, line[0], line[1], line[3])
            print
    except: jesus = "dead"
    print 

def yesterday():
    from datetime import datetime
    from datetime import timedelta
    f = open(output_file_name, 'r')
    lineList = f.readlines()
    time_now = datetime.now()
    print 
    print "-----------------------------Yesterday---------------------------------"
    print
    total_time = "00:00:00"
    total_time_alt = "00:00:00"
    logged_time = "00:00:00"
    specific_job_catch = "empty"
    for line in lineList:
        line = line.replace('\n', '')
        today_date = day_index(str(time_now)[:10])
        modify_date = int(today_date)-1
        today_date = day_index(modify_date)
        line  = line.split(', ')
        if today_date == line[0][:10]:
            worked = line[3]
            read_out = line[5]
            time_labels = print_time_labels(worked)
            read_out_block = "%s for %s: %s" % (line[1], time_labels, read_out)
            dedented_text = textwrap.dedent(read_out_block).strip()
            print textwrap.fill(dedented_text, initial_indent='', subsequent_indent='    ')
            FMT = '%H:%M:%S'
            lt = datetime.strptime(worked, FMT)
            logged_time = datetime.strptime(str(logged_time), FMT) + timedelta(hours=lt.hour,minutes=lt.minute,seconds=lt.second)
            logged_time = str(logged_time)[11:]
            if line[1] in work_tasks:
                tt = datetime.strptime(worked, FMT)
                total_time = datetime.strptime(str(total_time), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                total_time = str(total_time)[11:]
    productivity_measure = (float(total_time[:2])*60+\
            float(total_time[3:5]))/500*100
    if total_time == '00:00:00':
        print "    You didn't log any work yesterday."
        print "    You were not productive in that regard."
        print
        print "-----------------------------------------------------------------------"
        print 
    if total_time != '00:00:00':
        print
        print "You worked a total of %s yesterday." % print_time_labels(total_time)
        print "(But you logged %s.)" % print_time_labels(logged_time)
        print "You were %.2f%% productive." % productivity_measure
        print
        print "-----------------------------------------------------------------------"
        print 

def this_week():
    from datetime import datetime
    from datetime import timedelta
    f = open(output_file_name, 'r')
    lineList = f.readlines()
    time_now = datetime.now()
    print 
    print "-----------------------------This Week---------------------------------"
    work_totality = "00:00:00"
    logged_totality = "00:00:00"
    lt_days = 0
    wt_days = 0
    productivity = 0
    for x in range(int(sys.argv[2])):
        total_time = "00:00:00"
        total_time_alt = "00:00:00"
        logged_time = "00:00:00"
        specific_job_catch = "empty"
        for line in lineList:
            line = line.replace('\n', '')
            today_date = day_index(str(time_now)[:10])
            modify_date = int(today_date)-int(x)
            today_date = day_index(modify_date)
            line  = line.split(', ')
            if today_date == line[0][:10]:

                if len(line) == 3:
                    # if line[1] in work_tasks:
                    on = line[0]
                    off = str(datetime.now())
                    FMT = '%H:%M:%S'
                    tdelta = datetime.strptime(off[11:19], FMT) - datetime.strptime(on[11:19], FMT)
                    on = lineList[-1].replace(", ", ". Your current Operation: ").replace(",", ".")
                    worked = str(tdelta)
                    read_out = "Ongoing..."
                    FMT = '%H:%M:%S'
                    lt = datetime.strptime(worked, FMT)
                    logged_time = datetime.strptime(str(logged_time), FMT) + timedelta(hours=lt.hour,minutes=lt.minute,seconds=lt.second)
                    logged_time = str(logged_time)[11:]
                    try:
                        if sys.argv[3] == "logged":
                            logged_totality = datetime.strptime(str(logged_totality), FMT) \
                                    + timedelta(hours=lt.hour,minutes=lt.minute,seconds=lt.second)
                            if str(logged_totality)[9] == '2':
                                lt_days += 1
                            logged_totality = str(logged_totality)[11:]
                    except: exams = "are coming"
                    if line[1] in work_tasks:
                        tt = datetime.strptime(worked, FMT)
                        total_time = datetime.strptime(str(total_time), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                        total_time = str(total_time)[11:]
                if len(line) > 3:
                    worked = line[3]
                    read_out = line[5]
                    time_labels = print_time_labels(worked)
                    # read_out_block = "%s for %s: %s" % (line[1], time_labels, read_out)
                    # dedented_text = textwrap.dedent(read_out_block).strip()
                    # print textwrap.fill(dedented_text, initial_indent='', subsequent_indent='    ')
                    FMT = '%H:%M:%S'
                    lt = datetime.strptime(worked, FMT)
                    logged_time = datetime.strptime(str(logged_time), FMT) + timedelta(hours=lt.hour,minutes=lt.minute,seconds=lt.second)
                    logged_time = str(logged_time)[11:]
                    try:
                        if sys.argv[3] == "logged":
                            logged_totality = datetime.strptime(str(logged_totality), FMT) \
                                    + timedelta(hours=lt.hour,minutes=lt.minute,seconds=lt.second)
                            if str(logged_totality)[9] == '2':
                                lt_days += 1
                            logged_totality = str(logged_totality)[11:]
                    except: exams = "are coming"

                    if line[1] in work_tasks:
                        tt = datetime.strptime(worked, FMT)
                        total_time = datetime.strptime(str(total_time), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                        total_time = str(total_time)[11:]
                        work_totality = datetime.strptime(str(work_totality), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                        if str(work_totality)[9] == '2':
                            wt_days += 1
                        work_totality = str(work_totality)[11:]
        
        productivity_measure = (float(total_time[:2])*60+float(total_time[3:5]))/500*100
        productivity += productivity_measure
        print
        if x == 0: print "You've worked %s today." % \
            print_time_labels(total_time)
        if x == 1:
            print "You worked a total of %s yesterday." % \
            print_time_labels(total_time)
        if x >= 2:
            print "You worked a total of %s %s days ago." % \
        (print_time_labels(total_time), x)
        try:
            if sys.argv[3] == "logged":
                print "(But you logged %s.)" % print_time_labels(logged_time)
        except: penguins = "penguins"
        print "You were %.2f%% productive." % productivity_measure

    if lt_days != int(0):
        logged_totality = str((lt_days*24) + int(logged_totality[:2])) + logged_totality[2:]
    if wt_days != int(0):
        work_totality = str((wt_days*24) + int(work_totality[:2])) + work_totality[2:]
    productivity = productivity / float(int(sys.argv[2]))
    print
    print "-----------------------------------------------------------------------"
    print "This week, you have worked %s." % print_time_labels(work_totality)
    if productivity < 20:
        print "You are and were really lazy and inept." 
    if productivity < 50:
        print "You were only %s%% productive" % productivity
    if productivity >= 50:
        print "You were %s%% productive." % productivity
    if productivity >= 75:
        print "You were, at %s%%, actually pretty productive." %productivity
    if productivity >= 100:
        print "Well done. You were really fucking productive. %s%%, to be \
        exact." % productivity
    work_totality = work_totality.split(':')
    hours_per_diem = float(work_totality[0])/float(sys.argv[2])
    print "Which is %s hours per day." % hours_per_diem
    if logged_totality != "00:00:00":
        print
        print "Time actually logged: %s." % print_time_labels(logged_totality)
        logged_totality = logged_totality.split(':')
        hours_per_diem = float(logged_totality[0])/float(sys.argv[2])
        print "Which is %s hours per day." % hours_per_diem
    print "-----------------------------------------------------------------------"
    print 


def topics():
    import pprint
    f = open(output_file_name, 'r+')
    lineList = f.readlines()
    topics = []
    print
    print "---------------------------------Topics---------------------------------"
    for line in lineList:
        line = line.split(', ')
        topics.append(line[1])
    set = {}
    map(set.__setitem__, topics, []) 
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(set.keys())
    print "------------------------------------------------------------------------"

def fence():
    f = open(output_file_name,'r+')
    from datetime import datetime
    from datetime import timedelta
    time_now = datetime.now()
    lineList = f.readlines()
    last_line = lineList[-1].split(', ')
    ## Make sure that there isn't any current job
    if len(last_line) == 2:
        if (sys.argv[2] == 'manual'):
            f.write("\n")
            last_line = "012345"
            print 
            print 'K\"amakto luke fya\'o!'
            print 'Zene ziveyko nga!'
            print
        if (sys.argv[2] != 'manual'):
            print
            print "      *****************************"
            print "      *Last job unfinished, error.*"
            print "      *****************************"
            print
    if len(last_line) >= 6:
        print 
        print "-------------------------------Fence------------------------------------"

        project = raw_input(' project: ')
        first_time = raw_input(' from: ')
        if len(first_time) != 5:
            if first_time != "last":
                print "Military time please."
                first_time = raw_input(' from (HH:MM): ')
        second_time = raw_input(' to: ')
        if second_time == "now":
            now = datetime.now()
            second_time = str(now)[11:16]
        print ' Comment can be -x or -c.'
        comment = raw_input(' comment: ')
        PID = raw_input(' PID: - ')
        if PID == 'list':
            os.system('wyr today tasks all')
            PID = raw_input(' PID: - ')
        print

        ## Find the first time. 
        if first_time == "last":
            on = last_line[2]
        if first_time != "last":
            pattern = re.compile("\d+:\d+")
            match_o = re.match(pattern, first_time)
            if (match_o != None):
                today = str(datetime.now())
                pattern = re.compile("\d+:")
                match_h = re.match(pattern, first_time)
                if (match_h != None):
                    today = today[:11] + match_h.group(0) + today[14:]
                    on = today[:14] + first_time[-2:] + ":00.000000"

        ## Find the second time.
        pattern = re.compile("\d+:\d+")
        match_o = re.match(pattern, second_time)
        if (match_o != None):
            today = str(datetime.now())
            pattern = re.compile("\d+:")
            match_h = re.match(pattern, second_time)
            if (match_h != None):
                today = today[:11] + match_h.group(0) + today[14:]
                off = today[:14] + second_time[-2:] + ":00.000000"

        ## Compute the total time. 
        off = str(off)
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(off[11:19], FMT) - datetime.strptime(on[11:19], FMT)
        total_time = str(tdelta)
        if len(total_time) == 15:
            total_time = total_time[-7:]
        if len(total_time) == 16:
            total_time = total_time[-8:]
        print 'You were on the surface of Pandora from: ' + on[:19] + ' to ' + off[11:19] + '.'
        time_labels = print_time_labels(total_time)
        comment = comment.replace(', ', ',')
        if comment == "-x":
            comment = ""
        if comment == "-c":
            comment = "Class."

        try:
            pattern = re.compile("\d+")
            match_o = re.match(pattern, comment)
            if (match_o != None):
                    print "You survived for %s, and killed like %s %s." %\
                    (time_labels, match_o.group(), random_navi_animal())
            if (match_o == None):
                    print "You survived for %s." % time_labels
        except: x = "moose"
        
        print 'Operation ' + project + ' is now terminated.'
        print "------------------------------------------------------------------------"
        print 
        
        ## Write to output file.
        f.write(str(on) + ", ")
        f.write(project + ", ")
        f.write(str(off) + ", ")
        f.write(total_time + ", ")
        f.write(project + ", ")
        f.write(comment.replace("\"", "'"))
        if len(PID) != 0:
            f.write(", " + PID)
        f.write("\n")
        f.close()


'''
The next segment is all for the tasks.csv file. This is different from the
oxygen file in that it is for actual things which need to be done, and not for
a log of time. Hopefully, this will evolve into a task manager that is more
suited to my needs than things is.
'''

def projects():
    import pprint
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    topics = []
    print
    print "-----------------------------Task Topics--------------------------------"
    for line in lineList:
        line = line.split(', ')
        topics.append(line[0])
    set = {} 
    map(set.__setitem__, topics, []) 
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(set.keys())
    print "------------------------------------------------------------------------"
    try:
        tasks = []
        time_expected = []
        date_due = []
        for line in lineList:
            line = line.split(', ')
            if sys.argv[2] == line[0]:
                tasks.append(line[1])
                time_expected.append(line[2])
                date_due.append(line[3].replace('\n',''))
        print
        print "For the task %s you should:" % sys.argv[2]
        print
        for x in range(len(time_expected)):
            print "%s. \n Expected time: %s. Due: %s.\n" % (tasks[x], \
                    print_time_labels(time_expected[x]), date_due[x])
        print "------------------------------------------------------------------------"
    except: john = "a chicken."

def random_task():
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    today_lineList = []
    try:
        if sys.argv[2] == 'today':
            for line in lineList:
                line_split = line.split(', ')
                today = str(datetime.datetime.now())[:10]
                if line_split[3] != 'x':
                    if day_index(line_split[3][:10]) <= day_index(today):
                        today_lineList.append(line)
            chosen = today_lineList[random.randrange(len(today_lineList))]
            line = chosen.split(', ')
        if sys.argv[2] != 'today':
            chosen = lineList[random.randrange(len(lineList))]
            line = chosen.split(', ')
    except:
        chosen = lineList[random.randrange(len(lineList))]
        line = chosen.split(', ')
    print 
    print "---------------------------Task Appointed-------------------------------"
    print " Behold! The task appointed for you!"
    print
    print " Under the auspices of \'%s\', you must:" % line[0]
    print " %s." % line[1]
    try:
        print " This may take up to %s." % print_time_labels(line[2])
        print " This is due on %s." % line[3][:10]
    except: damn = "damn"
    print "------------------------------------------------------------------------"
    print

def w_choice(lst):
    n = random.uniform(0, 1)
    for index, item, weight in lst:
        if n < weight:
            break
        n = n - weight
    return index

def task_write():
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    print
    print "Adding STD... "

    task = raw_input('project: ')

    job = raw_input('task: ')
    job = job.replace(', ', ',')
    if job[-1] == '.': job = job[:-1]

    time_exp = raw_input('expected time: ')
    pattern = re.compile("\d\d:\d\d:\d\d")
    match_o_time = re.search(pattern, time_exp)
    if (match_o_time == None):
        hour_input = 0
        minutes_input = ''
        time_exp = time_exp.split(' ')

        for x in range(len(time_exp)):
            if (time_exp[x] == "minutes") or (time_exp[x] == "minute"):
                minutes_input = number_string(time_exp[x-1])
                if int(minutes_input) >= 60:
                    hour_input += 1
                    hour_input = str(hour_input)
                    minutes_input = int(minutes_input)-60
                    minutes_input = str(minutes_input)
                    if len(time_exp) != 2:
                        print "Perhaps too many minutes there?"
                if len(minutes_input) == 1:
                    minutes_input = '0' + minutes_input

        if (time_exp[1] == "hour") or (time_exp[1] == "hours"):
            hour_input = int(hour_input)
            hour_input += int(time_exp[0])
            hour_input = str(hour_input)
        if hour_input == int(0):
            hour_input = str(hour_input)
        if len(hour_input) == 1:
            hour_input = '0' + hour_input
        if len(hour_input) > 2:
            print "TOO MANY HOURS! O GOD NO!"
        if (time_exp[0] == 'half') and (time_exp[2] == "hour"):
            hour_input = '00:30:00'
        if hour_input == 0:
            hour_input = '00'
        if minutes_input == '':
            minutes_input = '00'
        final_time_exp = hour_input + ':' + minutes_input \
                + ':00'
        time_exp = final_time_exp


    date = raw_input('date due: ')

    if date != 'today':
        if date != 'x':

            days_before = raw_input('days to work on: ')

            print
            print '(Task Types: hard  soft  cont  dead)'
            task_type = raw_input('type: ')

    if date == 'today':

        days_before = '1'
        task_type = 'dead'

    if date == 'x':

        days_before = '1'
        task_type = 'x'

    date = date_string(date)

    weight = raw_input('weight: ')

    PID = 0
    for line in lineList:
        line = line.split(', ')
        PID = int(line[-1]) + 1

    print
    f.write(task + ', ' + job + ', ' + time_exp + ', ' + date \
            + ', ' + weight + ', ' + days_before + \
            ', ' + task_type + ', ' + str(PID) + '\n')
    f.close()

# Today has some messed up metric where it views also to do today as today, and
# just task (sys.argv[2]) doesn't work for some reason. Huh. Will need fixing. 
def todo():
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    to_do_today = []
    error = []
    for line in lineList:
        line = task_division(line)
        line = line.split(', ')
        today = datetime.datetime.now()
        if str(today)[:10] == line[3][:10]:
            to_do_today.append(line)
        ## You're going to need to fix this later when you have dates that go
        ## over a month. As it is, this'll only work inside of month boundries.
        elif line[3] != "x":
            try:
                if (sys.argv[2] == "today"):
                    if (int(line[3][8:10])-int(line[5])) <= int(str(today)[8:10]):
                        to_do_today.append(line)
                if (sys.argv[2] == "all"):
                    to_do_today.append(line)
            except: i_am = "one with the freaks"
        try:
            if (sys.argv[2] == "all"):
                if line[3] == "x":
                    to_do_today.append(line)
        except: error.append('error')

    if len(error) == len(lineList):
        print
        print 'There are simply no tasks due today, apparently.'
        print

    if len(error) != len(lineList):
        weights = 0
        lst = []
        for line in to_do_today:
            weights += int(line[4])
        for x in range(len(to_do_today)):
            line = to_do_today[x]
            app = (x, line[0], float(line[4])/weights)
            lst.append(app)
        line = to_do_today[w_choice(lst)]
        print
        print "---------------------------Task Appointed-------------------------------"
        print " Behold! The task appointed for you!"
        print
        print " Under the auspices of \'%s\', you must:" % line[0]
        print " %s." % line[1]
        try:
            print " This may take up to %s." % print_time_labels(line[2])
            print " This is due on %s." % line[3][:10]
        except: damn = "damn"
        print "------------------------------------------------------------------------"
        print

'''
The following functions are for shopping lists.
'''


def view_list():
    f = open(shopping_list, 'r+')
    lineList = f.readlines()
    print
    urgent = []
    food = []
    life = []
    uni = []
    gifts = []
    other = []

    for line in lineList:
        line = line.split(', ')
        line[3] = line[3].replace('\n','')
        if line[3] == 'y':
            urgent.append(line)
        if line[3] != 'y':
            # Wish I could do line[2].append(line)
            if line[2] == 'food':
                food.append(line)
            if line[2] == 'life':
                life.append(line)
            if line[2] == 'uni':
                uni.append(line)
            if line[2] == 'gifts':
                gifts.append(line)
            if line[2] == 'other':
                other.append(line)
    if urgent:
        print 'URGENT: '
        for item in urgent:
            print '%s (%s,00 €) [%s]' % (item[0], item[1], item[2])
        print
    if food:
        print 'Food:'
        for item in food:
            print '%s (%s,00 €)' % (item[0], item[1])
        print
    if life:
        print 'Life:'
        for item in life:
            print '%s (%s,00 €)' % (item[0], item[1])
        print
    if gifts:
        print 'Gifts:'
        for item in gifts:
            print '%s (%s,00 €)' % (item[0], item[1])
        print
    if uni:
        print 'Uni:'
        for item in uni:
            print '%s (%s,00 €)' % (item[0], item[1])
        print
    if other:
        print 'Other:'
        for item in other:
            print '%s (%s,00 €)' % (item[0], item[1])
        print


def buy():
    f = open(shopping_list, 'r+')
    lineList = f.readlines()
    buyd = []
    print 
    print 'Add to list:'
    item = raw_input('Item: ')
    price = raw_input('Price (€): ')
    print 'Reasons: food, life, gifts, uni, other'
    reason = raw_input('Reason: ')
    urgent = raw_input('Urgent [y/n]: ')
    buyd.extend([item, price, reason, urgent])
    buyd = ', '.join(buyd)
    f.write(buyd)
    print 'Added to list.'
    print
    f.close()

'''
The final argument functions.
'''

'''
This is an attempt to basically make argparse work instead.
Kind of abandoned due to difficulty, and due to not wanting to use
excess key strokes to type in - for each command.

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--write', action='store_true', help='Write a task to file')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    if (args.write): 
        task_write()
    # ... do something with args.output ...
    # ... do something with args.verbose ..

'''
# Today is now dependant in some aspects \
            # on tasks.csv
if __name__ == "__main__":
    try:

        possible_arguments = ['mvim', 'vi', 'test', 'today', 'vacation',
        'search', 'cease', 'status', 'end', 'begin', 'being', 'start', 'help',
        'yesterday', 'topics', 'week', 'fence', 'tasks', 'projects', 'random',
        'write', 'task', 'PID', 'list', 'buy', 'm', 'v', 'to', 's', 'e', 'b',
        'h', 'y', 'f', 'ta', 'p', 'r', 'w', 'l']

        # Editing
        if (sys.argv[1] == "mvim") or (sys.argv[1] == "m"): edit(sys.argv[2])
        if (sys.argv[1] == "vi") or (sys.argv[1] == "v"): edit(sys.argv[2])
        if (sys.argv[1] == "test"): task_division(sys.argv[2])

        # Logs
        if (sys.argv[1] == "today") or (sys.argv[1] == "to"): today()
        if (sys.argv[1] == "vacation"): vacation()
        if (sys.argv[1] == "search"): search()
        if (sys.argv[1] == "cease"): cease()
        if (sys.argv[1] == "status") or (sys.argv[1] == "s"): status()
        if (sys.argv[1] == "end") or (sys.argv[1] == "e"): end()
        if (sys.argv[1] == "begin") or (sys.argv[1] == "b"): begin()
        if (sys.argv[1] == "start"): begin()
        if (sys.argv[1] == "help") or (sys.argv[1] == "h"): help()
        if (sys.argv[1] == "yesterday") or (sys.argv[1] == "y"): yesterday()
        if (sys.argv[1] == "topics"): topics()
        if (sys.argv[1] == "week"): this_week()
        if (sys.argv[1] == "fence") or (sys.argv[1] == "f"): fence()

        # Tasks
        if (sys.argv[1] == "tasks") or (sys.argv[1] == "ta"): tasks()
        if (sys.argv[1] == "projects") or (sys.argv[1] == "p"): projects()
        if (sys.argv[1] == "random") or (sys.argv[1] == "r"): random_task()
        if (sys.argv[1] == "write") or (sys.argv[1] == "w"): task_write()
        if (sys.argv[1] == "task"): todo()
        if (sys.argv[1] == "PID"): PID(sys.argv[2])

        # Shopping list
        if (sys.argv[1] == 'list') or (sys.argv[1] == "l"): view_list()
        if (sys.argv[1] == 'buy'): buy()

        if sys.argv[1] not in possible_arguments:
            print '\n You were just mauled by a ' + random_navi_animal() + '.\n '
    except: status()


# Today's my birthday, after all. - Jake Sully
