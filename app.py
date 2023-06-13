from flask import Flask, render_template, flash, request, redirect, url_for
from sklearn.model_selection import train_test_split
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
    y = df_num[target_name].values
    X_col = df_num.columns.to_list()
    X_col.remove(target_name)
    X = df_num[X_col].values
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, y, test_size=0.3)
    # 4. train a decision tree
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(Xtrain, Ytrain)  # 使用实例化好的模型进行拟合操作
    score = clf.score(Xtest,Ytest) #返回预测的准确度
    # 5. plot the tree
    class_name = []
    for i in df[target_name].unique():
        class_name.append(target_name+' of '+i)
    dot_data = tree.export_graphviz(clf, feature_names= X_col, class_names=class_name)
    graph = graphviz.Source(dot_data)
    # save to .dot
    res_fl_path = RESULT_FOLDER+file.filename
    graph.save(res_fl_path+".dot")
    # transfer to .png file
    from os import popen
    popen("dot -Tpng "+res_fl_path+".dot -o "+res_fl_path+".png")
    #### NOTE: here `res_fl_path+".png"` represent the result decision tree png file name
    #### TODO: and it can be post on the result html page
    #### NOTE: `score` represent the accuracy of decision
    print(score) # can be posted on the result page
    return res_fl_path+".png"


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
        if not (file and allowed_file(file.filename)):
            print(request.form['class_column_name'])
            return render_template('result.html', tree=calc_tree_from_file(file, ["Play", "Not Play"]))
    
    return redirect('/start')

if __name__ == '__main__':
    app.debug = True
    app.run()