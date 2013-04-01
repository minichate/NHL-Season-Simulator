import os
import sys

import heroku

"""Scale heroku web processes using the heroku python API."""

# you may want to add better argument processing, use argparse, etc.
dynos = int(sys.argv[1])
cloud = heroku.from_key(os.environ.get('HEROKU_API_KEY'))
app = cloud.apps['nhlplayoffscheer']

try:
    # you may want to add a maximum dyno check here to prevent costly mistakes ;)
    webproc = app.processes['worker']  
    webproc.scale(dynos)

except KeyError:
    # note: scaling to 0 dynos or attempting to scale up if 0 web dynos exist
    # both throw this error. Make sure you have at least one dyno.
    print >> sys.stderr, "Could not scale web processes - are there 0 web dynos running?"
