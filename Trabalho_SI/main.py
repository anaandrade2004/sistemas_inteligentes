import time
from spade import quit_spade

from Agentes.Monitor import MonitorAgent
from Agentes.Unidade import UnidadeAgent
from Agentes.Alerta import AlertAgent
from Agentes.Medico import MedicAgent
from Agentes.Gestor_Unidade import GestorUnidadeAgent



XMPP_SERVER = 'win-k89ugsd4eom'
#XMPP_SERVER = 'laptop-gdthqa6i'
#XMPP_SERVER = 	'win-k89ugsd4eom'
PASSWORD = 'NOPASSWORD'
MAX_MEDICOS = 5 
MAX_UTENTES = 1
MAX_UCI=3

if __name__ == '__main__':
    medico_agents_list=[]
    unidade_agents_list=[]
    monitor_agents_list=[]

    #Gestor hospitalar
    gestor_jid="gestor@"+XMPP_SERVER
    gestor_agent=GestorUnidadeAgent(gestor_jid,PASSWORD)
    gestor_agent.start()
    time.sleep(2)

    #Sistema de alertas
    alerta_jid="alerta@" + XMPP_SERVER
    alerta_agent=AlertAgent(alerta_jid,PASSWORD)
    alerta_agent.start()
    gestor_agent.set("alerta_jid",alerta_jid)
    time.sleep(2)

    #UCIs

    for i in range(1, MAX_UCI + 1):
        unidade_jid="unidade_{}@".format(i) + XMPP_SERVER
        unidade_agent = UnidadeAgent(unidade_jid, PASSWORD)

        res_unidade = unidade_agent.start(auto_register=True)

        unidade_agents_list.append(unidade_agent)

        unidade_agent.set("gestor_jid",gestor_jid)
        time.sleep(2)
    

    
    
    #Médicos do hospital
    for i in range(1, MAX_MEDICOS + 1):
        medico_jid = 'medico_{}@'.format(str(i)) + XMPP_SERVER
        medico_agent = MedicAgent(medico_jid, PASSWORD)

        
        alerta_agent.set('medico_{}'.format(i), medico_jid)


        res_medico = medico_agent.start(auto_register=True)
        
        medico_agents_list.append(medico_agent)

        medico_agent.set("gestor_jid",gestor_jid)
        time.sleep(5)
    
    #Monitor do utente
    for i in range(1, MAX_UTENTES + 1):
        monitor_jid="monitor_{}@".format(i) + XMPP_SERVER
        monitor_agent=MonitorAgent(monitor_jid,PASSWORD)
        monitor_agent.set("gestor_jid",gestor_jid)
        


        res_monitor = monitor_agent.start(auto_register=True)
        
        monitor_agents_list.append(monitor_agent)

        monitor_agent.set("gestor_jid",gestor_jid)
        monitor_agent.set("alerta_jid",alerta_jid)

        time.sleep(5)
    
    
    

    while gestor_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            
            for monitor_agent in monitor_agents_list:
                monitor_agent.stop()

            
            for medico_agent in medico_agents_list:
                medico_agent.stop()

            alerta_agent.stop()

            for unidade_agent in unidade_agents_list:
                unidade_agent.stop()


            # stop manager agent
            break
    print('Agents finished')
    

   

    
    quit_spade()





