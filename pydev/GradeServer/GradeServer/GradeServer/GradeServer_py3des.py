# -*- coding: utf-8 -*-
"""
    GradeServer py3des
    ~~~~~~~~

    GradeServer py3des 모듈. 

"""

from GradeServer.py3Des.pyDes import triple_des, ECB, PAD_PKCS5
from GradeServer.resource.otherResources import OtherResources

class TripleDES:
    
    __triple_des = None
    
    @staticmethod
    def init():
        # Triple Des init
        TripleDES.__triple_des =triple_des(OtherResources().const.TRIPLE_DES_KEY, 
                                     mode = ECB,
                                     IV = "\0\0\0\0\0\0\0\0",
                                     pad = None,
                                     padmode = PAD_PKCS5)
    
    @staticmethod
    def encrypt(data):
        return TripleDES.__triple_des.encrypt(data)

