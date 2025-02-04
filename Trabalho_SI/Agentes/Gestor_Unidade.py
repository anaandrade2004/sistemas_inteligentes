import spade
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour, OneShotBehaviour
from spade.message import Message
import jsonpickle
from Classes.MakeOperationPaciente import Utente
from Classes.MakeOperationMedico import Medico
from Classes.MakeOperationUCI import UCI
import random



class GestorUnidadeAgent(spade.agent.Agent):
    
    list_UCI=[]
    clock=0

    class Registo(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)

            if msg:
                p = msg.get_metadata("performative")
                if p == "utente":
                    print('----------------')
                    print('Paciente Registado')
                elif p == "medico":
                    
                    medico_info =jsonpickle.decode(msg.body)
                    for i in GestorUnidadeAgent.list_UCI:
                        if medico_info.getEsp()==i.getEsp():

                            msg1 = Message(to=i.getJid())

                            msg1.set_metadata("performative","adicionar")
                            msg1.body = jsonpickle.encode(medico_info)

                            await self.send(msg1)
                    
                        
                elif p== "uci":
                    
                    (uci_info)= jsonpickle.decode(msg.body)
                    
                    GestorUnidadeAgent.list_UCI.append(uci_info)
                    msg1 = Message(to=self.agent.get("alerta_jid"))

                    msg1.set_metadata("performative","add_uci")
                    msg1.body = jsonpickle.encode(uci_info)

                    await self.send(msg1)


                elif p == "redistribuir":
                    uci_n= jsonpickle.decode(msg.body)
                    m_camas= GestorUnidadeAgent.list_UCI[0]
                    for uci in GestorUnidadeAgent.list_UCI[1:]:
                        if uci.getCamas()>m_camas.getCamas(): 
                            m_camas=uci

                    if m_camas.getCamas()>2:
                        print("Adicionei")
                        m_camas.setCamas(m_camas.getCamas()-2)
                        uci_n.setCamas(uci_n.getCamas()+2) #mandar 2 msg

                    else:
                            print("Não foi possível redistribuir camas")
                            for uci in GestorUnidadeAgent.list_UCI:
                                if uci.getJid() == uci_n.getJid():
                                    uci.setCamas(random.randint(1,10))
                                    print("-------------------------")
                                    print(f"A UCI de {uci.getEsp()} tem agora {uci.getCamas()} camas na totalidade")
                                    print("-------------------------")
                                    reply = msg.make_reply()
                                    reply.body=jsonpickle.encode(uci.getCamas())
                                    reply.set_metadata("performative","update_camas")
                                    await self.send(reply)
                            
                        


                elif p =="remover_camas":
                    
                    uci_info= jsonpickle.decode(msg.body)
                    for uci in GestorUnidadeAgent.list_UCI:
                        if uci_info.getJid() == uci.getJid():
                            uci.setCamas(uci.getCamas()-1)


                elif p == "adicionar_camas":
                    
                    uci_info= jsonpickle.decode(msg.body)
                    for uci in GestorUnidadeAgent.list_UCI:
                        if uci_info.getJid() == uci.getJid():
                            uci.setCamas(uci.getCamas()+1)
                

                elif p=="disponivel":
                    medico_info = jsonpickle.decode(msg.body)
                    for uci in GestorUnidadeAgent.list_UCI:
                        if uci.getEsp()==medico_info.getEsp():
                            msg2 = Message(to=uci.getJid())
                            msg2.set_metadata("performative","pedido")
                            msg2.body = jsonpickle.encode(medico_info)
                            await self.send(msg2)

    class Clock(PeriodicBehaviour):
        async def run(self):
            if GestorUnidadeAgent.clock==23:
                GestorUnidadeAgent.clock=0
                print("Passou 1 dia")
            else:
                GestorUnidadeAgent.clock+=1
            print("São {} horas".format(GestorUnidadeAgent.clock))
            
            for uci in GestorUnidadeAgent.list_UCI:
                msg2 = Message(to=uci.getJid())
                msg2.set_metadata("performative","horario")
                msg2.body = jsonpickle.encode(GestorUnidadeAgent.clock)
                await self.send(msg2)






                            

                    
                    
            

    async def setup(self):
        regi=self.Registo()
        self.add_behaviour(regi)
        c=self.Clock(period=60)
        self.add_behaviour(c)
        

        print("GESTOR UCI foi ativada")