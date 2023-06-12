from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import graphviz

UPLOAD_FOLDER = './filestorage/upload/'
RESULT_FOLDER = './filestorage/result/'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '3479aae851326c367b6f42d08304879a2c45b213f0584d7c576f67d1b5866040'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calc_tree_from_file(file, target_name):
    # 1. store the filestream to .csv cache file
    file_store_path = UPLOAD_FOLDER + file.filename
    file.save(file_store_path)
    # 2. read the csv and transfer string category to number category
    df = pd.read_csv(file_store_path, index_col=0)
    le = LabelEncoder()
    df_num = pd.DataFrame()
    for col in df.columns:
        label = le.fit_transform(df[col])
        df_num[col] = label
    # 3. split df to X and y, transfer to numpy array
    X = df_num[df_num.columns[:-1]].values
    y = df_num[df_num.columns[-1]].values
    # 4. train a decision tree
    clf = tree.DecisionTreeClassifier(criterion="entropy")# 实例化模型，添加criterion参数
    clf = clf.fit(X, y)
    # 5. plot the tree
    dot_data = tree.export_graphviz(clf #训练好的模型
                                ,out_file = None
                                ,feature_names= df_num.columns[:-1]
                                ,class_names=target_name
                                ,filled=True  #进行颜色填充
                                ,rounded=True #树节点的形状控制
    )
    graph = graphviz.Source(dot_data)
    # save to .dot
    res_fl_path = RESULT_FOLDER+file.filename
    graph.save(res_fl_path+".dot")
    # transfer to .png file
    from os import popen
    popen("dot -Tpng "+res_fl_path+".dot -o "+res_fl_path+".png")
    return res_fl_path+".png"

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
            return render_template('result.html', tree=calc_tree_from_file(file, ["Play", "Not Play"]))
    
    return redirect('/start')

if __name__ == '__main__':
    app.debug = True
    app.run()