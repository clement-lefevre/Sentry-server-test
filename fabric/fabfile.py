# -*- coding: utf8 -*-

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import *

#####
# Host(s), user and password(s)
env.hosts = ['10.1.250.185']
env.user = 'test'
env.password = 'test'
#####

#####
# Directory where we works : root dir and working dir.
root_path = '/tmp'
working_dir =  'test_fabric'
#####

#####
# Database configuration
#####
# Instructions :
# engine :
# 	- SQLite : put 'sqlite' at engine, let simple quotes to other vars.
# 	- Postgresql/MySQL : put 'pgsql' for the first, 'mysql' for the second
#	  to engine into simple quotes, then complete others variables :
#	  name refers to base's name, others variables have clear significations.
#####
ENGINE = ''
name = ''
user = ''
password = ''
host = ''
port = ''
#####

def create_dir() :
	with cd(root_path) :
		if exists(working_dir) :
			print "Directory already exists !"

			if confirm("Remove directory and contents ?") :
				run("rm -Rf " + working_dir)
		else :
			run("mkdir " + working_dir)



def create_venv() :
	if exists (".venv/bin/activate") :
		print "Virtualenv already exists."

		if confirm("Remove it ?") :
			run("rm -Rf .venv")
			run("virtualenv .venv")

	else :
		run("virtualenv .venv")



def install_sentry() :
	if exists(".venv/bin/sentry") :
		print "Sentry and dependencies seems to be installed."

		if confirm("Make clean install of virtualenv (remove it) ?") :
			run("rm -Rf .venv")
			create_venv()

		else :
			if confirm("Update ? (if not, it will do nothing)") :
				run("pip install -U sentry")

	else :
		run("pip install sentry")



def update_sentry() :
	print "It will update Sentry and all dependencies !"
	if confirm("Continue anyway ?") :
		run("pip install -U sentry")



def sentry_create_conf() :
	run("sentry init sentry.conf.py")



def sentry_conf_db() :
	if ENGINE == 'sqlite' :
		ENGINE = "'django.db.backends.sqlite3',"
		name = "os.path.join(CONF_ROOT, 'sentry.db'),"
		user = env.user
	else :
		if ENGINE == 'pgsql' :
			engine = "'django.db.backends.postgresql_psycopg2',"
		elif ENGINE == 'mysql' :
			engine = "'django.db.backends.mysql',"
		else :
			print "Unknown database engine"
			Py_Exit(-1)

	run("sentry --config=sentry.conf.py upgrade")



def run_server() :
	run("sentry --config=sentry.conf.py start")



def install_all() :
	create_dir()
	with cd(root_path + "/" + working_dir) :
		create_venv()
		with prefix("source .venv/bin/activate") :
			install_sentry()
			sentry_create_conf()
			sentry_conf_db()
			run_server()