#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
#-*- coding: utf-8 -*-

"""

Wired In: Time tracker and Task manager
CC-Share Alike 2012 © Richard Littauer
https://github.com/RichardLitt/wired-in

All issues are tracked with ghi from the terminal (for future reference.)

"""

# Let's fedex in some packages!
# This may not be the best way to do this, actually. 
import os
import datetime
import sys
import re
import random
import textwrap

# These are going to have to be edited for new users.
folder_path = '/Users/richardlittauer/Github/wired-in'
output_file_name = folder_path + '/wyred/oxygen.csv'
tasks_file = folder_path +  '/wyred/tasks.csv'
shopping_list = folder_path + '/wyred/shopping_list.csv'
issues_list = folder_path + '/wyred/ghi'

# This is the amount of time you are expected to work each day
exp_wpd = 480

# These change each semester, obviously.
work_tasks = ["hiwi", 'conf', 'research', 'rep', 'grad', 'ema', 'nex', \
        'work', 'review', 'lrl', 'realise', 'admin', 'bank', #Non-denominational
        "FLST", "PSR", "syntax", 'CL4LRL', 'stats', #Wintersommester
        'SE', 'bracoli', 'coli', 'sem', 'LT', 'disc', 'mword', #Sommersemester
        'thesis', 'como', 'nlp', 'rm', 'sw', 'ml', 'wyrd', 'math'] #malta 1

# The help desk.
def help():
    print
    print "-------------------Help Desk-------------------"
    print
    print " b, begin PROJECT [last]/[%d | backtime]"
    print " e, end PROJECT <\"comment\">/<\"-x\">/<\"-c\"> [%d | backtime]" 
    print " f, fence, log [manual]"
    print " s, status"
    print " c, cease"
    print " t, topics"
    print " P, PID"
    print
    print " se, search PROJECT [print]"
    print " n, today [-][project]/[left]/[tasks] [all]/[display] [x]"
    print " y, yesterday"
    print " we, week <%d | days to search> [logged] [workdays] [%d | holidays]"
    print
    print " w, write/w (Hours and minutes, or today optional)"
    print " p, projects PROJECT"
    print " l, todo [topic/date]"
    print " r, random [today]"
    print " task [today/all]"
    print " m, mvim FILE"
    print " v, vi FILE"
    print " u, unify"
    print
    print " li, list"
    print " bi, buy"
    print
    print " ca, ical"
    print
    print " g, ghi"
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

'''
The following are the shims used for data conversion or manipulation
'''


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
        # This sould be able to account for strings over the new year, starting
        # in november.
        if int(day_index(str(now)[0:10])) > 304:
            if int(x) < 200:
                date[0] = date.append(int(str(now)[0:4])+1)
        for month in range(len(months)):
            if int(x) > months[month][1]:
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

# Makes a minute index HHMMSS
def minutes_index(string):
    string = str(string)
    if len(string) == 7:
        string = '0' + string
    if len(string) == 5:
        string = string + ':00'
    if len(string) == 8:
        output = 0
        splstr = string.split(':')
        output = int(splstr[0])*60 + int(splstr[1])
    if len(string) != 8:
        output = []
        string = int(string)
        hour = string / 60
        if hour < 10:
            hour = '0' + str(hour)
        output.append(str(hour))
        minute = string % 60
        if minute < 10:
            minute = '0' + str(minute)
        output.append(str(minute))
        output.append('00')
        output = ':'.join(output)
    return output

# NLP for manual date input
# This doesn't take into account weeks, or weekdays. And it should. How?
def date_string(x):
    from datetime import date
    today = datetime.datetime.now()

    # Converts YYYY/MM/DD to YYYY-MM-DD
    if len(x.split('/')) == 3:
        x = x.split('/')
        x = '-'.join(x)

    # This is for non-dates. 
    if x == 'x':
        date = 'x'

    # If the string is just today
    elif x == "today":
        date = str(today)[:10]

    # If it is tomorrow
    elif x in ('tomorrow', 'manana', 'mañana'):
        date = day_index(int(day_index(str(today)[:10]))+1)

    # If it is the day after tomorrow
    elif x in ('day after tomorrow', 'the day after tomorrow'):
        date = day_index(int(day_index(str(today)[:10]))+2)

    # If it is next week:
    #elif x in ('next week', 'in a week'):
    #   weekday = date.today().isoweekday()

    # If it is this week:
    #elif x in ('this week', 'this weekend', 'by next week', \
    #        'before next week'):

    # If it is neither
    else:
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
            if x[0] in months:
                month_check = x[0]
                if months.index(month_check) < 10:
                    month = '0' + str(months.index(month_check))
                if months.index(month_check) == 10: month = '10'
                if months.index(month_check) == 11: month = '11'
                if months.index(month_check) == 12: month = '12'
            pattern = re.compile("\d\d")
            match_p = re.match(pattern, x[1])
            if (match_p != None):
                day = x[1][:2]
            # This should ignore case, but it doesn't.
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
            # Will need to change this to automatic recognition.
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


'''
The following are callable functions

# This function should demand a write if nothing else is or has been going on.
def void():
    f = open(output_file_name, 'r+')
    lineList = f.readlines()
    final_line = lineList[-1].split(', ')
    if len(final_line) != 3:
        print final_line
    # Need an easy way to make sure that it doesn't just print all of the time
    # when status() is being called. Maybe after most of the __main__
    # functions.

'''

# PIS should be field 1, but it isn't. Grevious oversight. v2 will have to
# change this.
def PID(PID):
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    for line in lineList:
        if line[0] == '#': continue
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

