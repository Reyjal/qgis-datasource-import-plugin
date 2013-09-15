# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PostgresDatasource

 Datasource for PostgreSQL layers
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
"""

from datasource import *

class PostgresDatasource(Datasource):

    def __init__(self, layer):
        Datasource.__init__(self, layer)

    # get datasource name and identifier strings from local settings
    @staticmethod
    def localSettings():
        connections = {}
        settings = QSettings()
        settings.beginGroup(u"/PostgreSQL/connections/")
        for name in settings.childGroups():
            settings.beginGroup(name)
            connections[name] = PostgresDatasource.identifierString(settings.value("host"), settings.value("port"), settings.value("database"), settings.value("username"), settings.value("password"), settings.value("service"))
            settings.endGroup()
        return connections

    @staticmethod
    def identifierString(host, port, database, username, password, service):
        return "%s:%s|%s|%s:%s|%s" % (host, port, database, username, password, service)

    def providerName(self):
        return "PostgreSQL"

    # get datasource identifier string
    def identifier(self):
        datasource_uri = QgsDataSourceURI(self.layer.source())
        return PostgresDatasource.identifierString(datasource_uri.host(), datasource_uri.port(), datasource_uri.database(), datasource_uri.username(), datasource_uri.password(), datasource_uri.service())

    # get suggested name for new local settings entry
    def suggestedName(self):
        datasource_uri = QgsDataSourceURI(self.layer.source())
        return "%s (%s:%s)" % (datasource_uri.database(), datasource_uri.host(), datasource_uri.port())

    # add local settings entry
    def addToSettings(self, name):
        settings = QSettings()
        settings.beginGroup(u"/PostgreSQL/connections/")
        settings.beginGroup(name)
        datasource_uri = QgsDataSourceURI(self.layer.source())
        settings.setValue("service", datasource_uri.service())
        settings.setValue("host", datasource_uri.host())
        settings.setValue("port", datasource_uri.port())
        settings.setValue("database", datasource_uri.database())
        settings.setValue("username", datasource_uri.username())
        settings.setValue("password", datasource_uri.password())
        settings.setValue("publicOnly", False)
        settings.setValue("geometryColumnsOnly", False)
        settings.setValue("dontResolveType", False)
        settings.setValue("allowGeometrylessTables", False)
        settings.setValue("sslmode", 0)
        settings.setValue("saveUsername", datasource_uri.username() != "")
        settings.setValue("savePassword", datasource_uri.password() != "")
        settings.setValue("estimatedMetadata", False)
