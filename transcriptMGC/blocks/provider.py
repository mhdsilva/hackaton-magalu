class ProviderTransformer:
    def __init__(self, aws_provider_config):
        self.aws_provider_config = aws_provider_config
        self.unmapped_configs = []

    def transform(self):
        mgc_provider_config = {
            'mgc': {
                'api_key': '${var.api_key}',
                'region': '${var.region}'
            }
        }

        aws_config = self.aws_provider_config.get('aws', {})

        aws_region = aws_config.get('region')
        if aws_region:
            aws_to_mgc_region_map = {
                'us-east-1': 'br-se1',
                'us-west-1': 'br-ne1',
            }
            mgc_region = aws_to_mgc_region_map.get(aws_region)
            if mgc_region:
                mgc_provider_config['mgc']['region'] = mgc_region
            else:
                print(f"A região '{aws_region}' não tem um equivalente na Magalu Cloud. Usando a região padrão.")
                self.unmapped_configs.append('region')
        else:
            print("Nenhuma região especificada no provedor AWS. Usando a região padrão.")

        if 'access_key' in aws_config or 'secret_key' in aws_config:
            print("As configurações 'access_key' e 'secret_key' não existe naMagalu Cloud e serão ignoradas.")
            self.unmapped_configs.extend(['access_key', 'secret_key'])

        if 'profile' in aws_config:
            print("A configuração 'profile' não existe na Magalu Cloud e será ignorada.")
            self.unmapped_configs.append('profile')

        if 'assume_role' in aws_config:
            print("A configuração 'assume_role' não existe na Magalu Cloud e será ignorada.")
            self.unmapped_configs.append('assume_role')

        if 'shared_credentials_file' in aws_config:
            print("A configuração 'shared_credentials_file' não existe na Magalu Cloud e será ignorada.")
            self.unmapped_configs.append('shared_credentials_file')

        if 'max_retries' in aws_config:
            print("A configuração 'max_retries' não existe na Magalu Cloud e será ignorada.")
            self.unmapped_configs.append('max_retries')

        for key in aws_config.keys():
            if key not in ['region', 'api_key']:
                if key not in self.unmapped_configs:
                    print(f"A configuração '{key}' não existe na Magalu Cloud e será ignorada.")
                    self.unmapped_configs.append(key)

        return mgc_provider_config
