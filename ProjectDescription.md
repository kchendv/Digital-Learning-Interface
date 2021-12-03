# Digital Learning Database Organization Interface
Team Members:

Henry Yu (jyhheng2@illinois.edu)

Kevin Chen (kevinc17@illinois.edu)

Julian Kao (juliank3@illinois.edu)

Davy Ji (davyji2@illinois.edu) 


## Project Summary
This interface is dedicated to helping students gather feedback from other students. Students first submit their work to the platform, and their works will be made available to other students for peer review. The grades of their assignments will be based on the rating received from other students that is based on provided rubrics.


## Detailed Description
We want to create a homework submission system focused around students, where questions can not only be created, answered and graded but also rated by peers.  The homework organization interface will feature a login system where users will be able to create their own account and login to the system either as an administrator or as a student. Administrators will be able to create new questions / homework sets and modify details such as the title, description, due date, file attachments and tags such as difficulty. After the question is created, students will be able to make a new submission either in text or document (.jpg, .png or .pdf) format. Students can also provide ratings of other students’ submissions based on administrator-defined factors like accuracy and fluency. 


The project will use a relational database with four tables: Users, Questions, Submissions and Ratings. Submissions will be related to Users (the submitter) and Questions (the question submitted for). Ratings will be related to the User (the rater) and Submissions (the submission being rated). This will allow for an efficient system in which related items, such as all the submissions of a user of a question, can be queried and filtered. 


## Usefulness
### Usefulness Description
Our integrated feedback system uses the power of experienced students, who have already taken the class or have preliminary knowledge on the subject, to give feedback on homework submissions in a quantitative way. By summarizing the numerical rubric developed by us, students who submit the homework would be able to have direct feedback regarding the quality of the assignment. 


### Similar applications and how yours is different?
Similar applications include Gradescope, Canvas, Prairielearn and Moodle. The closest application to our platform is Gradescope, where our main difference is the peer-review functionality and student feedback, a feature that is not used by the other applications. Secondly, one of the pain points for students doing homework online is that those platforms only provide a submission portal for students to complete their assignments, while websites such as Chegg and CourseHero are at a vague position between referencing solution suggestions and actually copying the solution for a student’s homework submission. Our website provides a fair and open platform for students to gather feedback without risking plagiarism or directly copy the results of someone else's work. This is done by having an anonymous and numerical rating system which covers several rubrics that gives an indication for the quality of the work. 


## Realness: How and where you’ll get the data?
User information will be gathered at the stage of creating a new user profile, where new users type in their name, email address, and other personal information required to create new profiles. Only after having an account can they proceed onto the next step - create/schedule homework assignments, submit homework, and provide feedback for other students’ homeworks.


Homework information will be provided by administrators when creating new homework, and then homework data will be collected from students through their submission. Peer rating and feedback is provided as responses from students to others’ work.

### Test Data Description
Due to the large quantity of data needed to keep relations at a reasonable ratio (e.g. each Class should have multiple Questions, which should each have multiple Submissions), the sourcing of real text data is infeasible. **The Class table will contain data from the UIUC courses catalog**, while the rest of the data will be automatically generated, including Teacher and Student names, emails, Question titles, Submission content etc. We will use a script that automatically generates foreign keys that correspond to the constraints of our project. Namely:
-  Each Submission to a Question must be submitted by a Student that belongs in the same Class
- Each Rating of a Submission must be submitted by a Student that belongs in the same Class (and not the original author of the Submission) 

## Description of the functionalities
### Describe what data is stored in the database.
The login system manipulates data input provided by the user, including user name (varchar), email address (varchar), role (integer), and password (varchar). The Question table data include title (varchar), subject (varchar), course name (varchar), description (varchar), file name (varchar), and due date (varchar).
Question submissions will include the date of submission (varchar), question id (integer), user id (integer), content (varchar) and file name (varchar). Ratings will include the date of submission (varchar), submission id (integer), user id (integer) and rating (integer).


### What are the basic functions of your web application?
Our web application will have a page for homework creation and assigning. The instructor will be able to assign homeworks to different classes and students, as well as create homework in different formats, whether a word document or a video format. Students will have a page for homework submission, which can also be in different formats. There will be a user grading submission form, which will have instructor created grade guidelines, of which the student can grade on a scale of 1-10, this numerical system will allow for grade display/distribution, which is another function of our web application. Numerical grading will be easier to process compared to student comments.


### What would be a good creative component (function) that can improve the functionality of your application?
A distribution curve of all grades after everything has been graded, as well as a distribution curve of how each student has graded and how they have been graded. This improves functionality as it provides a nice visual representation of grades and is easier to understand for the student.


This will also provide a visual representation of which students rate harsher and which students grade easier, so the teacher can make an educated decision as to what the students final grade is.


### A low fidelity UI mockup: (a sketch) of your interface (at least one image)
![image1](https://github.com/uiuc-fa21-cs411/24/blob/main/image/1.JPG)

![image2](https://github.com/uiuc-fa21-cs411/24/blob/main/image/2.JPG)

![image3](https://github.com/uiuc-fa21-cs411/24/blob/main/image/3.JPG)

## Project Work Distribution
Every week, deliverables will be determined by the entire team and each member can volunteer to choose which deliverable they would like to work on. If nobody volunteers, the group will meet and figure out who is able to work on the deliverable.


Every member agrees to put in the necessary amount of time to finish their deliverable. If somebody is unable to complete a deliverable, then the member will ask in the group chat for any suggestions. If the member is still unable to complete the deliverable, then we will meet and try to switch tasks. 

- Dataset creation and organization: Henry, Davy, Kevin, Julian
- Database operation designs: Henry, Davy, Kevin, Julian
- Front-end development (UI design, HTML, CSS): Henry, Julian
- Back-end development (Python Flask, SQL): Kevin, Davy
- Group's Azure account user: Kevin

If a team member is habitually not completing their deliverable, then they will be asked the reasoning and based on the answer the group may respond accordingly. 


 
 
