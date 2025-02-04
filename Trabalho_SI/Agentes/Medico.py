from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour ,PeriodicBehaviour
from spade.message import Message
import jsonpickle
from Classes.MakeOperationMedico import Medico
from Classes.MakeOperationPaciente import Utente
import random
import time
import asyncio

class MedicAgent(Agent):
    especialidades = ["Cardiologia", "Pneumologia", "Medicina_Geral"]
    turnos={(0,8):0,(8,16):0,(16,0):0}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.medico_info = None

    class Registar_Medico(OneShotBehaviour):
        
        async def run(self):
            jid=str(self.agent.jid)
            esp=random.choice(MedicAgent.especialidades)
            turno_ordenado = sorted(MedicAgent.turnos.items(), key=lambda item: item[1])
            primeiro_turno = turno_ordenado[0][0]  
            MedicAgent.turnos[primeiro_turno] += 1  
            print(f'{jid} entrou no turno {primeiro_turno}')
            
            disp= True
            ent=primeiro_turno[0]
            sai = primeiro_turno[1]
            trab=True
            self.agent.medico_info = Medico(jid,esp,disp,ent,sai,trab) 
            print(f"""
-------------------------------
Medico:
Especialidade: {esp}
Disponibilidade: {disp}
Entrada: {ent}
Saida: {sai}
Trab: {trab}
Jid: {jid}
-------------------------------""")
            
            msg = Message(to=self.agent.get("gestor_jid"))
            msg.set_metadata("performative","medico")
            msg.body = jsonpickle.encode(self.agent.medico_info)
            await self.send(msg)
            

    class MedicoAtivo(CyclicBehaviour):       
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                p = msg.get_metadata("performative")
                if p == "notify":
                    self.agent.medico_info.setDisp(False)
                    paciente_info = jsonpickle.decode(msg.body)

                    print("-------------------------------------------------------------------------")
                    print("Alerta Médico do Utente {} Recebido pelo {}".format(paciente_info.getJid(),self.agent.medico_info.getJid()))
                    print("-------------------------------------------------------------------------")
                    

                    print("A curar o paciente")
                    await asyncio.sleep(random.randint(1,10))


                    print("O paciente {} foi tratado".format(paciente_info.getJid()))

                    msg2 = Message(to=paciente_info.getJid())
                    msg2.set_metadata("performative","cured")
                    msg2.body = jsonpickle.encode(self.agent.medico_info.getEsp())
                    await self.send(msg2)

                    self.agent.medico_info.setDisp(True)

                    reply = msg.make_reply()
                    reply.set_metadata("performative","curado")
                    reply.body=jsonpickle.encode(self.agent.medico_info)
                    await self.send(reply)
                    self.agent.paciente = None

                    msg2 = Message(to=self.agent.get("gestor_jid"))
                    msg2.set_metadata("performative","disponivel")
                    msg2.body = jsonpickle.encode(self.agent.medico_info)
                    await self.send(msg2)



    class Pedido(PeriodicBehaviour):

        async def run(self):
            if self.agent.medico_info.getDisp() and self.agent.medico_info.getTrab():
                msg2 = Message(to=self.agent.get("gestor_jid"))
                msg2.set_metadata("performative","disponivel")
                msg2.body = jsonpickle.encode(self.agent.medico_info)
                await self.send(msg2)
            





    async def setup(self):
        
        print("Configurando o agente médico...")
        registar_medico=self.Registar_Medico()
        medico_ativo = self.MedicoAtivo()
        pedido=self.Pedido(period=30)
        self.add_behaviour(registar_medico)
        self.add_behaviour(medico_ativo)
        self.add_behaviour(pedido)
                    
