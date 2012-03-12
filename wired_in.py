#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This is a code for managing my time in a simple and orderly fashion.
Richard Littauer
"""
import os
import time
import datetime
import sys
import re
import dis
import random
import math
import textwrap

output_file_name = "oxygen_log.csv"
tasks_file = "tasks.csv"


work_tasks = ["hiwi", "FLST", "PSR", "syntax", "CL4LRL", "stats"]


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
    print
    print "-----------------------------------------------"
    print




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
    output = "%s %s, %s %s, and %s %s" % (hours, hour_string, minutes, minute_string, seconds, second_string)
    if hours == 0:
        output = "%s %s and %s %s" % (minutes, minute_string, seconds, second_string)
    if seconds == 0:
        output = "%s %s and %s %s" % (hours, hour_string, minutes, minute_string)
    if minutes == 0:
        output = "%s %s" % (hours, hour_string)
    if (seconds == 0) and (hours == 0):
        output = "%s %s" % (minutes, minute_string)
    if (seconds == 0) and (hours == 0) and (minutes == 0):
        output = "a while"
    return output

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

def day_index(x):
    days = 0
    days += int(x[8:10])
    months = [[], \
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
    days += months[int(x[5:7])][1]
    return str(days)

#Natural language processor for numbers
#input whatever, returns string
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


def random_navi_animal():
    animal = ["'angts\xcck", "eltungawng", "ngawng", "fpxafaw", "ikran",
            "ikranay", "kali'weya", "lenay'ga", "lonataya", "nantang",
            "pa'li", "palulukan", "riti", "talioang", "teylu", "toruk",
            "yerik", "yomh\xcc'ang", "hi'ang", "zize'"]
    return str(animal[random.randrange(len(animal)-1)])



def test():
    ##This is currently testing the ability to divide up time in different
    ##ways. What would be good is an output format that isn't a day string.
    ##Also, to output line by line, but recall original dates. 
    task_types = ['dead', #Day of only.
            'hard', #Days before, doesn't divide.
            'soft', #Days before, divides time.
            'cont', #Repeats from start date for x days.
            'x'] #Doesn't repeat or show unless asked.
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    for line in lineList:
        line = line.split(', ')
        task_type = line[6].replace('\n', '')
        day = line[3]

        if task_type not in task_types:
            print "Something is wrong with your formatting tasks."

        if task_type == 'dead':
            print line

        if task_type == 'hard':
            start_appearing = int(day_index(day)) - int(line[5])
            print line[2], day_index(day), line[5], task_type
            #Not sure about this one. Not printing, for one.

        if task_type == 'soft':
            start_appearing = int(day_index(day)) - int(line[5])
            time_for_task = int(line[2][0:2])*60 + int(line[2][3:5])
            time_for_task = time_for_task / int(line[5])
            print time_for_task
            print line[2], day_index(day), line[5], task_type
            #ibid

        if task_type == 'cont':
            today = str(datetime.datetime.now())[:10]
            if day_index(today) >= day_index(day):
                    print "strange"
            print line[2], day_index(day), line[5], task_type

        if task_type == 'x':
            print line[2], line[5], task_type



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
    print

    print 'You were on the surface of Pandora from: ' + on[:19] + ' to ' + off[11:19] + '.'
    time_labels = print_time_labels(total_time)
    try:
        pattern = re.compile("\d+")
        match_o = re.match(pattern, comment)
        if (match_o != None):
                print "You survived for %s, and killed like %s nantangs." % (time_labels, match_o.group())
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
    f.write("\n")
    f.close()


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
        #Clean this us using split()
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



def today():
    from datetime import datetime
    from datetime import timedelta
    f = open(output_file_name, 'r')
    lineList = f.readlines()
    #Will be useful when you integrate PIDs.
    oxygenList = lineList
    time_now = datetime.now()
    print 
    total_time = "00:00:00"
    total_time_alt = "00:00:00"
    logged_time = "00:00:00"
    specific_job_catch = "empty"

    for line in lineList:
        line = line.replace('\n', '').split(', ')
        if str(time_now)[:10] == line[0][:10]:

            if len(line) == 3:
                #if line[1] in work_tasks:
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
                #if line[1] in work_tasks:
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
#    print
#    print "You have worked a total of %s today." % print_time_labels(total_time)
#    if total_time != logged_time:
#        print "(But you've logged %s.)" % print_time_labels(logged_time)
#    print "So far, you have been %.2f%% productive." % productivity_measure

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
 #   print 

    #This loads up the tasks bit if you want to see what you need to do today.
    try:
        if sys.argv[2] == "tasks":
            f = open(tasks_file, 'r+')
            lineList = f.readlines()

            print
            print "You need to:"

            time_left_today = "00:00:00"
            time_also_left_today = "00:00:00"
            to_do_today = []
            to_do_today_as_well = []

            #Adds the tasks to do to a list.
            for line in lineList:
                line = line.split(', ')
                today = datetime.now()

                #Checks based on PIDs if the task if done 
                #Subtracts time from tasks done. 
                    #To do:
                        #Repeating tasks.
                        #Under zero tasks?
                        #In progress tasks.

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



                if line[3] != "x":
                    if day_index(str(today)[:10]) >= day_index(line[3][:10]):
                        to_do_today.append(line)
                    elif (int(day_index(line[3]))-int(line[5])+1) <= \
                    int(day_index(str(today)[:10])):
                        to_do_today_as_well.append(line)

                if line[3] == 'x':
                    to_do_today_as_well.append(line)

            #Prints out what you have to do today (or yesterday...)
            for x in range(len(to_do_today)):
                line = to_do_today[x]
                PID = line[7].replace('\n', '')
                time_left_today = time_add(line[2], time_left_today)
                if print_time_labels(line[2]) != "0 minutes":
                    print " %s %s : %s for %s." % (PID, line[0], line[1], \
                            print_time_labels(line[2]))
                if print_time_labels(line[2]) == "0 minutes":
                    print " %s %s : %s." % (PID, line[0], line[1])
            print
    except: jesus = "dead"
    print 
'''
            #Prints out the rest if you want to see them. 
            try:
                if sys.argv[3] == "all":
                    print "Also to do today:"
                    for x in range(len(to_do_today_as_well)):
                        line = to_do_today_as_well[x]
                        PID = line[7].replace('\n', '')
                        time_also_left_today = time_add(line[2], \
                                time_also_left_today)
                        #print " %s %s : %s for %s." % (PID, line[0], line[1], \
                        #        print_time_labels(line[2]))
                        if print_time_labels(line[2]) != "0 minutes":
                            print " %s %s : %s for %s." % (PID, line[0], line[1], \
                                    print_time_labels(line[2]))
                        if print_time_labels(line[2]) == "0 minutes":
                            print " %s %s : %s." % (PID, line[0], line[1])
                    print
                    print

            #Nonsense is good.
            except: jesus = "is he dead?"

            #Prints the total time left given the tasks to do.
            print "You have %s to go." % print_time_labels(time_left_today)
            if time_also_left_today != "00:00:00":
                print "You have %s to go, as well." % \
                print_time_labels(time_also_left_today)

    except: jesus = "dead"
    print 
'''

def vacation():
    from datetime import datetime
    from datetime import timedelta
    f = open(output_file_name, 'r')
    lineList = f.readlines()
    #Will be useful when you integrate PIDs.
    oxygenList = lineList
    time_now = datetime.now()
    print 
    total_time = "00:00:00"
    total_time_alt = "00:00:00"
    logged_time = "00:00:00"
    specific_job_catch = "empty"

    for line in lineList:
        line = line.replace('\n', '').split(', ')
        if str(time_now)[:10] == line[0][:10]:

            if len(line) == 3:
                #if line[1] in work_tasks:
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
                #if line[1] in work_tasks:
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

    #This loads up the tasks bit if you want to see what you need to do today.
    try:
        if sys.argv[2] == "tasks":
            f = open(tasks_file, 'r+')
            lineList = f.readlines()

            print
            print "You need to:"

            time_left_today = "00:00:00"
            time_also_left_today = "00:00:00"
            to_do_today = []

            #Adds the tasks to do to a list.
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

            #Prints out what you have to do today (or yesterday...)
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
    total_time = "00:00:00"
    total_time_alt = "00:00:00"
    logged_time = "00:00:00"
    specific_job_catch = "empty"
    for line in lineList:
        line = line.replace('\n', '')
        today_date = str(time_now)[:10]
        if int(today_date[8:]) < 30:
            modify_date = int(today_date[8:])-1
            today_date = today_date[:8] + str(modify_date)
        if int(today_date[8:]) >= 30: print "Uh. End of month. Awkward."
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
    print
    print "You worked a total of %s yesterday." % print_time_labels(total_time)
    print "(But you logged %s.)" % print_time_labels(logged_time)
    print "You were %.2f%% productive." % productivity_measure
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
            today_date = str(time_now)[:10]
            if int(today_date[8:]) < 30:
                modify_date = int(today_date[8:])-x
                today_date = today_date[:8] + str(modify_date)
            if int(today_date[8:]) >= 30: print "Uh. End of month. Awkward."
            line  = line.split(', ')
            if today_date == line[0][:10]:

                if len(line) == 3:
                    #if line[1] in work_tasks:
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
                    #read_out_block = "%s for %s: %s" % (line[1], time_labels, read_out)
                    #dedented_text = textwrap.dedent(read_out_block).strip()
                    #print textwrap.fill(dedented_text, initial_indent='', subsequent_indent='    ')
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
    if len(last_line) != 6:
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
    if len(last_line) == 6:
        print 
        print "-------------------------------Fence------------------------------------"

        project = raw_input(' project: ')
        first_time = raw_input(' from (HH:MM): ')
        if len(first_time) != 5:
            if first_time != "last":
                print "You're an idiot."
                first_time = raw_input(' from (HH:MM): ')
        second_time = raw_input(' to (HH:MM): ')
        if second_time == "now":
            now = datetime.now()
            second_time = str(now)[11:16]
        print ' Comment can be -x or -c.'
        comment = raw_input(' comment: ')
        print

        ## Find the first time. 
        if first_time == "last":
            on = last_line[2]
            print on
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
                    print "You survived for %s, and killed like %s nantangs." % (time_labels, match_o.group())
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
        f.write("\n")
        f.close()


'''
The next segment is all for the tasks.csv file. This is different from the
oxygen file in that it is for actual things which need to be done, and not for
a log of time. Hopefully, this will evolve into a task manager that is more
suited to my needs than things is.
'''

def tasks():
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
    today = datetime.datetime.now()
    # You should put in a converter here to convert from 0000/00/00 to
    # 0000-00-00

    if date == "today":
        date = str(today)[:10]
    if date == "tomorrow":
        date = str(today)[:8] + str(int(str(today)[8:10])+1)
        bad_dates = ["29", "30", "31"]
        if date[8:10] in bad_dates:
            print "Check the month - there may be no tomorrow."

    weight = raw_input('weight: ')

    noose = "filler"

    if (date != 'x'):
        if date != str(today)[:10]:

            days_before = raw_input('days to work on: ')

            #noose = raw_input('hard or soft: ')

    if (date == 'x') or (date == str(today)[:10]):

        days_before = '1'
        #noose = 'x'

    PID = 0
    for line in lineList:
        line = line.split(', ')
        PID = int(line[-1]) + 1

    print
    f.write(task + ', ' + job + ', ' + time_exp + ', ' + date \
            + ', ' + weight + ', ' + days_before + \
            ', ' + noose + ', ' + str(PID) + '\n')
    f.close()

def todo():
    f = open(tasks_file, 'r+')
    lineList = f.readlines()
    to_do_today = []
    for line in lineList:
        line = line.split(', ')
        today = datetime.datetime.now()
        if str(today)[:10] == line[3][:10]:
            to_do_today.append(line)
        ##You're going to need to fix this later when you have dates that go
        ##over a month. As it is, this'll only work inside of month boundries.
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
        except: this_is = "a fail"
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


if __name__ == "__main__":
    if (sys.argv[1] == "test"):
        test()
    #Today is now dependant in some aspects \
            #on tasks.csv
    if (sys.argv[1] == "today"):
        today()
    if (sys.argv[1] == "vacation"):
        vacation()
    if (sys.argv[1] == "search"):
        search()
    if (sys.argv[1] == "cease"):
        cease()
    if (sys.argv[1] == "status"):
        status()
    if (sys.argv[1] == "end"):
        end()
    if (sys.argv[1] == "begin") or (sys.argv[1] == "being"):
        begin()
    if (sys.argv[1] == "start"):
        begin()
    if (sys.argv[1] == "help"):
        help()
    if (sys.argv[1] == "yesterday"):
        yesterday()
    if (sys.argv[1] == "topics"):
        topics()
    if (sys.argv[1] == "week"):
        this_week()
    if (sys.argv[1] == "fence"):
        fence()
    #From here is for the tasks.csv file.
    if (sys.argv[1] == "projects"):
        tasks()
    if (sys.argv[1] == "random"):
        random_task()
    if (sys.argv[1] == "write") or (sys.argv[1] == "w"):
        task_write()
    if (sys.argv[1] == "task"):
        todo()


'''
To do:
    - integrate with an SQL database, make the comment feature better.
    - Add in a thing about weekly estimates.
    - Figure out the noose hard soft continuum thing bitch
    - Divide up tasks according to days left in them. 
    - Find a way to figure out the time lost between projects.
    - make a date_added function. 
    - Make a function that separates work form non-work in today tasks. 
    - Make PIDs - this will have to be integrated with SQL.
'''
