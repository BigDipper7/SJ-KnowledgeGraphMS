# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from tj.db.util.cayley_util import CayleyUtil
from tj.util.import_util import import_excel
from forms import AddRelationForm
import json
import threading
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jiu bu gao su ni'
app.config['UPLOAD_FOLDER'] = './'
bootstrap = Bootstrap(app)
manager = Manager(app)


@app.route('/sjkg/card')
def card():
    return render_template("card/cardbase.html")


@app.route('/sjkg/control', methods=['GET', 'POST'])
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


@app.route('/sjkg/control/relation/delete', methods=['GET'])
def control_relation_delete():
    subject = request.args.get("subject").encode("utf-8")
    object = request.args.get("object").encode("utf-8")
    predicate = request.args.get("predicate").encode("utf-8")
    print subject, object, predicate

    result = False

    if subject and object and predicate:
        cayley_util = CayleyUtil()
        result = cayley_util.delete_quads_triple(subject, predicate, object)
    return json.dumps({"result": result})


@app.route('/sjkg/entity')
def entity():
    return render_template("entity/entitybase.html")


@app.route('/sjkg/entity/<name>')
def entity_name(name):
    return render_template("entity/entityname.html", name=name)


@app.route('/sjkg/home')
@app.route('/sjkg')
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
        return None

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
    return result_rlts

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

        result_rlts = fetch_relations_by_entity(entity_name)

        if not result_rlts:
            # when result_rlts is None means no such entity found!
            app.logger.warning("No such entity: {0}".format(entity_name))
            flash("Can not find entity: {0}, Check it!".format(entity_name))
            return redirect(url_for('card'))
        else:
            return render_template("card/card.html", data={"data": result_rlts}, name=entity_name)


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
            t = threading.Thread(target=import_excel, args=(file_location,))
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




if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
