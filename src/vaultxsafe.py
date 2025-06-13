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
        self.detail_page = self.detail_page()

        # Add pages to stack
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.welcome_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.store_password)
        self.stack.addWidget(self.store_books)
        self.stack.addWidget(self.detail_page)

        # Load stylesheet (engine handles fallback internally)
        self.setStyleSheet(engine.getfile_css(css_file_name="button"))

    def login_page(self):
        print(self.login_page.__name__)
        self.stack.setCurrentIndex(self.WELCOME_PAGE)
        page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Enter your name and password")
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        layout.addWidget(self.name_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.handle_submit)
        layout.addWidget(self.submit_btn)
        self.handle_submit() 
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
        page = QWidget()
        self.layout = QVBoxLayout()

        # Top bar: Search + Search Button + Category dropdown + Add
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID...")
        top_bar.addWidget(self.search_input)

        search_btn = QPushButton("🔍")
        search_btn.clicked.connect(self.perform_search)
        top_bar.addWidget(search_btn)

        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems(engine.get_password_categories())
        top_bar.addWidget(self.category_combo)

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.show_add_fields)
        top_bar.addWidget(self.add_btn)

        self.layout.addLayout(top_bar)

        # ID and Password Fields (Initially Hidden)
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("User ID")
        self.id_input.setVisible(False)
        self.layout.addWidget(self.id_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setVisible(False)
        self.layout.addWidget(self.pass_input)
        # Submit Button
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.handle_submit)
        self.layout.addWidget(self.submit_btn)
        self.submit_btn.setVisible(False)
        # Show Add Fields Button    
        self.show_fields_btn = QPushButton("Show Fields")
        self.show_fields_btn.clicked.connect(self.show_add_fields)
        self.layout.addWidget(self.show_fields_btn)
        self.show_fields_btn.setVisible(False)
        # Submit Button
        self.submit_btn = QPushButton("Submit")
        

        # Scrollable List (Initially Hidden)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVisible(False)

        self.content_widget = QWidget()
        self.card_layout = QVBoxLayout()
        self.content_widget.setLayout(self.card_layout)

        self.scroll.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll)

        page.setLayout(self.layout)
        return page

    def show_add_fields(self):
        self.id_input.setVisible(True)
        self.pass_input.setVisible(True)

    def perform_search(self):
        keyword = self.search_input.text().lower()
        found = False

        # Remove all existing widgets
        while self.card_layout.count():
            item = self.card_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Add card if match found (for demo, show any non-empty result)
        if keyword:
            card = self.create_password_card(keyword)
            self.card_layout.addWidget(card)
            found = True

        self.scroll.setVisible(found)

    def create_password_card(self, id_text):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 10px;")
        card_layout = QHBoxLayout()

        label = QLabel(f"ID: {id_text}")
        label.setFont(QFont("Arial", 12))
        card_layout.addWidget(label)

        card_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        open_btn = QPushButton("Open")
        open_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        card_layout.addWidget(open_btn)

        card.setLayout(card_layout)
        return card

    def detail_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.detail_label = QLabel("Password Details View")
        self.detail_label.setFont(QFont("Arial", 16))
        layout.addWidget(self.detail_label)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(back_btn)

        page.setLayout(layout)
        return page











    def settings_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings Page"))
        page.setLayout(layout)
        return page


    def store_books(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Book Store Page"))
        page.setLayout(layout)
        return page

    def handle_submit(self):
        name = self.name_input.text()
        password = self.pass_input.text()
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
