import sys
pp = "C:\\Python27\\lib\\site-packages\\nose-1.3.7-py2.7.egg"
sys.path.append(pp)

import maya.standalone
maya.standalone.initialize(name='python')

import nose
nose.run()

