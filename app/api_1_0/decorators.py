from functools import wraps
from .errors import forbidden
from flask import g

def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not g.current_user.can(permission):
				return forbidden('无效身份')
			return f(*args, **kwargs)
		return decorated_function
	return decorator