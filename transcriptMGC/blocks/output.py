class OutputTransformer:
    def __init__(self, aws_output, resource_mapping):

        self.aws_output = aws_output
        self.resource_mapping = resource_mapping
        self.unmapped_outputs = []

    def transform(self):
        transformed_outputs = []
        for output_name, attributes in self.aws_output.items():
            transformed_output = self.transform_output(output_name, attributes)
            if transformed_output:
                transformed_outputs.append(transformed_output)
        return transformed_outputs

    def transform_output(self, output_name, attributes):
        value = attributes.get('value', '')
        transformed_value = self.map_resource_references(value)

        if transformed_value is None:
            print(f"Não foi possível transformar o valor do output '{output_name}'.")
            self.unmapped_outputs.append(output_name)
            return None

        mgc_output = {
            'output': {
                output_name: {
                    'value': transformed_value
                }
            }
        }

        return mgc_output

    def map_resource_references(self, value):
        import re

        pattern = r'aws_(\w+)\.(\w+)\.(\w+)'
        matches = re.findall(pattern, value)

        if not matches:
            print(f"Nenhuma referência de recurso AWS encontrada no valor '{value}'.")
            self.unmapped_outputs.append(value)
            return None

        transformed_value = value
        for match in matches:
            resource_type, resource_name, attribute = match
            aws_resource = f'aws_{resource_type}.{resource_name}.{attribute}'
            mgc_resource_type = self.resource_mapping.get(f'aws_{resource_type}')

            if not mgc_resource_type:
                print(f"Tipo de recurso AWS '{resource_type}' não possui mapeamento para MGC.")
                self.unmapped_outputs.append(aws_resource)
                continue

            mgc_resource = f'{mgc_resource_type}.{resource_name}.{attribute}'
            transformed_value = transformed_value.replace(aws_resource, mgc_resource)

        return transformed_value