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



def answer_3a(conn):
    with open("queries/3a.sql") as fp:
        query = fp.read()

        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            if PRINT_VALUES:
                print("Question 3a")
                print("Units\t|\tPercent Taking")
                for item in results:
                    print("{}\t\t|\t{}".format(item[0], item[1] * 100))


def answer_3b(conn):
    with open("queries/3b.sql") as fp:
        query = fp.read()

    if PRINT_VALUES:
        print("Question 3b")

    for i in range(1, 21):
        with conn.cursor() as cursor:
            cursor.execute(query.format(i))
            result = cursor.fetchall()

        quarter_dict = {}

        for item in result:
            grade = item[0]
            quarter = item[1]
            units = item[2]
            if item[1] not in quarter_dict:
                if grade in GRADE_MAP:
                    if quarter in quarter_dict:
                        quarter_dict[quarter]['gp'] += float(units) * GRADE_MAP[grade]
                        quarter_dict[quarter]['units'] += float(units)

                    else:
                        quarter_dict[quarter] = {'gp': float(units) * GRADE_MAP[grade], 'units': float(units)}

        averages = [x['gp'] / x['units'] for x in quarter_dict.values() if x['units'] > 0.0]

        average = sum(averages) / len(averages)

        if PRINT_VALUES:
            print("On average students taking {} units have a {} quarter GPA".format(i, average))


if __name__ == "__main__":
    with psy.connect(database="FakeU", user="fakeuser", password="") as conn:
        answer_3a(conn)
        answer_3b(conn)
