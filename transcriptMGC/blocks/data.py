class DataTransformer:
    def __init__(self, aws_data_source):
        self.aws_data_source = aws_data_source
        self.unmapped_attributes = []

    def transform(self):
        if not self.aws_data_source:
            print("Nenhum data source fornecido para transformação.")
            return {}

        data_source_type = list(self.aws_data_source.keys())[0]
        data_source_content = self.aws_data_source[data_source_type]

        if data_source_type == 'aws_ami':
            return self.transform_aws_ami(data_source_content)
        elif data_source_type == 'aws_instance':
            return self.transform_aws_instance(data_source_content)
        else:
            print(f"Tipo de data source '{data_source_type}' não é suportado para transformação.")
            return {}

    def transform_aws_ami(self, data_source_content):
        mgc_data_source = {
            'data': {
                'mgc_virtual_machine_images': {}
            }
        }

        for name, attributes in data_source_content.items():
            mgc_data_source['data']['mgc_virtual_machine_images'][name] = {}
            if attributes:
                print(f"A data source AWS 'aws_ami' '{name}' possui atributos que não são necessários para a MGC e serão ignorados: {list(attributes.keys())}")
                self.unmapped_attributes.extend(attributes.keys())

        return mgc_data_source

    def transform_aws_instance(self, data_source_content):
        mgc_data_source = {
            'data': {
                'mgc_virtual_machine_instances': {}
            }
        }

        for name, attributes in data_source_content.items():
            instance_id = attributes.get('id', '')
            mgc_data_source['data']['mgc_virtual_machine_instances'][name] = {
                'id': instance_id
            }

            known_attributes = {'id'}
            extra_attributes = set(attributes.keys()) - known_attributes
            if extra_attributes:
                print(f"A data source AWS 'aws_instance' '{name}' possui atributos que não são necessários para a MGC e serão ignorados: {extra_attributes}")
                self.unmapped_attributes.extend(extra_attributes)

        return mgc_data_source