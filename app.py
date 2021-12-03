from flask import Flask, render_template, request, session, url_for, redirect, flash, send_file
import re
import mysql.connector
from signal import SIGINT, signal
from PIL.Image import core as image
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
cnx = mysql.connector.connect(user='kevinc17', password='Secure!24', host='localhost', database='kevinc17_database')


@app.route('/')
@app.route('/index')
def index():
    if 'logintype' in session:
        return render_template('index.html', email=session['email'], logintype = session['logintype'])
    return render_template('index.html')

@app.route("/classes", methods=['GET'])
def class_list():
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return render_template('index.html')
    cur = cnx.cursor(buffered = True)
    if session['logintype'] == "teacher":
        strw = 'SELECT class_id, teacher_email, class_name, count(*) FROM (Class NATURAL JOIN Enrollment) WHERE class_id IN (SELECT class_id FROM Class WHERE teacher_email=\''+session['email']+'\') GROUP BY  class_id, teacher_email, class_name;'
    else:
        strw = 'SELECT class_id, teacher_email, class_name, count(*) FROM (Class NATURAL JOIN Enrollment) WHERE class_id IN (SELECT class_id FROM Enrollment WHERE student_email=\''+session['email']+'\') GROUP BY  class_id, teacher_email, class_name;'
    cur.execute(strw)
    rows = cur.fetchall()
    return render_template('class.html', classlist = rows, email=session['email'], logintype = session['logintype'])

@app.route("/questions", methods=['GET', 'POST'])
def question_list():
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return render_template('index.html')
    cur = cnx.cursor(buffered = True)
    # With search
    if request.method == 'POST':
        keyword = request.form['search']
        if session['logintype'] == "teacher":
            strw = 'SELECT * FROM (Question NATURAL JOIN Class) WHERE title LIKE \'%'+ keyword +'%\' AND class_id IN (SELECT class_id FROM Class WHERE teacher_email=\''+session['email']+'\');'
        else:
            strw = 'SELECT * FROM (Question NATURAL JOIN Class) WHERE title LIKE \'%'+ keyword +'%\' AND class_id IN (SELECT class_id FROM Enrollment WHERE student_email=\''+session['email']+'\');'
    # Without search
    elif session['logintype'] == "teacher":
        strw = 'SELECT * FROM (Question NATURAL JOIN Class) WHERE class_id IN (SELECT class_id FROM Class WHERE teacher_email=\''+session['email']+'\');'
    else:
        strw = 'SELECT * FROM (Question NATURAL JOIN Class) WHERE class_id IN (SELECT class_id FROM Enrollment WHERE student_email=\''+session['email']+'\');'
    cur.execute(strw)
    rows = cur.fetchall()
    return render_template('questions.html', questionlist = rows, email=session['email'], logintype = session['logintype'])

@app.route("/advancesql1", methods=['GET'])
def advanced_one():
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return render_template('index.html')
    cur = cnx.cursor(buffered = True)
    strw = "SELECT Teacher.teacher_email, teacher_name, count(class_id) FROM Teacher LEFT JOIN Class ON Teacher.teacher_email = Class.teacher_email  GROUP BY Teacher.teacher_email, teacher_name  ORDER BY Teacher.teacher_email ASC LIMIT 15;"
    cur.execute(strw)
    rows = cur.fetchall()
    return render_template('query_first.html', resultlist = rows, email=session['email'], logintype = session['logintype'])

@app.route("/advancesql2", methods=['GET'])
def advanced_two():
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return render_template('index.html')
    cur = cnx.cursor(buffered = True)
    strw = "SELECT Student.student_email, Student.student_name, AVG(points) FROM Student LEFT JOIN Submission ON Student.student_email = Submission.submitter LEFT JOIN Rating ON Submission.submission_id = Rating.submission GROUP BY Student.student_email, Student.student_name ORDER BY Student.student_email ASC LIMIT 15;"
    cur.execute(strw)
    rows = cur.fetchall()
    return render_template('query_second.html', resultlist = rows, email=session['email'], logintype = session['logintype'])

@app.route("/question/<id>", methods=['GET'])
def question_view(id):
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return render_template('index.html')
    cur = cnx.cursor(buffered = True)
    strw =  'SELECT * FROM (Question NATURAL JOIN Class) WHERE question_id=\''+ id +'\';'
    cur.execute(strw)
    rows = cur.fetchone()
    if rows:
        return render_template('question_option.html', question=rows, email=session['email'], logintype = session['logintype'])
    return render_template('question_option.html')

