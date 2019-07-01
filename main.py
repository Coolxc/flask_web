#! /usr/bin/python3
# coding:utf-8 
import os
from app import create_app, db
from app.models import User, Role, Post, Follow, Comment
from flask_migrate import Migrate, MigrateCommand
import click
import sys

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Follow=Follow, Comment=Comment)


COV = None
if os.environ.get('FLASK_COVERAGE'):
	import coverage
	COV  = coverage.coverage(branch=True, include='app/*')
	COV.start()


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False)
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    """Run the tests."""
    if coverage and not os.getenv('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('覆盖报告')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version:file://%s/index.html' %covdir)
        COV.erase()


@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
help='Directory where profiler data files are saved.')
def profile(length=25, profile_dir=None):
	from werkzeug.contrib.profiler import ProfilerMiddleware
	app.wagi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
	app.run()


@app.cli.command()
def deploy():
	from flask_migrate import upgrade
	from app.models import Role, User

	upgrade()
	Role.insert_roles()
	User.add_self_follows()
