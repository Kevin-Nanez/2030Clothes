import dotenv
from flask import flash, jsonify, Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, \
    AnonymousUserMixin
from crypto import eth_price
import os
from dotenv import load_dotenv, dotenv_values

# Configurations
app = Flask(__name__)
load_dotenv()
config = dotenv_values(".env")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['APP_BASE_URL'] = os.getenv('APP_BASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login Setup
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Modelos
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    address = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    phone_num = db.Column(db.String(50))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    img_url = db.Column(db.String(100))
    gender = db.Column(db.String(10))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_ids = db.Column(db.String(100))
    units = db.Column(db.String(100))
    total_price = db.Column(db.Float)
    date = db.Column(db.String(100))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_ids = db.Column(db.String(100))
    units = db.Column(db.String(100))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Line below only required once, when creating DB.
# with app.app_context():
#    db.create_all()
# Functions

def modifica_cadena(indice, cadena):
    # Convertir la cadena en una lista
    lista = list(cadena)
    # Aumentar en 1 el valor del número en el índice especificado
    numero = int(lista[indice])
    numero += 1
    lista[indice] = str(numero)
    # Convertir la lista de nuevo en una cadena
    nueva_cadena = ' '.join(lista)
    return nueva_cadena


# Routes Rendering

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():  # put application's code here
    print(eth_price, "aqui esta api")
    if current_user.is_authenticated:
        user_name = current_user.name
        return render_template('Index.html', user_name=user_name, logged_in=current_user.is_authenticated)
    else:
        return render_template('Index.html')


@app.route('/carro_compras')
def carro_compras():  # put application's code here
    if isinstance(current_user, AnonymousUserMixin):
        return redirect("/login_modal")
    cart_list = []
    total = 0
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first().to_dict()
        productos_ids = cart["product_ids"].split()
        unidades = cart["units"].split()
        pares = zip(productos_ids, unidades)
        dictionary = dict(pares)
        for key in dictionary.keys():
            product = Products.query.filter_by(id=key).first().to_dict()
            new = {
                "id": int(product["id"]),
                "units": int(dictionary[key]),
                "img_url": product["img_url"],
                "price": int(product["price"]),
                "name": product["name"]
            }
            cart_list.append(new)
            total += new["price"] * int(new["units"])
    return render_template('carro-compras.html', cart_list=cart_list, total=total,
                           logged_in=current_user.is_authenticated, eth_mxn=eth_price)


@app.route('/formato')
def formato():  # put application's code here
    return render_template('Formato.html')


@app.route('/hombre1', methods=["POST", "GET", "DELETE"])
def hombre1():  # put application's code here
    if isinstance(current_user, AnonymousUserMixin):
        return redirect("/login_modal")
    cart_list = []
    user_id = 0
    total = 0
    products = [product.to_dict() for product in Products.query.filter_by(gender="male").all()]
    if current_user.is_authenticated:
        user_id = current_user.id
        cart = Cart.query.filter_by(user_id=current_user.id).first().to_dict()
        productos_ids = cart["product_ids"].split()
        unidades = cart["units"].split()
        pares = zip(productos_ids, unidades)
        dictionary = dict(pares)
        for key in dictionary.keys():
            product = Products.query.filter_by(id=key).first().to_dict()
            new = {
                "id": int(product["id"]),
                "units": int(dictionary[key]),
                "img_url": product["img_url"],
                "price": int(product["price"]),
                "name": product["name"]
            }
            cart_list.append(new)
            total += new["price"] * int(new["units"])
    if request.method == "GET":
        return render_template('hombre1.html', user_id=user_id, products=products, cart_list=cart_list, total=total,
                               logged_in=current_user.is_authenticated)
    if request.method == "POST":
        print("post")
        for boton in request.form:
            if boton.startswith('button_'):
                id_boton = boton.split('_')[1]
                user_cart = Cart.query.filter_by(user_id=current_user.id).first()
                productos_ids = user_cart.product_ids.split()
                if str(id_boton) not in productos_ids:
                    user_cart.product_ids += " " + id_boton
                    user_cart.units += " 1"
                    db.session.commit()
                else:
                    indice = productos_ids.index(id_boton)
                    user_cart.units = modifica_cadena(indice, unidades)
                    db.session.commit()
        return redirect(url_for('hombre1'))


@app.route('/hombres')
def hombres():  # put application's code here
    return render_template('hombres.html')


@app.route('/landing_page')
def landing_page():  # put application's code here
    return render_template('landingPage.html')


@app.route('/login_modal', methods=["POST", "GET"])
def login_modal():  # put application's code here
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Ese email no existe, vuelve a intentarlo")
            return redirect(url_for('login_modal'))
            # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Contraseña incorrecta. ')
            return redirect(url_for('login_modal'))
            # Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for("home"))
    else:
        return render_template('login.modal.html', logged_in=current_user.is_authenticated)


@app.route('/mujer', methods=["POST", "GET"])
def mujer():  # put application's code here
    if isinstance(current_user, AnonymousUserMixin):
        return redirect("/login_modal")
    cart_list = []
    total = 0
    user_id = 0
    products = [product.to_dict() for product in Products.query.filter_by(gender="female").all()]
    if current_user.is_authenticated:
        user_id = current_user.id
        cart = Cart.query.filter_by(user_id=current_user.id).first().to_dict()
        productos_ids = cart["product_ids"].split()
        unidades = cart["units"].split()
        pares = zip(productos_ids, unidades)
        dictionary = dict(pares)
        for key in dictionary.keys():
            product = Products.query.filter_by(id=key).first().to_dict()
            new = {
                "id": int(product["id"]),
                "units": int(dictionary[key]),
                "img_url": product["img_url"],
                "price": int(product["price"]),
                "name": product["name"]
            }
            cart_list.append(new)
            total += new["price"] * int(new["units"])
    if request.method == "GET":
        return render_template('mujer.html', user_id=user_id, products=products, cart_list=cart_list, total=total,
                               logged_in=current_user.is_authenticated)
    if request.method == "POST":
        for boton in request.form:
            if boton.startswith('button_'):
                id_boton = boton.split('_')[1]
                user_cart = Cart.query.filter_by(user_id=current_user.id).first()
                productos_ids = user_cart.product_ids.split()
                if str(id_boton) not in str(productos_ids):

                    user_cart.product_ids += " " + id_boton
                    user_cart.units += " 1"
                    db.session.commit()
                else:
                    indice = productos_ids.index(id_boton)
                    user_cart.units = modifica_cadena(indice, unidades)
                    db.session.commit()
        return redirect("/mujer")


@app.route('/mujeres', methods=["GET", "POST"])
def mujeres():  # put application's code here
    return render_template('mujeres.html')


@app.route('/nosotros')
def nosotros():  # put application's code here
    return render_template('nosotros.html')


@app.route('/selecproducto')
def producto():  # put application's code here
    id_producto = request.args.get("id_producto")
    producto = Products.query.filter_by(id=id_producto).first()
    return render_template('selecproducto.html', producto=producto.to_dict())


@app.route('/registro_modal', methods=["POST", "GET"])
def registro_modal():  # put application's code here
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        phone = request.form.get('phone_number')
        zip = request.form.get('zip_code')
        address = request.form.get('address')
        if User.query.filter_by(email=request.form.get('email')).first():
            # User already exists
            flash("Ya hay un usuario con ese email, prueba con otro. ")
            return redirect(url_for('registro_modal'))
        hash_and_salted_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=email,
            name=name,
            password=hash_and_salted_password,
            address=address,
            phone_num=phone,
            zip_code=zip
        )
        db.session.add(new_user)
        db.session.flush()
        new_cart = Cart(
            user_id=new_user.id,
            product_ids="",
            units=""
        )
        db.session.add(new_cart)
        db.session.commit()
        return render_template("login.modal.html")
    else:
        return render_template('registro-modal.html', logged_in=current_user.is_authenticated)


