from market import app
from flask import render_template, url_for, redirect, flash, send_from_directory, request, jsonify
from market.model import Item, User, Cart, Order
from market.forms import RegisterForm, LoginForm, ChangePasswordForm, ShopItemForm, OrderForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

import stripe

publishable_key ='pk_test_51O82EHFB9TUhHIlDj2QhNo7K8WhYGe7SM8LoQ44JQfIUselH8OgvG9jlFGrO4rYMJdkCeaF3F7lmHAqkTr656rYr00HV372zjs'
stripe.api_key = 'sk_test_51O82EHFB9TUhHIlDua9VUsJbFENZn6ujrxQ1dPQZicZPwPu2rXTRPh0RHE7ycIzpiMSkXpET92ZmSM6ES2DV5sMZ00rTubXKAe'

@app.route('/payment', methods=['POST'])
def payment():
    cart = Cart.query.filter_by(user_link=current_user.id).all()

    amount = 0

    for item in cart:
        amount += item.item.price * item.quantity
        total = amount + 200
        amount1 = (total * 100)

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
        customer=customer.id,
        description='T-shirt',
        amount=amount1,
        currency='usd'
    )
    return redirect(url_for("thanks"))

@app.route('/thanks')
def thanks():
    return render_template('thank.html')

""" from market.test import API_PUBLISHABLE_KEY, API_TOKEN, APIService """
"""
API_PUBLISHABLE_KEY = 'ISPubKey_test_f6027e69-2ca7-40a2-9c06-5e53d770b3f4'
API_TOKEN = 'ISPubKey_test_f6027e69-2ca7-40a2-9c06-5e53d770b3f4'
"""


@app.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/shop')
@login_required
def shop_page():
    items = Item.query.all()
    cart = Cart.query.filter_by().all
    return render_template('shop.html', items=items, cart=cart if current_user.is_authenticated else [])

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_create = User(username=form.username.data,
                           email_addr=form.email_addr.data,
                           password=form.password1.data)
        db.session.add(user_create)
        db.session.commit()
        login_user(user_create)
        flash(f'Account created! {user_create.username}', category='success')
        return redirect(url_for('shop_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'error with creating user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_login = User.query.filter_by(username=form.username.data).first()
        if user_login and user_login.check_password_correction(attempted_password=form.password1.data):
            login_user(user_login)
            flash(f'You are logged in {user_login.username}', category='success')
            return redirect(url_for('shop_page'))
        else:
            flash('Username or password not match', category='danger')


    return render_template('login.html', form=form)

@app.route('/add-cart/<int:item_id>', methods=['GET', 'POST'])
@login_required
def cart_add(item_id):
    item_to_add = Item.query.get(item_id)
    if not item_to_add:
        flash("Item not found", "error")
        return redirect(url_for('show_cart'))

    item_exists = Cart.query.filter_by(user_link=current_user.id, item_link=item_id).first()
    if item_exists:
        item_exists.quantity = item_exists.quantity + 1
        db.session.commit()
        flash(f' Quantity of {item_exists.item.name} has been updated', category='success')
        return redirect(request.referrer)
    else:
        new_cart_item = Cart(user_link=current_user.id, item_link=item_id, quantity=1)
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.item.name} added to cart', category='success')

    return redirect(request.referrer)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You are logout', category='info')
    return redirect(url_for("home_page"))

@app.route('/profile/<int:user_id>', endpoint='profile')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)


@app.route('/change-password/<int:user_id>', endpoint='change_password', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    user = User.query.get(user_id)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        if user.check_password_correction(current_password):
            if new_password == confirm_password:
                user.password = confirm_password
                db.session.commit()
                flash("Password Updated!")
                return redirect(f'/profile/{user.id}')
        else:
            flash('Password not match')

    return render_template('change_pass.html', form=form, user=user)


@app.route('/add-shop-item', methods=['GET', 'POST'])
@login_required
def admin_add_page():
    if current_user.id == 1:
        form = ShopItemForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            price = form.price.data
            in_stock = form.in_stock.data
            file = form.product_image.data
            add_product = form.add_product.data
            update_product = form.update_product

            file_name = secure_filename(file.filename)

            file_path = f'./media/{file_name}'
            file.save(file_path)

            new_shop_item = Item()
            new_shop_item.name = product_name
            new_shop_item.price = price
            new_shop_item.stock = in_stock

            new_shop_item.item_picture = file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added successfully', category='success')
                return  render_template('add-shop-item.html', form=form)
            except Exception as e:
                print(e)
                flash(f'{product_name} Failed', category='danger')


        return render_template('add-shop-item.html', form=form)

    return render_template(404)

@app.route('/shop-item', methods=['GET','POST'])
@login_required
def shop_item():
    if current_user.id == 1:
        items = Item.query.order_by(Item.date_added).all()
        return render_template('shop-item.html', items=items)

    return render_template(404)


@app.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 1:
        form = ShopItemForm()

        item_update = Item.query.get(item_id)
        form.product_name.render_kw = {'placeholder': item_update.name}
        form.price.render_kw = {'placeholder': item_update.price}
        form.in_stock.render_kw = {'placeholder': item_update.stock}


        if form.validate_on_submit():
            product_name = form.product_name.data
            price = form.price.data
            in_stock = form.in_stock.data

            file = form.product_image.data

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'

            file.save(file_path)

            try:
                Item.query.filter_by(id=item_id).update(dict(name=product_name,
                                                             price=price,
                                                             stock=in_stock,
                                                             item_picture=file_path))
                db.session.commit()
                flash(f'{product_name} has be updated', category='success')
                return redirect('/shop-item')
            except Exception as e:
                print(e)
                flash(f'{product_name} not updated', category='danger')

        return render_template('update_item.html', form=form)

    return render_template(404)


@app.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1:
        try:
            item_delete = Item.query.get(item_id)
            db.session.delete(item_delete)
            db.session.commit()
            flash('item deleted', category='Success')
            return redirect('/shop-item')
        except Exception as e:
            flash('item not deleted', category='danger')
        return redirect('/shop-item')

    return render_template(404)


@app.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(user_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += float(item.item.price * item.quantity)

    return render_template('cart.html', cart=cart, amount=amount, total=amount+200)


@app.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity += 1
        db.session.commit()

        cart = Cart.query.filter_by(user_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.item.price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)


@app.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity - 1
        db.session.commit()

        cart = Cart.query.filter_by(user_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.item.price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)

@app.route('/removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(user_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.item.price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)

@app.route('/customer')
@login_required
def display_customer():
    if current_user.id == 1:
        users = User.query.all()
        return render_template('user.html', users=users)
    return render_template(404)

@app.route('/admin-page')
@login_required
def admin_page():
    items = Item.query.all()
    user = User.query.all()
    if current_user.id == 1:
        return render_template('admin.html', items=items, user=user)
    return render_template(404)

@app.route('/view-orders')
@login_required
def order_view():
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('order.html', orders=orders)
    return render_template(404)


@app.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id == 1:
        form = OrderForm()

        order = Order.query.get(order_id)

        if form.validate_on_submit():
            status = form.order_status.data
            order.status = status

            try:
                db.session.commit()
                flash(f'Order {order_id} Updated successfully')
                return redirect('/view-orders')
            except Exception as e:
                print(e)
                flash(f'Order {order_id} not updated')
                return redirect('/view-orders')

        return render_template('order_update.html', form=form, order=order)

    return render_template('404.html')