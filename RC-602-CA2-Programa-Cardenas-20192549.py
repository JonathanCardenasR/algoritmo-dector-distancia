# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 11:02:02 2021

@author: Sistema
"""

from memory_profiler import profile
import os

class Redes:
    def __init__(self): #constructor de la clase redes
        self.__routers = []
        self.__listaEnlaces = []
        self.__minutos=0
        self.__segundos=0
    
    def getMinutos(self):
        return self.__minutos
    def setMinutos(self,m):
        self.__minutos =m
    def getSegundos(self):
        return self.__segundos
    def setSegundos(self,s):
        self.__segundos =s
    
    def getRoutersRed(self):
        return self.__routers
    
    def getListaEnlacesRed(self):
        return self.__listaEnlaces
        
    def agregarRouter(self,r):
        self.__routers.append(r)
        self.actualizarRouter()
        
    def reinciarReloj(self):
        self.setMinutos(0)
        self.setSegundos(0)
        
    def actualizarRouter(self):
        for r in self.__routers:
            r.setRouterEnRed(self.__routers)
        
    def routerPorIndex(self,n): #no borrar
        return self.__routers[n] #no borrar
        
    def agregarEnlace(self,r1,r2,m):
        e1 = Enlace(r1, r2, m)
        e2 = Enlace(r2, r1, m)
        self.__listaEnlaces.append(e1)
        self.__listaEnlaces.append(e2)
    
    def ImprimirTodasTablas(self):
        print("REPORTE DE TABLAS")
        print("")
        for r in self.__routers:
            r.imprimirTabla()
            
    def ImprimirTodasTablasResumen(self):
        print("REPORTE DE TABLAS RESUMEN")
        print("")
        for r in self.__routers:
            r.imprimirTablaResumen(self.__routers)
          
    def buscarRouter(self,nombre):
        for r in self.__routers:
            if r.getNombre() == nombre:
                return r
    
    def listarRouter(self):
         print("Router en la red")
         for r in self.__routers:
             print("Router: {0}".format(r.getNombre()))
         print("")

    def listarEnlaces(self):
         print("Enlaces formados")
         for e in self.__listaEnlaces:
             print("RO: {0} | RD: {1} | Metrica: {2}".format(e.getOrigen().getNombre(),e.getDestino().getNombre(),e.getMetrica()))
         print("")

    def anularEnlace(self,r1,r2): #el while funciona hasta que se genera una excepcion por salir del rango de la lista
        r1.eliminarConn(r2)
        r2.eliminarConn(r1)
        pos=0
        while True: 
            try: 
                if r1==self.__listaEnlaces[pos].getOrigen() and r2==self.__listaEnlaces[pos].getDestino():
                    self.__listaEnlaces.remove(self.__listaEnlaces[pos])
                elif r2==self.__listaEnlaces[pos].getOrigen() and r1==self.__listaEnlaces[pos].getDestino():
                    self.__listaEnlaces.remove(self.__listaEnlaces[pos])
                else:
                    pos=pos+1
            except IndexError:
                break
            
    def crearEnlace(self,r1,r2,m): #el while funciona hasta que se genera una excepcion por salir del rango de la lista
        r1.crearConn(r2,m)
        r2.crearConn(r1,m)
        self.agregarEnlace(r1, r2, m)
     
    def eliminarRouter(self,nom):
        for r in self.__routers:     
            if r.getNombre() == nom:  
                pos=0
                while True: #el while funciona hasta que se genera una excepcion por salir del rango de la lista
                    try: 
                        if r==self.__listaEnlaces[pos].setOrigen() or r==self.__listaEnlaces[pos].getDestino():
                            self.__listaEnlaces.remove(self.__listaEnlaces[pos])
                        else:
                            pos=pos+1
                    except IndexError:
                        break
                self.__routers.remove(r)
        print("")
    
    def actualizarTablaRouterRed(self):
        for r in self.__routers:
            r.actualizarTabla()
            r.limpiarTablasTemp()
    

    def enviarTablas(self):
        for r in self.__routers:
            r.enviarTablasPuerto()
                
    def genTablaRed(self):
        for r in  self.__routers:
            r.genTabla()
    
    def InicioConn(self):
        for r in self.__routers:
            r.tablaConnIni()
            
    def genTodosPuertos(self):
        for r in self.__routers:
            r.genPuertos(self.__listaEnlaces)
    
    def contador(self):
        m=self.getMinutos()
        s=self.getSegundos()
        if s == 30:
            self.setSegundos(0)
            self.setMinutos(m+1)
        else:
            self.setSegundos(30)
    
    def imprimirTiempo(self):
        cadena= "{0} minutos {1} segundos".format(self.getMinutos(),self.getSegundos())
        print(cadena)
        return cadena
        
    def crearVerificador(self):
        lista = []
        for r in self.getRoutersRed():
            for t in r.getTabla():
                lista.append(t.getMetrica())
                lista.append(t.getSalto())
        return lista
    
    def verificarIgualdad(self,lista1):
        lista2 = self.crearVerificador()
        if lista1 == lista2:
            return True
        else:
            return False
        
class Tabla:
    def __init__(self,d,r):
        self.__dest = d
        self.__ruta = r 
        self.__metrica = 0
        self.__salto = 0        
    def setDest(self,d):
        self.__dest=d      
    def getDest(self):
        return self.__dest   
    def setRuta(self,r):
        self.__ruta = r   
    def getRuta(self):
        return self.__ruta
    def setMetrica(self,m):
        self.__metrica=m
    def getMetrica(self):
        return self.__metrica 
    def setSalto(self,s):
        self.__salto=s
    def getSalto(self):
        return self.__salto
    
class TablaTemp:
    def __init__(self,r):
        self.__routerOrig = r
        self.__tablaTemp = []
    def setRouterOrig(self,r):
        self.__routerOrig = r
    def getRouterOrig(self):
        return self.__routerOrig
    def setTablaTemp(self,t):
        self.__tablaTemp = t
    def getTablaTemp(self):
        return self.__tablaTemp

class Router:
    def __init__(self):
        self.__routerEnRed = []
        self.__nombre = ""
        self.__tabla = []
        self.__tablasMomentaneas = []
        self.__listaPuertos = []
    
    def genTabla(self):    # genera la tabla de rutas del router vacia
        for d in self.getRouterEnRed():
            for r in self.getRouterEnRed():
                celda = Tabla(d, r)
                self.getTabla().append(celda)
                
    def routerEncontrado(self,router):
        for r in self.getListaPuertos():
            if router == r.getDestino():
                return True
            
    def conseguirMetrica(self,r):
        for p in self.getListaPuertos():
            if r == p.getDestino():
                return p.getMetrica()
                   
    def tablaConnIni(self): #valores iniiciales de las conecciones
        for celda in self.getTabla():
            if self.routerEncontrado(celda.getRuta()) and celda.getDest() != self:
                if celda.getDest() == celda.getRuta():
                    celda.setMetrica(self.conseguirMetrica(celda.getDest()))
                    celda.setSalto(0)  
            else:
                celda.setMetrica(0)
                celda.setSalto(0)
    
    def buscarCeldaTabla(self,destino,ruta): 
        for c in self.getTabla():
            if c.getDest() == destino and c.getRuta()==ruta:
                return c
    
    def recibirTabla(self,t): ## funcion que agrega las tablas de otros raouter en una lista para su posterior procesamiento
        self.getTablasMomentaneas().append(t)
    
    def limpiarTablasTemp(self):
        vacio = []
        self.setTablasMomentaneas(vacio)
    
    def enviarTablasPuerto(self): #envia a los router que esten conectados su tabla con el puntero del roouter
        tablaTemp = self.generarTablaEnvio()
        for p in self.getListaPuertos():  
            p.getDestino().recibirTabla(tablaTemp)
      
    def generarTablaEnvio(self): #empaqueta en una  instancia la tabla y el puntero del router para ser enviado
        tablaTemporal = TablaTemp(self)
        tablaTemporal.setTablaTemp(self.clonarTabla())
        return tablaTemporal
    
    def actualizarTabla(self):
        self.actualizarCeldas()
            
    def clonarTabla(self):
        tablaClonada = []
        for c in self.getTabla():
            CeldaClonada = Tabla(c.getDest(),c.getRuta())
            CeldaClonada.setMetrica(c.getMetrica())
            CeldaClonada.setSalto(c.getSalto())
            tablaClonada.append(CeldaClonada)
        return tablaClonada
   
    def actualizarCeldas(self):
        self.puertoConnAct()
   
    def buscarMenorCeldaTablasTemporales(self,r,dest):
        menor = Tabla(None,None)
        for tt in self.getTablasMomentaneas():
            if tt.getRouterOrig() == r:
                for c in tt.getTablaTemp():
                    if c.getDest() == dest:
                        if c.getMetrica()  !=0:
                                if menor.getMetrica() == 0:
                                    menor = c
                                elif c.getMetrica()< menor.getMetrica():
                                    menor = c
                return menor
                        
    def buscarCeldaTablasTemporales(self,r):
        for tt in self.getTablasMomentaneas():
            if tt.getRouterOrig() == r:
                for c in tt.getTablaTemp():
                    if c.getDest() == self and c.getRuta() == self:
                        return c
                    
    def estaConectado(self,ro):
        for r in self.getListaPuertos():
            if r.getDestino() == ro:
                return True
        return False
                    
    def puertoConnAct(self): #actualiza operacion en la tabla               
                for c in self.getTabla():
                    m=0
                    s=0
                    if  c.getDest() != self and c.getRuta() != self and c.getDest() != c.getRuta() and self.estaConectado(c.getRuta()):
                       # print("entro router: {0} dist: {1} via: {2}".format(self.getNombre(),c.getDest().getNombre(),c.getRuta().getNombre()))
                        dest = c.getDest()
                        ruta = c.getRuta()
                        celda1 = self.buscarMenorCeldaTablasTemporales(ruta,dest)
                        celda2 = self.buscarMenorCeldaTablasTemporales(ruta,self)
                        
                        if celda1.getMetrica() != 0 :
                           # print("celda1: {0}  celda2: {1}".format(celda1.getMetrica(),celda2.getMetrica()))
                            m = celda1.getMetrica() +  celda2.getMetrica()
                            s =  celda1.getSalto() + celda2.getSalto() + 1
                            c.setMetrica(m)
                            c.setSalto(s)
    
    def buscarMenorRutaDisponibleDestino(self,destino):
        menor = Tabla(None,None)
        for c in self.getTabla():
            if c.getMetrica()  !=0 and c.getDest()==destino:
                if menor.getMetrica() == 0:
                    menor = c
                elif c.getMetrica()< menor.getMetrica():
                    menor = c
        return menor
    
    def imprimirTablaResumen(self,listaRouter):
        print("Tabla del Router {0}".format(self.getNombre()))
        print("Destino\t|",end="")
        print ("",end="\t")
        print("Metrica\t|",end="")
        print ("",end="\t")
        print("Salto\t|",end="")
        print ("",end="\t")
        print("Interfaz",end="")
        print ("")
        print ("-----------------------------------------------------------")
        for router in listaRouter:
            menor = self.buscarMenorRutaDisponibleDestino(router)
            if menor.getMetrica() !=0:
                print("{0}\t|".format(menor.getDest().getNombre()),end="")
                print ("",end="\t")
                print("{0}\t|".format(menor.getMetrica()),end="")
                print ("",end="\t")
                print("{0}\t|".format(menor.getSalto()),end="")
                print ("",end="\t")
                for p in self.getListaPuertos():
                    if p.getDestino() == menor.getRuta():
                        print("{0} - {1}".format(p.getNombre(),menor.getRuta().getNombre()),end="")
                        print ("",end="\t")
                        print("")
        print("")
             
                                   
    def imprimirTabla(self):
        print("Tabla del Router {0}".format(self.getNombre()))
        print("dest",end="")
        print ("",end="\t")
        for r in self.getRouterEnRed():  
            print(".{0}".format(r.getNombre()),end="\t")
            print ("",end="\t")
        print("")
        for f in self.getRouterEnRed():  
            print("{0}".format(f.getNombre()),end="\t")
            print ("[",end="\t")
            for c in self.getRouterEnRed():
                for t in self.getTabla():
                    if t.getRuta()==c and t.getDest() == f:      
                        print("({0},{1})".format(t.getMetrica(),t.getSalto()),end="\t")
            print("]")
        print("")
          
    def genPuertos(self,enlaces):
        i=1
        for e in enlaces:
            if e.getOrigen()==self:
                n= "p{0}".format(i)
                puerto = Puerto(n,e.getDestino(),e.getMetrica())
                self.getListaPuertos().append(puerto)
                i=i+1
                
    def eliminarConn(self,d):
        for p in self.getListaPuertos():
            if p.getDestino()==d:
                self.getListaPuertos().remove(p)
    
    def crearConn(self,d,m):
        for p in self.getListaPuertos():
            if p.getDestino()== None:
                p.setDestino(d)
                p.setMetrica(m)

    def getNombre(self):
        return self.__nombre
    def setNombre(self,n):
        self.__nombre = n
    def getTabla(self):
        return self.__tabla
    def setTabla(self,t):
        self.__tabla = t
    def getRouterEnRed(self):
        return self.__routerEnRed
    def setRouterEnRed(self,r):
        self.__routerEnRed = r
    def getListaPuertos(self):
        return self.__listaPuertos
    def setListaPuertos(self,p):
        self.__listaPuertos=p    
    def getTablasMomentaneas(self):
        return self.__tablasMomentaneas  
    def setTablasMomentaneas(self,t):
        self.__tablasMomentaneas=t

class Puerto:
    def __init__(self,n,d,m):
        self.__nombre = n
        self.__destino = d
        self.__metrica = m
    def setNombre(self,n):
        self.__nombre = n  
    def getNombre(self):
        return self.__nombre
    def setDestino(self,d):
        self.__destino = d    
    def getDestino(self):
        return self.__destino
    def setMetrica(self,m):
        self.__metrica = m    
    def getMetrica(self):
        return self.__metrica
    
class Enlace:
    def __init__(self,o,d,m):
        self.__origen = o
        self.__destino = d
        self.__metrica = m      
    def setDestino(self,r):
        self.__destino=r    
    def getMetrica(self):
        return self.__metrica
    def setMetrica(self,r):
        self.__metrica = r          
    def getOrigen(self):
        return self.__origen 
    def setOrigen(self,r):
        self.__origen=r
    def getDestino(self):
        return self.__destino


@profile
def main():
    os.system("")
    color = 31
    listaTiempos = []
    grafo = Redes()
    listaRouters =[]
    listaEnlaces = []
    f = open("simula2.txt", "r")
    primario = f.read().split("\n")
    for linea in primario:    
        separado = linea.split(",")
        listaEnlaces.append(separado)

    for linea in listaEnlaces:
        pos=0
        for e in linea:
            if pos<2:
               if e not in listaRouters:
                   listaRouters.append(e)
            pos=pos+1
               
    for e in listaRouters:
        r = Router()
        r.setNombre(e)
        grafo.agregarRouter(r)
    
    listaRoutersRed = grafo.getRoutersRed()
    
    for e in listaEnlaces:
        r1 = None
        r2 = None
        for r in listaRoutersRed:
            if e[0] == r.getNombre():
                r1=r
        for r in listaRoutersRed:
            if e[1] == r.getNombre():
                r2=r
        grafo.agregarEnlace(r1, r2, int(e[2]))
    
    grafo.genTodosPuertos()
    grafo.genTablaRed() 
    grafo.InicioConn()
    i=0
    print("t= {0}".format(i))
    tiempo=grafo.imprimirTiempo()
    grafo.contador()
    grafo.ImprimirTodasTablasResumen()
    print("t= {0}".format(i))  
    print("\x1b[0;{0}m".format(color)+"----")   
    #time.sleep(0.5)
    z=0
    p=0 
    while z<30:  
        i=i+1 
        lista = grafo.crearVerificador()
        grafo.enviarTablas()
        grafo.actualizarTablaRouterRed()
        grafo.InicioConn()           
        igual = grafo.verificarIgualdad(lista)
        
        if igual != True:
            print("t= {0}".format(i))  
            tiempo = grafo.imprimirTiempo()
        else:
            print(".")
        

        if igual == True and p==0:
            listaTiempos.append(tiempo)
            p=1
        elif igual == False:
            p=0
            
        
        if igual != True:
            grafo.ImprimirTodasTablasResumen()
            print("t= {0}".format(i))
            print("\x1b[0;{0}m".format(color) +"*******************************************************************")
            tiempo = grafo.imprimirTiempo()
        else:
            print("\x1b[0;{0}m".format(color) +".")
        
        
        grafo.contador()
        
        #time.sleep(0.5)
        z=z+1
        
        color=color+1
        if color == 38:
            color = 31
        
        if i == 10:
                print("simulacion de fallo de una conexion")
                n=1
                f=1
                listamomentanea=[]
                for r in grafo.getListaEnlacesRed():
                    if f % 2 !=0:
                        print("{0}: {1} - {2} met: {3}".format(n,r.getOrigen().getNombre(),r.getDestino().getNombre(),r.getMetrica()))
                        l=[]
                        l.append(r.getOrigen())
                        l.append(r.getDestino())
                        listamomentanea.append(l)
                        n=n+1
                    f=f+1
                num = int(input("Elija el numero del enlace que desea desea romper"))
                      
                grafo.anularEnlace(listamomentanea[num-1][0],listamomentanea[num-1][1])
                grafo.reinciarReloj()
            
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("|||||||||INDICADORES DE LA REPLICAICON||||||||||||||||")
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    for l in listaTiempos:
        print("Tablas se completaron en: {0}".format(l))     
    print("")
    
    
    

main()


