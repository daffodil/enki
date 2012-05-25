"""
shortcuts --- Manages QScintilla shortcuts
==========================================

Creates QActions, which represent QScintilla actions.

Sends commands to the current editor, when action was triggered
"""

from PyQt4.QtCore import QObject
from PyQt4.QtGui import QAction, QApplication, QIcon
from PyQt4.Qsci import QsciScintilla as qsci

from mks.core.core import core

def tr(text):  # pylint: disable=C0103
    """ Stub for translation procedure
    """
    return text

MKS_TOGGLE_BOOKMARK = -1
MKS_NEXT_BOOKMARK = -2
MKS_PREV_BOOKMARK = -3

MKS_PASTE = -4
MKS_PASTE_LINE = -5
MKS_MOVE_LINES_DOWN = -6
MKS_MOVE_LINES_UP = -7


_MENUS = (\
('mEdit/mSelection', tr('Selection'), ''),
('mEdit/mSelection/mRectangular', tr('Rectangular'), ''),
('mEdit/mSelection/mParagraph', tr('Extend by Paragraph'), ''),
('mNavigation/mMove', tr('Move'), ''),
('mEdit/mCopyPaste', tr('Copy-pasting'), 'cut.png'),
('mEdit/mHistory', tr('History'), 'undo.png'),
('mEdit/mCase', tr('Change case'), 'abbreviation.png'),
('mNavigation/mScroll', tr('Scroll'), ''),
)


class Shortcuts(QObject):
    """Class creates all actions and sends events commands to the editor
    """
    def __init__(self):
        QObject.__init__(self)
        self._createdActions = []
        self._createdMenus = []
        self._currentDocument = core.workspace().currentDocument()  # probably None
        model = core.actionManager()
        
        for menu in _MENUS:
            if menu[2]:
                menuObj = model.addMenu(menu[0], menu[1], QIcon(':/mksicons/' + menu[2]))
            else:
                menuObj = model.addMenu(menu[0], menu[1])
            menuObj.setEnabled(False)
            self._createdMenus.append(menuObj)
        
        for command, path, text, shortcut, icon in _ACTIONS:
            actObject = QAction(text, self)
            if shortcut:
                actObject.setShortcut(shortcut)
            if icon:
                actObject.setIcon(QIcon(':/mksicons/' + icon))
            actObject.setData(command)
            actObject.setEnabled(False)
            actObject.triggered.connect(self.onAction)
            model.addAction(path, actObject)
            self._createdActions.append(actObject)
        
        core.workspace().currentDocumentChanged.connect(self.onCurrentDocumentChanged)

    def del_(self):
        model = core.actionManager()
        for actObject in self._createdActions:
            model.removeAction(actObject)

        for menuObj in self._createdMenus[::-1]:
            model.removeMenu(menuObj)

    def onCurrentDocumentChanged(self, oldDocument, document):  # pylint: disable=W0613
        """Current document changed slot handler
        """
        for actObject in self._createdActions:
            actObject.setEnabled(document is not None)
        for menuObject in self._createdMenus:
            menuObject.setEnabled(document is not None)
        self._currentDocument = document
    
    def onAction(self):
        """Action action triggered handler
        """
        action = self.sender()
        code = action.data().toInt()[0]
        
        focusWidget = QApplication.focusWidget()
        if focusWidget is not None and isinstance(focusWidget, qsci):
            editor = focusWidget
        else:
            editor = self._currentDocument.qscintilla
        
        if code > 0:
            editor.SendScintilla(code)
        elif MKS_TOGGLE_BOOKMARK == code:
            editor.parent().toggleBookmark()
        elif MKS_NEXT_BOOKMARK == code:
            editor.parent().nextBookmark()
        elif MKS_PREV_BOOKMARK == code:
            editor.parent().prevBookmark()
        elif MKS_PASTE == code:  # Paste via method, to fix EOL
            editor.paste()
        elif MKS_PASTE_LINE == code:  # Own method
            editor.pasteLine()
        elif MKS_MOVE_LINES_DOWN == code:
            editor.parent().moveLinesDown()
        elif MKS_MOVE_LINES_UP == code:
            editor.parent().moveLinesUp()
        else:
            assert 0
