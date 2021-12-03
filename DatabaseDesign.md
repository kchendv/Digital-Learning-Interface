## Summary

The Database for this project is implemented in `kevinc17_database`.

We created all 7 tables in our design, with the corresponding number of sample rows for each: `Student` (1000), `Teacher` (1000), `Submission` (30000), `Rating` (60000), `Question` (3000), `Class` (1000), Enrollment (10000).

### Note

- The quantity of data inserted for each table is  adjusted such that for every one-to-many relationship, one parent maps to more than one children on average (e.g. On average, each `Class` will have 10 corresponding `Enrollement`s)

- For `Class`, real data from the UIUC courses catalog is used. Other sample data is randomly generated.

- For `Question`, the `feedback` attribute is intentionally left blank, since feedback is meant to be added later by the end user

## DDL Commands Used
```
CREATE TABLE Teacher(teacher_email VARCHAR(255) PRIMARY KEY, teacher_name, VARCHAR(255), password VARCHAR(255));

CREATE TABLE Student(student_email VARCHAR(255) PRIMARY KEY, student_name VARCHAR (255), password VARCHAR(255));

CREATE TABLE Class(class_id INT PRIMARY KEY, teacher_email VARCHAR(255), class_name VARCHAR(255), FOREIGN KEY (teacher_email) REFERENCES Teacher(teacher_email));

CREATE TABLE Question(question_id INT PRIMARY KEY, class_id INT, title VARCHAR(255), description VARCHAR(255), score INT, feedback VARCHAR(255), FOREIGN KEY (class_id) REFERENCES Class(class_id));

CREATE TABLE Submission(submission_id INT PRIMARY KEY, submitter VARCHAR(255), question INT, content VARCHAR(255), FOREIGN KEY(submitter) REFERENCES Student(student_email), FOREIGN KEY(question) REFERENCES Question(question_id));

CREATE TABLE Rating(rating_id INT PRIMARY KEY, submission INT, rater VARCHAR(255), points INT, FOREIGN KEY(submission) REFERENCES Submission(submission_id), FOREIGN KEY(rater) REFERENCES Student(student_email));

CREATE TABLE Enrollment(enrollment_id INT PRIMARY KEY, class_id INT , student_email VARCHAR(255) , final_grade VARCHAR(255), FOREIGN KEY(class_id) REFERENCES Class(class_id), FOREIGN KEY(student_email) REFERENCES Student(student_email));
```

## SQL Queries

**Find the number of classes taught by each teacher**
```
SELECT Teacher.teacher_email, teacher_name, COUNT(class_id)
FROM Teacher LEFT JOIN Class ON Teacher.teacher_email = Class.teacher_email 
GROUP BY Teacher.teacher_email, teacher_name 
ORDER BY Teacher.teacher_email ASC
LIMIT 15;
```

![Query1](https://github.com/uiuc-fa21-cs411/24/blob/main/image/Query1.JPG)


**Find the average rating of all submissions submitted by each student**
```
SELECT Student.student_email, Student.student_name, AVG(points)
FROM Student LEFT JOIN Submission ON Student.student_email = Submission.submitter
LEFT JOIN Rating ON Submission.submission_id = Rating.submission
GROUP BY Student.student_email, Student.student_name
ORDER BY Student.student_email ASC
LIMIT 15;
```

![Query2](https://github.com/uiuc-fa21-cs411/24/blob/main/image/Query2.JPG)

## Indexing

### Before Indexing

`EXPLAIN ANALYZE` Query 1:
```
| -> Limit: 15 row(s)  (actual time=6.033..6.157 rows=15 loops=1)
    -> Sort: Teacher.teacher_email, Teacher.teacher_name, limit input to 15 row(s) per chunk  (actual time=8.531..8.532 rows=15 loops=1)
        -> Table scan on <temporary>  (actual time=0.001..0.060 rows=1000 loops=1)
            -> Aggregate using temporary table  (actual time=8.177..8.297 rows=1000 loops=1)
                -> Nested loop left join  (cost=451.75 rows=1000) (actual time=0.092..3.972 rows=1352 loops=1)
                    -> Table scan on Teacher  (cost=101.75 rows=1000) (actual time=0.068..0.429 rows=1000 loops=1)
                    -> Index lookup on Class using teacher_email (teacher_email=Teacher.teacher_email)  (cost=0.25 rows=1) (actual time=0.003..0.003 rows=1 loops=1000)
 |

```

`EXPLAIN ANALYZE` Query 2:
```
| -> Limit: 15 row(s)  (actual time=268.101..268.103 rows=15 loops=1)
    -> Sort: Student.student_email, Student.student_name, limit input to 15 row(s) per chunk  (actual time=298.304..298.304 rows=15 loops=1)
        -> Table scan on <temporary>  (actual time=0.002..0.292 rows=1000 loops=1)
            -> Aggregate using temporary table  (actual time=297.688..298.029 rows=1000 loops=1)
                -> Nested loop left join  (cost=801.50 rows=1000) (actual time=0.095..203.534 rows=64355 loops=1)
                    -> Nested loop left join  (cost=451.50 rows=1000) (actual time=0.074..27.141 rows=30000 loops=1)
                        -> Table scan on Student  (cost=101.50 rows=1000) (actual time=0.048..0.522 rows=1000 loops=1)
                        -> Index lookup on Submission using submitter (submitter=Student.student_email)  (cost=0.25 rows=1) (actual time=0.008..0.025 rows=30 loops=1000)
                    -> Index lookup on Rating using submission (submission=Submission.submission_id)  (cost=0.25 rows=1) (actual time=0.005..0.006 rows=2 loops=30000)
 |
```

### After Indexing
Query 1 (Actual Time Taken):

- Without indexing: 6.033..6.157
- Index `Teacher(teacher_email)`: 6.083..6.086
- Index `Teacher(teacher_name)`: 6.466..6.468
- Index `Teacher(teacher_email, teacher_name)`: 0.069..0.145

We chose the index design with teacher_email and teacher_name. The index design resulted in a speed increase of 210x. We also chose it since our Teacher advanced query selected teacher_email and teacher_name, and because indexing speeds up SELECT queries.. Furthermore, since a new teacher will not be input as often, the index slowing down data input can be considered negligible when compared to its query speed benefits.


Query 2 (Actual Time Taken):
- Without indexing: 268.101..268.103
- Index `Student(student_email)`: 298.158..298.160
- Index `Student(student_name)`: 311.028..311.030
- Index `Student(student_email, student_name)`: 1.707..5.151
- Index `Student(student_name, student_email)`: 278.400..278.402

We chose the index design with student_email, student_name.The index design resulted in a speed increase of 300x. We also chose it since our Student advanced query selected student_email, student_name. Since indexing speeds up SELECT queries, and since new students will not be input as often, the index slowing down data input can be considered negligible when compared to its query speed benefits.
