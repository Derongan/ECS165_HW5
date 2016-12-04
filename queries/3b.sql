WITH unitgrade AS (SELECT units, grade, term FROM
(SELECT numunit, id, term FROM (
	SELECT id,term,SUM(units) as numunit
	FROM FakeU.studentcourse
	GROUP BY id,term)
	AS unitbyquarter
WHERE numunit=2)
AS idquarters
JOIN FakeU.studentcourse USING(id, term))

SELECT grade, term, SUM(units) FROM unitgrade
GROUP BY grade, term;
