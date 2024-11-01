class ResourceTransformer:
    def __init__(self, aws_resource):
        self.aws_resource = aws_resource
        self.unmapped_attributes = []

    def transform(self):
        transformed_resources = []
        resource_type = list(self.aws_resource.keys())[0]
        resource_configs = self.aws_resource[resource_type]
        for resource_name, attributes in resource_configs.items():
            if resource_type == 'aws_instance':
                transformed_resource = self.transform_ec2_instance(resource_name, attributes)
            elif resource_type == 'aws_s3_bucket':
                transformed_resource = self.transform_s3_bucket(resource_name, attributes)
            else:
                print(f"Tipo de recurso '{resource_type}' não é suportado para transformação.")
                continue
            transformed_resources.append(transformed_resource)
        return transformed_resources

    def transform_ec2_instance(self, resource_name, attributes):
        mgc_resource = {
            'mgc_virtual_machine_instances': {
                resource_name: {
                    'name': attributes.get('tags', {}).get('Name', resource_name),
                    'machine_type': {
                        'name': self.map_instance_type(attributes.get('instance_type'))
                    },
                    'image': {
                        'name': self.map_ami(attributes.get('ami'))
                    },
                    'ssh_key_name': attributes.get('key_name', '')
                }
            }
        }

        network = {}
        if attributes.get('associate_public_ip_address') is not None:
            network['associate_public_ip'] = attributes.get('associate_public_ip_address')
        else:
            network['associate_public_ip'] = False

        security_groups = attributes.get('vpc_security_group_ids', attributes.get('security_groups', []))
        if security_groups:
            network['interface'] = {
                'security_groups': [{'id': sg_id} for sg_id in security_groups]
            }

        if network:
            mgc_resource['mgc_virtual_machine_instances'][resource_name]['network'] = network

        known_attributes = {'ami', 'instance_type', 'key_name', 'associate_public_ip_address', 'vpc_security_group_ids', 'security_groups', 'tags'}
        extra_attributes = set(attributes.keys()) - known_attributes
        if extra_attributes:
            print(f"Atributos não mapeados em aws_instance '{resource_name}': {extra_attributes}")
            self.unmapped_attributes.extend(extra_attributes)

        return mgc_resource

    def transform_s3_bucket(self, resource_name, attributes):
        mgc_resource = {
            'mgc_object_storage_buckets': {
                resource_name: {
                    'bucket': attributes.get('bucket', resource_name),
                    'enable_versioning': attributes.get('versioning', {}).get('enabled', False)
                }
            }
        }

        # Controle de Acesso
        acl = attributes.get('acl', 'private')
        acl_mapping = {
            'private': {'private': True},
            'public-read': {'public_read': True},
            'public-read-write': {'public_read_write': True},
            'authenticated-read': {'authenticated_read': True}
        }
        mgc_acl = acl_mapping.get(acl)
        if mgc_acl:
            mgc_resource['mgc_object_storage_buckets'][resource_name].update(mgc_acl)
        else:
            print(f"ACL '{acl}' em aws_s3_bucket '{resource_name}' não é suportada e será definida como 'private' por padrão.")
            self.unmapped_attributes.append('acl')

        known_attributes = {'bucket', 'acl', 'versioning', 'tags'}
        extra_attributes = set(attributes.keys()) - known_attributes
        if extra_attributes:
            print(f"Atributos não mapeados em aws_s3_bucket '{resource_name}': {extra_attributes}")
            self.unmapped_attributes.extend(extra_attributes)

        return mgc_resource

    def map_instance_type(self, aws_instance_type):
        instance_type_mapping = {
            't2.micro': 'cloud-bs1.xsmall',
            't2.small': 'cloud-bs1.small',
            't2.medium': 'cloud-bs1.medium',
            # Adicionar outros mapeamentos conforme necessário
        }
        mgc_machine_type = instance_type_mapping.get(aws_instance_type)
        if mgc_machine_type:
            return mgc_machine_type
        else:
            print(f"Tipo de instância AWS '{aws_instance_type}' não possui um mapeamento direto. Usando 'cloud-bs1.small' como padrão.")
            self.unmapped_attributes.append('instance_type')
            return 'cloud-bs1.small'

    def map_ami(self, aws_ami):
        ami_mapping = {
            'ami-0abc12345def67890': 'cloud-ubuntu-22.04 LTS',
            # Adicionar outros mapeamentos conforme necessário
        }
        mgc_image_name = ami_mapping.get(aws_ami)
        if mgc_image_name:
            return mgc_image_name
        else:
            print(f"AMI AWS '{aws_ami}' não possui um mapeamento direto. Usando 'cloud-ubuntu-22.04 LTS' como padrão.")
            self.unmapped_attributes.append('ami')
            return 'cloud-ubuntu-22.04 LTS'
