WITH countunitfreq AS (
	SELECT numunit, COUNT(*) FROM (
		SELECT id,term,SUM(units) as numunit
		FROM FakeU.studentcourse
		GROUP BY id,term)
		AS unitbyquarter
	GROUP BY numunit ORDER BY numunit
)

SELECT numunit, count/(SELECT SUM(count) FROM countunitfreq) AS percent
FROM countunitfreq
WHERE numunit <= 20 AND numunit >= 1 AND numunit % 1 = 0