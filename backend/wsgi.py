import os
import sys

# Ensure the proper working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set default encoding to UTF-8
if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

from app import create_app

application = create_app()

if __name__ == '__main__':
    application.run()
