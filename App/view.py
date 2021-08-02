"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
from DISClib.ADT import map as m
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT.graph import gr


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información de cables submarinos")
    print("2- Req 1")
    print("3- Req 2")
    print("4- Req 3")
    print("5- Req 4")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        analyzer = controller.init()
        controller.loadData(analyzer)
        print("El total de landing points del grafo: " + str(gr.numVertices(analyzer['connections'])))
        primLanding = lt.getElement(m.valueSet(analyzer['landings']), 1)['info']
        print("El identificador, el nombre, la latitud y la longitud del primer landing point cargado en el mapa es " + str(primLanding['id']) + ", " + str(primLanding['name']) + ", " + str(primLanding['latitude']) + "y " +  str(primLanding['longitude']) + " respectivamente")
        print("El total de conexiones entre landing points: " + str(gr.numEdges(analyzer['connections'])))
        print("El numero de países es: " + str(m.size(analyzer['countries'])))
        ultPais = lt.getElement(m.valueSet(analyzer['countries']), m.size(analyzer['countries']) - 1)
        print("La población y el número de usuarios del último país cargado en el mapa es de " + ultPais['Population'] + " y " + ultPais['Internet users'] + " personas respectivamente")


    elif int(inputs[0]) == 2:
        pass

    else:
        sys.exit(0)
sys.exit(0)