@app.route("/chart", methods=['GET'])
def chart():
    cur = cnx.cursor(buffered = True)
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return redirect(url_for('index'))
    if session['logintype'] != "student":
        flash(f'Invalid: Not a student', 'info')
        return redirect(url_for('index'))
    strw = 'SELECT Class.class_name, AVG(points) AS avg_pts FROM Student JOIN Submission ON Student.student_email = Submission.submitter JOIN Rating ON Submission.submission_id = Rating.submission JOIN Question ON Submission.question = Question.question_id JOIN Class ON Question.class_id = Class.class_id WHERE Student.student_email=\''+ session['email'] +'\'GROUP BY Class.class_name ORDER BY avg_pts DESC;'
    cur.execute(strw)
    rows = cur.fetchall()
    class_label = [i[0][:-1] for i in rows]
    avg_pts = [i[1] for i in rows]

    y_pos = [i for i, _ in enumerate(class_label)]
    plt.figure(figsize=(30, 6), dpi=200)
    plt.barh(y_pos, avg_pts, color='blue')
    plt.ylabel("Class Name")
    plt.xlabel("Average Rating")
    plt.title("Average Rating By Class")

    plt.yticks(y_pos, class_label)
    plt.savefig('testplot.png')
    #image.open('testplot.png').save('testplot.jpg','JPEG')
    return send_file("testplot.png")


@app.route("/submissions/<qid>", methods=['GET'])
def submission_list(qid):
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return render_template('index.html')
    cur = cnx.cursor(buffered = True)
    strw =  'SELECT * FROM Submission WHERE question=\''+ qid +'\' ORDER BY submission_id DESC;'
    cur.execute(strw)
    rows = cur.fetchall()
    return render_template('submissions.html', qid=qid, submissions=rows, email=session['email'], logintype = session['logintype'])

@app.route("/ratings/<submission_id>", methods=['GET'])
def rating_list(submission_id):
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return render_template('index.html')
    cur = cnx.cursor(buffered = True)
    strw =  'SELECT * FROM Rating WHERE submission=\''+ submission_id +'\' ORDER BY rating_id DESC;'
    cur.execute(strw)
    rows = cur.fetchall()
    cur = cnx.cursor(buffered = True)
    strw =  'SELECT * FROM Submission WHERE submission_id=\''+ submission_id +'\';'
    cur.execute(strw)
    rows2 = cur.fetchone()
    return render_template('view_rating.html', ratings=rows, submission = rows2, email=session['email'], logintype = session['logintype'])

#2 submit rating
@app.route("/ratings/<submission_id>/submitnew", methods=['GET','POST'])
def submit_rating(submission_id):
    if session['logintype'] != "student":
        flash(f'Invalid: Not a student', 'info')
        return redirect(url_for('index'))

    cur = cnx.cursor(buffered = True)
    strw =  'SELECT * FROM Submission WHERE submission_id=\''+ submission_id +'\';'
    cur.execute(strw)
    rows = cur.fetchone()
    if not rows:
        flash(f'Invalid submission ID', 'info')
        return redirect(url_for('index'))
    if request.method == 'POST':
        cur = cnx.cursor(buffered = True)
        rater = session['email']
        points = request.form['points']
        strw = 'SELECT rating_id FROM Rating ORDER BY rating_id DESC LIMIT 1;'
        cur.execute(strw)
        rating_id =  cur.fetchone()[0] + 1
        strw =  'INSERT INTO Rating VALUES ('+ str(rating_id) +','+ str(submission_id) +',\''+ rater +'\','+ str(points) +');'
        cur.execute(strw)
        cnx.commit()
        flash(f'Sucessfully added rating', 'info')
        return redirect(url_for('rating_list', submission_id = submission_id))
    return render_template('submit_rating.html', submission = rows, email=session['email'], logintype = session['logintype'])
