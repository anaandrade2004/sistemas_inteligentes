import spade
from spade.behaviour import CyclicBehaviour, OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
import jsonpickle
from Classes.MakeOperationUCI import UCI
import asyncio
import random
import time



class UnidadeAgent(spade.agent.Agent):
    especialidades = ["Cardiologia", "Pneumologia", "Medicina_Geral"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lista_medicos = []  
        self.uci_info= None
        self.dici_espera={}  

    class Add_camas(PeriodicBehaviour):
        async def run(self):
            await asyncio.sleep(60)
            self.agent.uci_info.setCamas(self.agent.uci_info.getCamas()+random.randint(1,10))
            print("-------------------------")
            print(f"A UCI de {self.agent.uci_info.getEsp()} tem {self.agent.uci_info.getCamas()} camas na totalidade")
            print("-------------------------")


            
    class Registar(OneShotBehaviour):
        async def run(self):

            jid = str(self.agent.jid)
            esp = UnidadeAgent.especialidades[0]
            UnidadeAgent.especialidades = UnidadeAgent.especialidades[1:]
            camas = 3
            uci_info = UCI(jid, esp, camas)
            self.agent.uci_info = uci_info

            print(f"""
--------------------------------------
UCI:
Especialidade: {esp}
Camas: {camas}
Jid: {jid}
--------------------------------------""")
            
            msg = Message(to=self.agent.get("gestor_jid"))
            
            msg.set_metadata("performative", "uci")
            msg.body = jsonpickle.encode(self.agent.uci_info) 
            await self.send(msg)


    class Receive(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                p = msg.get_metadata("performative")
                if p == "adicionar":
                    medico_info = jsonpickle.decode(msg.body)
                    self.agent.lista_medicos.append(medico_info)

                elif p =="direcionar":
                    print("... a ser direcionado para um médico...")
                    online=False
                    for medico in self.agent.lista_medicos:
                        if medico.getTrab():
                            online=True
                            break
                    
                    if len(self.agent.lista_medicos) !=0 and online and len(self.agent.dici_espera)<len(self.agent.lista_medicos)*2:
                        if self.agent.uci_info.getCamas()>=(len(self.agent.dici_espera)+1):
                            (paciente_info,dic_grav)= jsonpickle.decode(msg.body)
                            self.agent.dici_espera[paciente_info]=(paciente_info.getGrav(),dic_grav)
                            self.agent.dici_espera = dict(sorted(self.agent.dici_espera.items(), key=lambda item: item[1][0], reverse=True))
                            print("Paciente: {} adicionado à fila de espera".format(paciente_info.getJid()))
                        else:
                            print("Não há camas disponíveis na uci {}".format(self.agent.uci_info.getEsp()))
                            print("A ver se é possivél redistribuir camas")
                            msg1 = Message(to=self.agent.get("gestor_jid"))
                            msg1.set_metadata("performative", "redistribuir")
                            msg1.body = jsonpickle.encode(self.agent.uci_info)
                            await self.send(msg1)
                            await asyncio.sleep(5)
                            (paciente_info,dic_grav)= jsonpickle.decode(msg.body)
                            self.agent.dici_espera[paciente_info]=(paciente_info.getGrav(),dic_grav)
                            self.agent.dici_espera = dict(sorted(self.agent.dici_espera.items(), key=lambda item: item[1][0], reverse=True))
                            print("Paciente: {} adicionado à fila de espera".format(paciente_info.getJid()))
                    else:
                        reply = msg.make_reply()
                        reply.set_metadata("performative","refuse_medico")
                        await self.send(reply)

                elif p=="pedido":
                    if len(self.agent.dici_espera)!=0:
                        for medico in self.agent.lista_medicos:
                            if medico.getDisp()==True and medico.getTrab()==True:
                                medico.setDisp(False)
                                self.agent.uci_info.setCamas(self.agent.uci_info.getCamas()-1)
                                msg3 = Message(to=self.agent.get("gestor_jid"))
                                msg3.set_metadata("performative", "remover_camas")
                                msg3.body = jsonpickle.encode(self.agent.uci_info)
                                await self.send(msg3)
                                paciente_info= next(iter(self.agent.dici_espera))
                                self.agent.dici_espera.pop(paciente_info)
                                msg1 = Message(to=medico.getJid())
                                msg1.set_metadata("performative","notify")
                                msg1.body=jsonpickle.encode(paciente_info)
                                await self.send(msg1)
                                break
                            

                    
                        
                elif p=="curado":
                    medico_info=jsonpickle.decode(msg.body)
                    for medico in self.agent.lista_medicos:
                        if medico_info.getJid() == medico.getJid():
                            medico.setDisp(True)
                            self.agent.uci_info.setCamas(self.agent.uci_info.getCamas()+1)
                            msg3 = Message(to=self.agent.get("gestor_jid"))
                            msg3.set_metadata("performative", "adicionar_camas")
                            msg3.body = jsonpickle.encode(self.agent.uci_info)
                            await self.send(msg3)
                            print("O número de camas agora é {}".format(self.agent.uci_info.getCamas()))
                
                
                elif p=="update_camas":
                    camas=jsonpickle.decode(msg.body)
                    self.agent.uci_info.setCamas(camas)

                    
                elif p =="remove_camas":
                    self.agent.uci_info.setCamas(self.agent.uci_info.getCamas-2)



                elif p == "horario":
                    horario =jsonpickle.decode(msg.body)
                    
                    for medico in self.agent.lista_medicos:
                        if medico.getEntrada() < medico.getSaida():
                            
                            if medico.getEntrada() <= horario < medico.getSaida():
                                medico.setTrab(True)
                            else:
                                medico.setTrab(False)
                        else:
                            
                            if horario >= medico.getEntrada() or horario < medico.getSaida():
                                medico.setTrab(True)
                            else:
                                medico.setTrab(False)
                
                
                




    async def setup(self):
        r = self.Registar()
        m = self.Receive()
        add=self.Add_camas(period=120)
        
        self.add_behaviour(r)
        self.add_behaviour(m)
        self.add_behaviour(add)
        
        print("UCI foi ativada")

