# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import pyttsx #importo librerias de audio

def index():
    # armo un formulario para buscar alumno por su dni
    form = SQLFORM.factory(
        Field("dni", "integer"),
        )
    q= db.personas.id>0
    if form.accepts(request.vars, session):
        
        # buscar el alumno
        q = db.personas.dni == form.vars.dni
        persona = db(q).select().first()
        if persona:
            # encontrado, redirigo al menu alumnos en ficha, en codigo d barras, miniatura y tarjeta
            redirect(URL(f=ficha, vars={'personaid': persona.personaid}))
            redirect(URL(f=codigo_barras, vars={'personaid': persona.personaid}))
            redirect(URL(f=miniatura, vars={'personaid': persona.personaid}))
            redirect(URL(f=tarjeta, vars={'personaid': persona.personaid}))
            
            
        #else:
         #   engine= pyttsx.init() #inicio el patron de voz
          #  engine.setProperty('voice', 'spanish-latin-american') #doy propiedad de audio en español latino
           # engine.say('No se encuentra registrado') #digo lo qe se debe ejecutar al iniciar el audio
            #engine.runAndWait() #ejecuto la voz
            #response.flash = "Datos invalidos..."  
            
    else:
        response.flash= "Bienvenido !!!"
    
    #response.view = "generic.html"  # HACER una vista de verdad
    
        
    return dict (form = form)
 

   
def ficha():
    if request.vars:
        fecha = request.now.date()
        hora = request.now.time()
        personaid= request.vars['personaid']
        #nombre= db(db.personas.nombre).select(db.personas.personaid==personaid)
        db.movimientos.insert(personaid=personaid, fecha=fecha, hora=hora)
        response.flash='Usted fue registrado...'
        
        # si me pasan en la URL el docente, lo filtro 
        q=db.personas.personaid == personaid
        persona= db(q).select(db.personas.personaid, db.personas.nombre, db.personas.dni, db.personas.foto).first()
        #engine= pyttsx.init()
        #engine.setProperty('voice', 'spanish-latin-american')
        #engine.say('Bienvenido %s' %persona.nombre)
        #traigo el registro directamente de la consulta para q el audio lo reproduzca
        #engine.runAndWait()
    
    return dict (persona=persona)
    
    

        
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
