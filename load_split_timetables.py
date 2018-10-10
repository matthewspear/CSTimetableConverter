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

# filenames
lectures_name = 'Lectures.ics'
workshops_name = 'Workshops.ics'
labs_name = 'Labs.ics'
other_name = 'Other.ics'

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
        'COMP28512':'Mobile Systems',
        'COMP30040':'Third Year Project',
        'COMP32211':'System-on-Chip',
        'COMP33511':'User Experience',
        'COMP33711':'Software Engineering',
        'COMP36111':'Advanced Algorithms 1',
        'COMP37111':'Advanced Computer Graphics',
        'COMP38411':'Cryptography',
        'COMP34412':'Natural Language Systems',
        'COMP35112':'Chip Multiprocessors',
        'COMP36212':'Advanced Algorithms 2',
        'COMP36512':'Compilers',
        'COMP37212':'Computer Vision',
        'COMP32412':'Internet of Things',
        'COMP34120':'AI and Games',
        'COMP38120':'Documents, Service and Data'
        }

global lectures
global workshops
global labs
global other

def main():
    global lectures
    global workshops
    global labs
    global other

    # create calendars
    lectures = create_calendar()
    workshops = create_calendar()
    labs = create_calendar()
    other = create_calendar()

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
    write_calendar(lectures_name, lectures)
    write_calendar(workshops_name, workshops)
    write_calendar(labs_name, labs)
    write_calendar(other_name, other)

    # open files
    if open_on_completion:
        open_calendar(lectures_name)
        open_calendar(workshops_name)
        open_calendar(labs_name)
        open_calendar(other_name)

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
    global lectures
    global workshops
    global labs
    global other

    print event['summary']

    if "LECTURE" in str(event['description']):
        lectures.add_component(event)
    elif "WORKSHOP" in str(event['description']):
        workshops.add_component(event)
    elif "EXAMPLES" in str(event['description']):
        workshops.add_component(event)
    elif "TEAM STUDY" in str(event['description']):
        workshops.add_component(event)
    elif "LAB" in str(event['description']):
        labs.add_component(event)
    elif str(event['summary']) == 'COMP-PASS':
        print 'Removed 1st year pass'
    else:
        other.add_component(event)

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