@login_required
@app.route("/actualizarcarrito", methods=["POST"])
def actualizar_carrito():
    if request.method == "POST":
        user_id = current_user.id
        products_ids = request.args.get("products_ids")
        units = request.args.get("units")
    cart = Cart.query.filter_by(user_id=user_id).first()
    cart.product_ids = products_ids
    cart.units = units
    db.session.commit()
    return jsonify(response={"success": "exito, se actualizo el correctamente"}), 200


@login_required
@app.route("/carrito/eliminarproducto", methods=["DELETE"])
def eliminar_decarrito():
    user_id = request.args.get("id")
    carrito = Cart.query.filter_by(user_id=user_id).first()
    product_id = request.args.get("product_id")
    unidades_list = carrito.units.split()
    product_list = carrito.product_ids.split()
    print(product_list, product_id, user_id)
    indice = product_list.index(product_id)
    unidades_list.pop(indice)
    product_list.pop(indice)
    unidades = ' '.join(unidades_list)
    productos = " ".join(product_list)
    carrito.units = unidades
    carrito.product_ids = productos
    db.session.commit()
    return jsonify(response={"response": "si"}), 200


@login_required
@app.route("/carrito/disminuirproducto", methods=["DELETE"])
def disminuir_decarrito():
    user_id = request.args.get("id")
    carrito = Cart.query.filter_by(user_id=user_id).first()
    product_id = request.args.get("product_id")
    unidades_list = carrito.units.split()
    product_list = carrito.product_ids.split()
    indice = product_list.index(product_id)
    # Aumentar en 1 el valor del número en el índice especificado
    numero = int(unidades_list[indice])
    numero -= 1
    unidades_list[indice] = str(numero)
    # Convertir la lista de nuevo en una cadena
    nueva_cadena = ' '.join(unidades_list)
    carrito.units = nueva_cadena
    db.session.commit()
    return jsonify(response={"response": "si"}), 200


