from flask import Flask, request, redirect, render_template_string, session
from kafka import KafkaProducer
import json
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# HTML login form
form_html = '''
<h2>Login</h2>
<form method="POST">
  Username: <input type="text" name="username" required><br>
  Password: <input type="password" name="password" required><br>
  <input type="submit" value="Login">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']

        if user_id == "admin" and password == "123":
            session['user'] = user_id

            login_event = {
                "user_id": user_id,
                "event": "login",
                "page": "/login",
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            producer.send('user-activity', value=login_event)
            return redirect('/dashboard')
        else:
            return "Invalid credentials", 401
    return render_template_string(form_html)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return f"Welcome {session['user']}! You are logged in."

if __name__ == '__main__':
    app.run(port=5000, debug=True)
