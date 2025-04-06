from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        new_submission = Submission(text=user_input)
        db.session.add(new_submission)
        db.session.commit()
        return redirect(url_for('index'))
    
    submissions = Submission.query.order_by(Submission.timestamp.desc()).all()
    return render_template('index.html', submissions=submissions)

@app.route('/delete/<int:id>')
def delete(id):
    submission = Submission.query.get_or_404(id)
    db.session.delete(submission)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
