from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
import random
from config import Config  # Import settings

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)  # Load configurations

# Function to Generate Random Math Questions
def generate_question(operation, level):
    num1, num2 = random.randint(1, 10), random.randint(1, 10)

    if level == 'medium':
        num1, num2 = random.randint(10, 50), random.randint(10, 50)
    elif level == 'hard':
        num1, num2 = random.randint(50, 100), random.randint(50, 100)

    if operation == 'addition':
        question = f"{num1} + {num2}"
        answer = num1 + num2
    elif operation == 'subtraction':
        question = f"{num1} - {num2}"
        answer = num1 - num2
    elif operation == 'multiplication':
        question = f"{num1} × {num2}"
        answer = num1 * num2
    else:
        num1, num2 = max(num1, num2), min(num1, num2) or 1
        question = f"{num1} ÷ {num2}"
        answer = num1 // num2  # Integer division

    return question, answer

# Flask-WTF Form for Quiz Settings
class QuizForm(FlaskForm):
    operation = SelectField('Operation', choices=[('addition', 'Addition'),
                                                  ('subtraction', 'Subtraction'),
                                                  ('multiplication', 'Multiplication'),
                                                  ('division', 'Division')],
                            validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[('easy', 'Easy'),
                                                    ('medium', 'Medium'),
                                                    ('hard', 'Hard')],
                             validators=[DataRequired()])
    num_questions = IntegerField('Number of Questions', validators=[DataRequired()])
    submit = SubmitField('Start Quiz')

# Home Page (Start Quiz)
@app.route('/', methods=['GET', 'POST'])
def home():
    form = QuizForm()
    if form.validate_on_submit():
        session['operation'] = form.operation.data
        session['difficulty'] = form.difficulty.data
        session['num_questions'] = form.num_questions.data
        session['score'] = 0  # Reset score
        session['current_question'] = 0  # Reset question count
        return redirect(url_for('quiz'))
    return render_template('index.html', form=form)

# Quiz Page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'num_questions' not in session:
        return redirect(url_for('home'))

    operation = session['operation']
    difficulty = session['difficulty']
    num_questions = session['num_questions']

    if session['current_question'] >= num_questions:
        return redirect(url_for('result'))

    question, correct_answer = generate_question(operation, difficulty)
    session['correct_answer'] = correct_answer

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer and user_answer.isdigit():
            if int(user_answer) == session['correct_answer']:
                session['score'] += 1
        session['current_question'] += 1
        return redirect(url_for('quiz'))

    return render_template('quiz.html', question=question, question_num=session['current_question'] + 1, total=num_questions)

# Result Page
@app.route('/result')
def result():
    score = session.get('score', 0)
    num_questions = session.get('num_questions', 1)
    return render_template('result.html', score=score, total=num_questions)

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