#4 add new question
@app.route("/question/<class_id>/create_new", methods=['GET','POST'])
def create_new_question(class_id):
    if session['logintype'] != "teacher":
        flash(f'Invalid: Not a teacher', 'info')
        return redirect(url_for('question_list'))
    cur = cnx.cursor(buffered = True)
    strw =  'SELECT * FROM Class WHERE class_id=\''+ class_id +'\';'
    cur.execute(strw)
    rows = cur.fetchone()
    if not rows:
        flash(f'Invalid class ID', 'info')
        return redirect(url_for('index'))
    if request.method == 'POST':
        cur = cnx.cursor(buffered = True)
        description = request.form['description']
        title =  request.form['title']
        score = request.form['score']
        strw = 'SELECT question_id FROM Question ORDER BY question_id DESC LIMIT 1;'
        cur.execute(strw)
        question_id =  cur.fetchone()[0] + 1
        strw =  'INSERT INTO Question VALUES ('+ str(question_id) +','+ str(class_id) +',\''+ title +'\',\''+ description +'\','+ str(score) +',\'\');'
        print(strw)
        cur.execute(strw)
        cnx.commit()
        flash(f'Sucessfully added question', 'info')
        return redirect(url_for('question_list'))
    return render_template('question_create.html', class_row = rows, email=session['email'], logintype = session['logintype'])

    cur = cnx.cursor(buffered = True)
    description = request.form['description']
    title =  request.form['title']
    score = request.form['score']

    strw = 'SELECT question_id FROM Question ORDER BY question_id DESC LIMIT 1;'
    cur.execute(strw)
    new_question_id =  cur.fetchone()[0][0] + 1

    # Insert new submission
    strw =  'INSERT INTO Question VALUES ('+ str(new_question_id) + ','+ str(class_id) + ',\''+ title + '\',\''+ description +'\',\''+score+'\',\''+feedback+'\');'
    cur.execute(strw)
    # TODO: Uncomment this (danger)
    #without commit, it wont save
    #cnx.commit()
    flash(f'Question added', 'info')
    return redirect(url_for('question_list'))


@app.route("/question/<id>/edit", methods=['GET', 'POST'])
def question_edit(id):
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return render_template('index.html')
    cur = cnx.cursor(buffered = True)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        score = request.form['score']
        strw =  'UPDATE Question SET title=\''+ title +'\', description=\''+ description +'\', score=\''+ score +'\' WHERE question_id =\''+ id +'\' ;'
        cur.execute(strw)
        cnx.commit()
        return redirect(url_for('question_view', id = id))
    strw =  'SELECT * FROM (Question NATURAL JOIN Class) WHERE question_id=\''+ id +'\';'
    cur.execute(strw)
    rows = cur.fetchone()
    return render_template('question_edit.html', question=rows, email=session['email'], logintype = session['logintype'])

@app.route("/question/<id>/delete", methods=['GET'])
def question_delete(id):
    if 'logintype' not in session:
        flash(f'You are not logged in', 'info')
        return render_template('index.html')
    cur = cnx.cursor(buffered = True)
    # DELETE FROM table_name WHERE condition;
    # TODO: UNCOMMENT THIS (DANGER)
    strw= 'DELETE FROM Rating WHERE rating_id IN (SELECT rating_id FROM (SELECT rating_id FROM Rating JOIN Submission ON Rating.submission = Submission.submission_id WHERE question=\''+ id +'\') as T);'
    cur.execute(strw)
    cnx.commit()
    strw =  'DELETE FROM Submission WHERE question=\''+ id +'\';'
    cur.execute(strw)
    cnx.commit()
    strw =  'DELETE FROM Question WHERE question_id=\''+ id +'\';'
    cur.execute(strw)
    cnx.commit()
    flash(f'Question deleted', 'info')
    return redirect(url_for('question_list'))

@app.route("/question/<id>/submitnew", methods=['GET', 'POST'])
def submit_new(id):
    cur = cnx.cursor(buffered = True)
    strw =  'SELECT * FROM Question WHERE question_id=\''+ id +'\';'
    cur.execute(strw)
    rows = cur.fetchone()
    if not rows:
        flash(f'Invalid question ID', 'info')
        return redirect(url_for('index'))

    if session['logintype'] != "student":
        flash(f'Invalid: Not a student', 'info')
        return redirect(url_for('question_view', id = id))

    if request.method == 'POST':
        answer_content = request.form['answer']
        question_id = rows[0]
        submitter = session['email']
        strw = 'SELECT submission_id FROM Submission ORDER BY submission_id DESC LIMIT 1;'
        cur.execute(strw)
        new_submission_id =  cur.fetchone()[0] + 1

        # Insert new submission
        strw =  'INSERT INTO Submission VALUES ('+ str(new_submission_id) + ','+ '\'' + submitter + '\','+ str(question_id) + ',\''+ answer_content+'\');'
        # TODO: Uncomment this (danger)
        cur.execute(strw)
        cnx.commit()
        flash(f'Submission added', 'info')
        return redirect(url_for('question_view', id = id))
    return render_template('question_submit.html', question=rows, email=session['email'], logintype = session['logintype'])

