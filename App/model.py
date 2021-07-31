"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config
import haversine as hs


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    try:
        analyzer = {
                    'countries': None,
                    'landings': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }

        analyzer['countries'] = m.newMap(numelements=2,
                                    maptype='PROBING')

        analyzer['landings'] = m.newMap(numelements=2,
                                    maptype='PROBING',
                                    comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=300,
                                            comparefunction=compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al catalogo

def addCountry(analyzer, country):
    m.put(analyzer['countries'], country['CountryName'], country)

def addStop(analyzer, landingid):
    """
    Adiciona un landing como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], landingid):
            gr.insertVertex(analyzer['connections'], landingid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addInfoOnLandings(analyzer, paisName, paisInfo, marcador = None):
    allLandings =  analyzer['landings']
    existslanding = m.contains(allLandings, paisName)
    if existslanding:
        entry = m.get(allLandings, paisName)
        landing = me.getValue(entry)
    else:
        landing = newPais(paisInfo)
        m.put(allLandings, paisName, landing)
    if marcador is not None:
        lt.addLast(landing['cables'], marcador)

def newPais(info):
    pais = {'info' : None,
            'cables' : None}
    pais['info'] = info
    pais['cables'] = lt.newList("ARRAY_LIST")
    return pais

def addStopConnection(analyzer, cable):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = formatVertex(cable)[0]
        destination = formatVertex(cable)[1]
        if not gr.containsVertex(analyzer['connections'], origin):
            addStop(analyzer, origin)
            pais = me.getValue(analyzer['landings'], m.get(analyzer['landings'], cable['origin']))['info']['name']
            locCap = m.get(analyzer['countries'], cable)

        if not gr.containsVertex(analyzer['connections'], destination):
            addStop(analyzer, destination)
        loc_origin =      
        distance = 
        distance = abs(distance)
        addConnection(analyzer, origin, destination, distance)
        addRouteStop(analyzer, service)
        addRouteStop(analyzer, lastservice)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')
    

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones helper

def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1