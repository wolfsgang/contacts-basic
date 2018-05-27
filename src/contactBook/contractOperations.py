from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from models import index_properties
import hashlib
from config import app_config

from elasticsearch_dsl import connections

s = Search(using=Elasticsearch(app_config.ELASTICSEARCH_URL))
es = Elasticsearch(hosts=app_config.ELASTICSEARCH_URL)
curr_index = "contactBook"
curr_doc_type = "doc"


class ContractOperations:
    def addContact(self, new_contact_body):
        new_doc = {}

        if new_contact_body["email"] is None:
            return "Email Cannot be null"

        new_doc_id = hashlib.sha1(new_doc["email"])

        if es.get(index=curr_index, doc_type=curr_doc_type, id=new_doc_id):
            return "Entry already exists with this emailId"

        for key in index_properties:

            i_key = index_properties[key]
            c_key = new_contact_body[key]

            if i_key in "name":
                if c_key is None or c_key["first"] is None:
                    return pif, ": cannot be null, at least first name is needed"
                for pif in c_key:
                    new_doc[key[pif]] = c_key[pif]

            new_doc[key] = c_key

        new_doc_id = hashlib.sha1(new_doc["email"])
        res = es.index(index=curr_index, doc_type=curr_doc_type, id=new_doc_id, body=new_doc)
        return res['result']

    def editContact(self, email_key, req_data):
        return

    def deleteContact(self, email_key):
        if email_key is None:
            return "Empty request, nothing to be deleted"
        else:
            del_id = hashlib.sha1(email_key)
            res = es.delete(index=curr_index, doc_type=curr_doc_type, id=del_id)
            return res['result']
        
    def searchContact(self, keyword, filters):
        return
