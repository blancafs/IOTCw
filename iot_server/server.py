# Imports
import os
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

# dependencies can be any iterable with strings,
# e.g. file line-by-line iterator
dependencies = [
  'Flask>=0.9', 'scipy', 'pandas', 'sklearn', 'numpy','matplotlib'
]

# Check for dependencies
try:
# here, if a dependency is not met, a DistributionNotFound or VersionConflict
# exception is thrown.
    pkg_resources.require(dependencies)
    print('Dependencies Met')
except:
    print('Some dependencies not found, installing now ...')
    d = ' '.join(dependencies)
    os.system('pip3 install '+ d)

# Custom imports
from engine import Engine

# Web imports
from flask import Flask, render_template, flash, request, redirect, url_for, session

# Initialize serving configuration
app = Flask(__name__)
data = 'data'
PORT = 5000

# Initialize engine
engine = Engine()

## ROUTES ##
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Receive string argument
    arg = request.args.get(data)
    print(arg)
    #info = engine.dealWithData(arg)
    return str(1) #info


### MAIN ###
if __name__=='__main__':
    app.run(host='0.0.0.0', port=PORT)
    print('[main]: main(): Server is listening on port:', PORT)
