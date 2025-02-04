from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, OneShotBehaviour
from spade.message import Message
import random 
import jsonpickle
from Classes.MakeOperationPaciente import Utente
from Classes.MakeOperationMedico import Medico

class MonitorAgent(Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paciente_info=None
    
        self.cardiologia = {
            'freq_card' : 'Normal',
            'press_art' : 'Normal'
        }

        self.pneumologia = {
            'freq_resp' : 'Normal',
            'press_parc_o2' : 'Normal'
        }
        
        self.medicina_geral = {
            'temp' : 'Normal'
        }

    class Monitoramento(PeriodicBehaviour): 
        async def run(self):
            #ver cena de probabilidade de ele ficar
            paciente_jid = str(self.agent.jid)
            freq_card = random.randint(60,100)
            freq_resp = random.randint(12,16)
            temp = round(random.uniform(36.0,37.2),2)
            press_art = random.randint(90,120)
            press_parc_o2 = random.randint(75,100)


            # Frequência Cardíaca
            if 60 <= freq_card <= 100:
                self.agent.cardiologia['freq_card'] = 'Normal'
            elif 40 <= freq_card < 60 or 100 < freq_card <= 140:
                self.agent.cardiologia['freq_card'] = 'Alerta'
            else:
                self.agent.cardiologia['freq_card'] = 'Crítico'

            # Frequência Respiratória
            if 12 <= freq_resp <= 16:
                self.agent.pneumologia['freq_resp'] = 'Normal'
            elif 8 <= freq_resp < 12 or 16 < freq_resp <= 30:
                self.agent.pneumologia['freq_resp'] = 'Alerta'
            else:
                self.agent.pneumologia['freq_resp'] = 'Crítico'

            #Temperatura
            if 36.0 <= temp <= 37.2:
                self.agent.medicina_geral['temp'] = 'Normal'
            elif 35 <= temp < 36.0 or 37.2 < temp <= 39:
                self.agent.medicina_geral['temp'] = 'Alerta'
            else:
                self.agent.medicina_geral['temp'] = 'Crítico'
            
            # Pressão Arterial Sistólica
            if 90 <= press_art <= 120:
                self.agent.cardiologia["press_art"] = 'Normal'
            elif 70 <= press_art < 90 or 120 < press_art <= 180:
                self.agent.cardiologia["press_art"] = 'Alerta'
            else:
                self.agent.cardiologia["press_art"] = 'Crítico'

            # Pressão Parcial de Oxigênio
            if 75 <= press_parc_o2 <= 100:
                self.agent.pneumologia["press_parc_o2"] = 'Normal'
            elif 60 <= press_parc_o2 < 75 or 100 < press_parc_o2 <= 150:
                self.agent.pneumologia["press_parc_o2"] = 'Alerta'
            else:
                self.agent.pneumologia["press_parc_o2"] = 'Crítico'

            
            

            print(f"""
----------------------------------------------------
Sinais vitais iniciais:
Paciente: {paciente_jid} 
Temperatura: {temp} ºC {self.agent.medicina_geral["temp"]}
Frequencia Cardica: {freq_card} bpm {self.agent.cardiologia["freq_card"]}
Pressão Arterial: {press_art} mmHg {self.agent.cardiologia["press_art"]}
Frequencia Respiratória: {freq_resp} rpm {self.agent.pneumologia["freq_resp"]}
Pressão parcial de oxigênio (PaO2): {press_parc_o2} mmHg {self.agent.pneumologia["press_parc_o2"]}
----------------------------------------------------""")

            # print(self.agent.cardiologia)
            # print(self.agent.pneumologia)
            # print(self.agent.medicina_geral)

            #Ver gravidade de cada especialidade
            dic_grav={"Cardiologia":0,"Pneumologia":0,"Medicina_Geral":0}

            #Gravidade Cardiologia
            for value in self.agent.cardiologia.values():
                if value == 'Crítico':
                    dic_grav["Cardiologia"]+=2

                elif value == 'Alerta':
                    dic_grav["Cardiologia"]+=1

                else:
                    dic_grav["Cardiologia"]=dic_grav["Cardiologia"]
            

            #Gravidade Pneumologia
            for value in self.agent.pneumologia.values():
                if value == 'Crítico':
                    dic_grav["Pneumologia"]+=2
                elif value == 'Alerta':
                    dic_grav["Pneumologia"]+=1
                else:
                    dic_grav["Pneumologia"]==dic_grav["Pneumologia"]

            #Gravidade Medicina_Geral
            for value in self.agent.medicina_geral.values():
                if value == 'Crítico':
                    dic_grav["Medicina_Geral"]+=2
                elif value == 'Alerta':
                    dic_grav["Medicina_Geral"]+=1
                else:
                    dic_grav["Medicina_Geral"]= dic_grav["Medicina_Geral"]            

            if sum(dic_grav.values())!=0: 
                esp=""
                maior=-1
                for i in dic_grav.keys():
                    if dic_grav[i] >maior:
                        maior=dic_grav[i]
                        esp=i
                    elif dic_grav[i] == maior:
                        esp="Medicina_Geral"
                        break
                        

                self.agent.paciente_info = Utente(paciente_jid, freq_card, freq_resp, temp,press_art,press_parc_o2, sum(dic_grav.values()))
                msg = Message(to=self.agent.get("alerta_jid"))
                msg.set_metadata("performative","inform")
                msg.body = jsonpickle.encode((self.agent.paciente_info,esp,dic_grav))
                await self.send(msg)

                print("Paciente em estado crítico. Necessita de Atendimento de {}".format(esp))

                msg1 = await self.receive(timeout=120)

                if msg1:
                    p = msg1.get_metadata("performative")
                    if p == "cured":
                        especialidade=jsonpickle.decode(msg.body)
                        
                        for i in self.agent.medicina_geral.keys():
                            self.agent.medicina_geral[i]="Normal"

                        for i in self.agent.cardiologia.keys():
                            self.agent.cardiologia[i]="Normal"

                        for i in self.agent.pneumologia.keys():
                            self.agent.pneumologia[i]="Normal"

                        if especialidade=="Cardiologia":
                            self.agent.paciente_info.setFreqCard(random.randint(60,100))
                            self.agent.paciente_info.setPressArt(random.randint(90,120))

                        elif especialidade=="Pneumologia":
                            self.agent.paciente_info.setFreqResp(random.randint(12,16))
                            self.agent.paciente_info.setPressParcO2(random.randint(75,100))

                        else:
                            self.agent.paciente_info.setFreqResp( random.randint(12,16))
                            self.agent.paciente_info.setTemp (round(random.uniform(36.0,37.2),2))
                            self.agent.paciente_info.setFreqCard( random.randint(60,100))
                            self.agent.paciente_info.setPressParcO2(random.randint(75,100))
                            self.agent.paciente_info.setPressArt(random.randint(90,120))

                        self.agent.paciente_info.setGrav(0)

                        print(f"""
------------------------------------------------------
Sinais vitais finais
Paciente: {self.agent.paciente_info.getJid()}
Temperatura: {self.agent.paciente_info.getTemp()} ºC
Frequencia_Cardica: {self.agent.paciente_info.getFreqCard()} bpm
Pressão Arterial: {self.agent.paciente_info.getPressArt()} mmHg
Frequencia_Respiratória: {self.agent.paciente_info.getFreqResp()} rpm
Pressão parcial de oxigênio (PaO2): {self.agent.paciente_info.getPressParcO2()} mmHg
Gravidade: {self.agent.paciente_info.getGrav()}
Obrigado estou saudável
------------------------------------------------------
                            """)
            else:
                print("Utente em bom estado")

    
    async def setup(self):
        
        monit=MonitorAgent.Monitoramento(period=15)
        self.add_behaviour(monit)
        






                    # # pH Sanguíneo
                    # ''' if 7.35 <= pH_sang <= 7.45:
                    #     AlertAgent.endocrinologia[pH_sang] = 'Normal'
                    # elif 7.2 <= pH_sang < 7.35 or 7.45 < pH_sang <= 7.6:
                    #     AlertAgent.endocrinologia[pH_sang] = 'Alerta'
                    # else:
                    #     AlertAgent.endocrinologia[pH_sang] = 'Crítico' '''

                    

                    