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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    loadCountries(analyzer)
    loadLandings(analyzer)
    loadCables(analyzer)

def loadCountries(analyzer):
    archivo = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(archivo, encoding='utf-8'), delimiter = ",")
    
    for country in input_file:
        model.addCountry(analyzer, country)
        model.addStop(analyzer, country['CountryName'])

def loadLandings(analyzer):
    archivo = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(archivo, encoding='utf-8'), delimiter = ",")
    
    for file in input_file:
        model.addInfoOnLandings(analyzer, file['landing_point_id'], file)

def loadCables(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    connectionsfile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(connectionsfile, encoding="utf-8"),
                                delimiter=",")

    for cable in input_file:
        model.addStopConnection(analyzer, cable)
        
    model.addRouteConnections(analyzer)
    return analyzer

        
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    res = model.minimumCostPaths(analyzer, initialStation)
    return res

def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)

def MST(analyzer):
    return model.MST(analyzer)
    