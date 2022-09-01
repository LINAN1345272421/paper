import operator

from flask import Flask, request, jsonify
from flask import render_template
import util

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/query")
def query_data():
    title=request.values.get("title")
    mainworld=request.values.get("mainworld")
    author=request.values.get("author")
    year=request.values.get("year")
    meet=request.values.get("meet")
    Data=[]
    for data in util.query_data(title,mainworld,author,year,meet):
        Data.append(data)
    return jsonify({"data":Data})

@app.route('/tem2')
def hello_world2():
    return render_template("show.html")
#词云图
@app.route('/wordCloud')
def wordCloud():
    return render_template("wordCloud.html")
#top_10显示页面
@app.route('/top10_show')
def top10_show():
    return render_template("top10.html")

#获取top10热词
@app.route("/top_10")
def top_10():
    word_num=util.word_cloud_top()
    word_cloud_num=[]
    flag=0;
    for i in word_num:
        if(' ' in i[0]):
            word_cloud_num.append([i[0],i[1]])
            flag=flag+1;
            if(flag>9):
                break
    return jsonify({"data":word_cloud_num})
#获取top_10的子热词
@app.route("/top_10_class")
def top_10_class():
    word_cloud_num = []
    word_cloud = []
    top_word=request.values.get("top_word")
    word_num = util.get_top_10_class(top_word)
    for i in word_num:
        word_cloud.append(i[0])
        word_cloud_num.append(i[1])
    return jsonify({"name": word_cloud,"value":word_cloud_num})
#关键词分类统计、柱状图
@app.route("/key_word_class")
def key_word_class():
    word_num=util.word_cloud_top()
    word_cloud_num=[]
    word_cloud=[]
    flag=0;
    for i in word_num:
        word_cloud.append(i[0])
        word_cloud_num.append(i[1])
        flag=flag+1;
        if(flag>150):
            break
    return jsonify({"name":word_cloud,"value":word_cloud_num})
#词云图数据
@app.route("/word_cloud_date")
def word_cloud_date():
    word_num=util.word_cloud_top()
    word_cloud_num=[]
    flag=0;
    for i in word_num:
        word_cloud_num.append({"name":i[0],"value":i[1]})
        flag=flag+1;
        if(flag>30):
            break
    return jsonify({"data":word_cloud_num})
#词云图表格
@app.route("/word_cloud_date_list")
def word_cloud_date_list():
    word_num=util.word_cloud_top()
    word_cloud_list=[]
    word_cloud_class=[]
    flag=0;
    for i in word_num:
        word_cloud_class=[i[0],i[1]]
        word_cloud_list.append(word_cloud_class)
        flag=flag+1;
        if(flag>30):
            break
    return jsonify({"data":word_cloud_list})

#论文页面
@app.route("/paper_update")
def paper_update():
    title=request.values.get("title")
    print(title)
    data = util.query_by_title(title)
    return render_template("paperupdate.html",data=data)
#论文删除
@app.route("/paper_delete")
def paper_delete():
    title=request.values.get("title")
    data=util.delete_paper_title(title)
    return jsonify({"data":data})
#论文修改
@app.route("/update_paper")
def update_paper():
    title=request.values.get("title")
    if(title=="@"):
        data=["","","","","",""]
    else:
        data=util.query_by_title(title)
    return render_template("paper.html",data=data)
@app.route("/update_paper_submit")
def update_paper_submit():
    title = request.values.get("title")
    authors = request.values.get("authors")
    meet = request.values.get("meet")
    yeardate = request.values.get("yeardate")
    abstract = request.values.get("abstract")
    keyword = request.values.get("keyword")
    data=util.update_paper_submit(title,authors,meet,yeardate,abstract,keyword)
    return jsonify({"data":data})


if __name__ == '__main__':
    app.run()
