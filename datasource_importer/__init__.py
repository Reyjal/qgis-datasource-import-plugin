# -*- coding: utf-8 -*-
"""
/***************************************************************************
 datasource_importer
                                 A QGIS plugin
 Import datasources from a project if they are missing in the local QGIS configuration
                             -------------------
        begin                : 2013-09-13
        copyright            : (C) 2013 by Sourcepole
        email                : mwa@sourcepole.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load datasource_importer class from file datasource_importer
    from datasource_importer import datasource_importer
    return datasource_importer(iface)
