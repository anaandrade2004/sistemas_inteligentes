
class Utente:
    
    def __init__(self,jid:str, freq_card:int, freq_resp:int, temp:float,press_art:int,press_parc_o2:int, gravidade:int):
        self.jid=jid
        self.freq_card = freq_card
        self.freq_resp = freq_resp
        self.temp = temp
        self.press_art = press_art
        self.press_parc_o2 = press_parc_o2

        self.gravidade = gravidade

    def getJid(self):
        return self.jid


    def getFreqCard(self):
        return self.freq_card
    
    def setFreqCard(self, freq_card:int):
        self.freq_card = freq_card

    def getFreqResp(self ):
        return self.freq_resp
    
    def setFreqResp(self, freq_resp:int):
        self.freq_resp = freq_resp

    def getTemp(self):
        return self.temp
    
    def setTemp(self,temp:float):
        self.temp = temp
    
    def getPressArt(self):
        return self.press_art
    
    def setPressArt(self, press_art:int):
        self.press_art=press_art
    
    def getPressParcO2(self):
        return self.press_parc_o2
    
    
    def setPressParcO2(self, press_parc_o2:int):
        self.press_parc_o2=press_parc_o2
    
    def getGrav(self):
        return self.gravidade
    
    def setGrav(self, gravidade:int):
        self.gravidade = gravidade
    


    



#frequência cardíaca - 60 a 100 batimentos por minuto
#frequência respiratória - 12 a 16 respirações por minuto. 
#temperatura - 36,6 e 37,2 °C.
#pressão arterial - 90 e 120 mm Hg
#pH sanguíneo:  7,35 a 7,45. Valores abaixo de 7,35 indicam acidose, enquanto valores acima de 7,45 indicam alcalose.
#Pressão parcial de oxigênio (PaO2): m 75 e 100 mmHg. Baixos níveis de PaO2 podem indicar hipoxemia (baixos níveis de oxigênio no sangue).
#Pressão parcial de dióxido de carbono (PaCO2):  de 35 a 45 mmHg. Valores elevados de PaCO2 indicam hiperapneia (ventilação insuficiente), enquanto valores baixos podem sugerir hiperventilação.




