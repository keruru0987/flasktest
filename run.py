# coding=utf-8
# @Author : Eric

import pandas
from flask import Flask, render_template, request
import settings
import re
from bs4 import BeautifulSoup
from markdown import markdown
import math


app = Flask(__name__)


def get_title(api=''):
    # 获取标题数据
    nlp_choose = settings.nlp_choose  # 选择要研究的NLP库
    nlp_api = settings.nlp_api[nlp_choose]
    if api != '':
        nlp_api = api
    print('正在获取' + nlp_api + '的title')

    # 数据的获取以及处理
    fpath = settings.new_github_filepath[nlp_api]

    df = pandas.read_csv(fpath)
    df = df.fillna('')
    title_texts = []

    # 去掉其中的pull,保留issue
    for index, row in df.iterrows():
        title_texts.append(row['title'])
    return title_texts


def get_raw_data(api=''):
    # 直接将没有清洗的字符串数组返回，s2v用
    # 如果指定了api，则按照指定的api来，否则选择setting中默认的api
    nlp_choose = settings.nlp_choose  # 选择要研究的NLP库
    nlp_api = settings.nlp_api[nlp_choose]
    if api != '':
        nlp_api = api
    print('正在获取' + nlp_api + '的body')

    # 数据的获取以及处理
    fpath = settings.new_github_filepath[nlp_api]

    df = pandas.read_csv(fpath)
    df = df.fillna('')
    texts = []

    for index, row in df.iterrows():
        texts.append(row['body'])

    non_code_texts = []
    for i in range(0, len(texts)):
        # 消除代码块
        pattern = r'```(.*\n)*?```'
        text = re.sub(pattern, '', texts[i])
        # 消除命令行指令
        pattern2 = r'> > > .*'
        text = re.sub(pattern2, '', text)
        # 消除报错 一般两行
        pattern3 = r'File .*\n.*'
        text = re.sub(pattern3, '', text)
        html = markdown(text)
        non_code_texts.append(BeautifulSoup(html, 'html.parser').get_text())

    return non_code_texts


def get_labels(api=''):
    # 获取label数据,返回的是一个二维数组
    nlp_choose = settings.nlp_choose  # 选择要研究的NLP库
    nlp_api = settings.nlp_api[nlp_choose]
    if api != '':
        nlp_api = api
    print('正在获取' + nlp_api + '的label')

    # 数据的获取以及处理
    fpath = settings.new_github_filepath[nlp_api]

    df = pandas.read_csv(fpath)
    df = df.fillna('')
    labels = []

    for index, row in df.iterrows():
        cur_labels = []
        label_list = eval(row['labels'])
        for label_dict in label_list:
            cur_labels.append(label_dict['name'])
        labels.append(cur_labels)
    return labels


def process_query(query):
    # 删代码
    pattern = r'<code>(.*\n)*?</code>'
    text = re.sub(pattern, '', query)
    # 删图片
    pattern2 = r'<img.*?>'
    text = re.sub(pattern2, '', text)
    re_query = BeautifulSoup(text, 'html.parser').get_text()
    return re_query


def alter_pic_size(query):
    # 修改显示图片长度为1000px
    pattern = r'<img'
    text = re.sub(pattern, "<img style='width: 1000px'", query)
    return text


