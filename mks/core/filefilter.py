"""
filefilter --- Filter temporary files from FS views
===================================================

File browser, Locator, and probably other functionality shall ignore temporaty files,
such as *.bak, *.o for C++, *.pyc for Python.
        
This module provides regular expression, which tests, if file shall be ignored.
Regexp is constructed from patterns, configurable in the settings
"""

import fnmatch
import re

from PyQt4.QtCore import pyqtSignal, QObject

from mks.core.core import core
from mks.core.uisettings import ModuleConfigurator, ListOnePerLineOption

class _Configurator(ModuleConfigurator):
    """ModuleConfigurator implementation
    """
    def __init__(self, dialog):
        ModuleConfigurator.__init__(self, dialog)
        self._options = \
          [ListOnePerLineOption(dialog, core.config(), "NegativeFileFilter", dialog.pteFilesToHide)]


class FileFilter(QObject):
    """Module implementation
    """
    
    regExpChanged = pyqtSignal()
    """
    regExpChanged()
    
    **Signal** emitted, when regExp has changed
    """  # pylint: disable=W0105

    
    def __init__(self):
        QObject.__init__(self)
        self._applySettings()
        core.uiSettingsManager().dialogAccepted.connect(self._applySettings)
        core.moduleConfiguratorClasses.append(_Configurator)

    def regExp(self):
        """Get negative filer reg exp.
        
        If file name matches it, ignore this file
        """
        return self._regExp
    
    def _applySettings(self):
        """Settings dialogue has been accepted.
        Recompile the regExPatterns
        """
        filters = core.config()["NegativeFileFilter"]
        regExPatterns = [fnmatch.translate(f) for f in filters]
        compositeRegExpPattern = '(' + ')|('.join(regExPatterns) + ')'
        self._regExp = re.compile(compositeRegExpPattern)
        self.regExpChanged.emit()
