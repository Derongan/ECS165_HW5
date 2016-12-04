from parser import parse_quarter
import psycopg2 as psy
from psycopg2.extensions import AsIs
import os


def insert_data(conn, table, stdict, suffix = b''):
    with conn.cursor() as cursor:

        if type(stdict) is dict:
            items = list(stdict.values())
        else:
            items = stdict

        if not items:
            return

        keys = tuple(items[0].keys())

        # Syntax for AsIs found by consulting:
        # http://stackoverflow.com/questions/29461933/insert-python-dictionary-using-psycopg2
        values = b','.join([cursor.mogrify('%s', (tuple(item.values()),)) for item in items])

        statement = cursor.mogrify("INSERT INTO FakeU."+table+" (%s) VALUES ", (AsIs(",".join(keys)),))

        cursor.execute(statement + values + suffix)


if __name__ == "__main__":
    with psy.connect(database="FakeU", user="fakeuser", password="") as conn:
        for filename in os.listdir('data/Grades/'):

            print("Starting file {}".format(filename))

            result = parse_quarter(filename)

            insert_data(conn, 'student', result['student'], b"ON CONFLICT DO NOTHING")
            insert_data(conn, 'StudentQuarterData', result['studentquarterdata'], b"ON CONFLICT DO NOTHING")
            insert_data(conn, 'course', result['course'], b"ON CONFLICT DO NOTHING")
            insert_data(conn, 'meeting', result['meeting'], b"ON CONFLICT DO NOTHING")
            insert_data(conn, 'studentcourse', result['studentcourse'])

            print("Finished file {}".format(filename))
            break