def search(selected_api, so_query):
    """
    根据给定的API和查询语句，返回与其相关的so posts，根据相关程度进行降序排序
    :return: 包含posts信息的列表，信息分别为链接（用ID进行构造），标题，内容，相关度
    """
    fpath = settings.stackoverflow_filepath[selected_api]
    sodata_df = pandas.read_csv(fpath)
    sodata_df = sodata_df.fillna('')

    # selected_df = pd.DataFrame(columns=['ID', 'Title', 'Body'])
    result_so = []

    for index, row in sodata_df.iterrows():
        match_score = 0
        # 把所有字符转换为小写形式
        for word in so_query.lower().split():
            if word in row['Title'].lower():
                match_score += 1
            if word in row['Tags'].lower():
                match_score += 1
            # 这里还可以考虑body的影响

        if match_score >= 1:
            link = 'https://stackoverflow.com/questions/' + str(row['Id'])
            # 构造其中一条数据
            acc_id = ''
            if row['AcceptedAnswerId'] != '':
                acc_id = int(row['AcceptedAnswerId'])
            processed_body_text = process_query(row['Body'])  # 去掉code，图片的
            imgsize_fixed_body = alter_pic_size(row['Body'])  # 调整图片大小后的
            tag_str = row['Tags']
            tag_pattern = r'<.*?>'
            tags = re.findall(tag_pattern, tag_str)
            re_tag = ''
            for tag in tags:
                tag1 = tag.replace('<', '')
                tag2 = tag1.replace('>', '')
                re_tag = re_tag + tag2 + ' '

            information = [link, row['Title'], imgsize_fixed_body, str(row['Id']), str(acc_id), processed_body_text,
                           str(row['Score']), str(row['ViewCount']), re_tag, str(row['AnswerCount']),
                           str(row['CommentCount']), match_score, row['ViewCount']]
            result_so.append(information)

    # 先根据热度进行排序
    so_hot_sorted = sorted(result_so, reverse=True, key=lambda post: post[12])
    # 再按照query相关度进行排序
    return_so = sorted(so_hot_sorted, reverse=True, key=lambda post: post[11])

    return return_so


def find(selected_api, id_str):
    fpath = settings.stackoverflow_filepath[selected_api]
    sodata_df = pandas.read_csv(fpath)
    sodata_df = sodata_df.fillna('')
    matched_so = []
    match_flag = 0
    for index, row in sodata_df.iterrows():
        if str(row['Id']) == id_str:
            acc_id = ''
            if row['AcceptedAnswerId'] != '':
                acc_id = int(row['AcceptedAnswerId'])
            tag_str = row['Tags']
            tag_pattern = r'<.*?>'
            tags = re.findall(tag_pattern, tag_str)
            tag_list = []
            for tag in tags:
                tag1 = tag.replace('<', '')
                tag2 = tag1.replace('>', '')
                tag_list.append(tag2)
            matched_so = [row['Title'], row['Body'], row['Tags'], str(acc_id), str(row['Score']),
                          str(row['ViewCount']), str(row['AnswerCount']), str(row['CommentCount']), tag_list]
            match_flag = 1
            break
    if match_flag == 0:
        raise Exception('没有匹配的ID')
    return matched_so


def girecommend(api, title, body, tags):
    docs = get_raw_data(api)
    titles = get_title(api)
    tag_list = get_labels(api)
    scores = score_all(docs, titles, tag_list, process_query(body), title, tags)
    # print(scores)

    select_num = settings.select_num
    # sort_re = list(map(scores.index, heapq.nlargest(select_num, scores)))
    sort_re_all = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
    sort_re = sort_re_all[0:select_num]
    # print(sort_re)
    fpath = settings.new_github_filepath[api]
    gi_df = pandas.read_csv(fpath)
    gi_df = gi_df.fillna('')

    tags = get_labels(api)

    result_gi = []
    for index in sort_re:
        link = settings.api_prelink[api] + str(gi_df.loc[index]['number'])
        state = ''
        if gi_df.loc[index]['state'] == 'open':
            state = '1'
        clean_body = gi_df.loc[index]['body']
        # 消除代码块
        pattern = r'```(.*\n)*```'
        clean_body = re.sub(pattern, '', clean_body)
        # 消除命令行指令
        pattern2 = r'> > > .*'
        clean_body = re.sub(pattern2, '', clean_body)
        # 消除报错 一般两行
        pattern3 = r'File .*\n.*'
        clean_body = re.sub(pattern3, '', clean_body)
        html = markdown(clean_body)
        clean_body = BeautifulSoup(html, 'html.parser').get_text()

        tag_str = ''
        for tag in tags[index]:
            tag_str = tag_str + tag + ' '

        information = [link, gi_df.loc[index]['title'], gi_df.loc[index]['body'], gi_df.loc[index]['number'],
                       state, clean_body, str(gi_df.loc[index]['comments']), tag_str]
        result_gi.append(information)

    return result_gi