def task_division(line,oxygenList):
    line  = line.split(', ')
    'life, Memorize the articles of the constitution, \
    03:00:00, 2012-03-21, 1, 1, hard, 28'
    time_for_task = line[2]
    date_due = line[3]
    days_to_do = line[5]
    task_type = line[6]
    PID = line[7]

    # Splits according to days left
    today = str(datetime.datetime.now())[0:10]
    days_left = int(days_to_do)

    # This clears tasks where you overshot the suggested time but have totally
    # finished for the day anyway.
    for output in oxygenList:
        output = output.split(', ')
        try:
            if output[6] == PID:
                if output[0][:10] == today:
                    if output[5][0] == 'x':
                        task_type = 'x'
        except: continue

    ## What would be good is an output format that isn't a day string.
    task_types = [\
            'hard', # Days before, doesn't divide.
            'soft', # Days before, divides time.
            'dsoft', # Soft with hard deadline
            'dcont', # Cont with hard deadline and not as_well placement
            'cont', # Repeats from start date for x days.
            'over', # When it's cont but it should rollover (per week)
            'dover', # dcont + over
            'x' ] # Doesn't repeat or show unless asked

    if task_type not in task_types:
        print "Something is wrong with your formatting tasks."
        print "Look at PID: " + PID

    if task_type == 'hard':
        # Currently, the way it is set up is on hard - shows the full time, days
        # before. 

        if time_for_task == 0: line[4] = '0'

        line = ', '.join(line)
        return line

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
                    if time_for_task < time_taken_already:
                        time_for_task = 0
                    else:
                        time_for_task = time_for_task - time_taken_already

        # If it already should have been appearing
        if start_appearing <= int(day_index(today)):
            days_left = int(day_index(date_due))-int(day_index(today))+1
            if days_left <= 0:
                days_left = 1
            line[3] = today
        
        time_for_task = (time_for_task / days_left) \
                + time_for_task%days_left
        
        line[2] = minutes_index(time_for_task)

        if time_for_task == 0: line[4] = '0'

        line = ', '.join(line)

        return line

    if task_type == 'dsoft':

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

        # This may break the dsoft- if it is overshot, then it will reset to 0.
        # Should change to perhaps 30 minutes? Not sure. 

        if time_for_task < 0: time_for_task = 0
        line[2] = minutes_index(time_for_task)

        if time_for_task == 0: line[4] = '0'

        line = ', '.join(line)
        return line

    # For continuous tasks that need to be done each day. 
    if task_type == 'cont':
        time_for_task = minutes_index(line[2])
        f = open(output_file_name, 'r+')
        lineList = f.readlines()
        today = str(datetime.datetime.now())[:10]

        # For each normal line, check the PID
        for logline in lineList:
            logline = logline.split(', ')
            if len(logline) == 7:
                logPID = logline[6]
                if logPID == PID:

                    # If there was work done today
                    if str(today)[:10] == logline[0][:10]:
                        
                        # Adjust the minutes left to do.
                        time_taken_already = minutes_index(logline[3])
                        time_for_task = time_for_task - time_taken_already

        # If it shouldn't be appearing yet
        if int(day_index(line[3]))-int(line[5]) >= day_index(today):

            # If there are no more minutes to go
            if time_for_task <= 0:
                print time_for_task, minutes_index(time_for_task)
                # Adjust time left
                line[2] = minutes_index(time_for_task)

                # Day due is tomorrow
                line[3] = day_index(str(int(day_index(today))+1))

            # If there is still work to do
            if time_for_task >= minutes_index(line[2]):
                line[3] = today

        if time_for_task == 0: line[4] = '0'

        line = ', '.join(line)
        return line

    if task_type == 'dcont':
        time_for_task = minutes_index(line[2])
        f = open(output_file_name, 'r+')
        lineList = f.readlines()
        today = str(datetime.datetime.now())[:10]

        # For each normal line, check the PID
        for logline in lineList:
            logline = logline.split(', ')
            if len(logline) == 7:
                logPID = logline[6]
                if logPID == PID:

                    # If there was work done today
                    if str(today)[:10] == logline[0][:10]:
                        
                        # Adjust the minutes left to do.
                        time_taken_already = minutes_index(logline[3])
                        time_for_task = time_for_task - time_taken_already

        # If it shouldn't be appearing yet
        if int(day_index(line[3]))-int(line[5]) >= day_index(today):

            # If there are no more minutes to go
            if time_for_task <= 0:
                print time_for_task, minutes_index(time_for_task)
                # Adjust time left
                line[2] = minutes_index(time_for_task)

                # Day due is tomorrow
                line[3] = day_index(str(int(day_index(today))+1))

            # If there is still work to do
            if time_for_task >= minutes_index(line[2]):
                line[3] = today

        if time_for_task == 0: line[4] = '0'

        line = ', '.join(line)
        return line

    # For continuous tasks that need to be done each day. 
    if task_type == 'over':
        time_for_task = minutes_index(line[2])
        f = open(output_file_name, 'r+')
        lineList = f.readlines()
        today = str(datetime.datetime.now())[:10]

        time_taken_already = 0

        # For each normal line, check the PID
        for logline in lineList:
            logline = logline.split(', ')
            if len(logline) == 7:
                logPID = logline[6]
                if logPID == PID:

                    # If there was work done in the past three days
                    if int(day_index(today)) - int(day_index(logline[0])) <= 3:
                        time_for_task += minutes_index(logline[3])

        # Adjust the minutes left to do if there's been rollover.
        if time_for_task - (time_taken_already/7) <= time_for_task:
            time_for_task = time_for_task - (time_taken_already/7)


        # If it shouldn't be appearing yet
        if int(day_index(line[3]))-int(line[5]) >= day_index(today):

            # If there are no more minutes to go
            if time_for_task <= 0:
                print time_for_task, minutes_index(time_for_task)
                # Adjust time left
                line[2] = minutes_index(time_for_task)

                # Day due is tomorrow
                line[3] = day_index(str(int(day_index(today))+1))

            # If there is still work to do
            if time_for_task >= minutes_index(line[2]):
                line[3] = today

        if time_for_task == 0: line[4] = '0'

        line = ', '.join(line)
        return line

    if task_type == 'dover':
        time_for_task = minutes_index(line[2])
        f = open(output_file_name, 'r+')
        lineList = f.readlines()
        today = str(datetime.datetime.now())[:10]

        time_taken_already = 0

        # For each normal line, check the PID
        for logline in lineList:
            logline = logline.split(', ')
            if len(logline) == 7:
                logPID = logline[6]
                if logPID == PID:

                    # If there was work done in the past three days
                    if int(day_index(today)) - int(day_index(logline[0])) <= 3:
                        time_taken_already += minutes_index(logline[3])

        # Adjust the minutes left to do if there's been rollover.
        if time_for_task - (time_taken_already/7) <= time_for_task:
            time_for_task = time_for_task - (time_taken_already/7)

        # If it shouldn't be appearing yet
        if int(day_index(line[3]))-int(line[5]) >= day_index(today):

            # If there are no more minutes to go
            if time_for_task <= 0:
                print time_for_task, minutes_index(time_for_task)
                # Adjust time left
                line[2] = minutes_index(time_for_task)

                # Day due is tomorrow
                line[3] = day_index(str(int(day_index(today))+1))

            # If there is still work to do
            if time_for_task >= minutes_index(line[2]):
                line[3] = today

        if time_for_task == 0: line[4] = '0'

        line = ', '.join(line)
        return line

    if task_type == 'x':
        # Always another day ahead...
        today =datetime.datetime.now()
        line[3] = day_index(str(int(day_index(str(today)[:10]))+1))
        line = ', '.join(line)
        return line

