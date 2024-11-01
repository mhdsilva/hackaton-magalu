class VariableTransformer:
    def __init__(self, aws_variables):
        self.aws_variables = aws_variables
        self.unmapped_variables = []

    def transform(self):
        mgc_variables = {
            "mgc_api_key": {
                "description": "API key para autenticação."
            },
            "mgc_obj_key_id": {
                "description": "Key ID para acessar o produto de Object Storage."
            },
            "mgc_obj_key_secret": {
                "description": "Secret da key para acessar o produto de Object Storage."
            },
            "mgc_region": {
                "description": "Especifica a região onde os recursos serão criados e gerenciados.",
                "default": "br-se1"
            },
            "mgc_env": {
                "description": "Define o ambiente operacional.",
                "default": "prod"
            }
        }

        transformed_variables = mgc_variables.copy()

        # Mapeamento de variáveis AWS para MGC, se aplicável
        # Atualmente, não há mapeamento direto, mas pode ser adicionado conforme necessário
        aws_to_mgc_variable_map = {
            # Exemplo:
            # "aws_access_key": "mgc_api_key"
        }

        for aws_var, mgc_var in aws_to_mgc_variable_map.items():
            if aws_var in self.aws_variables:
                transformed_variables[mgc_var] = self.aws_variables[aws_var]
                del self.aws_variables[aws_var]

        for var in self.aws_variables:
            print(f"A variável AWS '{var}' não possui mapeamento para a Magalu Cloud e será ignorada.")
            self.unmapped_variables.append(var)

        return transformed_variables
