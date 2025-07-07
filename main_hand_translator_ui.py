# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_hand_translator.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QDockWidget, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(987, 686)
        MainWindow.setMaximumSize(QSize(1100, 800))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Start_translation = QPushButton(self.centralwidget)
        self.Start_translation.setObjectName(u"Start_translation")
        self.Start_translation.setMinimumSize(QSize(130, 35))

        self.horizontalLayout.addWidget(self.Start_translation)

        self.End_translation = QPushButton(self.centralwidget)
        self.End_translation.setObjectName(u"End_translation")
        self.End_translation.setMinimumSize(QSize(130, 35))

        self.horizontalLayout.addWidget(self.End_translation)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.toggle_cam = QPushButton(self.centralwidget)
        self.toggle_cam.setObjectName(u"toggle_cam")
        self.toggle_cam.setMinimumSize(QSize(130, 35))

        self.horizontalLayout.addWidget(self.toggle_cam)

        self.open_text = QPushButton(self.centralwidget)
        self.open_text.setObjectName(u"open_text")
        self.open_text.setMinimumSize(QSize(130, 35))

        self.horizontalLayout.addWidget(self.open_text)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.video_page = QWidget()
        self.video_page.setObjectName(u"video_page")
        self.gridLayout_3 = QGridLayout(self.video_page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.video_capture = QLabel(self.video_page)
        self.video_capture.setObjectName(u"video_capture")
        self.video_capture.setMinimumSize(QSize(528, 410))
        self.video_capture.setMaximumSize(QSize(773, 712))
        self.video_capture.setStyleSheet(u"background-color: black;")

        self.gridLayout_3.addWidget(self.video_capture, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.video_page)
        self.blank_page = QWidget()
        self.blank_page.setObjectName(u"blank_page")
        self.blank_page.setStyleSheet(u"background-color: black;")
        self.stackedWidget.addWidget(self.blank_page)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.dockWidget_text = QDockWidget(MainWindow)
        self.dockWidget_text.setObjectName(u"dockWidget_text")
        self.dockWidget_text.setMinimumSize(QSize(217, 172))
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.gridLayout_2 = QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.text_translation = QPlainTextEdit(self.dockWidgetContents_2)
        self.text_translation.setObjectName(u"text_translation")

        self.gridLayout_2.addWidget(self.text_translation, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Export_btn = QPushButton(self.dockWidgetContents_2)
        self.Export_btn.setObjectName(u"Export_btn")

        self.horizontalLayout_2.addWidget(self.Export_btn)

        self.Clear_btn = QPushButton(self.dockWidgetContents_2)
        self.Clear_btn.setObjectName(u"Clear_btn")

        self.horizontalLayout_2.addWidget(self.Clear_btn)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.dockWidget_text.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidget_text)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Start_translation.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.End_translation.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.toggle_cam.setText(QCoreApplication.translate("MainWindow", u"On/Off", None))
        self.open_text.setText(QCoreApplication.translate("MainWindow", u"Open Text", None))
        self.video_capture.setText("")
        self.Export_btn.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.Clear_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
    # retranslateUi

