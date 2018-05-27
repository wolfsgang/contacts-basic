index_properties = {
    "countryCode": {
        "type": "text",
        "constraint": "default"
    },
    "email": {
        "type": "text",
        "constraint" : "notNull"
    },
    "modified_time": {
        "type": "date",
        "constraint": "notNull"
    },
    "name": {
            "first": {
                "type": "text",
                "constraint": "notNull"
            },
            "last": {
                "type": "text",
                "constraint" : "default"
            }
    },
    "phoneNumber": {
        "type": "long",
        "constraint": "default"
    }
}

for k in index_properties:
    print index_properties[k], type(index_properties[k])
    if len(index_properties[k])>1:
        print 1