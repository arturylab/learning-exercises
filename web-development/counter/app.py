from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres1234@localhost/counter"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/get_count', methods=['GET'])
def get_count():
    counter = Counter.query.first()
    if not counter:
        counter = Counter(count=0)
        db.session.add(counter)
        db.session.commit()
    return jsonify({"count": counter.count})

@app.route('/click/<action>', methods=['POST'])
def update_counter(action):
    counter = Counter.query.first()
    if not counter:
        counter = Counter(count=0)
        db.session.add(counter)

    if action  == 'increase':
        counter.count += 1
    elif action == 'decrease':
        counter.count -= 1
    elif action == 'reset':
        counter.count = 0
    
    db.session.commit()
    return jsonify({'count': counter.count})

if __name__ == '__main__':
    app.run(debug=True)
