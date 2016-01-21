#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib2
import json
import logging
from webapp import app

# 利用RESTful API的Cayley工具类
class CayleyUtil(object):

    # Gremlin Query
    query_gremlin = "/api/v1/query/gremlin"
    query_shape_gremlin = "/api/v1/shape/gremlin"

    # MQL Query
    query_mql = "/api/v1/query/mql"
    query_shape_mql = "/api/v1/shape/mql"

    # Write Commands
    write = "/api/v1/write"
    delete = "/api/v1/delete"

    def __init__(self, host="localhost", port="64210"):
        ''' just init self.__url_prefix whit host and port
        '''
        self.__url_prefix = "http://" + host + ":" + port

    @staticmethod
    def __curl_cayley(url, values):
        request = urllib2.Request(url, values)
        response = urllib2.urlopen(request)
        return response.read()

    def query(self, values, gremlin=True):
        url = self.__url_prefix
        url += self.query_gremlin if gremlin else self.query_mql
        return CayleyUtil.__curl_cayley(url, values)

    def query_shape(self, values, mql=False):
        url = self.__url_prefix
        url += self.query_shape_mql if mql else self.query_shape_gremlin
        return CayleyUtil.__curl_cayley(url, values)

    def insert_quads(self, values):
        url = self.__url_prefix + self.write
        result = CayleyUtil.__curl_cayley(url, values)
        data = json.loads(result)
        return False if data.get("error", None) else True

    def insert_quads_triple(self, temp_subject, temp_predicate, temp_object):
        # insert_json = """
        # [{
        #     "subject": \"%s\",
        #     "predicate": \"%s\",
        #     "object": \"%s\"
        # }]""" % (temp_subject, temp_predicate, temp_object)
        dict_insert_data = {}
        dict_insert_data['subject'] = temp_subject
        dict_insert_data['predicate'] = temp_predicate
        dict_insert_data['object'] = temp_object

        insert_json = json.dumps(dict_insert_data)

        # insert_json = """
        # [{
        #     "subject": \"%s\",
        #     "predicate": \"%s\",
        #     "object": \"%s\"
        # }]""" % (temp_subject, temp_predicate, temp_object)

        print 'insert_json is \n\n',insert_json

    	# just for logging and for record
    	app.logger.info("Log: Insert - Ready to insert succeed, triad:< {}, {}, {} >".format(temp_subject.decode("utf-8"), temp_predicate.decode("utf-8"), temp_object.decode("utf-8")))

        return self.insert_quads(insert_json)

    def delete_quads(self, values):
        url = self.__url_prefix + self.delete
        result = CayleyUtil.__curl_cayley(url, values)
        data = json.loads(result)
        return False if data.get("error", None) else True

    def delete_quads_triple(self, temp_subject, temp_predicate, temp_object):
        delete_json = """
        [{
            "subject": \"%s\",
            "predicate": \"%s\",
            "object": \"%s\"
        }]""" % (temp_subject, temp_predicate, temp_object)

        print 'delete_json is \n\n',delete_json

        return self.delete_quads(delete_json)

    def find_relations(self, node):
        node = node.encode("utf-8")
        gremlin_query = "g.V(\"" + node + "\").Tag(\"source\").Out(null, \"relation\").Tag(\"target\").All()"
        return self.query(gremlin_query)

    def find_relations_from_node(self, node):
        node = node.encode("utf-8")
        gremlin_query = "g.V(\"" + node + "\").Tag(\"source\").Out(null, \"relation\").Tag(\"target\").All()"
        return json.loads(self.query(gremlin_query))["result"]

    def find_all_paths(self, start, end, temp_path=[], temp_relation=[], rel=None, level=10):
        if level < 0:
            return [], []
        temp_path = temp_path + [start]
        if rel:
            temp_relation = temp_relation + [rel]
        if start == end:
            return [temp_path], [temp_relation]
        relations_from_start = self.find_relations_from_node(start)
        if relations_from_start is None:
            return [], []
        paths = []
        relations = []
        level -= 1
        for r in relations_from_start:
            if r["target"] not in temp_path:
                new_paths, new_relations = self.find_all_paths(r["target"], end, temp_path, temp_relation, r, level)
                for new_path in new_paths:
                    paths.append(new_path)
                for new_relation in new_relations:
                    relations.append(new_relation)
        return paths, relations


if __name__ == "__main__":
    cayley_util = CayleyUtil()
    # gremlin_query_test = "g.V(\"体育\").Tag(\"source\").Out(null, \"relation\").Tag(\"target\").All()"
    # print cayley_util.query(gremlin_query_test)
    #
    # gremlin_query_test = "g.V(\"体育奖项\").Tag(\"source\").Out(null, \"relation\").Tag(\"target\").All()"
    # print cayley_util.query(gremlin_query_test)

    # paths, relations = cayley_util.find_all_paths("体育", "体育组织", [], [], None, 10)
    # relations_dict = {"relations": relations}
    # print json.dumps(relations_dict)

    # results = cayley_util.find_relations_from_node("体育")
    # if results is None:
    #     exit(1)
    # for result in results:
    #     print result["source"], result["relation"], result["target"]

    # print cayley_util.insert_quads_triple("A", "B", "C")

    # mql_query_test = """
    # [{
    #     "id": "alice",
    #     "follows": "bob",
    #     "is": "cool"
    # }]"""
    # print cayley_util.query(mql_query_test, False)

    # insert_test = """
    # [{
    #     "subject": "A",
    #     "predicate": "B",
    #     "object": "C"
    # }]"""
    # print cayley_util.insert_quads(insert_test)

    # gremlin_query_test = "graph.Vertex(\"panda\").Out(\"follows\").All()"
    # print cayley_util.query(gremlin_query_test)
    #
    # delete_test = """
    # [{
    #     "subject": "panda",
    #     "predicate": "follows",
    #     "object": "bob"
    # },
    # {
    #     "subject": "panda",
    #     "predicate": "follows",
    #     "object": "alice"
    # }]"""
    # print cayley_util.delete_quads(delete_test)
    #
    # gremlin_query_test = "graph.Vertex(\"panda\").Out(\"follows\").All()"
    # print cayley_util.query(gremlin_query_test)
