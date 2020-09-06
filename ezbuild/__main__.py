import sys

from ezbuild import app
from ezbuild.common import zlog

# MAIN entry point

if __name__ == "__main__":
    zlog.info('Number of arguments:', len(sys.argv), 'arguments.')
    zlog.info('Argument List:', str(sys.argv))
    app.run(sys.argv[1:])
