#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from webapp.businesslogic.db.util.cayley_util import CayleyUtil
import xlrd
import time

import logging
from webapp import app


def import_excel(filename):
    cayley_util = CayleyUtil()
    data = xlrd.open_workbook(filename)
    entities = []
    entityMap = {}
    table = data.sheet_by_index(0)
    if table:
        nrows = table.nrows
        ncols = table.ncols
        if nrows > 1:
            for i in range(nrows - 1):
                subject = table.cell(i + 1, 0).value.encode("utf-8")
                if not subject:
                    continue
                english = table.cell(i + 1, 1).value.encode("utf-8")
                if english:
                    cayley_util.insert_quads_triple(subject, '英文名', english)
                description = table.cell(i + 1, 2).value.encode("utf-8")
                if description:
                    try:
                        cayley_util.insert_quads_triple(subject, 'attribute:解释', description)
                    except:
                        pass
                    print subject, description
                tongyi = table.cell(i + 1, 3).value.encode("utf-8")
                if tongyi:
                    tongyis = tongyi.split("/")
                    entityMap[subject] = tongyis
                    for word in tongyis:
                        if description:
                            try:
                                cayley_util.insert_quads_triple(word, 'attribute:解释', description)
                            except:
                                pass
    table = data.sheet_by_index(1)
    if table:
        nrows = table.nrows
        ncols = table.ncols
        if nrows > 1:
            for i in range(nrows - 1):
                entity1 = table.cell(i + 1, 0).value.encode("utf-8")
                relation = table.cell(i + 1,1).value.encode("utf-8")
                entity2 = table.cell(i+1,2).value.encode("utf-8")
                relation = relation.replace("属性：", "attribute:")
                entity2 = entity2.replace("。", "")
                print entity2
                if entity1 and relation and entity2:
                    try:
                        cayley_util.insert_quads_triple(entity1, relation, entity2)
                    except:
                        pass




def import_excel_new_version(filename):
    #const variable to change header height
    CONST_OFFSET_HEADER_LEN = 1

    cayley_util = CayleyUtil()
    data = xlrd.open_workbook(filename)
    entities = []
    entityMap = {}

    #概念表
    table = data.sheet_by_index(0)
    if table:
        nrows = table.nrows
        ncols = table.ncols
        if nrows > CONST_OFFSET_HEADER_LEN:
            for i in range(CONST_OFFSET_HEADER_LEN, nrows):
                subject = table.cell(i, 0).value.encode("utf-8")
                if not subject:
                    #just get a critical log and record it
                    app.logger.warning("[ImportError] : subject in cell({},0) in sheet 0 in file: \n-- {} is empty, checks it".format(i,filename))
                    continue
                english = table.cell(i, 1).value.encode("utf-8")
                description = table.cell(i, 2).value.encode("utf-8")
                # print 'raw english is', english
                # english = english.encode("utf-8")
                # print 'encode with utf-8', english
                # english = english.encode('string-escape')
                # print 'encode with string-escape', english

                # english = english.replace('\n','\\n')

                # subject, english, description = _str_pre_process(subject, english, description)
                if english:
                    try:
                        cayley_util.insert_quads_triple(subject, '英文名', english)
                        app.logger.info("[Success] : insert Success with traid <{};\n{};\n{};>".format(subject.decode('utf-8'), '英文名', english.decode('utf-8')))
                    except Exception as e:
                        app.logger.error("[ImportError] : Exception in english:{}".format(english.decode('utf-8')))
                        raise
                else:
                    #just get a useful log and record it
                    app.logger.warning("[ImportError] : subject:{} doesn't has english name".format(subject.decode('utf-8')))

                if description:
                    try:
                        cayley_util.insert_quads_triple(subject, 'attribute:解释', description)
                        app.logger.info("[Success] : insert Success with traid <{};\n{};\n{};>".format(subject.decode('utf-8'), 'attribute:解释', description.decode('utf-8')))
                    except:
                        app.logger.error("[ImportError] : Exception in description:{}".format(description.decode('utf-8')))
                        raise
                    # print subject, description
                else:
                    #just get a useful log and record it
                    app.logger.warning("[ImportError] : description is None in subject:{}".format(subject.decode('utf-8')))

                tongyi = table.cell(i, 3).value.encode("utf-8")
                if tongyi:
                    tongyis = tongyi.split("/")
                    entityMap[subject] = tongyis
                    for word in tongyis:
                        if description:
                            try:
                                cayley_util.insert_quads_triple(word, 'attribute:解释', description)
                                app.logger.info("[Success] : insert Success with traid <{};\n{};\n{};>".format(word.decode('utf-8'), 'attribute:解释', description.decode('utf-8')))
                            except:
                                app.logger.error("[Log] : ImportError, except in tongyi:{} with description:{}".format(tongyi.decode('utf-8'), description.decode('utf-8')))
                                raise
                        else:
                            #just get a useful log and record it
                            app.logger.warning("[ImportError] : description is None in subject:{} of tongyis".format(subject.decode('utf-8')))

    #TODO： 仍然存在的问题是如何确定很多关系，就是比如说很多页同时存在的情况，同时mongodb还要加上一个词条，可以进行处理
    #概念关系表
    table = data.sheet_by_index(1)
    if table:
        nrows = table.nrows
        ncols = table.ncols
        if nrows > CONST_OFFSET_HEADER_LEN:
            for i in range(CONST_OFFSET_HEADER_LEN, nrows):
                entity1 = table.cell(i, 0).value.encode("utf-8")
                relation = table.cell(i, 1).value.encode("utf-8")
                entity2 = str(table.cell(i, 2).value).encode("utf-8")

                #pre process of the strings
                #if exists this string "属性：" "属性:", replace it with "attribute:"
                relation = relation.replace("属性：", "attribute:")
                relation = relation.replace("属性:", "attribute:")

                #i really seems not understand why we use this. replace "。"?
                # entity2 = entity2.replace("。", "")
                if '\r\n' in entity2:
                    app.logger.info("[Log] : '\\r\\n' exists")
                elif '\n' in entity2:
                    app.logger.info("[Log] : '\\n' exists")
                else:
                    app.logger.info("[Log] : Nothing exists")
                # entity2 = entity2.replace("\n"," || ")
                entity2 = entity2.replace("\n","\\n")
                # print entity2.decode("utf-8")

                app.logger.info("[Log] : traid after process in --- sheet 1, line id: {} --- :\n\t< {}; {}; {} >".format(i, entity1, relation, entity2))

                if entity1 and relation and entity2:
                    try:
                        cayley_util.insert_quads_triple(entity1, relation, entity2)
                    except:
                        app.logger.error("[ImportError] :  - Exception occurs in here  --- Sheet 1 line id: {} --- :\n\twith traid:<{},{},{}>".format(i, entity1, relation, entity2))
                        app.logger.error("[Error] : Exception occurs in sheet 2 line_id {}  with Exception:{}".format(i, sys.exc_info()[0]))
                        raise
                else:
                    app.logger.error("Something Error In --- Sheet 1 line id: {} --- :\n\twith traid:<{},{},{}>\nMay exists None Type data! Forbbiden".format(i, entity1, relation, entity2))

def _str_pre_process(*args, **kwargs):
    result = []
    for arg in args:
        arg = arg.replace('\n','\\n')
        result.append(arg)
    return result[0] if len(result)<=1 else result