# How to start a log line. 
def begin():
    f = open(output_file_name,'r+')
    from datetime import datetime
    from datetime import timedelta
    time_now = datetime.now()
    lineList = f.readlines()
    last_line = lineList[-1].split(', ')
    ## Make sure that there isn't any current job
    if len(last_line) == 3:
        try:
            if (sys.argv[2] == 'manual'):
                f.write("\n")
                last_line = "000000"
                print 
                print 'Kämakto luke fya\'o!'
                print 'Zene ziveyko nga!'
                print
        except:
            print
            print "      *****************************"
            print "      *Last job unfinished, error.*"
            print "      *****************************"
            print
    if len(last_line) >= 6:
        print
        print "Mask on!"

        # Can process this as arguments, too
        try: 
            if (sys.argv[2] != 'manual'):
                project = sys.argv[2]
            if (sys.argv[2] == 'manual'):
                project = raw_input('project: ')
        except: project = raw_input('project: ')

        # Same with time
        try: what_time = str(sys.argv[3])
        except: 
            what_time = raw_input('begin: now. ')

        if what_time == '': time_adjust = datetime.now()

        if what_time != '':
            try:
                if len(what_time.split(':')) == 2:
                    time_now = str(datetime.now())
                    time_adjust = time_now[:11] + what_time + ':00.000000'
                    ## Failed attempt to subtract. Now really necessary, so
                    ## discaded.
                    #what_time = what_time.split(':')
                    #time_now = minutes_index(str(datetime.now())[11:16])
                    #what_time = int(what_time[0])*60 + int(what_time[1])
                    #what_time = time_now - what_time
                    print
                    print "-----------------------------------------------------------------------"
                    print "You have just adjusted time backwards: " 
                    print time_now + " is now " + time_adjust + "."
                    print "-----------------------------------------------------------------------"
                else:
                    pattern = re.compile("\d+")
                    match_o = re.match(pattern, what_time)
                    if (match_o != None):
                        what_time = what_time
                    time_now = datetime.now()
                    min_change = timedelta(minutes=int(what_time))
                    time_adjust = time_now - min_change
                    print
                    print "-----------------------------------------------------------------------"
                    print "You have just adjusted time backwards: " 
                    print str(time_now) + " is now " + str(time_adjust) + "."
                    print "-----------------------------------------------------------------------"
            except:
                if what_time == "last":
                    f = open(output_file_name, 'r+')
                    lineList = f.readlines()
                    time_adjust = lineList[-1].split(', ')[2]
                    print
                    print "-----------------------------------------------------------------------"
                    print "You start when you stopped, at " + time_adjust + "."
                    print "-----------------------------------------------------------------------"

        print
        f.write(str(time_adjust) + ', ' + project + ', ')
        f.close()

# How to end a logline. 
def end():
    f = open(output_file_name, 'r+')
    from datetime import datetime
    from datetime import timedelta
    lineList = f.readlines()
    on = lineList[-1]
    testLine = on.split(', ')
    if len(testLine) != 3:
        print
        print '    You are not currently working on a project.'
        answer = raw_input('    Fence it? yn ')
        if answer == 'y':
            fence()
        if answer == 'n':
            print '    Goodbye.'
            print 
        '''
        if len(testLine) == 3:
            print
            print '    You must manually fix log. '
            print
            testLine[1] = testLine[1].replace(',\n', '')
            testLine.append('')
            on = ', '.join(testLine)
        '''
    if len(testLine) == 3:
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
            if len(what_time.split(' ')) == 2:
                what_time = what_time.split(' ')
                if what_time[1][0] == 'y':
                    today = datetime.now()
                    off = what_time[0] + ':00.000000'
                    off = on[0:11] + off
                    print "You have just adjusted time backwards: " + \
                    str(today) + " is now " + str(off) + "."
                else: print 'I do not understand that word.'
            elif len(what_time.split(':')) == 2:
                today = datetime.now()
                off = what_time + ':00.000000'
                off = str(today)[0:11] + off
                print "You have just adjusted time backwards: " + str(today) \
                + "is now " + str(off) + "."
            else:
                today = datetime.now()
                min_change = timedelta(minutes=int(what_time))
                time_adjust = today - min_change
                print "You have just adjusted time backwards: " + str(off) + " is now " + str(time_adjust) + "."
                off = time_adjust
        off = str(off)
        FMT = '%H:%M:%S'
        tdelta = datetime.strptime(off[11:19], FMT) - datetime.strptime(on[11:19], FMT)
        total_time = str(tdelta)

        # This was adjusted to make the time not be stored as seven
        if len(total_time) == 16:
            total_time = total_time[-8:]
        if len(total_time) == 15:
            total_time = '0' + total_time[-7:]
        if len(total_time) == 7:
            total_time = '0' + total_time
        comment = raw_input('comment: ')
        comment = comment.replace(', ', ',')
        if comment == "x":
            comment = ""
        if comment == "c":
            comment = 'class'
        if comment == 'h':
            comment = 'homework'

        # This should give you the available PID options
        g = open(tasks_file, 'r+')
        g = g.readlines()
        PIDs = {}
        for line in g: 
            if line[0] == '#': continue
            line = line.split(', ')
            if line[0] == project:
                pid = line[7].replace('\n','')
                PIDs[pid] = line[1]
        if PIDs:
            print ' Possible PIDs for \'%s\':' % project
            print
            for keys in PIDs: print '\t%s\t%s' % (keys, PIDs[keys])
        else:
            pass

        # If there is only one PID, suggest it automagically.
        if len(PIDs) == 1:
            for keys in PIDs: key = keys
            PID = raw_input('PID (y): ' + key + ' ')
            if PID in ('y', 'ye', 'yes'):
                PID = key
        else:
            PID = ''
            PID = raw_input('PID: - ')
            if PID != '':
                while PID not in PIDs:
                    PID = raw_input('PID: - ')
        print

        print 'You were on the surface of Pandora from: ' + on[11:19] + ' to ' + off[11:19] + '.'
        time_labels = print_time_labels(total_time)
        try:
            pattern = re.compile("\d+")
            match_o = re.match(pattern, comment)
            if (match_o != None):
                    print "You survived for %s, and killed like %s %s." % (time_labels, match_o.group())
            if (match_o == None):
                    print "You survived for %s." % time_labels
        except: pass
        print
        if PID == '':
            print 'Operation ' + project + ' is now terminated. Your activity report readout: '
        else:
            print 'Operation ' + project + ' ('+PID+') is now terminated. Your activity report readout: '
        print comment
        
        print "------------------------------------------------------------------------"
        f.write(str(off) + ", ")
        f.write(total_time + ", ")
        f.write(project + ", ")
        f.write(comment.replace("\"", "'"))
        f.write(', ' + PID)
        f.write("\n")
        f.close()

