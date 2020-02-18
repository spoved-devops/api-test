# Import the json module
import json
from orator import DatabaseManager, Schema

from pprint import pprint


data_fields = {"city": {"type": "string"},
        "country": {"type": "string"},
        "description": {"type": "string"},
        "guid": {"type": "string"},
        "job_family": {"type": "string"},
        "link": {"type": "string"},
        "location": {"type": "string"},
        "pub_date": {"type": "datetime"},
        "rid": {"type": "integer"},
        "role_description": {"type": "string"},
        "title": {"type": "string"},
}

db_config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'apitest',
        'user': 'test-user',
        'password': 'test-pass',
        'prefix': ''
    }
}

db = DatabaseManager(db_config)
schema = Schema(db)

# TODO: Spin up docker container here
# sudo docker run -d -p 3306:3306 -e MYSQL_DATABASE=apitest -e MYSQL_USER=test-user -e MYSQL_PASSWORD=test-pass mysql/mysql-server --default_authentication_plugin=mysql_native_password


# TODO: Replace reading file with pulling from API endpoint

# Load the file 
json_data = json.loads(open('data.json').read())
 
# Set field sizes
for field in data_fields.keys():

    # Max of length of values of entries in the array
    print(field)
    seq = [len(x[field]) for x in json_data if x[field]]

    if max(seq) > 255:
        data_fields[field]["size"] = max(seq)
    else:
        data_fields[field]["size"] = 255

    
    print(f"  Max length: {data_fields[field]['size']}")



# Create a table
with schema.create('data') as table:
    for field in data_fields.keys():
        if data_fields[field]["type"] == "string": table.string(field, data_fields[field]["size"]).nullable()
        if data_fields[field]["type"] == "integer": table.integer(field).nullable()
        if data_fields[field]["type"] == "datetime": table.string(field).nullable()


# Fire in the data
for record in json_data:
    db.table('data').insert(record)
