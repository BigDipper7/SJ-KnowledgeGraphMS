# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from tj.db.util.cayley_util import CayleyUtil
from tj.util.import_util import import_excel_new_version
from forms import AddRelationForm
import json
import threading
import os

import functools
import inspect
from datetime import timedelta
import traceback

is_login = str('is_login')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jiu bu gao su ni'
app.config['UPLOAD_FOLDER'] = './'
bootstrap = Bootstrap(app)
manager = Manager(app)

@app.before_request
def make_session_permanent():
    '''setting for session expire span, now we set it to 3min
    '''
    # app.logger.info("@app.before_request invoke, refresh session expire time")
    expire_span = 3#3 minutes
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=expire_span)


def check_is_login(next_url = None):
    def check_is_login_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # func_args = inspect.getcallargs(func, *args, **kwargs)
            # print func_args
            # if func_args.get('username') != 'admin':
            #     raise Exception('permission denied')
            app.logger.debug('check_is_login')
            if not session.get(is_login):
                flash('Plz login first')
                app.logger.error('must login first')
                return redirect(url_for('login', next=next_url if not next_url))
            return func(*args, **kwargs)
        return wrapper
    return check_is_login_decorator


@app.route('/sjkg/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('session/login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app.logger.info('IMPORT: Attemp login... with username:{} password:{}'.format(username, password))

        next_url = request.args.get('next')
        app.logger.info('login module: next_url is {}'.format(next_url))

        if not username and not password:
            flash('Field can not be blank! Try again.')
            return redirect(url_for('login', next = next_url if not next_url))
        elif username == "admin" and password == 'nicai':
            session[is_login] = True
            flash('Login Success~')
            app.logger.info('login success')
            # return redirect(url_for('home'))
            return redirect(next if not next_url else url_for('home'))
        else:
            flash('Wrong username or password! Try again.')
            return redirect(url_for('login', next = next_url if not next_url))


@app.route('/sjkg/logout', methods=['GET'])
def logout():
    if session.get(is_login):
        flash('Logout Success~')
        session.pop(is_login, None)
    return redirect(url_for('home'))


@app.route('/sjkg/card')
def card():
    # session[is_login] = True
    return render_template("card/cardbase.html")


@app.route('/sjkg/control', methods=['GET', 'POST'])
@check_is_login(next_url = url_for('control'))
def control():
    add_relation_form = AddRelationForm()
    cayley_util = CayleyUtil()
    if add_relation_form.validate_on_submit():
        form_subject = add_relation_form.subject.data.encode("utf-8")
        form_predicate = add_relation_form.predicate.data.encode("utf-8")
        form_object = add_relation_form.object.data.encode("utf-8")
        cayley_util.insert_quads_triple(form_subject, form_predicate, form_object)
        return redirect(url_for("control"))
    gremlin_query = "g.V().Tag(\"Subject\").Out(null, \"Predicate\").Tag(\"Object\").All()"
    gremlin_result = json.loads(cayley_util.query(gremlin_query))
    return render_template("control/controlbase.html", triples=gremlin_result["result"],
                           add_relation_form=add_relation_form, status=request.args.get("status"))


@app.route('/sjkg/control/relation/delete', methods=['POST'])
def control_relation_delete():
    # subject = request.args.get("subject").encode("utf-8")
    # object = request.args.get("object").encode("utf-8")
    # predicate = request.args.get("predicate").encode("utf-8")
    subject = request.json["subject"].encode("utf-8")
    object = request.json["object"].encode("utf-8")
    predicate = request.json["predicate"].encode("utf-8")
    print subject, object, predicate

    result = False

    if subject and object and predicate:
        cayley_util = CayleyUtil()
        try:
            result = cayley_util.delete_quads_triple(subject, predicate, object)
        except Exception as e:
            app.logger.error(traceback.format_exc())
    return json.dumps({"result": result})


@app.route('/sjkg/entity')
def entity():
    # if session.get(is_login):
    #     session.pop(is_login, None)
    return render_template("entity/entitybase.html")


@app.route('/sjkg/entity/<name>')
def entity_name(name):
    return render_template("entity/entityname.html", name=name)


@app.route('/sjkg/home')
@app.route('/sjkg')
# @check_is_login
def home():
    '''bind both this two url to such a one method'''
    # return redirect(url_for("hehe"))
    return render_template("home.html")

# @app.route('/sjkg/home')
# def hehe():
#     return render_template("home.html")


def fetch_relations_by_entity(name):
    result_rlts = []
    cayley_util = CayleyUtil()
    #get result  relations origin data
    rlts_origin_data = cayley_util.find_relations_from_node(name)

    if not rlts_origin_data:
        #handle condition if not exist the entityname
        return None, None

    # print 'all changes....'

    app.logger.info("show data in rlts_origin_data query by entity name:{0}",name)
    _print_rlts_odata(rlts_origin_data)

    #doing sorting using lambda expr
    rlts_origin_data.sort(key=lambda x: x['relation'], reverse=False)

    app.logger.info("show data in rlts_origin_data after sort")
    _print_rlts_odata(rlts_origin_data)

    for item_rlts in rlts_origin_data:
        if not item_rlts['relation'].startswith("attribute:"):
            continue
        predicate = item_rlts['relation'].replace("attribute:", "").split("/")
        p_len = len(predicate)
        real_concept_1_subject = predicate[p_len - 1]

        result_rlts.append({"sect_title": real_concept_1_subject, "sect_text": item_rlts['target'], "margin_left": (p_len - 1) * 50})

    rest_attrs, rest_non_attrs = _process_rlts_odata(rlts_origin_data)
    app.logger.error(rest_attrs)
    app.logger.error(rest_non_attrs)
    # return result_rlts
    return rest_attrs, rest_non_attrs

def _process_rlts_odata(rlts_origin_data):
    '''generate section indicator in num, generate two kinds of model
    '''
    rest_non_attrs = []#None atrributes
    rest_attrs = []#attributes
    attrs_no = [0,0,0,0]

    for item_rlts in rlts_origin_data:
        item_rlts__source = item_rlts['source']
        item_rlts__relation = item_rlts['relation']
        item_rlts__id = item_rlts['id']
        item_rlts__target = item_rlts['target']
        if item_rlts__relation.startswith("attribute:"):
            #means atrribute if curren entity
            item_rlts__relation = item_rlts__relation.replace("attribute:","")#del no useful attribute: prefix
            hierachy_dirs_list = item_rlts__relation.split('/')
            hir_len = len(hierachy_dirs_list)

            sect_title = hierachy_dirs_list[hir_len-1]
            margin_left = hir_len - 1

            #there has some error, not always appear
            while(len(attrs_no)<hir_len):
                #ensure len equals
                attrs_no.append(0)

            attrs_no[hir_len-1] += 1
            attrs_no[hir_len:]=[]#del not useful list num
            no = ".".join(str(t) for t in attrs_no)
            # for index in range(hir_len,len(attrs_no)):
            #     attrs_no[index] = [1]

            rest_attrs.append({"sect_title":sect_title,"sect_text":item_rlts__target,"margin_left":margin_left,"no":no})
        else:
            #means not the atrribute
            rest_non_attrs.append({'subject':item_rlts__source, 'predicate':item_rlts__relation, 'object':item_rlts__target})

    return rest_attrs, rest_non_attrs

def _print_rlts_odata(rlts_origin_data):
    '''private method, just using to print rlts_origin_data.'''
    if not rlts_origin_data:
        app.logger.warning('Attention: rlts_origin_data is None')
        return
    for item in rlts_origin_data:
        source = item['source']
        relation = item['relation']
        id = item['id']
        target = item['target']
        info = "source:{}, relation:{}, id:{}, target:{}".format(source, relation, id, target).decode('utf-8')
        app.logger.debug(info)
        # print info
    return

@app.route('/sjkg/submitCard', methods=['POST', 'GET'])
def submitCard():
    '''submitCard calling by the form post action happened in /sjkg/card
    '''
    if request.method == "POST":
        entity_name = request.form["entity_name"].encode("utf-8")

        if not entity_name:
            app.logger.warning("No Input in form['entity_name'] from card page, alert~")
            flash("Field content can not be empty! Try again!")
            return redirect(url_for('card'))

        # result_rlts = fetch_relations_by_entity(entity_name)
        rest_attrs, rest_non_attrs = fetch_relations_by_entity(entity_name)

        if not rest_attrs and not rest_non_attrs:
            # when result_rlts is None means no such entity found!
            app.logger.warning("No such entity: {0}".format(entity_name))
            flash("Can not find entity: {0}, Check it!".format(entity_name))
            return redirect(url_for('card'))
        else:
            return render_template("card/card.html", data={"rest_attrs": rest_attrs, "rest_non_attrs":rest_non_attrs}, name=entity_name)


@app.route('/sjkg/search')
def search():
    if request.method == "GET":
        entity1 = request.args.get("entity1", "").encode("utf-8")
        entity2 = request.args.get("entity2", "").encode("utf-8")
        level = request.args.get("level", 6)
        if level == "大于6":
            level = 7
        level = int(level)
        level = level if level <= 6 else 10
        if entity1 == "" or entity2 == "":
            flash('test:Nothing in it')
            return render_template("home.html")
        else:
            cayley_util = CayleyUtil()
            paths, relations = cayley_util.find_all_paths(entity1, entity2, [], [], None, level)
            relation_dict = {"relations": relations}
            return render_template("search/searchbase.html", relations=json.dumps(relation_dict), paths=paths)


@app.route('/sjkg/ajax/entity/<name>', methods=['POST'])
def ajax_entity(name):
    cayley_util = CayleyUtil()
    return cayley_util.find_relations(name)

ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@app.route('/sjkg/excel_import', methods=['POST'])
def excel_import():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_location = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_location)
            t = threading.Thread(target=import_excel_new_version, args=(file_location,))
            t.start()
            return redirect(url_for("control", status="上传成功！请等待一段时间！"))
        elif file and not allowed_file(file.filename):
            return redirect(url_for("control", status="文件类型错误！"))
    return redirect(url_for("control", status="错误！请检查文件格式！"))


