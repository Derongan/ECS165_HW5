import psycopg2 as psy
from itertools import groupby

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


def answer_3c(conn):
    with open("queries/3c.sql") as fp:
        query = fp.read()

    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    prof_dict = {}

    for item in result:
        prof = item[0]
        grade = item[1]
        units = item[2]

        if grade in GRADE_MAP:
            if prof in prof_dict:
                prof_dict[prof]['gp'] += float(units) * GRADE_MAP[grade]
                prof_dict[prof]['units'] += float(units)
            else:
                prof_dict[prof] = {'gp': float(units) * GRADE_MAP[grade], 'units': float(units)}

    for prof in prof_dict:
        prof_dict[prof] = prof_dict[prof]['gp'] / prof_dict[prof]['units']

    pkey = list(prof_dict.keys())
    pvalue = list(prof_dict.values())

    mx = max(pvalue)
    mn = min(pvalue)

    max_idx = [x for x, j in enumerate(pvalue) if j == mx]
    min_idx = [x for x, j in enumerate(pvalue) if j == mn]

    if PRINT_VALUES:
        print("The easiest professor(s) are {} with a GPA of {}".format(
            " and, ".join(["'{}'".format(pkey[i]) for i in max_idx]), mx))
        print("The hardest professor(s) are {} with a GPA of {}".format(
            " and, ".join(["'{}'".format(pkey[i]) for i in min_idx]), mn))


def answer_3d(conn):
    with open("queries/3d.sql") as fp:
        query = fp.read()

    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    result.sort(key=lambda a: a[2])
    groups = (groupby(result, key=lambda a: a[2]))

    for crse, group in groups:
        group = list(group)
        group.sort(key=lambda a: a[0])
        profs = groupby(group, lambda a: a[0])

        pnp = False

        if all([x[1] not in GRADE_MAP.keys() for x in group]):
            pnp = True

        prof_dict = {}

        if pnp:
            for prof, grades in profs:
                grades = list(grades)
                prof_dict[prof] = sum([1 if x[1] == 'P' else 0 for x in grades]) / len(grades)
        else:
            for prof, grades in profs:
                grades = list(grades)
                prof_dict[prof] = sum([GRADE_MAP[x[1]] for x in grades if x[1] in GRADE_MAP]) / len(
                    [GRADE_MAP[x[1]] for x in grades if x[1] in GRADE_MAP])

        pkey = list(prof_dict.keys())
        pvalue = list(prof_dict.values())

        mx = max(pvalue)
        mn = min(pvalue)

        max_idx = [x for x, j in enumerate(pvalue) if j == mx]
        min_idx = [x for x, j in enumerate(pvalue) if j == mn]

        type = "pass rate" if pnp else "GPA"

        if PRINT_VALUES:
            print("The easiest professor(s) for {} are {} with a {} of {}".format(crse,
                " and, ".join(["'{}'".format(pkey[i]) for i in max_idx]), type, mx))
            print("The hardest professor(s) are {} for {} with a {} of {}".format(crse,
                " and, ".join(["'{}'".format(pkey[i]) for i in min_idx]), type, mn))



if __name__ == "__main__":
    with psy.connect(database="FakeU", user="fakeuser", password="") as conn:
        answer_3a(conn)
        # answer_3b(conn)
        answer_3c(conn)
        answer_3d(conn)
