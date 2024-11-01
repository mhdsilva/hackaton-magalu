from transcriptMGC.tffile import TerraformInstance

x = TerraformInstance('examples/main.tf')

#x.print_provider()
#x.print_resources()
#x.print_variables()
#x.print_datas()
x.print_outputs()

print('\n\n\n')
x.dump_tf('examples/magalumain.tf.json')
