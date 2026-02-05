from flask import Flask, render_template_string, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# -------------------- DATABASE MODEL --------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- ROUTES --------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please login.')
        return redirect(url_for('login'))

    return render_template_string(REGISTER_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('payment'))

        flash('Invalid login details')

    return render_template_string(LOGIN_HTML)

@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        amount = request.form['amount']
        flash(f'Payment of BWP {amount} successful (simulation).')
        return redirect(url_for('payment'))

    return render_template_string(PAYMENT_HTML, user=current_user.email)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# -------------------- HTML TEMPLATES --------------------
LOGIN_HTML = """
<h2>Login</h2>
<form method="POST">
  <input name="email" placeholder="Email" required><br>
  <input name="password" type="password" placeholder="Password" required><br>
  <button type="submit">Login</button>
</form>
<a href="/register">Register</a>
"""

REGISTER_HTML = """
<h2>Register</h2>
<form method="POST">
  <input name="email" placeholder="Email" required><br>
  <input name="password" type="password" placeholder="Password" required><br>
  <button type="submit">Register</button>
</form>
<a href="/login">Login</a>
"""

PAYMENT_HTML = """
<h2>Welcome {{ user }}</h2>
<h3>Make a Payment</h3>
<form method="POST">
  <input name="amount" placeholder="Amount (BWP)" required><br>
  <button type="submit">Pay Now</button>
</form>
<a href="/logout">Logout</a>
"""

# -------------------- RUN --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
