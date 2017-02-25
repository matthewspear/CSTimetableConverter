import os
import sys
import urllib2
from datetime import datetime
from icalendar import Calendar

# calendar url
path = os.path.dirname(os.path.abspath(__file__))
url = ''

# options
open_on_completion = False

# filename
timetable_name = 'Timetable.ics'

# replacements
replacements = {
        'COMP-1st Yr Tutorial': 'Tutorial',
        'COMP-2nd Yr Tutorial (SH)': 'Tutorial',
        'COMP-PASS':'Pass',
        'COMP-PASS2':'Pass',
        'COMP10120':'Group Project',
        'COMP11120':'Maths',
        'COMP11212':'Computation',
        'COMP12111':'Engineering',
        'COMP14112':'AI',
        'COMP15111':'Architecture',
        'COMP16212':'Java',
        'COMP18112':'Distributed Systems',
        'COMP23111':'Databases',
        'COMP23420':'Software Engineering',
        'COMP25111':'Operating Systems',
        'COMP26120':'Algorithms',
        'COMP21111':'Logic and Modelling',
        'COMP22111':'Processor Microarchitecture',
        'COMP24111':'Machine Learning',
        'COMP28411':'Networks',
        'COMP22712':'Microcontrollers',
        'COMP24412':'Symbolic AI',
        'COMP27112':'Computer Graphics',
        'COMP28112':'Distributed Computing',
        'COMP28512':'Mobile Systems'
        }

global timetable

def main():
    global timetable

    # create calendar
    timetable = create_calendar()

    # get request
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    # process data
    data = response.read()
    cal = Calendar.from_ical(data)
    for event in cal.walk('vevent'):
        event['summary'] = calculate_name(event)
        event['location'] = remove_comma(event)
        append_to_calendar(event)

    # write files
    write_calendar(timetable_name, timetable)

    # open files
    if open_on_completion:
        open_calendar(timetable_name)

def calculate_name(event):
    summary = event.get('summary')
    name = str(summary)
    for src, target in replacements.iteritems():
        name = name.replace(src, target)
    return name

def remove_comma(event):
    location = str(event.get('location'))
    location = location.replace('\, ', '')
    location = location.replace(', ', '')
    return location

def append_to_calendar(event):
    global timetable

    print event['summary']
    timetable.add_component(event)

def create_calendar():
    calendar = Calendar()
    calendar.add('prodid', '-//My calendar product//mxm.dk//')
    calendar.add('version', '2.0')
    return calendar

def write_calendar(name, calendar):
    f = open(name, 'w+b')
    f.write(calendar.to_ical())
    f.close()

def open_calendar(name):
    open_file(path + '/' + name)

def open_file(path):
    os.system('open ' + path)

if __name__ == '__main__':
    main()
