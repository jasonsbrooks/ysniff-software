import boto.dynamodb

conn = boto.dynamodb.connect_to_region('us-east-1')

table_schema = conn.create_schema(hash_key_name='MAC',hash_key_proto_value=str)

conn.create_table(name='dev-ysniff',schema=table_schema,read_units=10,write_units=10)
