import os
import sys
import urllib2
import difflib
from datetime import datetime
from icalendar import Calendar
from os.path import exists

# calendar url
path = os.path.dirname(os.path.abspath(__file__))

# user variables
url = ''
split_calendar = True

# filenames
previous_file = "Previous-Timetable.ics"
timetable_file = "Timetable.ics"
lectures_file = 'Lectures.ics'
workshops_file = 'Workshops.ics'
labs_file = 'Labs.ics'
other_file = 'Other.ics'

# replacements
replacements = {
    'COMP-1st Yr Tutorial': 'Tutorial',
    'COMP-2nd Yr Tutorial (SH)': 'Tutorial',
    'COMP-PASS': 'Pass',
    'COMP-PASS2': 'Pass',
    'COMP10120': 'Group Project',
    'COMP11120': 'Maths',
    'COMP11212': 'Computation',
    'COMP12111': 'Engineering',
    'COMP14112': 'AI',
    'COMP15111': 'Architecture',
    'COMP16212': 'Java',
    'COMP18112': 'Distributed Systems',
    'COMP23111': 'Databases',
    'COMP23420': 'Software Engineering',
    'COMP25111': 'Operating Systems',
    'COMP26120': 'Algorithms',
    'COMP21111': 'Logic and Modelling',
    'COMP22111': 'Processor Microarchitecture',
    'COMP24111': 'Machine Learning',
    'COMP28411': 'Networks',
    'COMP22712': 'Microcontrollers',
    'COMP24412': 'Symbolic AI',
    'COMP27112': 'Computer Graphics',
    'COMP28112': 'Distributed Computing',
    'COMP28512': 'Mobile Systems',
    'COMP30040': 'Third Year Project',
    'COMP32211': 'System-on-Chip',
    'COMP33511': 'User Experience',
    'COMP33711': 'Software Engineering',
    'COMP36111': 'Advanced Algorithms 1',
    'COMP37111': 'Advanced Computer Graphics',
    'COMP38411': 'Cryptography',
    'COMP34412': 'Natural Language Systems',
    'COMP35112': 'Chip Multiprocessors',
    'COMP36212': 'Advanced Algorithms 2',
    'COMP36512': 'Compilers',
    'COMP37212': 'Computer Vision',
    'COMP32412': 'Internet of Things',
    'COMP34120': 'AI and Games',
    'COMP38120': 'Documents, Service and Data'
}

global lectures
global workshops
global labs
global other
global timetable


def pretty_print(event):
    print("\t" + event.get('summary') + " on " + str(event.get('dtstart').dt))


def has_updated(event_a, event_b):
    if (event_a.get('summary') == event_b.get('summary')) \
            & (event_a.get('location') == event_b.get('location')) \
            & (event_a.get('dtstart').dt == event_b.get('dtstart').dt) \
            & (event_a.get('dtend').dt == event_b.get('dtend').dt) \
            & (event_a.get('rrate') == event_b.get('rrate')) \
            & (event_a.get('description') == event_b.get('description')):
        return False
    else:
        return True


def diff_calendar():
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)

    # process data
    live_data = response.read()
    live_timetable = Calendar.from_ical(live_data)
    live_events = live_timetable.walk('vevent')

    changes_found = False

    # check if previous file exists
    if exists(previous_file):

        previous_data = open(previous_file, "r").read()
        previous_timetable = Calendar.from_ical(previous_data)
        previous_events = previous_timetable.walk('vevent')

        live_uid = set(map(lambda x: x["uid"], live_events))
        previous_uid = set(map(lambda x: x["uid"], previous_events))
        deleted_uid = previous_uid.difference(live_uid)
        added_uid = live_uid.difference(previous_uid)

        if len(deleted_uid) > 0:
            changes_found = True
            print("Deleted Events:")
            for uid in deleted_uid:
                event = filter(lambda x: x["uid"] == uid, previous_events)
                pretty_print(event[0])

        if len(added_uid) > 0:
            changes_found = True
            print("\nAdded Events:")
            for uid in added_uid:
                event = filter(lambda x: x["uid"] == uid, live_events)[0]
                pretty_print(event)

        updated_events = []

        for event in live_events:
            event_uid = event.get('uid')
            matched_events = filter(lambda e: e.get('uid') == event_uid, previous_events)
            if len(matched_events) == 1:
                if has_updated(event, matched_events[0]):
                    updated_events.append(event)

        if len(updated_events) > 0:
            changes_found = True
            print("\nUpdated Events:")
            for event in updated_events:
                pretty_print(event)

        if changes_found:
            print("\nWARNING: Changes found - Re-import files to calendar to update")
        else:
            print("No changes found")

    else:
        print("Creating " + previous_file + " - Run again to check for updates")

    # Then log changes and update files

    f = open(previous_file, 'w+b')
    f.write(live_data)
    f.close()


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
    global timetable

    print(event['summary'])

    if split_calendar:
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
            print('Removed 1st year pass')
        else:
            other.add_component(event)
    else:
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


def process_timetable():
    global lectures
    global workshops
    global labs
    global other
    global timetable

    # create calendars
    if split_calendar:
        lectures = create_calendar()
        workshops = create_calendar()
        labs = create_calendar()
        other = create_calendar()
    else:
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
    if split_calendar:
        write_calendar(lectures_file, lectures)
        write_calendar(workshops_file, workshops)
        write_calendar(labs_file, labs)
        write_calendar(other_file, other)
    else:
        write_calendar(timetable_file, timetable)


def main():

    if url == '':
        print("\n> url parameter required in 'load_timetable.py'")
        return

    print("\n> Checking for changes to timetable...\n")
    diff_calendar()

    print("\n> Processing and exporting timetable...\n")
    process_timetable()

    print("\n> Done!")


if __name__ == '__main__':
    main()
