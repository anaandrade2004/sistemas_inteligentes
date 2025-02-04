class UCI:
    
    def __init__(self,jid:str, esp:str, camas:int):
        self.jid=jid
        self.esp=esp
        self.camas=camas

    def getJid(self):
        return self.jid

    def getEsp(self):
        return self.esp
    
    def setEsp(self, esp:str):
        self.esp = esp

    def getCamas(self):
        return self.camas
    
    def setCamas(self,camas:int):
        self.camas = camas