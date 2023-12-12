__version__ = '0.1.0'


import pyotp
from flask import Flask, flash, redirect, render_template, request, url_for
from tinydb import Query

from otpauth.util import extract_num_from_str, qrcode_base64

from .database import get_users_tbl

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return render_template('login.jinja2')


@app.route('/login', methods=['POST'])
def login():
    if request.form:
        query = Query()
        model = get_users_tbl()

        users = model.search(query.cpf == request.form.get('cpf'))
        if len(users) == 0:
            flash('CPF not found!', 'error')
            return redirect(url_for('index'))

        user = users[0]
        pin = extract_num_from_str(request.form.get('pin'))

        totp = pyotp.TOTP(user['secret'])
        if not totp.verify(pin):
            flash('Verification failed!', 'error')
            return redirect(url_for('index'))

        flash('Logged!')
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.form:
        if request.form['stage'] == 'register':
            query = Query()
            model = get_users_tbl()
            if len(model.search(query.cpf == request.form.get('cpf'))) > 0:
                flash('CPF already registered!', 'error')
                return redirect(url_for('register'))
            data = {}
            data['name'] = request.form.get('name')
            data['birthday'] = request.form.get('birthday')
            data['cpf'] = request.form.get('cpf')

            secret = pyotp.random_base32()
            data['secret'] = secret

            model.insert(data)

            uri = pyotp.totp.TOTP(secret).provisioning_uri(
                name=data['cpf'], issuer_name='OTP Auth'
            )

            data_qrcode_img = qrcode_base64(uri)

            flash(
                'New user registered! Proceed with the OTP authentication setup stage',
                'success',
            )
            return render_template(
                'register.jinja2',
                otp_stage=True,
                data_qrcode_img=data_qrcode_img,
                user_cpf=data['cpf'],
            )

        if request.form['stage'] == 'validate':
            cpf = request.form.get('cpf')
            pin = extract_num_from_str(request.form.get('pin'))

            query = Query()
            model = get_users_tbl()
            user = model.search(query.cpf == cpf)[0]

            totp = pyotp.TOTP(user['secret'])
            if not totp.verify(pin):
                uri = pyotp.totp.TOTP(user['secret']).provisioning_uri(
                    name=user['cpf'], issuer_name='OTP Auth'
                )

                data_qrcode_img = qrcode_base64(uri)

                flash('Verification failed!', 'error')
                return render_template(
                    'register.jinja2',
                    otp_stage=True,
                    data_qrcode_img=data_qrcode_img,
                    user_cpf=user['cpf'],
                )
            flash('Successfully registered and validated user!', 'success')
            return redirect(url_for('index'))

    return render_template('register.jinja2')


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))
