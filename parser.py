import csv
import os


def parse_quarter(filename):
    courses = []

    last_course = {}

    student = {}
    student_quarter_data = {}

    with open("data/Grades/{}".format(filename)) as fp:
        reader = csv.reader(fp, skipinitialspace=True)
        next(reader)  # Skip initial blank

        reading_course = False
        reading_instructor = False
        reading_student = False

        for row in reader:
            first = row[0]

            if len(row) <= 1:
                reading_course = False
                reading_instructor = False
                reading_student = False
            elif reading_course:
                last_course['data'] = row
                reading_course = False
            elif reading_instructor:
                last_course['meetings'].append(row)
            elif reading_student:
                # Commented out test that made sure emails always match on IDs. They do. Yay.
                # assert(students.get(row[1], None) is None or students[row[1]]['email'] == row[10])
                student[row[1]] = {'id': row[1], 'email': row[10]}
                student_quarter_data[(row[1], last_course['data'][1])] = {
                    'id': row[1],
                    'term': last_course['data'][1],
                    'level': row[4],
                    'class': row[6],
                    'major': row[7],
                    'prefname': row[3],
                    'surname': row[2]
                }
                last_course['students'].append(row)
            elif first == 'CID':
                reading_course = True
                if last_course:
                    if last_course['students']: #ignores courses which has no students in it
                        courses.append(last_course)
                last_course = {'students': [], 'meetings': []}
            elif first == 'INSTRUCTOR(S)':
                reading_instructor = True
            elif first == 'SEAT':
                reading_student = True

        courses.append(last_course)
        return {'student': student}


if __name__ == "__main__":
    for filename in os.listdir('data/Grades/'):
        result = parse_quarter(filename)
    pass
