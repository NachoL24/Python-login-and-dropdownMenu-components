from flask import Flask, render_template, url_for, request, redirect, flash, session
import secrets
from templates.authComponent.authComponent import AuthComponent
from templates.dropdownMenuComponent.dropdownMenu import DropdownMenuComponent
import os
from categories import categories
#la app se corre desde este archivo con "python app.py", "flask run" o "flask run --debug" en la consola de esta carpeta
app = Flask(__name__)


db_path = os.path.join(os.path.dirname(__file__), 'database/database.db')
auth = AuthComponent(session, db_path)
dropdownMenu = DropdownMenuComponent(categories)

app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    if 'email' in session:
        print(f'Logged in as {session["email"].split("@")[0]}')
        flash(f'bienvenido {session["email"].split("@")[0]}', 'info')
        return render_template('indexLogout.html', email=session['name'].split(" ")[0], dropdownMenu=dropdownMenu.generate_menu(), style=dropdownMenu.getStyle(), script=dropdownMenu.getScript(), dropdownImportStyle=dropdownMenu.getStyleImports(), dropdownImportScritp=dropdownMenu.getScriptImports())
    else:
        print('You are not logged in')
        return render_template('indexLogin.html', dropdownMenu=dropdownMenu.generate_menu(), style=dropdownMenu.getStyle(), script=dropdownMenu.getScript(), dropdownImportStyle=dropdownMenu.getStyleImports(), dropdownImportScritp=dropdownMenu.getScriptImports())

@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth.login(request)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return auth.register(request)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return auth.logout()

if __name__ == '__main__':
    app.run(debug=True)