@app.route('/sjkg/upload_pic', methods=['POST'])
def upload_pic():
    if request.method == 'POST':
        file = request.files['file']
        entity_name = request.form.get('entity').encode('utf-8')
        file_location = os.path.join(os.getcwd(), 'static/pic', file.filename)
        file.save(file_location)
        cayley_util = CayleyUtil()
        url_prefix = '/sjkg/pic/' + file.filename
        cayley_util.insert_quads_triple(entity_name, 'attribute:图片'.encode('utf-8'), url_prefix.encode('utf-8'))
    return redirect(url_for("control", status="添加图片成功！"))


@app.route('/sjkg/upload_vid', methods=['POST'])
def upload_vid():
    if request.method == 'POST':
        file = request.files['file']
        entity_name = request.form.get('entity').encode('utf-8')
        file_location = os.path.join(os.getcwd(), 'static/vid', file.filename)
        file.save(file_location)
        cayley_util = CayleyUtil()
        url_prefix = '/sjkg/vid/' + file.filename
        cayley_util.insert_quads_triple(entity_name, 'attribute:视频'.encode('utf-8'), url_prefix.encode('utf-8'))
    return redirect(url_for("control", status="添加视频成功！"))


@app.route('/sjkg/pic/<name>', methods=['GET'])
def show_pic(name):
    index = name.index('.')
    name1 = name[0:index]
    url = '/static/pic/' + name
    return render_template('pic.html', head=name1, url=url)


@app.route('/sjkg/vid/<name>', methods=['GET'])
def show_vid(name):
    index = name.index('.')
    name1 = name[0:index]
    url = '/static/vid/' + name
    return render_template('vid.html', head=name1, url=url)


#----------------------------------------
# main func snippet
#----------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
