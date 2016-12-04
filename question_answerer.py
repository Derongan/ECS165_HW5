import psycopg2 as psy

PRINT_VALUES = True

GRADE_MAP = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "D-": 0.7,
    "F": 0.0
}


def query_question(conn, name):
    with open("queries/{}.sql".format(name)) as fp:
        query = fp.read()

        if not query:
            return "No sql found"

        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def answer_3a(conn):
    results = query_question(conn, "3a")

    if PRINT_VALUES:
        print("Units\t|\tPercent Taking")
        for item in results:
            print("{}\t\t|\t{}".format(item[0], item[1]*100))



def answer_3b(conn):
    result = query_question(conn, "3b")

    #TODO




if __name__ == "__main__":
    with psy.connect(database="FakeU", user="fakeuser", password="") as conn:
        answer_3a(conn)
        answer_3b(conn)