@login_required
@app.route("/carrito/aumentarproducto", methods=["PUT"])
def aumentar_decarrito():
    user_id = request.args.get("id")
    carrito = Cart.query.filter_by(user_id=user_id).first()
    product_id = request.args.get("product_id")
    unidades_list = carrito.units.split()
    product_list = carrito.product_ids.split()
    indice = product_list.index(product_id)
    # Aumentar en 1 el valor del número en el índice especificado
    numero = int(unidades_list[indice])
    numero += 1
    unidades_list[indice] = str(numero)
    # Convertir la lista de nuevo en una cadena
    nueva_cadena = ' '.join(unidades_list)
    carrito.units = nueva_cadena
    db.session.commit()
    return jsonify(response={"response": "si"}), 200


@app.route("/carrito", methods=["GET"])
def ver_carrito():
    user_id = current_user.id
    cart = Cart.query.filter_by(user_id=user_id).first()
    return jsonify(spots=cart.to_dict()), 200


@app.route('/productos/agregar', methods=["POST"])
def agregar_producto():
    new_product = Products(
        name=request.args.get("name"),
        description=request.args.get("description"),
        price=request.args.get("price"),
        stock=request.args.get("stock"),
        img_url=request.args.get("img_url"),
        gender=request.args.get("gender")
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(response={"success": "Añadido"}), 200


@app.route('/selecproducto')
def selecproducto():  # put application's code here
    return render_template('selecproducto.html')


@app.route('/productos')
def productos():
    productos = db.session.query(Products).all()
    productos = [productos.to_dict() for producto in productos]
    return jsonify(productos=productos), 200


@app.route('/verproducto')
def ver_producto():
    id = request.args.get("id")
    producto = Products.query.filter_by(id=id).first()
    if producto:
        return jsonify(response=producto.to_dict()), 200
    else:
        return jsonify(response={"message": "ese producto no existe"}), 404


if __name__ == '__main__':
    app.run()
