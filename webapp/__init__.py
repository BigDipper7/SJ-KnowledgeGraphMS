__author__ = 'BigDipper7'

# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

# is_login = str('is_login')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jiu bu gao su ni'
app.config['UPLOAD_FOLDER'] = './FileUpload'
bootstrap = Bootstrap(app)
manager = Manager(app)

# seems circular import
import webapp.views.views

#
# #----------------------------------------
# # main func snippet
# #----------------------------------------
# if __name__ == '__main__':
#     app.run(debug=True, port=5000, host="0.0.0.0")
