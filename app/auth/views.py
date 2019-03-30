from flask import render_template, redirect, request, url_for, flash, session
from . import auth
from flask_login import login_user, login_required, logout_user,current_user
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from .. import db
from ..email import send_email


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('退出登录.')
	return redirect(url_for('main.index'))


@auth.route('/login',methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		else:
			session['email'] = form.email.data
			flash('用户名或密码错误')
			return redirect(url_for('auth.login'))	
	return render_template('auth/login.html', form=form, email=session.get('email'))


@auth.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, username=form.username.data,password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email,'确认你的账户','auth/email/confirm',user=user,token=token)
		flash('确认信息已经发送到你的邮箱.')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		db.session.commit()
		flash('你已经确认了你的账户')
	else:
		flash('验证链接失效或非法.')
	return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' and request.endpoint != 'static':
			return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, '确认你的账户','auth/email/confirm',user=current_user,token=token)
	flash('一个新的确认账户邮件已经发送到你的邮箱.')
	return redirect(url_for('main.index'))


@auth.route('/accout')
@login_required
def accout():
	return render_template('auth/accout.html')


@auth.route('/Change_password')
@login_required
def change_password():
	flash('邮件已发送到你的邮箱')
	send_email(current_user.email,'更改你的密码','auth/email/change_password',user=current_user)
	return render_template('auth/accout.html')


@auth.route('/change_p',methods=['GET','POST'])
@login_required
def change_p():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=current_user.username).first()
		user.username = form.username.data
		user.password = form.new_password1.data
		return redirect(url_for('auth.login'))
	return render_template('auth/change_p.html',form=form)

@auth.route('/reset_password/<email>',methods=['GET','POST'])
def reset_password(email):
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=email).first()
		user.password = form.new_password1.data
		return redirect(url_for('auth.login'))
	return render_template('auth/change_p.html',form=form)



@auth.route('/forget_password/<email>')
def forget_password(email):
	form = LoginForm()
	flash('邮件已发送到你的邮箱')
	send_email(email,'这封邮件用来更改你的密码','auth/email/forget_password',user=current_user,email=email)
	return render_template('auth/login.html',form=form)


@auth.route('/Change_email')
def change_email():
	pass