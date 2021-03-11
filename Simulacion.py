import simpy
import random

def CPU(nombre,env,cantidad_RAM,cantidad_Instrucciones,RAM,capacidad_instrucciones,cpu,tiempo_espera):
    global totalTiempo  
    yield env.timeout(tiempo_espera)
    corre=True
    
    while corre==True:
      yield RAM.get(cantidad_RAM)
      while cantidad_Instrucciones >0:
        
        with cpu.request() as turno:
          horaLlegada = env.now
          print('%s entro al CPU en %d'%(nombre,horaLlegada))
          yield turno
          yield env.timeout(1)
          cantidad_Instrucciones = cantidad_Instrucciones -3
          ficha=random.randint(1,2)

          if(ficha==1):
            print('%s ocupa %f de RAM, el tiempo acutal es %e' %(nombre,cantidad_RAM,env.now))
            yield env.timeout(1)

          elif(ficha==2):
            print('%s tenia muchas instrucciones, debe de seguir en cola. El tiempo actual es %e' %(nombre,env.now))

      tiempoCiclo = env.now-horaLlegada
      print('El %s ha teminado en tiempo %d' %(nombre,tiempoCiclo))
      corre=False
      RAM.put(cantidad_RAM)

      
    

    totalTiempo = totalTiempo + tiempoCiclo
           

# ----------------------

env = simpy.Environment() #ambiente de simulación
RAM = simpy.Container(env, init=100, capacity=100)
capacidad_instrucciones = simpy.Resource(env,capacity = 3)
cpu = simpy.Resource(env,capacity = 1)
random.seed(10) # fijar el inicio de random

totalTiempo = 0
for i in range(25):
    cantidad_RAM = random.randint(1,10)
    cantidad_Instrucciones = random.randint(1,10)
    env.process(CPU('Proceso %d'%(i+1),env,cantidad_RAM,cantidad_Instrucciones,RAM,capacidad_instrucciones,cpu,random.expovariate(1.0/10)))

env.run()
#env.run(until=50)  #correr la simulación hasta el tiempo = 50

print("")
print(totalTiempo, "Tiempo total")
print ("Tiempo promedio por proceso es: ", totalTiempo/25.0)