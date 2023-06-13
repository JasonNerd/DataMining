from flask import Flask, render_template, flash, request, redirect
from werkzeug.utils import secure_filename
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from os import popen
import graphviz
import time
from tree_explainer import *

UPLOAD_FOLDER = 'static/upload/'
RESULT_FOLDER = 'static/result/'
ALLOWED_EXTENSIONS = ['csv']

app = Flask(__name__)
app.config['SECRET_KEY'] = '3479aae851326c367b6f42d08304879a2c45b213f0584d7c576f67d1b5866040'

def generate_unique_file_name(base, ext):
    return base + str(int(time.time())) + '.' + ext

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cache_filestream_as_csv(file):
    # store the filestream to .csv cache file
    path_to_file = UPLOAD_FOLDER + file.filename
    file.save(path_to_file)
    return path_to_file
    
def save_tree_to_png_file(clf, feature_names, class_name, filename):
    # plot the tree
    dot_data = tree.export_graphviz(clf,
                                feature_names=feature_names,
                                class_names=class_name,
                                filled=True, 
                                rounded=True,
                                max_depth=5,
    )
    graph = graphviz.Source(dot_data)
    
    # save to .dot
    path_to_dot_file_without_ext = RESULT_FOLDER + filename
    graph.save(path_to_dot_file_without_ext + ".dot")
    
    # transfer to .png file
    popen("dot -Tpng " + path_to_dot_file_without_ext + ".dot" + " -o " + path_to_dot_file_without_ext + ".png")
    return 'result/' + filename + ".png"

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
        if 'class_column_name' not in request.form:
            flash('Column name/index not entered')
            return redirect('/start')
        if (not request.form['class_column_name'].strip()):
            flash('Column name/index cannot be empty')
            return redirect('/start')
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
        if not allowed_file(file.filename):
            flash('File type not supported')
            return redirect('/start')
        
        path_to_csv_file = cache_filestream_as_csv(file)
        df = pd.read_csv(path_to_csv_file)
        
        if request.form['class_column_name'] not in list(df.columns):
            flash('Column name not found')
            return redirect('/start')
        
        class_name = request.form['class_column_name']
        feature_names = list(df.columns).remove(class_name)
        
        X = df.drop(class_name, axis=1)
        y = df[class_name]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size=0.7)

        clf = tree.DecisionTreeClassifier(criterion="gini")# 实例化模型，添加criterion参数
        clf = clf.fit(X_train, y_train)
        
        accuracy = clf.score(X_test, y_test)
        
        print(accuracy)
        
        png_filename = save_tree_to_png_file(clf, feature_names, class_name, file.filename)
        
        tree_explanation = explain_tree(clf)

        return render_template(
            'result.html',
            tree_explanation=tree_explanation,
            class_name=class_name,
            accuracy=round(accuracy * 100, 2),
            tree_png_filename=png_filename
        )
    
    return redirect('/start')

if __name__ == '__main__':
    app.debug = True
    app.run()