# Fence works to make a begin and end together after the fact.
def fence():
    f = open(output_file_name,'r+')
    from datetime import datetime
    from datetime import timedelta
    time_now = datetime.now()
    lineList = f.readlines()
    last_line = lineList[-1].split(', ')
    ## Make sure that there isn't any current job
    if len(last_line) == 3:
        try:
            if (sys.argv[2] == 'manual'):
                f.write("\n")
                last_line = "000000"
                print 
                print 'Kämakto luke fya\'o!'
                print 'Zene ziveyko nga!'
                print
        except:
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
                # This will probably be buggy. 
                if first_time[6] != 'y':
                    conversion = raw_input('Did you mean 0'\
                            +first_time+'? yn ')
                    if conversion == 'y':
                        first_time = '0'+first_time
                    if conversion == 'n':
                        print "Military time please."
                        first_time = raw_input(' from (HH:MM): ')

        second_time = raw_input(' to: ')
        if len(second_time) != 5:
            if second_time != 'now':
                conversion = raw_input('Did you mean 0'\
                        +second_time+'? yn ')
                if conversion == 'y':
                    second_time = '0'+second_time
                if conversion == 'n':
                    print "Military time please."
                    second_time = raw_input(' from (HH:MM): ')
            if second_time == "now":
                now = datetime.now()
                second_time = str(now)[11:16]

        print ' Comment can be -x or -c.'
        comment = raw_input(' comment: ')

        # This should give you the available PID options
        g = open(tasks_file, 'r+')
        g = g.readlines()
        PIDs = {}
        for line in g: 
            if line[0] == '#': continue
            line = line.split(', ')
            if line[0] == project:
                pid = line[7].replace('\n','')
                PIDs[pid] = line[1]
        if len(PIDs) != 0:
            print ' Possible PIDs for \'%s\':' % project
            for keys in PIDs: print '\t%s\t%s' % (keys, PIDs[keys]) 

            PID = raw_input(' PID: - ')
            if PID == 'list':
                os.system('wyr today tasks all')
                PID = raw_input(' PID: - ')
            print
        else: PID = ''

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
                        # If we're dealing with yesterday
                        try:
                            if first_time[6] == 'y':
                                date = day_index(str(int(day_index(today[:10]))-1))
                                on = date + ' ' + first_time.split(' ')[0] + \
                                ':00.000000'
                        # Or today.
                        except:
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
        if minutes_index(on[11:19]) >= minutes_index(off[11:19]):
            check = raw_input('Are you sure? yn')
            if check in ('y', 'yes', 'ye'): print 'Ok then'
            if check not in ('y', 'yes', 'ye'): print 'Cancel then.'

        tdelta = datetime.strptime(off[11:19], FMT) \
                - datetime.strptime(on[11:19], FMT)
        total_time = str(tdelta)
        if len(total_time) == 7:
            total_time = '0' + total_time
        print
        print 'You were working from: %s %s to %s' \
            % (date_string(on[:10]), on[11:19], off[11:19])
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
        except: pass

        if PID != '':
            print 'This was assigned to PID: ' + PID + '.'
            print

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

# Am I running a project (one line print)
# This is useful for the bash prompt plugin

def state():
    f = open(output_file_name, 'r')
    lineList = f.readlines()
    line = lineList[-1].split(', ')
    if len(line) != 3: print 'off'
    if len(line) == 3: print line[1]

