from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Hello App</title>
</head>
<body>
    <h1>Enter your username</h1>
    <form method="POST" action="/hello">
        <input type="text" name="username" placeholder="Your username" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        username = request.form.get('username', 'World')
        return f"Hello, {username}!"
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)