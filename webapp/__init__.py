#encoding: utf-8
__author__ = 'BigDipper7'


from flask import Flask
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

# is_login = str('is_login')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jiu bu gao su ni'
# TODO: 注意的是这里的“.”指的是当前路径，而这里的当前路径并不是init_py的路径，
# 而是应该是运行的程序“start-server.py”所在的路径，
# 因为整个程序的调用顺序是start-server -> webapp.__init__.app -> import webapp.views.views -> import dependencies
app.config['UPLOAD_FOLDER'] = './webapp/FileUpload'
bootstrap = Bootstrap(app)
manager = Manager(app)

# seems circular import
#import webapp.views.views

#
# #----------------------------------------
# # main func snippet
# #----------------------------------------
# if __name__ == '__main__':
#     app.run(debug=True, port=5000, host="0.0.0.0")