# login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    message = ""
    if "logintype" in session:
        flash(f'You are already logged in', 'info')
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Assume username is going to be email, check for student or teacher
        if request.form['studentteacher'] == "student":
            email = request.form['email']
            password = request.form['password']
            cur = cnx.cursor(buffered = True)
            strw =  'SELECT * FROM Student WHERE (student_email=\'' + email + '\' AND password=\''+ password +'\r\');'
            cur.execute(strw)
            account = cur.fetchone()
            if account:
                # Create session data, we can access this data in other routes
                session['logintype'] = "student"
                session['email'] = account[0]
                # Redirect to logged in page
                flash(f'You have logged in', 'success')
                return redirect(url_for('index'))
            else:
                message = 'Incorrect username/password!'
        elif request.form['studentteacher'] == "teacher":
            email = request.form['email']
            password = request.form['password']
            cur = cnx.cursor(buffered = True)
            strw =  'SELECT * FROM Teacher WHERE (teacher_email=\'' + email + '\' AND password=\''+ password +'\r\');'
            cur.execute(strw)
            account = cur.fetchone()
            if account:
                # Create session data, we can access this data in other routes
                session['logintype'] = "teacher"
                session['email'] = account[0]
                # Redirect to logged in page
                return redirect(url_for('index'))
            else:
                message = 'Incorrect username/password!'

    # Show the login form with message (login page still undecided)
    return render_template('login.html', message=message)

# logout route
@app.route("/logout")
def logout():
    if "logintype" in session:
        # Remove session data, this will log the user out
        session.pop('logintype', None)
        session.pop('email', None)
        flash(f'You have logged out', 'success')
        # Redirect to login page
        return redirect(url_for('index'))
    else:
        flash(f'You are not logged in', 'info')
        return redirect(url_for('index'))

# Grade filtering tool

# logout route
@app.route("/gradefilter", methods=['GET', 'POST'])
def grade_filter():
    if request.method == 'POST':
        if "logintype" in session:
            q_type = session['logintype']
            q_email = session['email']
        else:
            q_type = 'x'
            q_email = 'x'
        if request.form['grade']:
            grade_threshold = request.form['grade']
        else:
            grade_threshold = 0
        if request.form['rating']:
            rating_threshold = request.form['rating']
        else:
            rating_threshold = 0
        cur = cnx.cursor(buffered = True)
        strw = 'SET @type = \''+q_type+'\';'
        cur.execute(strw)
        strw = 'SET @email = \''+q_email+'\';'
        cur.execute(strw)
        strw = 'SET @grade = '+str(grade_threshold)+';'
        cur.execute(strw)
        strw = 'SET @rating = '+str(rating_threshold)+';'
        cur.execute(strw)
        strw = 'SET @output=\'\';'
        cur.execute(strw)
        strw = 'CALL grade_filter(@type, @email, @grade, @rating, @output);'
        cur.execute(strw)
        strw = 'SELECT @output;'
        cur.execute(strw)
        outputstr = cur.fetchone()[0]
        outputlist = outputstr.split('\n')
        if "logintype" in session:
            return render_template('grade_filter.html', outputlist = outputlist, email=session['email'], logintype = session['logintype'])
        else:
            return render_template('grade_filter.html', outputlist = outputlist)

    if "logintype" in session:
        return render_template('grade_filter.html', email=session['email'], logintype = session['logintype'])
    else:
        return render_template('grade_filter.html')

# Interruption handler
def sigint_handler(signal_received, frame):
    global cnx
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    cnx.close()
    exit(0)

if __name__ == '__main__':
    signal(SIGINT, sigint_handler)
    app.run()
