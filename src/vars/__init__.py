
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'../../../'))


from .gvinformationschema import *
from .privilege.gvprivilege import Privilege
__all__=["Privilege"]