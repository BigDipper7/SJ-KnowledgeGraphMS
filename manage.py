# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request
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


@app.route('/sjkg')
def home():
    return redirect(url_for("hehe"))

@app.route('/sjkg/home')
def hehe():
    return render_template("home.html")

def haha(name):
    names = []
    cayley_util = CayleyUtil()
    direct_names = cayley_util.find_relations_from_node(name)
    print direct_names
    print type(direct_names)
    for direct_name in direct_names:
        if not direct_name['relation'].startswith("attribute:"):
            continue
        predicate = direct_name['relation'].replace("attribute:", "").split("/")
        p_len = len(predicate)
        name_hehe = predicate[p_len - 1]

        names.append({"name": name_hehe, "hehe": direct_name['target'], "level": (p_len - 1) * 50})
    return names

@app.route('/sjkg/submitCard', methods=['POST', 'GET'])
def submitCard():
    if request.method == "POST":
        name = request.form["hehe"].encode("utf-8")
        card_hehe = haha(request.form["hehe"].encode("utf-8"))
        return render_template("card/card.html", data={"data": card_hehe}, name=name)


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

