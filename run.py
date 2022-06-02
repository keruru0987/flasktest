# coding=utf-8
# @Author : Eric

from flask import Flask, render_template, request

from stackoverflow_search import SOSearcher

app = Flask(__name__)


@app.route("/")
def mainpage():
    return render_template("index.html")


@app.route("/soresult")
def soresult():
    selected_api = request.form.get("selected_api")
    so_query = request.form.get("so_query")
    print(selected_api, so_query)

    # 需要构造一个列表，其中的每一项内容需要包括:链接（由ID号进行构造）,标题，内容, Id, AcceptedAnswerId,
    # processed_body_text,score, viewcount, tag_list, AnswerCount, CommentCount
    SO_Seacher = SOSearcher(selected_api, so_query)
    result = SO_Seacher.search()

    return render_template("so_results.html", u=result, api=selected_api, query=so_query)



if __name__ == '__main__':
    app.run()
