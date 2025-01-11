from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from questions import questions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/aliosmanozturk/mysite/quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    # Get the highest score from the database
    highest_score = db.session.query(db.func.max(User.score)).scalar() or 0
    return render_template('index.html', questions=questions, highest_score=highest_score)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name', '')
    answers = data.get('answers', {})

    # Calculate score (10 points per correct answer)
    score = 0
    for q_id, answer in answers.items():
        question_id = int(q_id.replace('q', ''))
        # Find the corresponding question
        question = next((q for q in questions if q['id'] == question_id), None)
        if question and question.get('type') == 'multiple_choice':
            if answer == question['correct']:
                score += 10

    # Save to database
    user = User(name=name, score=score)
    db.session.add(user)
    db.session.commit()

    return jsonify({'success': True, 'score': score})

@app.route('/reset-score', methods=['POST'])
def reset_score():
    try:
        # Delete all records from the database
        db.session.query(User).delete()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
