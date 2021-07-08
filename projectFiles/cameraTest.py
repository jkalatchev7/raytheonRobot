import os
import sys
import subprocess
from datetime import datetime
def take_pic(title):
    start = datetime.now()
    command  = './webcam.sh ' + title
    os.system('chmod +x webcam.sh')
    print(command)
    os.system(command)
    name = 'webcam/' + title + '.png'
    print(datetime.now() - start)
    return name
