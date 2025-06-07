-------------------------
-- Project 1 Solution Template
-- COMP9311 24T3
-- Name: abc
-- zID: zxxxxxxx
-------------------------


-- Q1
DROP VIEW IF EXISTS Q1 CASCADE;
CREATE or REPLACE VIEW Q1(count) AS
-- SQL query

SELECT COUNT(DISTINCT ce.student)
FROM course_enrolments ce
JOIN courses c ON ce.course = c.id
JOIN subjects s ON c.subject = s.id
WHERE ce.mark > 85
  AND s.code LIKE 'COMP%';



-- Q2
DROP VIEW IF EXISTS Q2 CASCADE;
CREATE or REPLACE VIEW Q2(count) AS
-- SQL query

SELECT COUNT(*)
FROM (
  SELECT ce.student
  FROM course_enrolments ce
  JOIN courses c ON ce.course = c.id
  JOIN subjects s ON c.subject = s.id
  WHERE s.code LIKE 'COMP%'
    AND ce.mark IS NOT NULL
  GROUP BY ce.student
  HAVING AVG(ce.mark) > 85
) AS students_with_avg_mark_above_85;





-- Q3
DROP VIEW IF EXISTS Q3 CASCADE;
CREATE or REPLACE VIEW Q3(unswid,name) AS
-- SQL query

SELECT p.unswid, p.name
FROM people p 
JOIN students st ON p.id = st.id
JOIN course_enrolments ce ON st.id = ce.student
JOIN courses c ON ce.course = c.id
JOIN subjects s ON c.subject = s.id
WHERE s.code LIKE 'COMP%'
  AND ce.mark IS NOT NULL
GROUP BY p.unswid, p.name
HAVING AVG(ce.mark) > 85
  AND COUNT(ce.course) >= 6;



-- Q4
DROP VIEW IF EXISTS Q4 CASCADE;
CREATE or REPLACE VIEW Q4(unswid,name) AS
-- SQL query

SELECT p.unswid, p.name
FROM people p
JOIN students st ON p.id = st.id
JOIN (
    SELECT
        ce.student, 
        s.id, 
        MAX(ce.mark) AS highest_mark, 
        SUM(s.uoc) AS total_uoc 
    FROM course_enrolments ce
    JOIN courses c ON ce.course = c.id
    JOIN subjects s ON c.subject = s.id
    WHERE s.code LIKE 'COMP%'
      AND ce.mark IS NOT NULL
    GROUP BY ce.student, s.id
) AS mm ON st.id = mm.student
GROUP BY p.unswid, p.name
HAVING 
    COUNT(DISTINCT mm.id) >= 6
    AND (SUM(mm.highest_mark * mm.total_uoc) / SUM(mm.total_uoc)) > 85;




-- Q5
DROP VIEW IF EXISTS Q5 CASCADE;
CREATE or REPLACE VIEW Q5(count) AS
-- SQL query


SELECT COUNT(DISTINCT s.id)
FROM subjects s
JOIN orgunits o ON s.offeredby = o.id
JOIN courses c ON s.id = c.subject
JOIN semesters sem ON sem.id = c.semester
WHERE o.longname = 'School of Computer Science and Engineering'
  AND sem.year = 2012;



-- Q6
DROP VIEW IF EXISTS Q6 CASCADE;
CREATE or REPLACE VIEW Q6(count) AS
-- SQL query

SELECT COUNT(DISTINCT s.id)
FROM staff s
JOIN affiliations a ON s.id = a.staff
JOIN orgunits o ON a.orgunit = o.id
JOIN course_staff cs ON s.id = cs.staff
JOIN courses c ON cs.course = c.id
JOIN semesters sem ON sem.id = c.semester
JOIN staff_roles sr ON cs.role = sr.id
WHERE sr.name = 'Course Lecturer'
  AND o.longname = 'School of Computer Science and Engineering'
  AND sem.year = 2012;


-- Q7
DROP VIEW IF EXISTS Q7 CASCADE;
CREATE or REPLACE VIEW Q7(course_id,unswid) AS
-- SQL query

