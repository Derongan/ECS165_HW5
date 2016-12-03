from parser import parse_quarter
import psycopg2 as psy
from psycopg2.extensions import AsIs
import os


def insert_students(conn, stdict):
    with conn.cursor() as cursor:
        students = list(stdict.values())

        if not students:
            return

        keys = tuple(students[0].keys())

        # Syntax for AsIs found by consulting:
        # http://stackoverflow.com/questions/29461933/insert-python-dictionary-using-psycopg2
        values = b','.join([cursor.mogrify('%s', (tuple(student.values()),)) for student in students])

        statement = cursor.mogrify("INSERT INTO FakeU.student (%s) VALUES ", (AsIs(",".join(keys)),))

        cursor.execute(statement+values + b"ON CONFLICT DO NOTHING")



def insert_students_quarter(conn, stdict):
    with conn.cursor() as cursor:
        students = list(stdict.values())

        if not students:
            return

        keys = tuple(students[0].keys())

        # Syntax for AsIs found by consulting:
        # http://stackoverflow.com/questions/29461933/insert-python-dictionary-using-psycopg2
        values = b','.join([cursor.mogrify('%s', (tuple(student.values()),)) for student in students])

        statement = cursor.mogrify("INSERT INTO FakeU.StudentQuarterData (%s) VALUES ", (AsIs(",".join(keys)),))

        cursor.execute(statement+values)


if __name__ == "__main__":
    with psy.connect(database="FakeU", user="fakeuser", password="") as conn:
        for filename in os.listdir('data/Grades/'):
            result = parse_quarter(filename)

            insert_students(conn, result['student'])

            insert_students_quarter(conn, result['studentquarterdata'])
