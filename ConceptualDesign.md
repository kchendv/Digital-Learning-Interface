# Conceptual Design

## Description
In our project database, we want to keep track of several key entities: Student, Teacher, Class Question, Submission and Rating and Enrollment. Student and Teacher are user entities that can be logged in. A Class has a corresponding Teacher and collection of Questions. Each Question can have multiple Submissions by different Students, and each Submission can have multiple Ratings by different Students. Each Enrollment describes the Enrollment of one Student to one Class. Teachers can create Questions, rate Submissions and give a final grade to each Student in their Class. Students can create Submissions to Questions and Ratings to Submissions. 


## Assumption

### Entity Attributes
- Each Teacher has a primary key email, a name and a password
- Each Student has a primary key email, a name and a password
- Each Class has a primary key id, a foreign key for the Teach teaching that class, and a name
- Each Question has a primary key id, a foreign key for the Class it belongs to, a title, a description, the maximum possible score and the teacher's feedback
- Each Submission has a primary key id, a foriegn key for the student submitter, a foreign key for the question it corresponds to, and the content
- Each Rating has a primary key id, a foreign key for the student rater, a foreign key for the submission it corresponds to, and the points given
- Each Enrollments has a primary key id, a foreign key for the class it corresponds to, a foreign key for the student it corresponds to, and a final grade


### Relationships
- Each Teacher must teach one Class
- Each Class is taught by one Teacher
- Each Question belongs to one Class
- Each Submission is submitted by one Student (submitter)
- Each Submission corresponds to one Question
- Each Rating is submitted by one Student (rater)
- Each Rating corresponds to one Submission
- Each Enrollment corresponds to one Student
- Each Enrollment corresponds to one Class

## Conceptual Database Diagram (ER/UML Diagram)
![ER_UML](https://github.com/uiuc-fa21-cs411/24/blob/main/image/ER_UML.png)


## Logical Design
    Teacher(teacher_email:VARCHAR(255) [PK], teacher_name:VARCHAR(255), password:VARCHAR(255))

    Student(student_email:VARCHAR(255) [PK], student_name:VARCHAR (255), password:VARCHAR(255))

    Submission(submission_id:INT [PK], submitter:VARCHAR(255) [FK to Student.student_email], question:INT [FK to Question.question_id], content:VARCHAR(255))

    Rating(rating_id:INT [PK], submission:INT [FK to Submission.submission_id], rater:VARCHAR(255) [FK to Student.student_email], points:INT)

    Question(question_id:INT [PK], class_id:INT [FK to Class.class_id], title:VARCHAR(255), description:VARCHAR(255), score:INT, feedback:VARCHAR(255))

    Class(class_id:INT [PK], teacher_email:VARCHAR(255) [FK to Teacher.teacher_email], class_name:VARCHAR(255))

    Enrollment(enrollment_id:INT [PK], class_id:INT [FK to Class.class_id], student_email:VARCHAR(255) [FK to Student.student_email], final_grade:VARCHAR(255))


