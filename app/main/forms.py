from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField,SelectField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class EditprofileForm(FlaskForm):
	name = StringField('姓名', validators=[Length(0,64)])
	location = StringField('家庭地址', validators=[Length(0,64)])
	about_me = TextAreaField('关于我')
	submit = SubmitField('提交')

class EditprofileAdminForm(FlaskForm):
	email = StringField('电子邮件', validators=[Required(), Length(1,64),Email()])
	username = StringField('用户名', validators=[Required(),Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must have only letters,''numbers,dots or underscored')])
	confirmed = BooleanField('验证')
	role = SelectField('Role', coerce=int)
	name = StringField('姓名', validators=[Length(0,64)])
	location = StringField('家庭地址', validators=[Length(0,64)])
	about_me = TextAreaField('关于我')
	submit = SubmitField('提交')

	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('电子邮件地址已被注册')

	def validate_username(self, field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已被使用')

class PostForm(FlaskForm):
	title = PageDownField('标题')
	body = PageDownField('记录一下今天的心情吧~',validators=[Required()])
	submit = SubmitField('提交')

class CommentForm(FlaskForm):
	body = StringField('写点什么', validators=[Required()])
	submit = SubmitField('提交')
		
