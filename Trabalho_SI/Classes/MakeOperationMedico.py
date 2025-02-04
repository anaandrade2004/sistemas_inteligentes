
class Medico:
    
    def __init__(self,jid:str, esp:str, disp:bool, entrada:int, saida:int, trab:bool):
        self.jid=jid
        self.esp=esp
        self.disp=disp
        self.entrada = entrada
        self.saida=saida
        self.trab=trab

    def getJid(self):
        return self.jid

    def getEsp(self):
        return self.esp
    
    def setEsp(self, esp:str):
        self.esp = esp

    def getDisp(self):
        return self.disp
    
    def setDisp(self,disp:bool):
        self.disp = disp
    
    def setEntrada(self, entrada:int):
        self.entrada=entrada
        
    def getEntrada(self):
        return self.entrada
    
    def setSaida(self, saida:int):
        self.saida=saida

    def getSaida(self):
        return self.saida

    def setTrab(self, trab:bool):
        self.trab=trab

    def getTrab(self):
        return self.trab




