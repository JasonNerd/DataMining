from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '3479aae851326c367b6f42d08304879a2c45b213f0584d7c576f67d1b5866040'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calc_tree_from_file(file):
    return {
        "test": "test"
    }

# Just for demo use ###
name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]
# Just for demo use ###

@app.route('/test')
def test():
    # following is a demostration about how to pass argvs
    return render_template('testdemo.html', name=name, movies=movies)


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    return render_template('start.html', result_path="/result")

@app.route('/result', methods=['GET', 'POST'])
def calc_result():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file_input' not in request.files:
            flash('File missing')
            return redirect('/start')
        file = request.files['file_input']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/start')
        if file and allowed_file(file.filename):
            return render_template('result.html', tree=calc_tree_from_file(file))
    
    return redirect('/start')