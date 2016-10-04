import os
import sys
import urllib2
from icalendar import Calendar

path = os.path.dirname(os.path.abspath(__file__))
url = ''
filename = 'Timetable.ics'

replacements = {
'COMP-1st Yr Tutorial': 'Tutorial',
'COMP-PASS': 'Pass',
'COMP-PASS2': 'Pass',
'COMP10120': 'First Year Project',
'COMP11120': 'Mathematical Techniques',
'COMP11212': 'Computation',
'COMP12111': 'Computer Engineering',
'COMP14112': 'Artificial Intelligence',
'COMP15111': 'Computer Architecture',
'COMP16121': 'Object-Oriented Programming with Java',
'COMP16212': 'Object-Oriented Programming with Java',
'COMP18112': 'Distributed Systems',
'COMP24111':'Machine Learning and Optimisation',
'COMP23420':'Software Engineering',
'COMP23111':'Fundamentals of Databases',
'COMP25111':'Operating Systems',
'COMP26120':'Algorithms and Imperitive Programming',
'COMP28411':'Computer Networks'
}

def main():
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    timetable = Calendar()
    timetable.add('prodid', '-//My calendar product//mxm.dk//')
    timetable.add('version', '2.0')

    data = response.read()
    cal = Calendar.from_ical(data)
    for event in cal.walk('vevent'):
        event['summary'] = calculate_name(event)
        timetable.add_component(event)

    f = open(filename, 'w+b')
    f.write(timetable.to_ical())
    f.close()

    open_file(path + '/' + filename)

def calculate_name(event):
    summary = event.get('summary')
    name = str(summary)
    for src, target in replacements.iteritems():
         name = name.replace(src, target)
    return name

def open_file(path):
    os.system('open ' + path)

if __name__ == '__main__':
    main()
