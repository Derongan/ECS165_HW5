import csv


def parse_quarter(filename):
    courses = []

    last_course = {}

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
                last_course['students'].append(row)
            elif first == 'CID':
                reading_course = True
                if last_course:
                    courses.append(last_course)
                last_course = {'students': [], 'meetings': []}
            elif first == 'INSTRUCTOR(S)':
                reading_instructor = True
            elif first == 'SEAT':
                reading_student = True

        courses.append(last_course)
        return courses


if __name__ == "__main__":
    x = parse_quarter("2011_Q4.csv")
    pass
