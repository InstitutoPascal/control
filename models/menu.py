# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://127.0.0.1:8000/control/control/alta_persona")
response.title = request.application.replace('_',' ').title()
response.subtitle = T('')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Inicio'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (SPAN('Registro Nuevo', _class='highlighted'), False, 'http://127.0.0.1:8000/control/control/alta_persona',[
        ])
        #(T('Movimientos', _class='highlighted'), False, URL('control','listar'), [])
         ]
    response.menu += [
        (SPAN('Movimientos', _class='highlighted'), False, 'http://127.0.0.1:8000/control/control/listar', [])
         ]
         
if DEVELOPMENT_MENU: _()
