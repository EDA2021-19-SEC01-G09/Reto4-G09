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
    elif paisInfo is not None:
        landing = newPais(paisInfo)
        m.put(allLandings, paisName, landing)
    if marcador is not None:
        if not lt.isPresent(landing['cables'], marcador):
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
    extremos = formatVertex(cable)
    origin = extremos[0]
    destination = extremos[1]

    if not gr.containsVertex(analyzer['connections'], origin):
        addStop(analyzer, origin)
        landing = getLanding(analyzer, cable['\ufefforigin'])
        infoPais = countryExists(analyzer, landing)
        if infoPais is not None:
            if gr.containsVertex(analyzer['connections'], infoPais[1]):
                dist = distance2Capital(infoPais[0], getCoord(landing))
                addConnection(analyzer, origin, infoPais[1], dist)
                addConnection(analyzer, infoPais[1], origin, dist)
    
    if not gr.containsVertex(analyzer['connections'], destination):
        addStop(analyzer, destination)
        landing = getLanding(analyzer, cable['destination'])
        infoPais = countryExists(analyzer, landing)
        if infoPais is not None:
            if gr.containsVertex(analyzer['connections'], infoPais[1]):
                dist = distance2Capital(infoPais[0], getCoord(landing))
                addConnection(analyzer, destination, infoPais[1], dist)
                addConnection(analyzer, infoPais[1], destination, dist)
    
    distance = abs(hs.haversine(getCoord(getLanding(analyzer, cable['\ufefforigin'])), getCoord(getLanding(analyzer, cable['destination']))))
    addConnection(analyzer, origin, destination, distance)
    addInfoOnLandings(analyzer, cable['\ufefforigin'], None, cable['cable_id'])
    addInfoOnLandings(analyzer, cable['destination'], None, cable['cable_id'])

    return analyzer
    
def getLanding(analyzer, landingpoint):
    prelanding =  m.get(analyzer['landings'], landingpoint)
    landing = me.getValue(prelanding)['info']
    return landing
    
def getCoord(landing):
    locLanding = (float(landing['latitude']), float(landing['longitude']))
    return locLanding

def countryExists(analyzer, landing):
    pais = landing['name'].split(",")[-1].strip(" ")
    preInfoPais = m.get(analyzer['countries'], pais)
    if preInfoPais:
        return preInfoPais, pais
    else:
        return None

def distance2Capital(preInfoPais, coordPais):
    infoPais = me.getValue(preInfoPais)
    locPais = (float(infoPais['CapitalLatitude']), float(infoPais['CapitalLongitude']))
    disHav = hs.haversine(coordPais, locPais)
    return abs(disHav)

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un cable entre dos landing points
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer
    
def addRouteConnections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = m.keySet(analyzer['landings'])
    for key in lt.iterator(lststops):
        lstroutes = me.getValue(m.get(analyzer['landings'], key))['cables']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0.1)
                addConnection(analyzer, route, prevrout, 0.1)
            prevrout = route

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones helper

def formatVertex(cable):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    origen = str(cable['\ufefforigin']) + '-' + cable['cable_id']
    destino = str(cable['destination']) + '-' + cable['cable_id']
    return (origen, destino)

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
