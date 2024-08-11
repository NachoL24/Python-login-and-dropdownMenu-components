from flask import render_template, url_for, redirect, flash
from .authInterface import AuthInterface
import sqlite3

class AuthComponent(AuthInterface): 
    def __init__(self,s, db_path:str | None ='database.db'):
        self.__s = s
        self.db = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()
        
    def login(self, request):
        if request.method == 'POST':
            print("logueando")
            print(request.form['email'])
            print(request.form['password'])
            if request.form['email'] == '' or request.form['password'] == '':
                print('Los campos no pueden estar vacios')
                flash('Los campos no pueden estar vacios', 'warning')
                return render_template('authComponent/templates/login.html')
            else:
                user = self.login_user(request.form['email'], request.form['password'])
                if not user:
                    print('Usuario no encontrado')
                    flash('Usuario no encontrado', 'warning')
                    return render_template('authComponent/templates/login.html')
                self.__s['email'] = request.form['email']
                self.__s['password'] = request.form['password']
                self.__s['name'] = user[2]
                return redirect(url_for('home'))
        else:
            return render_template('authComponent/templates/login.html')

    def register(self, request):
        if request.method == 'POST':
            print(request.form['name'])
            print(request.form['email'])
            print(request.form['password'])
            print(request.form['confirm_password'])
            if request.form['password'] != request.form['confirm_password']:
                flash('Las contraseñas no coinciden', 'warning')
                return render_template('authComponent/templates/register.html', error='Passwords do not match')
            elif request.form['email'] == '' or request.form['password'] == '' or request.form['confirm_password'] == '' or request.form['name'] == '':
                flash('Los campos no pueden estar vacios', 'warning')
                return render_template('authComponent/templates/register.html', error='Fields cannot be empty')
            elif len(request.form['password']) < 8:
                flash('La contraseña debe tener al menos 8 caracteres', 'warning')
                return render_template('authComponent/templates/register.html', error='Password must be at least 8 characters')
            elif ' ' in request.form['name']:
                flash('El nombre no puede tener espacios', 'warning')
                return render_template('authComponent/templates/register.html', error='Name cannot have spaces')
            else:
                if(self.register_user(request.form['email'], request.form['name'], request.form['password'])):
                    print('Usuario registrado correctamente')
                    return self.login(request)
                else:
                    print('El usuario ya existe')
                    flash('El usuario ya existe', 'warning')
                    return render_template('authComponent/templates/register.html', error='User already exists')
        else:
            return render_template('authComponent/templates/register.html')
    
    def logout(self):
        self.__s.pop('email', None)
        self.__s.pop('password', None)
        return redirect(url_for('home'))

    def register_user(self, email, name, password):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            if user:
                return False
            else:
                cursor.execute('INSERT INTO users (email, name, password) VALUES (?, ?, ?)', (email, name, password))
                conn.commit()
                return True

    def login_user(self, email, password):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            return cursor.fetchone()
            