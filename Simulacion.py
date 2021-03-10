import simpy
import random

# el proceso car muestra un vehículo que se estaciona un tiempo
# y luego se conduce otro lapso de tiempo
def CPU(nombre,env,cantidad_RAM,cantidad_Instrucciones,RAM,capacidad_instrucciones):
    global totalTiempo  
    # entra al cpu
    horaLlegada = env.now
    print ('%s Instrucciones %f' % (nombre, cantidad_Instrucciones))
    if(cantidad_Instrucciones <= 3):
      with capacidad_instrucciones.request() as turno:
        yield turno      #ya puso la manguera de gasolina en el carro!
        yield env.timeout(cantidad_Instrucciones) #hecha gasolina por un tiempo
        print ('%s Entra al CPU a las %f' % (nombre, env.now))
        tiempoCiclo = env.now - horaLlegada
        print ('%s se tardo %f' % (nombre, tiempoCiclo))
        #aqui el carro hace un release automatico de la bomba de gasolina
      
    elif(cantidad_Instrucciones > 3):
      with capacidad_instrucciones.request() as turno:
        yield turno      #ya puso la manguera de gasolina en el carro!
        yield env.timeout(3) #hecha gasolina por un tiempo
        print ('%s Entra al CPU a las %f' % (nombre, env.now))
        tiempoCiclo = env.now - horaLlegada
        

      cantidad_Instrucciones = cantidad_Instrucciones - 3
      random_Gate = random.randint(1,2)
      if(random_Gate == 1):
        yield env.timeout(random.randint(1,2))
        env.process(CPU('proceso %d'%i,env,cantidad_RAM,cantidad_Instrucciones,RAM,capacidad_instrucciones))
        
      elif(random_Gate == 2):
        env.process(CPU('proceso %d'%i,env,cantidad_RAM,cantidad_Instrucciones,RAM,capacidad_instrucciones))
        
      
      
    
    totalTiempo = totalTiempo + tiempoCiclo
           

# ----------------------

env = simpy.Environment() #ambiente de simulación
RAM = simpy.Container(env, init=100, capacity=100)
capacidad_instrucciones = simpy.Resource(env,capacity = 3)
random.seed(10) # fijar el inicio de random

totalTiempo = 0
for i in range(10):
    cantidad_RAM = random.randint(1,10)
    cantidad_Instrucciones = random.randint(1,10)
    env.process(CPU('proceso %d'%i,env,cantidad_RAM,cantidad_Instrucciones,RAM,capacidad_instrucciones))

env.run()
#env.run(until=50)  #correr la simulación hasta el tiempo = 50

print ("tiempo promedio por vehículo es: ", totalTiempo/25.0)