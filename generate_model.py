print 'Setting up starting directory'
from os import environ
import sys
import os.path


current_dir = os.path.dirname(os.path.realpath(__file__))
target_dir = '\\'.join(current_dir.split('\\')[0:-2]) 
sys.path.insert(0,target_dir) 



# drop and create all model -------------------------------------
print '\ndrop and create all model...'
from core.models import *
from core.databases import *

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine) 



# initializing data ---------------------------------------------
print '\ninitializing data...'



print '\ninitializing function...'
#import core.databases.functions
