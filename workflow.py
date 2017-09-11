import molflow.definitions as defs

workflow = defs.WorkflowDefinition('convert')
__workflow__ = workflow

# Inputs
data = workflow.add_input('input_data',
                          description='Data to convert',
                          type=str)
infmt = workflow.add_input('input_format',
                           description='Input format (see `molflow '
                                       'convert --help for accepted formats)',
                           type=str)
outfmt = workflow.add_input('output_format',
                            description='Output format (see `molflow '
                                        'convert --help for accepted formats)',
                            type=str)

# Functions
convert = defs.Function('convert',
                        sourcefile='./source.py')

# Steps
output = convert(data, outfmt, infmt)


# Outputs
workflow.set_output(output,
                    'result',
                    'Output data (as a string)')

