import hcl2
import json

from transcriptMGC.blocks.provider import ProviderTransformer
from transcriptMGC.blocks.resource import ResourceTransformer
from transcriptMGC.blocks.variable import VariableTransformer
from transcriptMGC.blocks.data import DataTransformer
from transcriptMGC.blocks.output import OutputTransformer

class TerraformInstance():
    # --------------- CREATE ----------------
    def __init__(self, path:str):
        self.provider = None
        self.resources = []
        self.datas = []
        self.variables = None
        self.outputs = []

        with open(path, 'r') as file:
            self.instance = hcl2.load(file)

        self._parse_blocks()
    def _parse_blocks(self):
        relations = {
            'provider': self._parse_provider,
            'resource': self._parse_resouce,
            'data': self._parse_data,
            'variable': self._parse_variable,
            'output': self._parse_output
        }

        for key in self.instance.keys():
            if key in relations:
                relations[key]()

            else:
                raise f'Ainda não existe suporte para {key}.'
    def _parse_provider(self):
        provider_list = self.instance['provider']
        objProvider = ProviderTransformer(provider_list[0])
        self.provider = objProvider.transform()
    def _parse_resouce(self):
        resource_list = self.instance['resource']
        for resource in resource_list:
            objResource = ResourceTransformer(resource)
            self.resources.append(objResource.transform())
    def _parse_data(self):
        data_list = self.instance['data']
        for data in data_list:
            objData = DataTransformer(data)
            self.datas.append(objData.transform())
    def _parse_variable(self):
        variable_list = self.instance['variable']
        objVariable = VariableTransformer(variable_list)
        self.variables = objVariable.transform()
    def _parse_output(self):
        output_list = self.instance['output']
        for output in output_list:
            objOutput = OutputTransformer(output)
            self.outputs.append(objOutput.transform())

    # --------------- PRINTS ----------------
    def print_provider(self):
        print(f'\nProvider: {self.provider}')

    def print_resources(self):
        print(f'\nResource amount: {len(self.resources)}')
        for i, r in enumerate(self.resources):
            print(f'Resource {i}: {r}')

    def print_variables(self):
        print(f'\nVariable amount: {len(self.variables)}')
        for i, v in enumerate(self.variables):
            print(f'Variable {i}: {v}')

    def print_datas(self):
        print(f'\nData amount: {len(self.datas)}')
        for i, d in enumerate(self.datas):
            print(f'Data {i}: {d}')

    def print_outputs(self):
        print(f'\nOutput amount: {len(self.outputs)}')
        for i, o in enumerate(self.outputs):
            print(f'Data {i}: {o}')

    # --------------- OUTPUT ----------------
    def _config_output(self):
        output_config = {}
        if self.provider:
            output_config['provider'] = self.provider

        if self.resources:
            output_config['resource'] = {}
            for r in self.resources:
                for k, i in r.items():
                    output_config['resource'][k] = i

        if self.outputs:
            output_config['output'] = {}
            for o in self.outputs:
                if o:
                    for k, i in o.items():
                        output_config['output'][k] = i

        if self.variables:
            output_config['variable'] = {}
            for v in self.variables:
                for k, i in v.items():
                    output_config['variable'][k] = i

        if self.datas:
            output_config['output'] = {}
            for d in self.datas:
                for k, i in d.items():
                    output_config['output'][k] = i

        return output_config

    def dump_tf(self, path):
        with open(path, 'w') as f:

            if self.provider:
                json.dump(self._config_output(), f, indent=4)