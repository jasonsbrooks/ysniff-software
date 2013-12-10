import boto.dynamodb

dynamoconn = boto.dynamodb.connect_to_region('us-east-1')

table_schema_macs = dynamoconn.create_schema(hash_key_name='MAC',hash_key_proto_value=str)
table_schema_ips = dynamoconn.create_schema(hash_key_name='LOCATION',hash_key_proto_value=str)
dynamoconn.create_table(name='prod-ysniff',schema=table_schema_macs,read_units=5,write_units=40)
dynamoconn.create_table(name='prod-ysniff-ips',schema=table_schema_ips,read_units=4,write_units=1)

