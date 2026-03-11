from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = "MySuperSecretKey"

db = SQLAlchemy(app)


# --------------------
# Database Model
# --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


# --------------------
# Create Database
# --------------------
with app.app_context():
    db.create_all()


# --------------------
# Home Route
# --------------------
@app.route('/')
def home():

    if 'user_id' not in session:
        return render_template("index.html", logged_in=False)

    curr_user = User.query.get(session['user_id'])

    return render_template(
        "index.html",
        logged_in=True,
        curr_user=curr_user
    )


# --------------------
# Login Page
# --------------------
@app.route('/loginin')
def loginin():
    return render_template("auth/login.html")


# --------------------
# Login Logic
# --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session['user_id'] = user.id
            flash("Login successful!", "success")

            return redirect('/')

        flash("Invalid email or password", "danger")
        return redirect('/loginin')

    return render_template("auth/login.html")


# --------------------
# Register Page
# --------------------
@app.route("/registerr")
def registerr():
    return render_template("auth/register.html")


# --------------------
# Register Logic
# --------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists", "danger")
            return redirect('/registerr')

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for('loginin'))

    return render_template("auth/register.html")


# --------------------
# Logout
# --------------------
@app.route('/logout')
def logout():

    session.pop('user_id', None)
    flash("Logged out successfully", "info")

    return redirect('/')


# --------------------
# Meeting Page
# --------------------
@app.route("/meeting")
def meeting():

    if 'user_id' not in session:
        return redirect('/loginin')

    curr_user = User.query.get(session['user_id'])

    return render_template("meeting.html", curr_user=curr_user)


# --------------------
# Join Meeting Page
# --------------------
@app.route("/join")
def join():
    return render_template("join_meeting.html")


# --------------------
# Join Meeting Logic
# --------------------
@app.route("/joinn", methods=['GET', 'POST'])
def join_meeting():

    if request.method == 'POST':

        meetingid = request.form['room_id']

        return redirect(f'/meeting?roomID={meetingid}')

    return redirect("/join")


# --------------------
# Run App
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
