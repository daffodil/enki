"""
mitscheme --- MIT Scheme integration. Interactive Scheme console
================================================================

File contains integration with the core
"""

from PyQt4.QtCore import QObject, Qt
from PyQt4.QtGui import QIcon

from enki.core.core import core
from enki.core.uisettings import ChoiseOption, TextOption


class Plugin(QObject):
    """Module implementation
    """
    
    instance = None
    
    def __init__(self):
        QObject.__init__(self)
        self._installed = False
        self._evalAction = None
        self._activeInterpreterPath = None

        allDocs = core.workspace().documents()
        self._schemeDocumentsCount = len(filter(self._isSchemeFile, allDocs))
        
        # TODO handle situation, when lexer changed for current document
        core.workspace().documentOpened.connect(self._installOrUninstallIfNecessary)
        core.workspace().documentClosed.connect(self._installOrUninstallIfNecessary)
        core.workspace().currentDocumentChanged.connect(self._installOrUninstallIfNecessary)
        core.workspace().currentDocumentChanged.connect(self._updateEvalActionEnabledState)
        core.workspace().languageChanged.connect(self._installOrUninstallIfNecessary)
        core.workspace().languageChanged.connect(self._updateEvalActionEnabledState)
        core.uiSettingsManager().dialogAccepted.connect(self._applySettings)
        core.uiSettingsManager().aboutToExecute.connect(self._onSettingsDialogAboutToExecute)
        
        self._installOrUninstallIfNecessary()

    def __del__(self):
        self.del_()

    def _applySettings(self):
        """Apply settings. Called by configurator class
        """
        # if path has been changed - restart the interpreter
        if self._installed and \
           self._activeInterpreterPath != core.config()["Modes"]["Scheme"]["InterpreterPath"]:
            self.del_()
        
        self._installOrUninstallIfNecessary()
    
    def _onSettingsDialogAboutToExecute(self, dialog):
        """UI settings dialogue is about to execute.
        Add own options
        """
        from mitscheme import MitSchemeSettings
        widget = MitSchemeSettings(dialog)
        dialog.appendPage(u"Modes/MIT Scheme", widget, QIcon(':/enkiicons/languages/scheme.png'))

        # Options
        dialog.appendOption(ChoiseOption(dialog, core.config(), "Modes/Scheme/Enabled",
                                       {widget.rbWhenOpened: "whenOpened",
                                        widget.rbNever: "never",
                                        widget.rbAlways: "always"}))
        dialog.appendOption(TextOption(dialog, core.config(), "Modes/Scheme/InterpreterPath", widget.leInterpreterPath))

    def _isSchemeFile(self, document):
        """Check if document is highlighted as Scheme
        """
        return document is not None and \
               document.language() == 'Scheme'

    def _schemeDocumentIsOpened(self):
        """Check if at least one Scheme document is opened
        """
        schemeDocs = filter(self._isSchemeFile, core.workspace().documents())
        return len(schemeDocs) > 0

    def _updateEvalActionEnabledState(self):
        """Update action enabled state
        """
        if self._evalAction is None:
            return

        currDoc = core.workspace().currentDocument()
        self._evalAction.setEnabled(currDoc is not None and self._isSchemeFile(currDoc))

    def _installOrUninstallIfNecessary(self):
        """Install or uninstall according to settings and availability of opened Scheme files
        """
        enabled =  core.config()["Modes"]["Scheme"]["Enabled"]
        if enabled == 'always':
            if not self._installed:
                self._install()
        elif enabled == 'never':
            if self._installed:
                self.del_()
        else:
            assert enabled == 'whenOpened'
            if self._schemeDocumentIsOpened():
                self._install()
            else:
                self.del_()

    def _install(self):
        """Install the plugin to the core
        """
        if self._installed:
            return

        self._schemeMenu = core.actionManager().addMenu("mScheme", "MIT Scheme")
        self._evalAction = core.actionManager().addAction("mScheme/aEval", "Eval. selection/Save and eval.")
        self._evalAction.setStatusTip("Evaluate selection. If nothing is selected - save and evaluate whole file")
        self._evalAction.setShortcut("Ctrl+E")
        self._evalAction.triggered.connect(self._onEvalTriggered)
        self._breakAction = core.actionManager().addAction("mScheme/aBreak", "Stop the interpreter")
        self._breakAction.setStatusTip("Use it as a restart action.")
        self._breakAction.setShortcut("Pause")
        self._breakAction.triggered.connect(self._onBreakTriggered)
        self._breakAction.setEnabled(False)

        self._activeInterpreterPath = core.config()["Modes"]["Scheme"]["InterpreterPath"]
        
        from mitscheme import MitScheme
        self._mitScheme = MitScheme(self._activeInterpreterPath)
        
        self._mitScheme.processIsRunningChanged.connect(lambda isRunning: self._breakAction.setEnabled(isRunning))
        
        from mitscheme import MitSchemeDock
        self._dock = MitSchemeDock(self._mitScheme.widget())

        core.mainWindow().addDockWidget(Qt.BottomDockWidgetArea, self._dock)
        self._dock.hide()

        self._installed = True
    
    def del_(self):
        """Terminate the plugin. Method called by core, when closing Enki, and sometimes by plugin itself
        """
        if not self._installed:
            return
        self._mitScheme.stop()
        core.actionManager().removeAction(self._evalAction)
        self._evalAction = None
        core.actionManager().removeAction(self._breakAction)
        self._breakAction = None
        core.actionManager().removeMenu("mScheme")
        core.mainWindow().removeDockWidget(self._dock)
        self._dock.del_()
        del self._dock
        self._installed = False

    def _onEvalTriggered(self):
        """Eval action triggered. Evaluate file or expression
        """
        document = core.workspace().currentDocument()
        if document is None:
            return
        
        selection = document.selectedText()
        if selection:
            self._mitScheme.execCommand(selection)
            self._dock.show()
        else:
            if document.isModified():
                document.saveFile()
            if document.filePath():  # user may cancel saving document
                self._mitScheme.loadFile(document.filePath())
                self._dock.show()
    
    def _onBreakTriggered(self):
        """Break has been triggered. Stop the interpreter
        """
        self._mitScheme.stop()
