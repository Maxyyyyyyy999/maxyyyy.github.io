import os
import requests  # Make sure to install requests if you haven't already
from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

API_KEY = "e221ac6e55317912796bc7e4345fecf9"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Example user data
users = [
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'}
]

# Blog posts structure
blog_posts = []

@app.route('/', methods=['GET', 'POST'])
def home():
    image_url = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('static', filename='uploads/' + filename)
    return render_template('home.html', image_url=image_url)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        # Create a new blog post
        title = request.form['title']
        content = request.form['content']
        username = session.get('user', 'Anonymous')
        blog_posts.append({'title': title, 'content': content, 'username': username, 'replies': []})
        return redirect(url_for('blog'))

    return render_template('blog.html', blog_posts=blog_posts)

@app.route('/reply/<int:post_index>', methods=['POST'])
def reply(post_index):
    if post_index < len(blog_posts):
        reply_content = request.form['reply_content']
        username = session.get('user', 'Anonymous')
        blog_posts[post_index]['replies'].append({'username': username, 'content': reply_content})
    return redirect(url_for('blog'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username already exists
        if any(user['username'] == username for user in users):
            return "Username already exists!", 400
        
        # Add the new user to the user list
        users.append({'username': username, 'password': password})
        session['user'] = username  # Log the user in
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check for valid credentials
        if any(user['username'] == username and user['password'] == password for user in users):
            session['user'] = username  # Log the user in
            return redirect(url_for('home'))
        return "Invalid username or password!", 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Log the user out
    return redirect(url_for('home'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    weather = None
    error = None
    if request.method == 'POST':
        city = request.form['city']
        # Call the OpenWeatherMap API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            weather = response.json()
        else:
            error = "City not found."

    return render_template('search.html', weather=weather, error=error)

if __name__ == '__main__':
    app.run(debug=True)