import psycopg2 as psy


# Notes
# I use the with connection.cursor() as cursor patern
# This is useful and I would reccomend using. It automatically
# Closes the cursor after you exit the statment.
# The same thing happens with the connection inside the __main__
# DB chredentials are asumed to be:
# database="FakeU", user="fakeuser", password=""
# All tables are in the FakeU schema so we can easily manipulate all at once

def destroy_create_schema(conn):
    with conn.cursor() as cursor:
        cursor.execute("DROP SCHEMA IF EXISTS FakeU CASCADE")
        cursor.execute("CREATE SCHEMA FakeU")


def create_student_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS FakeU.student ("
                       "id integer PRIMARY KEY,"
                       "email varchar(254)"
                       ");"
                       )


def create_student_quarter_data_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS FakeU.StudentQuarterData ("
                       "level char(2),"
                       "class char(2),"
                       "major char(4),"
                       "prefname varchar(30),"
                       "surname varchar(30),"
                       "id integer references FakeU.student,"
                       "term integer,"
                       "PRIMARY KEY(id, term)"
                       ");")


def create_course_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS FakeU.course ("
                       "term integer,"
                       "cid integer,"
                       "section integer,"
                       "subject char(3),"
                       "crse integer,"
                       "units numrange,"
                       "PRIMARY KEY(term, cid, section)"
                       ");")


def create_meeting_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS FakeU.meeting ("
                       "mid serial,"
                       "days varchar(7),"
                       "starttime time,"
                       "endtime time,"
                       "type varchar(30),"
                       "building char(3),"
                       "room integer,"
                       "instructor varchar(30),"
                       "term integer,"
                       "cid integer,"
                       "section integer,"
                       "PRIMARY KEY(mid),"
                       "FOREIGN KEY(term, cid, section) references FakeU.course(term, cid ,section)"
                       ");")


def create_student_course_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS FakeU.studentcourse ("
                       "units integer,"
                       "seat integer,"
                       "status char(2),"
                       "grade varchar(3),"
                       "id integer references FakeU.student,"
                       "term integer,"
                       "cid integer,"
                       "section integer,"
                       "PRIMARY KEY(id, term, cid, section),"
                       "FOREIGN KEY(term, cid, section) references FakeU.course(term, cid, section)"
                       ");")


if __name__ == "__main__":
    with psy.connect(database="FakeU", user="fakeuser", password="") as conn:
        destroy_create_schema(conn)
        create_student_table(conn)
        create_course_table(conn)
        create_student_quarter_data_table(conn)
        create_meeting_table(conn)
        create_student_course_table(conn)
