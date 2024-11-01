import os

from transcriptMGC.tffile import TerraformInstance

def iterar_tfs(path):
    diretorio = path

    if not os.path.isdir(diretorio):
        print(f"O diretório '{diretorio}' não existe.")
        return

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.tf'):
            caminho_completo = os.path.join(diretorio, arquivo)
            print(caminho_completo)
            infra = TerraformInstance(caminho_completo)
            diretorio_pai = os.path.dirname(diretorio)
            print('\n\n\n')
            infra.dump_tf(diretorio_pai+'//paraMagalu//'+arquivo+'.json')

path = input('Qual pasta está sua infra ?\n')
iterar_tfs(path)

#x = TerraformInstance('examples/main.tf')

#x.print_provider()
#x.print_resources()
#x.print_variables()
#x.print_datas()
#x.print_outputs()

#print('\n\n\n')
#x.dump_tf('paraMagalu/main.tf.json')