# Import the json module
import json
import urllib.request
from orator import DatabaseManager, Schema

api_endpoint = "https://api.nanoporetech.com/oracle/v1/requisitions"

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

# Create DB Manager and Schema for interacting with the MySQL
db = DatabaseManager(db_config)
schema = Schema(db)

# Retrieve data from the API endpoint
print(f"Retrieving data from {api_endpoint}")
with urllib.request.urlopen(api_endpoint) as url:
    json_data = json.loads(url.read().decode())

# Set field sizes - we know some are longer than 255
print(f"Setting field sizes")
for field in data_fields.keys():

    # Max of length of values of entries in the array
    seq = [len(x[field]) for x in json_data if x[field]]

    if max(seq) > 255:
        data_fields[field]["size"] = max(seq)
    else:
        data_fields[field]["size"] = 255


# Create a table
print("Creating DB table named 'data'")
with schema.create('data') as table:
    for field in data_fields.keys():
        if data_fields[field]["type"] == "string": table.string(field, data_fields[field]["size"]).nullable()
        if data_fields[field]["type"] == "integer": table.integer(field).nullable()
        if data_fields[field]["type"] == "datetime": table.string(field).nullable()


# Fire in the data
print("Writing records")
for record in json_data:
    db.table('data').insert(record)

print("Complete!")