def computeTF(vocab, doc):
    tf = dict.fromkeys(vocab, 0)
    for word in doc:
        tf[word] += 1
    return tf


def computeIDF(tfList):
    idfDict = dict.fromkeys(tfList[0], 0)  # 词为key，初始值为0
    N = len(tfList)  # 总文档数量
    for tf in tfList:  # 遍历字典中每一篇文章
        for word, count in tf.items():  # 遍历当前文章的每一个词
            if count > 0:  # 当前遍历的词语在当前遍历到的文章中出现
                idfDict[word] += 1  # 包含词项tj的文档的篇数df+1
    for word, Ni in idfDict.items():  # 利用公式将df替换为逆文档频率idf
        idfDict[word] = math.log10(N / Ni)  # N,Ni均不会为0
    return idfDict  # 返回逆文档频率IDF字典


def computeTFIDF(tf, idfs):  # tf词频,idf逆文档频率
    tfidf = {}
    for word, tfval in tf.items():
        tfidf[word] = tfval * idfs[word]
    return tfidf


def score_all(docs, titles, tags_list, sequence, so_title_text, so_tags):
    vocab = set([word for doc in docs for word in doc])
    tf_list = []
    for doc in docs:
        tf = computeTF(vocab, doc)
        tf_list.append(tf)

    idfs = computeIDF(tf_list)
    tf_idf_list = []
    for tf in tf_list:
        tf_idf = computeTFIDF(tf, idfs)
        tf_idf_list.append(tf_idf)


    Dvector = pandas.DataFrame([tfidf for tfidf in tf_idf_list])  # 文档的向量

    query = []
    for word in sequence:
        if word in vocab:
            query.append(word)
        else:
            continue
    tf = computeTF(vocab, query)
    Q_tf_idf = computeTFIDF(tf, idfs)  # Query的向量

    scores = []
    for vector in Dvector.to_dict(orient='records'):
        score = 0
        for k in Q_tf_idf:
            if k in vector:
                score += Q_tf_idf[k] * vector[k]
        scores.append(score)
    return scores


@app.route("/", methods=["GET", "POST"])
def mainpage():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        selected_api = request.form.get("selected_api")
        so_query = request.form.get("so_query")
        print(selected_api, so_query)

        # 需要构造一个列表，其中的每一项内容需要包括:链接（由ID号进行构造）,标题，内容, Id, AcceptedAnswerId,
        # processed_body_text,score, viewcount, tag_list, AnswerCount, CommentCount
        result = search(selected_api, so_query)

        return render_template("so_results.html", u=result, api=selected_api, query=so_query)


@app.route("/recommend")
def recommend():
    """
    根据从前端传入的StackOverflow Id号和api，为其推荐相关的Github Issue
    :return:
    """
    api = request.args.get("api")
    id = request.args.get("id")  # str形式的
    print("当前要进行推荐的api: " + api)
    print("当前要进行推荐的so_id: " + id)
    matched_so = find(api, id)
    # title,body,tags,AcceptedAnswerId, score, view_count, answer_count, comment_count, tag_list
    img_processed_body = alter_pic_size(matched_so[1])
    title = matched_so[0]
    acc_id = matched_so[3]
    score = matched_so[4]
    view_count = matched_so[5]
    answer_count = matched_so[6]
    comment_count = matched_so[7]
    tag_list = matched_so[8]

    result = girecommend(api, matched_so[0], matched_so[1],
                         matched_so[2])  # link,title,body,number,state,clean_body,comments,tags
    # for inf in result:
    #     print(inf)

    label_pre_link = settings.api_label_prelink[api]

    return render_template('gi_results.html', u=result, img_processed_body=img_processed_body, title=title,
                           acc_id=acc_id, so_id=id, score=score, view_count=view_count, answer_count=answer_count,
                           comment_count=comment_count, tag_list=tag_list, tag_pre_link=label_pre_link)


if __name__ == '__main__':
    app.run()
