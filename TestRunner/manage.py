import sys,os
base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base)
from TestRunner.Command import ManagementTools

if __name__ == '__main__':
    ManagementTools().run()