from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cases.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database model
class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_name = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Case {self.case_name}>"

@app.route('/')
def home():
    cases = Case.query.all()
    return render_template('index.html', cases=cases)

@app.route('/add', methods=['GET', 'POST'])
def add_case():
    if request.method == 'POST':
        case_name = request.form['case_name']
        client_name = request.form['client_name']
        details = request.form['details']

        new_case = Case(case_name=case_name, client_name=client_name, details=details)
        db.session.add(new_case)
        db.session.commit()
        flash("Case added successfully!")
        return redirect(url_for('home'))
    return render_template('add_case.html')

@app.route('/delete/<int:case_id>')
def delete_case(case_id):
    case = Case.query.get_or_404(case_id)
    db.session.delete(case)
    db.session.commit()
    flash("Case deleted successfully!")
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()  # Ensure the database is created
    app.run(debug=True)
