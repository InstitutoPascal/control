# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

migrate = True

db.define_table('alumnos',
    Field('alumnoid', type='id'),
    Field('nombre', type='string', length=200),
    Field('dni', type='integer'),
    Field('sexo', type='string', length=1),
    Field('fechanacimiento', type='date'),
    Field('lugarnacimiento', type='string', length=250),
    Field('estadocivil', type='string', length=50),
    Field('nacionalidad', type='string', length=50),
    Field('direccion', type='string', length=200),
    Field('localidad', type='string', length=50),
    Field('cp', type='string', length=7),
    Field('telefono', type='string', length=250),
    Field('email1', type='string', length=100),
    Field('email2', type='string', length=100),
    Field('ingreso', type='date'),
    Field('egreso', type='date', readable= False, writable= False),
    Field('foto', type='upload', length=50),
    Field('user_id', db.auth_user, readable= False, writable= False),
    format= "%(alumnoid)s [%(nombre)s]",
    migrate=migrate)
db.alumnos.nombre.requires=IS_NOT_EMPTY(error_message='Ingrese el nombre')
db.alumnos.dni.requires=IS_NOT_EMPTY(error_message='Ingrese el dni')
db.alumnos.sexo.requires=IS_NOT_EMPTY(error_message='Ingrese el sexo')
db.alumnos.fechanacimiento.requires=IS_NOT_EMPTY(error_message='Ingrese la fecha de nacimiento')
db.alumnos.lugarnacimiento.requires=IS_NOT_EMPTY(error_message='Ingrese el lugar de nacimiento')
db.alumnos.estadocivil.requires=IS_NOT_EMPTY(error_message='Ingrese el estado civil')
db.alumnos.nacionalidad.requires=IS_NOT_EMPTY(error_message='Ingrese la nacionalidad')
db.alumnos.direccion.requires=IS_NOT_EMPTY(error_message='Ingrese la direccion')
db.alumnos.localidad.requires=IS_NOT_EMPTY(error_message='Ingrese la localidad')
db.alumnos.cp.requires=IS_NOT_EMPTY(error_message='Ingrese el codigo postal')
db.alumnos.telefono.requires=IS_NOT_EMPTY(error_message='Ingrese el telefono')
db.alumnos.email1.requires=IS_NOT_EMPTY(error_message='Ingrese el email')
db.alumnos.ingreso.requires=IS_NOT_EMPTY(error_message='Ingrese la fecha de ingreso')
