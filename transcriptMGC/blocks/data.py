class DataTransformer:
    def __init__(self, aws_data_source):
        self.aws_data_source = aws_data_source
        self.unmapped_attributes = []

    def transform(self):
        transformed_data_sources = []
        data_source_type = list(self.aws_data_source.keys())[0]
        data_source_configs = self.aws_data_source[data_source_type]

        for data_source_name, attributes in data_source_configs.items():
            if data_source_type == 'aws_instance':
                transformed_data = self.transform_aws_instance(data_source_name, attributes)
            elif data_source_type == 'aws_s3_bucket':
                transformed_data = self.transform_aws_s3_bucket(data_source_name, attributes)
            else:
                print(f"Tipo de data source '{data_source_type}' não é suportado para transformação.")
                continue
            transformed_data_sources.append(transformed_data)
        
        return transformed_data_sources


    def transform_aws_instance(self, data_source_name, attributes):
        mgc_data_source = {
            'mgc_virtual_machine_instances': {
                data_source_name: {
                    'id': attributes.get('id', '')
                }
            }
        }

        known_attributes = {'id'}
        extra_attributes = set(attributes.keys()) - known_attributes
        if extra_attributes:
            print(f"A data source AWS '{data_source_name}' possui atributos que não são necessários para a MGC e serão ignorados: {extra_attributes}")
            self.unmapped_attributes.extend(extra_attributes)

        return mgc_data_source

    def transform_aws_s3_bucket(self, data_source_name, attributes):
        mgc_data_source = {
            'mgc_object_storage_buckets': {
                data_source_name: {
                    'bucket': attributes.get('bucket', data_source_name),
                    'enable_versioning': attributes.get('versioning', {}).get('enabled', False)
                }
            }
        }

        acl = attributes.get('acl', 'private')
        acl_mapping = {
            'private': {'private': True},
            'public-read': {'public_read': True},
            'public-read-write': {'public_read_write': True},
            'authenticated-read': {'authenticated_read': True}
        }
        mgc_acl = acl_mapping.get(acl)
        if mgc_acl:
            mgc_data_source['mgc_object_storage_buckets'][data_source_name].update(mgc_acl)
        else:
            print(f"ACL '{acl}' em aws_s3_bucket '{data_source_name}' não é suportada e será definida como 'private' por padrão.")
            self.unmapped_attributes.append('acl')

        known_attributes = {'bucket', 'acl', 'versioning'}
        extra_attributes = set(attributes.keys()) - known_attributes
        if extra_attributes:
            print(f"A data source AWS '{data_source_name}' possui atributos que não são necessários para a MGC e serão ignorados: {extra_attributes}")
            self.unmapped_attributes.extend(extra_attributes)

        return mgc_data_source