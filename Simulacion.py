import simpy
import random
'''
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
    env.process(CPU('proceso %d'%(i+1),env,cantidad_RAM,cantidad_Instrucciones,RAM,capacidad_instrucciones))

env.run()
#env.run(until=50)  #correr la simulación hasta el tiempo = 50

print ("tiempo promedio por vehículo es: ", totalTiempo/25.0)
'''

def CPU(nombre,env,cantidad_RAM,cantidad_Instrucciones,RAM,capacidad_instrucciones,cpu):
    global totalTiempo  
    corre=True
    
    while corre==True:
      yield RAM.get(cantidad_RAM)
      while cantidad_Instrucciones >0:
        
        with cpu.request() as turno:
          horaLlegada = env.now
          yield turno
          yield env.timeout(1)
          cantidad_Instrucciones = cantidad_Instrucciones -3
          ficha=random.randint(1,2)

          if(ficha==1):
            print('%s ocupa %f de RAM, el tiempo acutal es %e' %(nombre,cantidad_RAM,env.now))
            yield env.timeout()

          elif(ficha==2):
            print('%s tenia muchas instrucciones, debe de seguir en cola. El tiempo actual es %e' %(nombre,env.now))

      tiempoCiclo = env.now-horaLlegada
      print("")
      print(tiempoCiclo,  "Tiempo Ciclo")
      print(env.now, "Hora Salida")
      print(horaLlegada,  "Hora Llegada")
      print(totalTiempo, "Tiempo Total")
      print("")
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
for i in range(50):
    cantidad_RAM = random.randint(1,10)
    cantidad_Instrucciones = random.randint(1,10)
    env.process(CPU('proceso %d'%(i+1),env,cantidad_RAM,cantidad_Instrucciones,RAM,capacidad_instrucciones,cpu))

env.run()
#env.run(until=50)  #correr la simulación hasta el tiempo = 50

print("")
print(totalTiempo, "tiempo total")
print ("tiempo promedio por proceso es: ", totalTiempo/50.0)