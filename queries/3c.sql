SELECT instructor, grade, SUM(units)
FROM FakeU.meeting
JOIN FakeU.studentcourse USING(term, cid, section)
WHERE instructor IS NOT NULL
GROUP BY instructor, grade;