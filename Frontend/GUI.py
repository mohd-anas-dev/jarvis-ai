from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget,
    QLineEdit, QGridLayout, QVBoxLayout, QPushButton, QFrame,
    QLabel, QSizePolicy, QHBoxLayout
)
from PyQt5.QtGui import (
    QIcon, QPainter, QMovie, QColor,
    QTextCharFormat, QFont, QPixmap, QTextBlockFormat
)
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assitantname", "Assistant")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics", "YouTube - Jarvis Material For GUI-20250410T202342Z-001", "YouTube - Jarvis Material For GUI")



def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)


def QueryModifier(Query):
    new_query = Query.lower().strip()
    question_words = [
        "how", "what", "who", "where", "when", "why", "which",
        "whose", "whom", "can you", "what's", "where's", "how's"
    ]
    if any(word + " " in new_query for word in question_words):
        if new_query[-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + " ?"
        else:
            new_query += "?"
    else:
        if new_query[-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()


def SetMicrophoneStatus(Command):
    with open(os.path.join(TempDirPath, 'Mic.data'), "w", encoding='utf-8') as file:
        file.write(Command)


def GetMicrophoneStatus():
    with open(os.path.join(TempDirPath, 'Mic.data'), "r", encoding='utf-8') as file:
        return file.read()


def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, 'Status.data'), "w", encoding='utf-8') as file:
        file.write(Status)


def GetAssistantStatus():
    with open(os.path.join(TempDirPath, 'Status.data'), "r", encoding='utf-8') as file:
        return file.read()


def MicButtonInitialed():
    SetMicrophoneStatus("False")


def MicButtonClosed():
    SetMicrophoneStatus("True")


def GraphicsDirectoryPath(Filename):
    return os.path.join(GraphicsDirPath, Filename)


def ShowTextToScreen(Text):
    with open(os.path.join(TempDirPath, 'Responses.data'), "w", encoding='utf-8') as file:
        file.write(Text)


def TempDirectoryPath(Filename):
    return os.path.join(TempDirPath, Filename)


class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(400, 270))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-right: 195px; border: none; margin-top: -30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def loadMessages(self):
        global old_chat_message
        with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            if messages and messages != old_chat_message:
                self.addMessage(message=messages, color='White')
                old_chat_message = messages

    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        fmt = QTextCharFormat()
        block_fmt = QTextBlockFormat()
        block_fmt.setTopMargin(10)
        block_fmt.setLeftMargin(10)
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.setBlockFormat(block_fmt)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)


class InitialScreen(QWidget):
    def __init__(self):
        super().__init__()
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        movie.setScaledSize(QSize(screen_width, int(screen_width / 16 * 9)))
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png')).scaled(60, 60)
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.icon_label.mousePressEvent = self.toggle_icon
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px;")
        content_layout.addWidget(gif_label)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path).scaled(width, height)
        self.icon_label.setPixmap(pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'))
            MicButtonClosed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'))
            MicButtonInitialed()
        self.toggled = not self.toggled


class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(""))
        layout.addWidget(ChatSection())
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)


class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.toggled = True
        self.initUI()

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        home_button = QPushButton("Home")
        home_button.setIcon(QIcon(GraphicsDirectoryPath('home.png')))
        home_button.setStyleSheet("height:40px; background-color:white; color: black")
        message_button = QPushButton("Chat")
        message_button.setIcon(QIcon(GraphicsDirectoryPath('Chats.png')))
        message_button.setStyleSheet("height:40px; background-color:white; color: black")
        minimize_button = QPushButton()
        minimize_button.setIcon(QIcon(GraphicsDirectoryPath('Minimize2.png')))
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow)
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
        self.restore_icon = QIcon(GraphicsDirectoryPath('Manimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        close_button = QPushButton()
        close_button.setIcon(QIcon(GraphicsDirectoryPath('Close.png')))
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.closeWindow)
        layout.addWidget(QLabel(f"{Assistantname} AI"))
        layout.addStretch()
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch()
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)

        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        QApplication.quit()

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)

        self.current_screen = message_screen
    
    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        initial_screen = InitialScreen()
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)

        self.current_screen = initial_screen

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget()
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()


