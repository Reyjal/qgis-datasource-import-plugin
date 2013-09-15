# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Datasource

 Abstract base class for datasources. Add subclasses for different data providers.
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

class Datasource:

    def __init__(self, layer):
        self.layer = layer

    # get datasource name and identifier strings from local settings
    @staticmethod
    def localSettings():
        raise NotImplementedError

    def providerName(self):
        raise NotImplementedError

    # get datasource identifier string
    def identifier(self):
        raise NotImplementedError

    # get suggested name for new local settings entry
    def suggestedName(self):
        raise NotImplementedError

    # add local settings entry
    def addToSettings(self, name):
        raise NotImplementedError
