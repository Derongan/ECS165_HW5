import csv
import os
from psycopg2.extras import NumericRange


def parse_quarter(filename):
    all_courses = []

    last_prof = None

    last_course = {}
    temp_meet = []

    courses = {}

    # Meeting is autoincrement primary key due to the bulk of missing data
    meeting = []
    student = {}
    student_quarter_data = {}
    student_course = {}

    with open("data/Grades/{}".format(filename)) as fp:
        reader = csv.reader(fp, skipinitialspace=True)
        next(reader)  # Skip initial blank

        reading_course = False
        reading_instructor = False
        reading_student = False

        for row in reader:

            row = [x if x != "" else None for x in row]

            first = row[0]

            if first == "49148":
                print("WTF")

            if len(row) <= 1:
                reading_course = False
                reading_instructor = False
                reading_student = False

            elif first == 'INSTRUCTOR(S)':
                reading_instructor = True
            elif first == 'SEAT':
                reading_student = True
            elif reading_course:
                last_course['data'] = row
                reading_course = False
            elif first == 'CID':
                reading_course = True
                if last_course and last_course['students']:
                    data = last_course["data"]

                    unit_vals = tuple(float(x) for x in data[-1].split("-"))

                    courses[(data[1], data[0], data[4])] = {
                        'term': data[1],
                        'cid': data[0],
                        'section': data[4],
                        'subject': data[2],
                        'crse': data[3],
                        'units': NumericRange(min(unit_vals), max(unit_vals), '[]')  # needs formatting as range
                    }
                    if temp_meet:
                        meeting.extend(temp_meet)

                    all_courses.append(last_course)

                last_course = {'students': [], 'meetings': []}
                temp_meet = []
                last_prof = None
            elif reading_instructor:
                data = last_course["data"]
                # can change building and room to instructor
                # no instructor can be at two places at the same day and time
                # but check for overlapping days

                if not row[3]:
                    times = [None, None]
                else:
                    times = row[3].split('-')

                if first:
                    last_prof = first

                temp_meet.append({
                    'term': data[1],
                    'starttime': times[0],
                    'endtime': times[1],
                    'days': row[2],
                    'building': row[4],
                    'room': row[5],
                    'instructor': last_prof,
                    'type': row[1],
                    'cid': data[0],
                    'section': data[4]
                })
                last_course['meetings'].append(row)
            elif reading_student:
                # Commented out test that made sure emails always match on IDs. They do. Yay.
                # assert(students.get(row[1], None) is None or students[row[1]]['email'] == row[10])

                data = last_course["data"]
                student[row[1]] = {'id': row[1], 'email': row[10]}

                # if (row[1], data[1]) in student_quarter_data:

                student_quarter_data[(row[1], data[1])] = {
                    'id': row[1],
                    'term': data[1],
                    'level': row[4],
                    'class': row[6],
                    'major': row[7],
                    'prefname': row[3],
                    'surname': row[2]
                }

                student_course[(row[1], data[0], data[1], data[4])] = {
                    'id': row[1],
                    'term': data[1],
                    'cid': data[0],
                    'section': data[4],
                    'units': row[5],
                    'seat': row[0],
                    'status': row[9],
                    'grade': row[8]
                }
                last_course['students'].append(row)


        # Add the last one on if we need to
        if last_course and last_course['students']:
            data = last_course["data"]

            unit_vals = tuple(float(x) for x in data[-1].split("-"))

            courses[(data[1], data[0], data[4])] = {
                'term': data[1],
                'cid': data[0],
                'section': data[4],
                'subject': data[2],
                'crse': data[3],
                'units': NumericRange(min(unit_vals), max(unit_vals), '[]')  # needs formatting as range
            }
            if temp_meet:
                meeting.extend(temp_meet)

            all_courses.append(last_course)

        return {
            'student': student,
            'studentquarterdata': student_quarter_data,
            'studentcourse': student_course,
            'course': courses,
            'meeting': meeting
        }


if __name__ == "__main__":
    for filename in os.listdir('data/Grades/'):
        result = parse_quarter(filename)
    pass
