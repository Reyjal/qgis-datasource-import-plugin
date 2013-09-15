# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WmsDatasource

 Datasource for WMS layers
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

class WmsDatasource(Datasource):

    def __init__(self, layer):
        Datasource.__init__(self, layer)

    # get datasource name and identifier strings from local settings
    @staticmethod
    def localSettings():
        connections = {}
        settings = QSettings()

        # parse WMS logins
        logins = {}
        settings.beginGroup(u"/Qgis/WMS")
        for name in settings.childGroups():
            settings.beginGroup(name)
            logins[name] = {
                "username": settings.value("username", ""),
                "password": settings.value("password", "")
            }
            settings.endGroup()
        settings.endGroup()

        # parse WMS settings
        settings.beginGroup(u"/Qgis/connections-wms/")
        for name in settings.childGroups():
            username = ""
            password = ""
            if logins.has_key(name):
                username = logins[name]["username"]
                password = logins[name]["password"]

            settings.beginGroup(name)
            connections[name] = WmsDatasource.identifierString(
                settings.value("url"),
                username,
                password,
                settings.value("referer"),
                settings.value("ignoreAxisOrientation", False, type=bool),
                settings.value("ignoreGetFeatureInfoURI", False, type=bool),
                settings.value("ignoreGetMapURI", False, type=bool),
                settings.value("invertAxisOrientation", False, type=bool),
                settings.value("smoothPixmapTransform", False, type=bool),
            )
            settings.endGroup()
        return connections

    @staticmethod
    def identifierString(url, username, password, referer, ignoreAxisOrientation, ignoreGetFeatureInfoUrl, ignoreGetMapUrl, invertAxisOrientation, smoothPixmapTransform):
        return "%s|%s:%s|%s|%s,%s,%s,%s,%s" % (url, username, password, referer, ignoreAxisOrientation, ignoreGetFeatureInfoUrl, ignoreGetMapUrl, invertAxisOrientation, smoothPixmapTransform)

    def providerName(self):
        return "WMS"

    # get datasource identifier string
    def identifier(self):
        datasource_uri = QgsDataSourceURI()
        datasource_uri.setEncodedUri(self.layer.source())
        return WmsDatasource.identifierString(
            datasource_uri.param('url'),
            datasource_uri.param('username'),
            datasource_uri.param('password'),
            datasource_uri.param('referer'),
            datasource_uri.param('IgnoreAxisOrientation') == "1",
            datasource_uri.param('IgnoreGetFeatureInfoUrl') == "1",
            datasource_uri.param('IgnoreGetMapUrl') == "1",
            datasource_uri.param('InvertAxisOrientation') == "1",
            datasource_uri.param('SmoothPixmapTransform') == "1"
        )

    # get suggested name for new local settings entry
    def suggestedName(self):
        datasource_uri = QgsDataSourceURI()
        datasource_uri.setEncodedUri(self.layer.source())
        url = QUrl(datasource_uri.param('url'))
        return url.host()

    # add local settings entry
    def addToSettings(self, name):
        settings = QSettings()

        settings.beginGroup(u"/Qgis/connections-wms/")
        settings.beginGroup(name)
        datasource_uri = QgsDataSourceURI()
        datasource_uri.setEncodedUri(self.layer.source())
        settings.setValue("url", datasource_uri.param('url'))
        settings.setValue("ignoreGetMapURI", datasource_uri.param('IgnoreGetMapUrl') == "1")
        settings.setValue("ignoreAxisOrientation", datasource_uri.param('IgnoreAxisOrientation') == "1")
        settings.setValue("invertAxisOrientation", datasource_uri.param('InvertAxisOrientation') == "1")
        settings.setValue("smoothPixmapTransform", datasource_uri.param('SmoothPixmapTransform') == "1")
        settings.setValue("ignoreGetFeatureInfoURI", datasource_uri.param('IgnoreGetFeatureInfoUrl') == "1")
        settings.setValue("referer", datasource_uri.param('referer'))
        settings.endGroup()
        settings.endGroup()

        settings.beginGroup(u"/Qgis/WMS")
        settings.beginGroup(name)
        settings.setValue("username", datasource_uri.param('username'))
        settings.setValue("password", datasource_uri.param('password'))
