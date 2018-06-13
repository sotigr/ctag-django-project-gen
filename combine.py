#DEPENDENCIES

#   pip install PyExecJS
#   npm install babel-core
#   npm babel-preset-es2015
#   npm babel-preset-stage-2

import os
import sys
import execjs 

INDIR = sys.argv[1]
OUTDIR = sys.argv[2]
out_str = ""
for folder, subs, files in os.walk(INDIR):
    for filename in files:
        with open(os.path.join(folder, filename), 'r') as src:
            out_str += src.read() + "\n"



here = os.path.dirname(__file__)
node_modules = os.path.abspath(os.path.join(here, './node_modules'))

class Babel:
    def __init__(self, *module_paths):
        """Constructor

        :param module_paths: Paths to node_modules
        """
        self.paths = module_paths
        # This is used to let execjs know where the
        # modules are
        self.module_append_string = '\n'.join(
            'module.paths.push("%s")\n' % p for p in self.paths
        )
        command_string = 'var babel = require("babel-core")'
        self.babel = execjs.compile(self.module_append_string + command_string)

    def transpile(self, code):
        options = {
            'presets': ['es2015']
        }

        transpiled_code = self.babel.call(
            'babel.transform', code, options
        )['code']

        return transpiled_code

babel = Babel(node_modules) 

original_source = out_str

if os.path.isfile(OUTDIR):
    os.remove(OUTDIR)

with open(OUTDIR, 'a') as out:
    out.write(babel.transpile(original_source))