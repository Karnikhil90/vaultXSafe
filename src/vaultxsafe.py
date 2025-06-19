# VaultXSafe - A simple vault application
import sys, os , inspect
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,QFrame,
    QVBoxLayout, QLineEdit, QMainWindow, QStackedWidget,
    QCheckBox, QListWidget, QComboBox, QRadioButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from src.lib.JsonEditor import JsonEditor
from src.lib.FileAccess import FileAccess
from src.vaultEngine import VaultEngine

# DEFAULT values
file_path = "./src/config/config_app.json"
engine = VaultEngine(file_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle(engine.getTitle())
        geometry = engine.getGeometry()
        self.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
        self.setWindowIcon(QIcon(engine.getfile_icon(icon_file_name="app")))

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Page index constants (must come before calling page methods)
        self.LOGIN_PAGE = 0
        self.WELCOME_PAGE = 1
        self.SETTINGS_PAGE = 2
        self.STORE_PASSWORD = 3
        self.STORE_BOOKS = 4
        self.DETAIL_PAGE = 5
        self.BOOK_DETAIL_PAGE = 6

        # Initialize pages
        self.login_page = self.login_page()
        self.welcome_page = self.welcome_page()
        self.settings_page = self.settings_page()
        self.store_password = self.store_password()
        self.store_books = self.store_books()
        # self.detail_page = self.detail_page()

        # Add pages to stack
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.welcome_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.store_password)
        self.stack.addWidget(self.store_books)
        # self.stack.addWidget(self.detail_page)

        # Load stylesheet (engine handles fallback internally)
        self.setStyleSheet(engine.getfile_css_multiple("global" , "store_password","login_page"))

    def login_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        label = QLabel("Enter your name and password")
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setObjectName("loginLabel")
        layout.addWidget(label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.name_input.setObjectName("loginInput")
        layout.addWidget(self.name_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setObjectName("loginInput")
        layout.addWidget(self.pass_input)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setObjectName("loginButton")
        self.submit_btn.clicked.connect(self.handle_submit)
        layout.addWidget(self.submit_btn)

        page.setLayout(layout)
        return page

    def welcome_page(self):
        page = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ─── Top Bar ───
        top_bar = QHBoxLayout()
        back_btn = QPushButton("⏴")
        back_btn.setFixedSize(40, 40)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(self.LOGIN_PAGE))
        back_btn.setToolTip("Back")

        title = QLabel("Welcome to VaultXSafe!")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(40, 40)
        settings_btn.setToolTip("Settings")

        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        top_bar.addWidget(settings_btn)

        main_layout.addLayout(top_bar)
        main_layout.addSpacing(10)
        main_layout.addWidget(title, alignment=Qt.AlignTop | Qt.AlignHCenter)
        main_layout.addSpacing(30)

        # ─── Big Navigation Buttons ───
        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)

        password_btn = QPushButton("🔒\nPassword Store")
        password_btn.setFixedSize(200, 200)
        password_btn.setFont(QFont("Arial", 14))
        password_btn.setStyleSheet("QPushButton { background-color: #aed6f1; border-radius: 20px; }")
        password_btn.setToolTip("Manage your stored passwords")
        password_btn.clicked.connect(lambda: self.stack.setCurrentIndex(self.STORE_PASSWORD))

        book_btn = QPushButton("📚\nBook Store")
        book_btn.setFixedSize(200, 200)
        book_btn.setFont(QFont("Arial", 14))
        book_btn.setStyleSheet("QPushButton { background-color: #a9dfbf; border-radius: 20px; }")
        book_btn.setToolTip("Manage your saved books")

        button_layout.addStretch()
        button_layout.addWidget(password_btn)
        button_layout.addWidget(book_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        page.setLayout(main_layout)
        return page

    def store_password(self):
        # Overview of this page
        # [search_bar] [search_btn]
        # Lable("─── ADD NEW id , pass ────") : add id_password 
        # [id]
        # [password]
        # [gmail,facebook, Other(edit)] 
        # [add_btn]
        page = QWidget()
        page.setObjectName("storePasswordPage")

        main_layout = QVBoxLayout()
        top_bar = QHBoxLayout()
        search_bar = QHBoxLayout()
        add_bar = QVBoxLayout()

        back_btn = QPushButton("⏴")
        back_btn.setFixedSize(40, 40)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(self.WELCOME_PAGE))
        back_btn.setToolTip("Back")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("By ID only...")
        self.search_input.setFixedHeight(40)
        self.search_input.setObjectName("searchInput")

        search_btn = QPushButton("🔍")
        search_btn.setFixedHeight(40)
        search_btn.setFixedWidth(100)
        search_btn.setFont(QFont("Arial", 16, QFont.Bold))
        search_btn.setObjectName("searchButton")
        search_btn.clicked.connect(self.search_btn_clicked)

        add_ID_title = QLabel("Add new UID & Password")
        add_ID_title.setFont(QFont("Arial", 20, QFont.Bold))
        add_ID_title.setAlignment(Qt.AlignCenter)
        add_ID_title.setObjectName("highlightLabel")

        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("Enter a new user ID")
        self.user_id_input.setFixedHeight(40)
        self.user_id_input.setObjectName("formInput")

        self.user_password_input = QLineEdit()
        self.user_password_input.setPlaceholderText("Enter a new user password")
        self.user_password_input.setFixedHeight(40)
        self.user_password_input.setObjectName("formInput")

        self.user_select_type_input = QComboBox()
        self.user_select_type_input.setEditable(True)
        self.user_select_type_input.addItems(engine.get_password_categories())
        # user_select_type_input.setObjectName("comboBox")

        user_ID_password_submit_btn = QPushButton("Submit")
        user_ID_password_submit_btn.setObjectName("submitButton")
        user_ID_password_submit_btn.clicked.connect(self.add_new_userID_clicked)

        # Layout setup
        add_bar.addWidget(add_ID_title)
        add_bar.addWidget(self.user_id_input)
        add_bar.addWidget(self.user_password_input)
        add_bar.addWidget(self.user_select_type_input)
        add_bar.addWidget(user_ID_password_submit_btn)

        search_bar.addWidget(self.search_input)
        search_bar.addWidget(search_btn)
        top_bar.addWidget(back_btn)
        top_bar.addStretch()

        main_layout.addLayout(top_bar)
        main_layout.addLayout(search_bar)
        main_layout.addLayout(add_bar)
        main_layout.addStretch()
        page.setLayout(main_layout)

        return page
    def search_btn_clicked(self):
        search_ = self.search_input.text()
        print(f"SEARCH_QUERY='{search_}'")

    def add_new_userID_clicked(self):
        uid = self.user_id_input.text()
        password = self.user_password_input.text()
        choice = self.user_select_type_input.currentText()
        print(f"UID:{uid} , PASSWORD: {password} ,CHOICE: {choice}")

    def store_books(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Book Store Page"))
        page.setLayout(layout)
        return page

    def settings_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings Page"))
        page.setLayout(layout)
        return page
    
    def handle_submit(self):
        name = self.name_input.text()
        password = self.pass_input.text()6
        print(f"Name: {name}, Password: {password}")
        self.stack.setCurrentIndex(self.WELCOME_PAGE)


class vaultXSafe:
    def __init__(self):
        pass

    @staticmethod
    def main():
        app = QApplication([])
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())


# Entry point
# if __name__ == "__main__":
#     vaultXSafe.main()
