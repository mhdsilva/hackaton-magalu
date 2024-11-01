class VariableTransformer:
    def __init__(self, aws_variables):
        self.aws_variables = aws_variables
        self.unmapped_variables = []

    def transform(self):
        # Definição das variáveis da Magalu Cloud
        mgc_variables = [
            {
                "mgc_api_key": {
                    "description": "API key para autenticação."
                }
            },
            {
                "mgc_obj_key_id": {
                    "description": "Key ID para acessar o produto de Object Storage."
                }
            },
            {
                "mgc_obj_key_secret": {
                    "description": "Secret da key para acessar o produto de Object Storage."
                }
            },
            {
                "mgc_region": {
                    "description": "Especifica a região onde os recursos serão criados e gerenciados.",
                    "default": "br-se1"
                }
            },
            {
                "mgc_env": {
                    "description": "Define o ambiente operacional.",
                    "default": "prod"
                }
            }
        ]

        # Mapeamento de variáveis AWS para MGC, se aplicável
        aws_to_mgc_variable_map = {
            # Adicione mapeamentos se houver variáveis AWS que possam ser mapeadas para MGC
            # Exemplo:
            # "aws_access_key": "mgc_api_key",
            # "aws_secret_key": "mgc_obj_key_secret"
        }

        for aws_var, mgc_var in aws_to_mgc_variable_map.items():
            if aws_var in self.aws_variables:
                mgc_variables.append({
                    mgc_var: self.aws_variables[aws_var]
                })
                del self.aws_variables[aws_var]

        for var in self.aws_variables:
            print(f"A variável AWS '{var}' não possui mapeamento para a Magalu Cloud e será ignorada.")
            self.unmapped_variables.append(var)

        return mgc_variables