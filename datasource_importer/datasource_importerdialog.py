# -*- coding: utf-8 -*-
"""
/***************************************************************************
 datasource_importerDialog
                                 A QGIS plugin
 Import datasources from a project if they are missing in the local QGIS settings
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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from datasource import *
from postgres_datasource import *
from wms_datasource import *
from ui_datasource_importer import Ui_datasource_importer

class datasource_importerDialog(QtGui.QDialog):
    COLUMN_NAME = 0
    COLUMN_TYPE = 1
    COLUMN_LAYER = 2
    COLUMN_IDENTIFIER = 3

    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_datasource_importer()
        self.ui.setupUi(self)

        self.ui.tblDatasources.insertColumn(self.COLUMN_IDENTIFIER)
        self.ui.tblDatasources.hideColumn(self.COLUMN_IDENTIFIER);

        QObject.connect(self.ui.chkSelectAll, SIGNAL("stateChanged(int)"), self.toggleSelectAll)

        self.missingDatasources = {}

    def toggleSelectAll(self, state):
        for row in range(0, self.ui.tblDatasources.rowCount()):
            self.ui.tblDatasources.item(row, self.COLUMN_NAME).setCheckState(state)

    def updateDatasources(self):
        localPostgresIdentifiers = PostgresDatasource.localSettings().values()
        localWmsIdentifiers = WmsDatasource.localSettings().values()

        # collect datasources missing in local settings
        self.missingDatasources = {}
        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            if layer.type() != QgsMapLayer.PluginLayer:
                provider = layer.dataProvider().name()

                datasource = None
                localIdentifers = []
                if provider == "postgres":
                    datasource = PostgresDatasource(layer)
                    localIdentifers = localPostgresIdentifiers
                elif provider == "wms":
                    datasource = WmsDatasource(layer)
                    localIdentifers = localWmsIdentifiers

                if datasource != None:
                    identifier = datasource.identifier()
                    if not identifier in localIdentifers:
                        if self.missingDatasources.has_key(identifier):
                            self.missingDatasources[identifier].append(datasource)
                        else:
                            self.missingDatasources[identifier] = [datasource]

        # clear list
        self.ui.tblDatasources.setSortingEnabled(False)
        while self.ui.tblDatasources.rowCount() > 0:
            self.ui.tblDatasources.removeRow(0)
        self.ui.chkSelectAll.setCheckState(QtCore.Qt.Unchecked)

        for datasources in self.missingDatasources.values():
            # collect layer names
            layers = []
            for datasource in datasources:
                layers.append(datasource.layer.name());

            # add row
            datasource = datasources[0]
            nameItem = QTableWidgetItem(datasource.suggestedName())
            nameItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
            nameItem.setCheckState(QtCore.Qt.Unchecked)
            typeItem = QTableWidgetItem(datasource.providerName())
            layerItem = QTableWidgetItem(', '.join(layers))
            layerItem.setToolTip(datasource.layer.source())
            identifierItem = QTableWidgetItem(datasource.identifier())

            row = self.ui.tblDatasources.rowCount()
            self.ui.tblDatasources.insertRow(row)
            self.ui.tblDatasources.setItem(row, self.COLUMN_NAME, nameItem)
            self.ui.tblDatasources.setItem(row, self.COLUMN_TYPE, typeItem)
            self.ui.tblDatasources.setItem(row, self.COLUMN_LAYER, layerItem)
            self.ui.tblDatasources.setItem(row, self.COLUMN_IDENTIFIER, identifierItem)

        self.ui.tblDatasources.resizeColumnsToContents()
        self.ui.tblDatasources.setSortingEnabled(True)
        self.ui.tblDatasources.sortItems(self.COLUMN_LAYER)
        self.ui.tblDatasources.sortItems(self.COLUMN_TYPE)

    def importSelectedDatasources(self):
        messages = []
        for row in range(0, self.ui.tblDatasources.rowCount()):
            if self.ui.tblDatasources.item(row, self.COLUMN_NAME).checkState() == QtCore.Qt.Checked:
                identifier = self.ui.tblDatasources.item(row, self.COLUMN_IDENTIFIER).text()
                datasource = self.missingDatasources[identifier][0]

                # try alternative name if it exists
                localNames = []
                if datasource.providerName() == "PostgreSQL":
                    localNames = PostgresDatasource.localSettings().keys()
                elif datasource.providerName() == "WMS":
                    localNames = WmsDatasource.localSettings().keys()
                name = self.ui.tblDatasources.item(row, self.COLUMN_NAME).text()
                newName = name
                index = 2
                while newName in localNames:
                    newName = "%s (%d)" % (name, index)
                    index += 1

                if newName != name:
                    messages.append("'%s' already exists, renamed new data source to '%s'" % (name, newName))

                datasource.addToSettings(newName)

        if len(messages) > 0:
            # notify user
            QMessageBox.information(self, "Datasource Import", '\n'.join(messages))