# Wait, what project am I running now, anyway?
def status():
    f = open(output_file_name, 'r')
    from datetime import datetime
    lineList = f.readlines()
    print 
    print "==============================  Status  =============================="
    line = lineList[-1].split(', ')

    # If there is no job currently going on
    if len(line) != 3:
        f = open(output_file_name, 'r+')
        lineList = f.readlines()

        # Find the last job and get the information for it
        on = lineList[-1].replace('\n', '').split(', ')
        onn = on[2].split(' ')[1].split('.')[0]

        # Find out how long it has been since then
        off = str(datetime.now())
        FMT = '%H:%M:%S'
        time_since = datetime.strptime(off[11:19], FMT) - \
        datetime.strptime(onn, FMT)

        # Split that up to deal with printing it
        time_since = str(time_since)
        time_since = time_since.split(', ')

        # If the last job was actually yesterday
        if len(time_since) == 2:
            if time_since[0] == '-1 day':
                time_since = time_since[1]
                print '\t\tYou\'ve crossed the dateline, Moby.'
                print

        # Otherwise
        if len(time_since) == 1:
            time_since = time_since[0]
        time_labels = print_time_labels(time_since)

        # time_since is actually a clever little hack where -1 day is the
        # string. It may not work if things are improved. 
        # In fact, I don't even think this is working now. 
        if len(time_since) >= 10:
            print "\tGood morning. You haven't started working yet today."
            print
            question = raw_input('\tWould you like to see what you did yesterday? yn ')
            if question == "y":
                yesterday()
            if question == "n":
                print

        # Tell me how long I haven't been working
        if len(time_since) < 10:
            print "\tYou have not been working for %s." % time_labels
            print
        print "\tYour last job, %s, lasted %s. Comment: \n\t%s" % (on[4], print_time_labels(on[3]), on[5])

    # If there is a job currently under way
    if len(line) == 3:
        on = line[0]
        last_job = line[1]
        off = str(datetime.now())

        # If you forgot to end the task yesterday or the days before
        # This won't work for month overflow.
        # This doesn't actually work -says you've been working for a day. Need
        # to fix later?
        if on[:10] != off[:10]:
            # Figure out how many days late
            #days_overflow = int(off[:10].split('-')[2]) - \
            #int(on[:10].split('-')[2])
            # NLP for the day string
            #day_string = 'day'
            #if days_overflow >= 2:
            #    day_string = 'days'
            FMT = '%H:%M:%S'
            tdelta = datetime.strptime(off[11:19], FMT) - datetime.strptime(on[11:19], FMT)
            if str(tdelta)[0] == '-':
                tdelta = str(tdelta)[8:]
                #print tdelta
            # Print it out properly
            print 'You are currently on project %s in Pandora.' % last_job
            print 'Time alive: %s.' % (#days_overflow, \
                    #day_string, 
                    print_time_labels(str(tdelta)))

        # If it is just a normal overflow, on the same day
        else:
            FMT = '%H:%M:%S'
            tdelta = datetime.strptime(off[11:19], FMT) - datetime.strptime(on[11:19], FMT)
            #print '\tYou are currently working on Wyrd In.' # % last_job
            print '\tYou are currently working on project \'%s\' in Pandora.' % last_job
            print '\tTime logged: %s.' % print_time_labels(str(tdelta))
    print "======================================================================"
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
    print "==============================  Cease  ==============================="
    print 'Mask off!'
    print 'You were on the surface of Pandora from ' + on[:19] + ' to ' + off[:19]
    print 'You survived for ' + str(tdelta) + '.'
    print 'What ho?! A break?'
    print "======================================================================"
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
        if line[0] == '#': continue
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
                except: pass
        if sys.argv[2] != line[1]:
            try:
                if (sys.argv[3] == "all"):
                    pattern = re.compile(str(sys.argv[2]), re.IGNORECASE)
                    match_o = re.search(pattern, line[5])
                    if (match_o != None):
                        FMT = '%H:%M:%S'
                        tt = datetime.strptime(line[3], FMT)
                        total_time = datetime.strptime(str(total_time), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                        if str(total_time)[9] == '2':
                            days += 1
                        total_time = str(total_time)[11:]
                        try:
                            if (sys.argv[4] == "print"):
                                line[5] = line[5].replace("\n", "")
                                print line[0][5:11] + "for " + print_time_labels(line[3]) + ": " + line[5]
                        except: pass
            except: pass
    if days == 1:
        day_string = "day"
    if days != 0:
        if sys.argv[2] == "wyring":
            print
            print "You have worked on this project for %d %s and %s." % (days, \
                    day_string, print_time_labels(total_time))
            print
        if sys.argv[2] != "wyring":
            print
            print "You have worked on %s for %d %s and %s." % (sys.argv[2], \
                days, day_string, print_time_labels(total_time))
            print
    if days == 0:
        if sys.argv[2] == "wyring":
            print
            print "You have worked on this project for %s." % print_time_labels(total_time)
            print
        if sys.argv[2] != "wyring":
            print
            print "You have worked on %s for %s." % (sys.argv[2], print_time_labels(total_time))
            print
    print "======================================================================"
    print
    f.close()


# What is happening today? How much have I worked, on what, and how productive
# have I been?
def today():
    global exp_wpd
    from datetime import datetime
    from datetime import timedelta
    f = open(output_file_name, 'r')
    lineList = f.readlines()
    time_now = datetime.now()
    print
    total_time = "00:00:00"
    total_time_alt = "00:00:00"
    logged_time = "00:00:00"
    specific_job_catch = "empty"
    done_jobs = []

    for line in lineList:
        if line[0] == '#': continue
        line = line.replace('\n', '').split(', ')
        if (str(time_now)[:10] == line[0][:10]) or (len(line) == 3):

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
                if worked[0] == '-': worked = worked[8:]
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
            except: continue #print 'problem with - statement' 

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
            except: continue #print 'problem with - except option'

    productivity_measure =(float(total_time[:2])*60+ \
            float(total_time[3:5]))/exp_wpd*100


    print "You have worked a total of %s today." % print_time_labels(total_time)
    if total_time != logged_time:
        print "(But you've logged %s.)" % print_time_labels(logged_time)
    print "So far, you have been %.2f%% productive." % productivity_measure

    try: 
        if (sys.argv[2] == "left"):
            time_left = exp_wpd-(float(total_time[:2])*60+float(total_time[3:5]))
            time_left_fmt = str(int((time_left-time_left%60)/60)) + ":" + str(int(time_left%60)) + ":00"
            print "You only have %s left to go!" % print_time_labels(time_left_fmt)
    except: pass

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
    except Exception,e: 
        print str(e)
        pass

    if len(done_jobs) != 0:
        print ''
        print 'Today, you have done: '

    # Tried to make a way to make the show more cleaning by collapsing similar
    # tasks.
    #for job in range(len(done_jobs)):
    #    if done_jobs[job].split()[0] == done_jobs[job+1].split()[0]:
    #        time_one = done_jobs[job].split(':')[0].split('for ')[1]
    #        time_two = done_jobs[job+1].split(':')[0].split('for ')[1]
    #        print time_two
    #        new_time = minutes_index(time_one) + minutes_index(time_two)
    #        print new_time

    if len(done_jobs) > 15:
        print '. . .'
    for job in done_jobs[-15:]:
        dedented_text = textwrap.dedent(job).strip()
        print textwrap.fill(dedented_text, initial_indent='',
        subsequent_indent='')
    print

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
        if line[0] == '#': continue
        line = task_division(line,oxygenList)
        line = line.split(', ')
        today = datetime.now()

        # Checks based on PIDs if the task if done 
        # Subtracts time from tasks done. 
            # To do:
                # In progress tasks.
                # No way of doing this atm - should log PIDs too, I guess?
                # Would have to change from .csv to do this. :/

        for log in oxygenList:
            if line[0] == '#': continue
            log = log.split(', ')

            # Ideally, this shouldn't neet to happen, but that's dependant on
            # only logging tasks to do.
            if len(log) == 6: pass
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
                    # This basically says that all conts go into to do later
                    # lists. May not be the best idea in the long run. We're
                    # going to have to see.
                    ignore = ['cont', 'over']
                    if line[6] not in ignore:
                        to_do_today.append(line)
                    else:
                        to_do_today_as_well.append(line)
                # Commenting this out because it doesn't help to see what you
                # do not need to do. Can uncomment later if needed.

                #if line[2] == '00:00:00':
                #    to_do_today_as_well.append(line)
            # Or if it is due tomorrow but should be done today.
            elif (int(day_index(line[3]))-int(line[5])+1) <= \
            today_index:
                ignore = ['cont', 'dcont', 'dover']
                if line[6] in ignore:
                    to_do_today.append(line)
                else:
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

    for x in range(len(to_do_today)):
        line = to_do_today[x]
        if line[6][0] == 'd':
            for original_line in lineList: 
                original_line = original_line.split(', ')
                if original_line[7] == line[7]:
                    date = original_line[3][5:]
                    if date[0] == '0': date = date[1:]
                    line[1] = line[1] + ' (' + date + ')'

    for x in range(len(to_do_today_as_well)):
        line = to_do_today_as_well[x]
        date = line[3][5:]
        if line[6][0] == 'd':
            if date[0] == '0': date = date[1:]
            line[1] = line[1] + ' (' + date + ')'

    # Sorts accoding to weight, and then alphabetically
    from operator import itemgetter
    to_do_today = sorted(to_do_today, key=itemgetter(2), reverse=True)
    to_do_today = sorted(to_do_today, key=itemgetter(4), reverse=True)

    to_do_today_as_well = sorted(to_do_today_as_well, key=itemgetter(2),
            reverse=True)
    to_do_today_as_well = sorted(to_do_today_as_well, key=itemgetter(4), reverse=True)


    # This checks to see if there is only one task going on which can be
    # subtracted from if you're trying to get a live amount left. 
    count = 0
    if len(log) <= 3:
        for check in to_do_today:
            if log[1] == check[0].strip(): count += 1
    try:
        if isinstance(int(sys.argv[3]), int): 
            visible = int(sys.argv[3])
            to_do_today = to_do_today[:visible]
    except:
        visible = 'all'

    # Prints out what you have to do today (or yesterday...)
    for line in to_do_today:
        # If there is only one task that can be subtracted from, subtract the
        # running tally from it. This more accurately shows the time left in
        # the list itself. 
        if count == 1:
            if log[1] == line[0].strip():
                on = log[0]
                off = str(datetime.now())
                if on[:10] == off[:10]:
                    FMT = '%H:%M:%S'
                    tdelta = datetime.strptime(off[11:19], FMT) - \
                    datetime.strptime(on[11:19], FMT)
                    worked = str(tdelta)
                    line[2] = minutes_index(line[2]) - minutes_index(worked)
                    if line[2] <= 0: line[2] = 0
                    line[2] = minutes_index(line[2])

        # Compiling the time left today
        time_left_today = time_add(line[2], time_left_today)

        # Formatting it for output
        if len(line[0]) <= 7: line[0] = line[0] + '\t'
        if print_time_labels(line[2]) != "a while":
            print "%s\t%s - %s." % (line[0], line[1], \
                    print_time_labels(line[2]))
        if print_time_labels(line[2]) == "a while":
            print "%s\t%s." % (line[0], line[1])

    # Prints out the rest if you want to see them. 
    try:
        if sys.argv[3] == "all":
            print
            print "Also to do today:"
            for line in to_do_today_as_well:

                # Compiling time left today
                time_also_left_today = time_add(line[2], \
                        time_also_left_today)

                # Formatting for output
                if len(line[0]) <= 6: line[0] = line[0] + '    '
                if print_time_labels(line[2]) != "a while":
                    print "%s\t %s - %s." % (line[0], line[1], \
                            print_time_labels(line[2]))
                if print_time_labels(line[2]) == "a while":
                    print "%s\t %s." % (line[0], line[1])

        # Trying to get a way to print out all dateless tasks
        try:
            if sys.argv[4] == 'x':
                print
                print 'X-tasks:'

                # Going back to the file
                for line in lineList:
                    if line[0] == '#': continue
                    line = line.split(', ')
                    if line[6] == 'x':

                        # Agg the time left
                        time_also_left_today = time_add(line[2], \
                                time_also_left_today)

                        #Formatting for output
                        if len(line[0]) <= 6: line[0] = line[0] + '    '
                        if print_time_labels(line[2]) != "a while":
                            print "%s\t %s - %s." % (line[0], line[1], \
                                    print_time_labels(line[2]))
                        if print_time_labels(line[2]) == "a while":
                            print "%s\t %s." % (line[0], line[1])
        except: pass
    except: pass

    # This should subtract the time from what you're doing from the total, 
    # based on seeing if the topic is in the tasks to do and is currently going
    # on.

    # This will run over and then have to be cut back if you go over. 
    if len(log) <= 3:
        if log[1] in projects:
            from datetime import datetime
            on = log[0]
            off = str(datetime.now())
            if on[:10] == off[:10]:
                FMT = '%H:%M:%S'
                tdelta = datetime.strptime(off[11:19], FMT) - datetime.strptime(on[11:19], FMT)
                #on = log.replace(", ", ". Your current Operation: ").replace(",", ".")
                worked = str(tdelta)
                time_left_today = minutes_index(time_left_today) - minutes_index(worked)
                time_left_today = minutes_index(time_left_today)

    print
    # Prints the total time left given the tasks to do.
    print "You have around %s of work to do." % print_time_labels(time_left_today)
    if time_also_left_today != "00:00:00":
        print "You also have an extra %s of work after that." % \
                print_time_labels(time_also_left_today)

def yesterday():
    global exp_wpd
    from datetime import datetime
    from datetime import timedelta
    f = open(output_file_name, 'r')
    lineList = f.readlines()
    time_now = datetime.now()
    print 
    print "-----------------------------Yesterday---------------------------------"
    print
    total_time = "00:00:00"
    logged_time = "00:00:00"
    for line in lineList:
        if line[0] == '#': continue
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
            float(total_time[3:5]))/exp_wpd*100
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
    global exp_wpd
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
    from datetime import date 
    if len(sys.argv) == 2: days_back = date.today().isoweekday()
    if len(sys.argv) >= 3: days_back = int(sys.argv[2])
    for x in range(days_back):
        total_time = "00:00:00"
        logged_time = "00:00:00"
        for line in lineList:
            if line[0] == '#': continue
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
                    except: pass
                    if line[1] in work_tasks:
                        tt = datetime.strptime(worked, FMT)
                        total_time = datetime.strptime(str(total_time), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                        total_time = str(total_time)[11:]
                if len(line) > 3:
                    worked = line[3]
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
                    except: pass

                    if line[1] in work_tasks:
                        tt = datetime.strptime(worked, FMT)
                        total_time = datetime.strptime(str(total_time), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                        total_time = str(total_time)[11:]
                        work_totality = datetime.strptime(str(work_totality), FMT) + timedelta(hours=tt.hour,minutes=tt.minute,seconds=tt.second)
                        if str(work_totality)[9] == '2':
                            wt_days += 1
                        work_totality = str(work_totality)[11:]
        
        productivity_measure = (float(total_time[:2])*60+ \
                float(total_time[3:5]))/exp_wpd*100
        productivity += productivity_measure
        print
        if x == 0: print "\tYou've worked %s today." % \
            print_time_labels(total_time)
        if x == 1:
            print "\tYou worked a total of %s yesterday." % \
            print_time_labels(total_time)
        if x >= 2:
            print "\tYou worked a total of %s %s days ago." % \
        (print_time_labels(total_time), x)
        try:
            if sys.argv[3] == "logged":
                print "\t(But you logged %s.)" % print_time_labels(logged_time)
        except: pass
        print "\tYou were %.2f%% productive." % productivity_measure

    if lt_days != int(0):
        logged_totality = str((lt_days*24) + int(logged_totality[:2])) + logged_totality[2:]
    if wt_days != int(0):
        work_totality = str((wt_days*24) + int(work_totality[:2])) + work_totality[2:]
    # This only counts today up to the current time, weighing it better.
    accurate_days = float(days_back)-1
    try:
        if sys.argv[4] == 'workdays': accurate_days = accurate_days*.7142
        try: 
            if len(sys.argv) == 6: accurate_days = \
                    accurate_days - int(sys.argv[5])
        except: pass
    except: pass
    accurate_days += float(minutes_index(str(time_now)[11:16]))/1440

    productivity = productivity / accurate_days
    print
    print "-----------------------------------------------------------------------"
    if int(days_back) <= 7:
        print "This week, you have worked %s." % print_time_labels(work_totality)
    if int(days_back) > 7:
        print "You have worked %s." % print_time_labels(work_totality)
    if 0 < productivity <= 20:
        print "You are and were really lazy and inept." 
    if 20 < productivity <= 50:
        print "You were only %.2f%% productive" % productivity
    if 50 < productivity <= 75:
        print "You were %.2f%% productive." % productivity
    if 75 < productivity <= 100:
        print "You were, at %.2f%%, actually pretty productive." %productivity
    if productivity > 100:
        print "Well done. You have been really fucking productive. %.2f%%, to be exact." \
                % productivity
    work_totality = work_totality.split(':')
    hours_per_diem = float(work_totality[0])/accurate_days
    print "Which is %.2f hours per day." % hours_per_diem
    if logged_totality != "00:00:00":
        print
        print "Time actually logged: %s." % print_time_labels(logged_totality)
        logged_totality = logged_totality.split(':')
        hours_per_diem = float(logged_totality[0])/accurate_days
        print "Which is %.2f hours per day." % hours_per_diem
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
        if line[0] == '#': continue
        line = line.split(', ')
        topics.append(line[1])
    set = {}
    map(set.__setitem__, topics, []) 
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(sorted(set.keys()))
    print "------------------------------------------------------------------------"


'''
The next segment is all for the tasks.csv file. This is different from the
oxygen file in that it is for actual things which need to be done, and not for
a log of time. Hopefully, this will evolve into a task manager that is more
suited to my needs than things is.
'''

def list_all():
    f = open(tasks_file, 'r+')
    print
    print 'All open tasks:'
    topics = {}
    try:
        if sys.argv[2] == 'topic':
            print 'By topic.'
            for line in f.readlines():
                if line[0] == '#': continue
                line = line.replace('\n','').split(', ')
                if line[0] in topics: 
                    topics[line[0]][line[1]] = line[2:]
                else: 
                    topics[line[0]] = {}
                    topics[line[0]][line[1]] = line[2:]

            for topic in topics.iterkeys():
                print
                print '%s: ' % topic
                for item in topics[topic]:
                    print '\t', topics[topic][item][1][5:], '\t', \
                            print_time_labels(topics[topic][item][0])\
                            .replace('a while', '-\t').replace('1 hour', \
                            '1 hour\t'), '\t', item
            print
        if sys.argv[2] == 'date':
            print 'By date.'
            for line in f.readlines():
                if line[0] == '#': continue
                line = line.replace('\n','').split(', ')
                if line[3] in topics: 
                    topics[line[3]][line[1]] = line
                else: 
                    topics[line[3]] = {}
                    topics[line[3]][line[1]] = line

            for topic in sorted(topics.iterkeys()):
                print
                print '%s: ' % topic
                for item in topics[topic]:
                    print '  ', print_time_labels(topics[topic][item][2])\
                            .replace('a while', '-\t').replace('1 hour', \
                            '1 hour\t'), '\t', topics[topic][item][0], '\t',\
                            item
            print
    except: 
        print 'Not ordered.'
        for line in f.readlines():
            if line[0] == '#': continue
            line = line.replace('\n','').split(', ')
            print '  %s\t%s\t%s\t%s' % (line[0], line[1], \
                    print_time_labels(line[2]), line[3])
        print 


def projects():
    import pprint
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    topics = []
    print
    print "-----------------------------Task Topics--------------------------------"
    for line in lineList:
        if line[0] == '#': continue
        line = line.split(', ')
        topics.append(line[0])
    set = {} 
    map(set.__setitem__, topics, []) 
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(sorted(set.keys()))
    print "------------------------------------------------------------------------"
    try:
        tasks = []
        time_expected = []
        date_due = []
        for line in lineList:
            if line[0] == '#': continue
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
    except: pass

def random_task():
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    today_lineList = []
    try:
        if sys.argv[2] == 'today':
            for line in lineList:
                if line[0] == '#': continue
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
    except: pass
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
            if time_exp[x][0] == "m":
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

        # Checks the time format until all options work.
        #checker = False
        #while checker == False:
        #    check = raw_input('is that ' + time_exp + '? ')
        #    if check in ('y', 'ye', 'yes', 'ok', ''):
        #        checker = True
        #    elif re.search(pattern, check) != None:
        #        time_exp = check
        #    else:
        #        check = raw_input('expected time: ')
        #        time_exp = check


    date = raw_input('date due: ')

    task_types = ['hard', 'soft', 'cont', 'over',\
            'dhard', 'dsoft', 'dcont', 'dover','x']

    if date not in ('today', 'tonight', 'now'):
        if date != 'x':

            days_before = raw_input('days to work on: ')

            task_type = raw_input('type: ')
            while task_type not in task_types:
                print 'Task types: hard  soft  cont over (d--)'
                task_type = raw_input('\ttype: ')

    if date in ('today', 'tonight', 'now'):

        task_type = raw_input('type: hard. ')
        if task_type == '': task_type = 'hard'
        while task_type not in task_types:
            print 'Task types: hard  soft  cont (d--)'
            task_type = raw_input('\ttype: ')

        days_before = '1'

    if date == 'x':

        days_before = '1'
        task_type = 'x'

    date = date_string(date)

    # Some weird issue with assigning April?
    # print date

    weight = raw_input('weight: 1 ')
    if weight == '':
        weight = '1'

    PID = 0
    for line in lineList[-5:]:
        # Commented out as it would ignore finished tasks and repeat PIDs
        #if line[0] == '#': continue
        line = line.split(', ')
        PID = int(line[-1]) + 1

    print
    print 'You have written this task: %s.' % (task)
    print ' -> '+ job
    print 'This should last %s, and is due %s.'%(print_time_labels(time_exp),\
            date)
    print 'Weight: %s. Days to work on: %s. Type: %s. PID: %s.' % \
            (weight, days_before, task_type, str(PID))
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
    f = open(output_file_name, 'r')
    oxygenList = f.readlines()
    to_do_today = []
    error = []
    for line in lineList:
        if line[0] == '#': continue
        line = task_division(line,oxygenList)
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
            except: pass
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
        except: pass
        print "------------------------------------------------------------------------"
        print

def unify():
    import pprint
    f = open(tasks_file, 'r+')
    taskList = f.readlines()
    f = open(output_file_name, 'r+')
    logList = f.readlines()
    tasks = []
    for line in taskList:
        if line[0] == '#': continue
        line = line.split(', ')
        tasks.append(line[0])
    logs = []
    for line in logList:
        if line[0] == '#': continue
        line = line.split(', ')
        logs.append(line[1])
    tasks_only = []
    logs_only = []
    for item in tasks: 
        if item not in logs: tasks_only.append(item)
    for item in logs: 
        if item not in tasks: logs_only.append(item)
    print
    print "--------------------------Incongruous Tasks-----------------------------"
    print 'Tasks not in the log:'
    set = {}
    map(set.__setitem__, tasks_only, []) 
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(set.keys())
    print 'Logs not in tasks:'
    set = {}
    map(set.__setitem__, logs_only, []) 
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(set.keys())
    print "------------------------------------------------------------------------"


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
        if line[0] == '#': continue
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
    readLines = f.readlines()
    buyd = []
    print 
    print 'Add to list:'
    item = raw_input('Item: ')
    price = raw_input('Price (€): ')
    print 'Reasons: food, life, gifts, uni, other'
    reason = raw_input('Reason: ')
    urgent = raw_input('Urgent [y/n]: ')
    buyd.extend([item, price, reason, urgent, '\n'])
    buyd = ', '.join(buyd)
    f.write(buyd)
    print 'Added to list.'
    print
    f.close()

def ghi():
    import subprocess
    cmd = [ 'ghi', 'list', '--reverse']
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    test = output.split('\n')
    if len(test) <= 2:
        print 'There is currently no internet connection.'
        print 
        f = open(issues_list, 'r+')
        f = f.read()
        print f
    else:
        f = open(issues_list, 'w+')
        f.write(output)
        print output

# This integrates with ical to grab todays tasks. must be done manually
def ical():
    import subprocess

    # print
    print ''
    print ' Writing to file...'
    print ''

    # Open tasks file for writing to.
    f = open(tasks_file, 'r+')
    lineList = f.readlines()

    # Get the last PID, for later.
    PID = 0
    line = lineList[-1].split(', ')
    PID = int(line[-1]) + 1

    # For predefined event names
    classes = {
        'Semantic Theorie': 'sem', \
        'Discourse Parsing and Language Technology': 'disc', \
        'Basic Algorithms for Computational Linguistics': 'bracoli', \
        'Language Technology': 'LT', \
        'Computational Linguistics': 'coli', \
        'Multiword Expressions and Collocations in theory and practice':\
        'mword',
        'CSA3221 - Semantic Technologies for the Web (CA & Mmo)': 'sw', \
        'CSA3220 - Machine Learning, Expert Systems and Fuzzy Logic (KG)':\
        'ml', 'ICS5000 - Natural Language Programming (MR)':'nlp', \
        'CPS5000 - Fundamentals of Discrete Mathematics (GP)':'math', \
        'LIN5570 - Computational Morphology (MR & CB)': 'como',\
        'ICT5901 - Research Methods (JM)':'rm',\
        'CSA5019 - Languages, Automata and Compilers (AF & SS)':'lac'
        }

    # ical has to be set up with a semlink. This only grabs the items from the
    # rest of today, not for ones that have passed already.
    cmd = [ 'ical', '-n', 'eventsToday' ]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

    # Split based on bullet points
    output = output.split('\xe2\x80\xa2 ')

    # For predefined calendars
    search_strings = ['University', 'Work']

    # Check to see if the event is in those
    for y in search_strings:

        # For each task
        for x in output:

            pattern = re.compile("\(" + y + "\)")
            match_o = re.search(pattern, x)
            if (match_o != None):
                replacement = ' (' + y + ')'
                # Grab it
                x = x.replace(replacement, '').replace('    ','').split('\n')
                # If it is predefined, sort it into the right topic
                if classes.has_key(x[0]):
                    topic = classes[x[0]]
                    task = 'Class'
                # Else, ask for it.
                else:
                    pass_statement = raw_input('\n\tWrite ' + x[0] + '? yn')
                    if pass_statement == 'y':
                        pass
                    else: continue
                    topic = raw_input('\tTopic for: "' + x[0] + '"? ')
                    if topic == 'none':
                        continue
                    task = raw_input('\tIs the task "' + x[0] + '"? yn ')
                    if task == 'y': task = x[0]
                    else:
                        task = raw_input('Task: ')
                # Except for location, lose that information
                # Get the time it will take (but not when.)
                pattern = re.compile("location")
                match_loc = re.search(pattern, x[1])
                if match_loc != None:
                    time = x[2].split(' - ')
                else:
                    time = x[1].split(' - ')
                print '\nFrom %s to %s: ' % (time[0], time[1])
                time = minutes_index(time[1])-minutes_index(time[0])
                time = minutes_index(time)
                # Get the date
                today = str(datetime.datetime.now())[:10]
                # The final string to be written
                task_line = [topic, task, time, today, '1', '1', 'hard', \
                        str(PID)+'\n']

                # Print it prettily
                print "    %s\t %s - %s." % (task_line[0], task_line[1], \
                        print_time_labels(task_line[2]))
                task_line = ', '.join(task_line)

                # Write it
                response = False
                while response == False:
                    write = raw_input('Write it? ')
                    if write in ('y', 'ye', 'yes', ''):
                        f.write(task_line)
                        PID += 1
                        response = True
                    if write in ('n', 'no'):
                        response = True

            continue

    print ''
    print 'Written.'
    print ''
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
    #void()
    #if (sys.argv[1] == "test"): minutes_index(sys.argv[2])
    try:
        possible_arguments = ['mvim', 'vi', 'test', 'today', 
        'search', 'cease', 'status', 'end', 'begin', 'being', 'start', 'help',
        'yesterday', 'topics', 'week', 'fence', 'tasks', 'projects', 'random',
        'write', 'task', 'PID', 'list', 'buy', 'to', 's', 'e', 'b',
        'h', 'y', 'f', 'ta', 'p', 'r', 'w', 'l', 'unify', 'ghi', 'ical',
        'todo', 'ca', 'n', 't', 'we', 'P', 'u', 'li', 'bi', 'g', 'ca', 'state',
        'log']

        # Terminal
        if (sys.argv[1] == "state"): state()

        # Editing
        if (sys.argv[1] == "mvim"): edit(sys.argv[2])
        if (sys.argv[1] == "vi"): edit(sys.argv[2])

        # Logs
        if (sys.argv[1] == "today") or (sys.argv[1] == "n"): today()
        if (sys.argv[1] == "search") or (sys.argv[1] == 'se'): search()
        if (sys.argv[1] == "cease") or (sys.argv[1] == 'cease'): cease()
        if (sys.argv[1] == "status") or (sys.argv[1] == "s"): status()
        if (sys.argv[1] == "end") or (sys.argv[1] == "e"): end()
        if (sys.argv[1] == "begin") or (sys.argv[1] == "b"): begin()
        if (sys.argv[1] == "start"): begin()
        if (sys.argv[1] == "help") or (sys.argv[1] == "h"): help()
        if (sys.argv[1] == "yesterday") or (sys.argv[1] == "y"): yesterday()
        if (sys.argv[1] == "topics") or (sys.argv[1] == 't'): topics()
        if (sys.argv[1] == "week") or (sys.argv[1] == 'we'): this_week()
        if (sys.argv[1] == "fence") or (sys.argv[1] == "f") or \
                (sys.argv[1] == "log"): fence()

        # Tasks
        if (sys.argv[1] == "todo") or (sys.argv[1] == "l"): list_all()
        if (sys.argv[1] == "tasks") or (sys.argv[1] == "ta"): tasks()
        if (sys.argv[1] == "projects") or (sys.argv[1] == "p"): projects()
        if (sys.argv[1] == "random") or (sys.argv[1] == "r"): random_task()
        if (sys.argv[1] == "write") or (sys.argv[1] == "w"): task_write()
        if (sys.argv[1] == "task"): todo()
        if (sys.argv[1] == "PID") or (sys.argv[1] == 'P'): PID(sys.argv[2])
        if (sys.argv[1] == "unify") or (sys.argv[1] == 'u'): unify()

        # Shopping list
        if (sys.argv[1] == 'list') or (sys.argv[1] == "li"): view_list()
        if (sys.argv[1] == 'buy') or (sys.argv[1] == 'bi'): buy()

        # Github issue tracker
        if (sys.argv[1] == 'ghi') or (sys.argv[1] == 'g'): ghi()

        # iCal integration
        if (sys.argv[1] == 'ical') or (sys.argv[1] == 'ca'): ical()

        if sys.argv[1] not in possible_arguments:
            print '\n You were just mauled by a ' + random_navi_animal() + '.\n '
    except IndexError: status()

    # Today's my birthday, after all. - Jake Sully
