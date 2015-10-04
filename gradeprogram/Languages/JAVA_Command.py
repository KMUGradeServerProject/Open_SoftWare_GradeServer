# -*- coding: utf-8 -*-
from Language import Language

class JAVA_Command(Language):
    def __init__(self, runFileName):
        Language.__init__(self, runFileName)
        
    def CompileCommand(self):
        return 'javac -nowarn -d ./ *.java 2>message.txt'
        
    def ExecuteCommand(self):
        runCommandList = []
        append = runCommandList.append
        
        append('/usr/bin/java')
        append('/usr/bin/java')
        append(self.runFileName)
            
        return runCommandList