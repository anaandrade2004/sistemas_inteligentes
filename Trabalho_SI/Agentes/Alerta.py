from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from Classes.MakeOperationPaciente import Utente
from Classes.MakeOperationMedico import Medico
import random


class AlertAgent(Agent):

    lista_UCI=[]
    

    class Alertar(CyclicBehaviour):
        
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                p = msg.get_metadata("performative")
                if p == "inform":
                    (paciente_info,esp,dic_grav) = jsonpickle.decode(msg.body)

                    print(f"O paciente vai ser direcionado para a UCI {esp}")
                    for uci in AlertAgent.lista_UCI:
                        if uci.getEsp()==esp:
                            msg1 = Message(to=uci.getJid())
                            if esp in dic_grav.keys():
                                dic_grav.pop(esp)
                            msg1.set_metadata("performative","direcionar")
                            msg1.body = jsonpickle.encode((paciente_info,dic_grav))
                            await self.send(msg1)


                elif p=="add_uci":
                    uci_info= jsonpickle.decode(msg.body)
                    AlertAgent.lista_UCI.append(uci_info)


                elif p =="refuse_medico":
                    (paciente_info,dic_grav)=jsonpickle.decode(msg.body)
                    if len(dic_grav)!=0:
                        maior = max(dic_grav.values())  
                        chaves_maiores = [chave for chave in dic_grav.keys() if dic_grav[chave] == maior]
                        if len(chaves_maiores)==1:
                            esp=chaves_maiores[0]
                        elif len(chaves_maiores)>1:
                            if "Medicina_Geral" in dic_grav.keys():
                                esp="Medicina_Geral"
                            else:
                                esp=random.choice(chaves_maiores)

                        for uci in AlertAgent.lista_UCI:
                            if uci.getEsp() == esp:
                                print("Não havia médico suficiente na UCI anteriro a ser redirecionado para a UCI de {}".format(esp))
                                msg1 = Message(to=uci.getJid())
                                dic_grav.pop(esp)
                                msg1.set_metadata("performative","direcionar")
                                msg1.body = jsonpickle.encode((paciente_info,dic_grav))
                                await self.send(msg1)
                                break


    async def setup(self):
        print("Sistema de alertas ativo")
        alert= self.Alertar()
        self.add_behaviour(alert)





