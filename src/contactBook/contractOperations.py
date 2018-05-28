from elasticsearch import Elasticsearch, ElasticsearchException
from elasticsearch_dsl import Search
from models import index_properties
import hashlib
from config import app_config
from time import time
from elasticsearch_dsl.query import MultiMatch, Match, Q
import json

es = Elasticsearch(hosts=app_config.ELASTICSEARCH_URL)
curr_index = "contact_book"
curr_doc_type = "doc"


class ContractOperations:
    def c_add(self, req_body):
        """add a new contact"""

        new_doc = {}

        if 'email' not in req_body:
            return "Email Cannot be null"
        # email id is primary key here using its hash as its id
        new_doc_id = hashlib.sha1(req_body["email"]).hexdigest()
        try:
            es.get(index=curr_index, doc_type=curr_doc_type, id=new_doc_id)
            return "This email already exists"
        except ElasticsearchException as es1:
            pass

        # only keys defined in properties will be accepted
        for key in index_properties:

            if key in "name":
                if key not in req_body or "first" not in req_body[key]:
                    return key, ": cannot be null, at least first name is needed"
                new_doc[key] = {}
                for skey in index_properties[key]:
                    if skey in req_body[key]:
                        new_doc[key][skey] = req_body[key][skey]

            if key not in req_body:
                pass
            new_doc[key] = req_body[key]

        # epoch time in millis
        new_doc["modified_time"] = int(round(time() * 1000))
        new_doc_id = hashlib.sha1(new_doc["email"]).hexdigest()
        res = es.index(index=curr_index, doc_type=curr_doc_type, id=new_doc_id, body=new_doc)
        return res['result'], new_doc_id

    def c_edit(self, email_key, req_data):
        """edit by email id key"""

        edit_doc = {}
        info = ""
        if email_key is None:
            return "Email id is needed as a unique identifier for edit"
        edit_doc_id = hashlib.sha1(email_key).hexdigest()

        try:
            res = es.get(index=curr_index, doc_type=curr_doc_type, id=edit_doc_id)
        except ElasticsearchException as es1:
            return "No entry with this email id"

        for key in res['_source']:
            edit_doc[key] = res['_source'][key]

        for key in index_properties:
            if key in req_data:
                edit_doc[key] = req_data[key]

        if "email" in req_data:
            info = "email cannot be updated, rest fields will be"
            edit_doc["email"] = email_key

        edit_doc["modified_time"] = int(round(time() * 1000))
        res = es.index(index=curr_index, doc_type=curr_doc_type, id=edit_doc_id, body=edit_doc)
        return res['result'], info

    def c_delete(self, email_key):
        """delete by email id"""

        if email_key is None:
            return "Empty request, nothing to be deleted"
        else:
            del_id = hashlib.sha1(email_key).hexdigest()
            res = es.delete(index=curr_index, doc_type=curr_doc_type, id=del_id)
            return res['result'], del_id

    def c_search(self, keyword, filters):
        """search by name, or email"""

        s = Search(using=es)
        if keyword is None:
            return "Empty Keyword"
        # default pagination size
        size = 10
        if 'size' in filters:
            size = filters['size']
        page = filters['page'] if 'page' in filters else 0
        s.query = Q("multi_match", query=keyword, fields=['email', 'name.first', 'name.last'])
        s = s[page * size:size]
        response = s.execute()

        json_data = [{"Total hits": response.hits.total}]
        for hit in response:
            one = {}
            for det in index_properties:
                if det in hit:
                    if det in "name":
                        one[det] = {}
                        if "first" in hit[det]:
                            one[det]["first"] = hit[det]["first"]
                        if "last" in hit[det]:
                            one[det]["last"] = hit[det]["last"]
                    else:
                        one[det] = hit[det]
            one['id'] = hit.meta.id
            json_data.append(one)
        return json.dumps(json_data)
