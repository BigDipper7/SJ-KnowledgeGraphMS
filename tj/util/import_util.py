#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from tj.db.util.cayley_util import CayleyUtil
import xlrd
import time


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
