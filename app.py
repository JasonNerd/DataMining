from flask import Flask, render_template
app = Flask(__name__)

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

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    # following is a demostration about how to pass argvs
    return render_template('testdemo.html', name=name, movies=movies)

@app.route('/upload')
def upload():
    return render_template('upload.html', name=name, movies=movies)


@app.route('/result')
def result():
    return render_template('result.html', name=name, movies=movies)