SELECT cs.course, p.unswid
FROM course_staff cs
JOIN staff_roles sr ON cs.role = sr.id
JOIN staff s ON cs.staff = s.id
JOIN people p ON s.id = p.id
JOIN courses c ON cs.course = c.id
JOIN subjects sub ON c.subject = sub.id
JOIN orgunits o ON sub.offeredby = o.id
JOIN semesters sem ON c.semester = sem.id
WHERE o.longname = 'School of Computer Science and Engineering'
  AND sem.year = 2012
  AND sr.name = 'Course Lecturer';


-- Q8
DROP VIEW IF EXISTS Q8 CASCADE;
CREATE or REPLACE VIEW Q8(course_id, unswid) AS
-- SQL query

SELECT cs.course, p.unswid
FROM course_staff cs
JOIN staff_roles sr ON cs.role = sr.id
JOIN staff s ON cs.staff = s.id
JOIN people p ON s.id = p.id
JOIN courses c ON cs.course = c.id
JOIN subjects sub ON c.subject = sub.id
JOIN orgunits o ON sub.offeredby = o.id
JOIN semesters sem ON c.semester = sem.id
WHERE o.longname = 'School of Computer Science and Engineering'
  AND sem.year = 2012
  AND sr.name = 'Course Lecturer'
  AND s.id IN (
    SELECT a.staff
    FROM affiliations a
    JOIN orgunits o2 ON a.orgunit = o2.id
    WHERE o2.longname = 'School of Computer Science and Engineering'
);

-- Q9
DROP FUNCTION IF EXISTS Q9 CASCADE;
CREATE or REPLACE FUNCTION Q9(subject1 integer, subject2 integer) 
returns text as $$
--Function body

DECLARE
  subject1_code varchar;
  subject2_prereq varchar;
BEGIN
  SELECT code INTO subject1_code
  FROM subjects
  WHERE id = subject1;
  
  SELECT _prereq INTO subject2_prereq
  FROM subjects
  WHERE id = subject2;

  IF subject2_prereq LIKE '%' || subject1_code || '%' THEN
    RETURN subject1 || ' is a direct prerequisite of ' || subject2 || '.';
  ELSE
    RETURN subject1 || ' is not a direct prerequisite of ' || subject2 || '.';
  END IF;
END;

$$ language plpgsql;





-- Q10
DROP FUNCTION IF EXISTS Q10 CASCADE;
CREATE or REPLACE FUNCTION Q10(subject1 integer, subject2 integer) returns text
as $$
--Function body

DECLARE
    subject1_code VARCHAR;
    subject2_prereqs TEXT;
    prereqs_found TEXT[];
    prereq_code TEXT;
    prereq_id INTEGER;
BEGIN
    SELECT code INTO subject1_code
    FROM subjects
    WHERE id = subject1;

    SELECT _prereq INTO subject2_prereqs
    FROM subjects
    WHERE id = subject2;

    -- Check if subject2 has prerequisites
    IF subject2_prereqs IS NULL THEN
        RETURN subject1 || ' is not a prerequisite of ' || subject2 || '.';
    END IF;

    -- Find all subject codes in the prerequisites using regex 
    SELECT array_agg(match) INTO prereqs_found
    FROM (
        SELECT unnest(regexp_matches(subject2_prereqs, '[A-Z]{4}[0-9]{4}', 'g')) AS match
    ) AS matches;

    -- Check if prereqs_found is null
    IF prereqs_found IS NULL OR array_length(prereqs_found, 1) IS NULL THEN
        RETURN subject1 || ' is not a prerequisite of ' || subject2 || '.';
    END IF;

    IF subject1_code = ANY(prereqs_found) THEN
        RETURN subject1 || ' is a prerequisite of ' || subject2 || '.';
    END IF;


    FOREACH prereq_code IN ARRAY prereqs_found LOOP
        SELECT id INTO prereq_id FROM subjects WHERE code = prereq_code;

        IF prereq_id IS NOT NULL THEN
            -- Recursive check for deeper prerequisites
            IF Q10(subject1, prereq_id) = subject1 || ' is a prerequisite of ' || prereq_id || '.' THEN
                RETURN subject1 || ' is a prerequisite of ' || subject2 || '.';
            END IF;
        END IF;
    END LOOP;

    RETURN subject1 || ' is not a prerequisite of ' || subject2 || '.';
END;
$$ LANGUAGE plpgsql;

