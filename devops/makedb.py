import boto.dynamodb

dynamoconn = boto.dynamodb.connect_to_region('us-east-1')
sdbconn = boto.connect_sdb()

table_schema_macs = dynamoconn.create_schema(hash_key_name='MAC',hash_key_proto_value=str)

#dynamoconn.create_table(name='dev-ysniff',schema=table_schema,read_units=5,write_units=40)

sdb.create_domain('dev-pi-locations')
