SELECT instructor, grade, crse, SUM(studentcourse.units)
FROM FakeU.meeting
JOIN FakeU.studentcourse USING(term, cid, section)
JOIN FakeU.course USING(term, cid, section)
WHERE instructor IS NOT NULL AND subject = 'ABC' AND crse >= 100 AND crse < 200
GROUP BY instructor, grade, crse;