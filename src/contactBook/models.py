index_properties = {
    "countryCode": {
        "type": "text",
        "constraint": "default"
    },
    "email": {
        "type": "text",
        "constraint" : "notNull"
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

