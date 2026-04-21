# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'l2sMainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)
import resources_rc

class Ui_l2sMainWindow(object):
    def setupUi(self, l2sMainWindow):
        if not l2sMainWindow.objectName():
            l2sMainWindow.setObjectName(u"l2sMainWindow")
        l2sMainWindow.resize(900, 700)
        l2sMainWindow.setMinimumSize(QSize(800, 600))
        l2sMainWindow.setWindowTitle(u"Learn 2 slither")
        l2sMainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(l2sMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.mainHLayout = QHBoxLayout(self.centralwidget)
        self.mainHLayout.setSpacing(6)
        self.mainHLayout.setObjectName(u"mainHLayout")
        self.mainHLayout.setContentsMargins(9, 9, 9, 4)
        self.centralWidgetLeft = QWidget(self.centralwidget)
        self.centralWidgetLeft.setObjectName(u"centralWidgetLeft")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralWidgetLeft.sizePolicy().hasHeightForWidth())
        self.centralWidgetLeft.setSizePolicy(sizePolicy1)
        self.centralWidgetLeft.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.mainVlayoutLeft = QVBoxLayout(self.centralWidgetLeft)
        self.mainVlayoutLeft.setSpacing(6)
        self.mainVlayoutLeft.setObjectName(u"mainVlayoutLeft")
        self.mainVlayoutLeft.setContentsMargins(0, 0, 0, 0)
        self.boardFrame = QFrame(self.centralWidgetLeft)
        self.boardFrame.setObjectName(u"boardFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(4)
        sizePolicy2.setHeightForWidth(self.boardFrame.sizePolicy().hasHeightForWidth())
        self.boardFrame.setSizePolicy(sizePolicy2)
        self.boardFrame.setFrameShape(QFrame.Shape.Box)
        self.boardFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.boardFrame.setLineWidth(2)
        self.boardFrameLayout = QVBoxLayout(self.boardFrame)
        self.boardFrameLayout.setSpacing(0)
        self.boardFrameLayout.setObjectName(u"boardFrameLayout")
        self.boardFrameLayout.setContentsMargins(0, 0, 0, 0)

        self.mainVlayoutLeft.addWidget(self.boardFrame)

        self.stdOutFrame = QFrame(self.centralWidgetLeft)
        self.stdOutFrame.setObjectName(u"stdOutFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(2)
        sizePolicy3.setHeightForWidth(self.stdOutFrame.sizePolicy().hasHeightForWidth())
        self.stdOutFrame.setSizePolicy(sizePolicy3)
        self.stdOutFrame.setFrameShape(QFrame.Shape.Box)
        self.stdOutFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.stdOutFrame.setLineWidth(2)
        self.stdOutFrameLayout = QVBoxLayout(self.stdOutFrame)
        self.stdOutFrameLayout.setSpacing(0)
        self.stdOutFrameLayout.setObjectName(u"stdOutFrameLayout")
        self.stdOutFrameLayout.setContentsMargins(0, 0, 0, 0)

        self.mainVlayoutLeft.addWidget(self.stdOutFrame)


        self.mainHLayout.addWidget(self.centralWidgetLeft)

        self.agentsFrame = QFrame(self.centralwidget)
        self.agentsFrame.setObjectName(u"agentsFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.agentsFrame.sizePolicy().hasHeightForWidth())
        self.agentsFrame.setSizePolicy(sizePolicy4)
        self.agentsFrame.setFrameShape(QFrame.Shape.Box)
        self.agentsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.agentsFrame.setLineWidth(2)
        self.agentsFrameLayout = QVBoxLayout(self.agentsFrame)
        self.agentsFrameLayout.setSpacing(0)
        self.agentsFrameLayout.setObjectName(u"agentsFrameLayout")
        self.agentsFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.agentsLabel = QLabel(self.agentsFrame)
        self.agentsLabel.setObjectName(u"agentsLabel")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(2)
        sizePolicy5.setHeightForWidth(self.agentsLabel.sizePolicy().hasHeightForWidth())
        self.agentsLabel.setSizePolicy(sizePolicy5)
        self.agentsLabel.setPixmap(QPixmap(u":/assets/snake_team_ai.jpeg"))
        self.agentsLabel.setScaledContents(True)

        self.agentsFrameLayout.addWidget(self.agentsLabel)

        self.agentsScrollArea = QScrollArea(self.agentsFrame)
        self.agentsScrollArea.setObjectName(u"agentsScrollArea")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(6)
        sizePolicy6.setHeightForWidth(self.agentsScrollArea.sizePolicy().hasHeightForWidth())
        self.agentsScrollArea.setSizePolicy(sizePolicy6)
        self.agentsScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.agentsScrollArea.setFrameShadow(QFrame.Shadow.Plain)
        self.agentsScrollArea.setLineWidth(0)
        self.agentsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.agentsScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 284, 451))
        self.agentsScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.agentsFrameLayout.addWidget(self.agentsScrollArea)

        self.createAgentButton = QPushButton(self.agentsFrame)
        self.createAgentButton.setObjectName(u"createAgentButton")
        icon = QIcon()
        icon.addFile(u":/assets/create_snake_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.createAgentButton.setIcon(icon)
        self.createAgentButton.setIconSize(QSize(30, 25))
        self.createAgentButton.setAutoDefault(True)
        self.createAgentButton.setFlat(False)

        self.agentsFrameLayout.addWidget(self.createAgentButton)


        self.mainHLayout.addWidget(self.agentsFrame)

        l2sMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(l2sMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 23))
        l2sMainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(l2sMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        l2sMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(l2sMainWindow)

        self.createAgentButton.setDefault(False)


        QMetaObject.connectSlotsByName(l2sMainWindow)
    # setupUi

    def retranslateUi(self, l2sMainWindow):
        self.agentsLabel.setText("")
#if QT_CONFIG(tooltip)
        self.createAgentButton.setToolTip(QCoreApplication.translate("l2sMainWindow", u"Create a new agent", None))
#endif // QT_CONFIG(tooltip)
        self.createAgentButton.setText("")
        pass
    # retranslateUi

