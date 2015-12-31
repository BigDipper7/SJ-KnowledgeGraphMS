#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from tj.db.util.cayley_util import CayleyUtil
import xlrd
import time

import logging


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
                    logging.warning("ImportError: subject in ({},0) in sheet 0 in {} is empty, checks it".format(i,filename))
                    continue
                
                english = table.cell(i, 1).value.encode("utf-8")
                if english:
                    cayley_util.insert_quads_triple(subject, '英文名', english)
                else:
                    #just get a useful log and record it
                    logging.info("Log: subject:{} doesn't has english name".format(subject.decode('utf-8')))
                
                description = table.cell(i, 2).value.encode("utf-8")
                if description:
                    try:
                        cayley_util.insert_quads_triple(subject, 'attribute:解释', description)
                    except:
                        logging.error("Log: ImportError, except in description:{}".format(description))
                        pass
                    print subject, description
                else:
                    #just get a useful log and record it
                    logging.info("Log: description is None in subject:{}".format(subject.decode('utf-8')))
                
                tongyi = table.cell(i, 3).value.encode("utf-8")
                if tongyi:
                    tongyis = tongyi.split("/")
                    entityMap[subject] = tongyis
                    for word in tongyis:
                        if description:
                            try:
                                cayley_util.insert_quads_triple(word, 'attribute:解释', description)
                            except:
                                logging.error("Log: ImportError, except in tongyi:{} with description:{}".format(tongyi, description))
                                pass
    
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
                entity2 = entity2.replace("。", "")
                print entity2.decode("utf-8")
                
                if entity1 and relation and entity2:
                    try:
                        cayley_util.insert_quads_triple(entity1, relation, entity2)
                    except:
                        logging.error("Log: ImportError - Exception occurs in here Sheet 2 line id:<{}> with traid:<{},{},{}>".format(i, entity1, relation, entity2))
                        pass
                else:
                    logging.error("Something Error In Sheet 2 line id:<{}> with traid:<{},{},{}>".format(i, entity1, relation, entity2))
