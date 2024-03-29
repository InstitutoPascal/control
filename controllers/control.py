# coding: utf8
# intente algo como
def inicio():
 
 return dict(message="Bienvenido")
 
import os

def backup():
    # Copia de seguridad de la base de datos..
    
    ruta = os.path.join (request.folder, "private" , "backup.csv") 
    arch = open (ruta, "wb")
    db.export_to_csv_file (arch)
    arch.close()
    
    return 'Backup Realizado'
    
def restauracion():
   
   # Restaura la base de datos de seguridad
    ruta = os.path.join (request.folder, "private" , "backup.csv") 
    arch = open (ruta, "rb")
   
    db.import_from_csv_file(arch)
   
    return 'Restauración Completada'
    
import Image, ImageFont, ImageDraw #importo librerias de imagen de python

def codigo_barras():
    "Generar una imágen con el código de barras Interleaved 2 of 5"
    # basado de:
    #  * http://www.fpdf.org/en/script/script67.php
    #  * http://code.activestate.com/recipes/426069/
    
    
    if request.vars:
        
        personaid= request.vars['personaid']
        persona = db(db.personas.personaid==personaid).select(db.personas.dni).first()
        code = str(persona.dni) #convierto el dni "entero" a string y lo guardo en code
        basewidth=3 #parametros de imagen
        height=30 #parametros de imagen
        extension = "PNG" #digo q la imagen se guarde cn la extencion PNG
    
        wide = basewidth
        narrow = basewidth / 3

        # códigos ancho/angostos (wide/narrow) para los dígitos
        bars = ("nnwwn", "wnnnw", "nwnnw", "wwnnn", "nnwnw", "wnwnn", "nwwnn", 
            "nnnww", "wnnwn", "nwnwn", "nn", "wn")

        # agregar un 0 al principio si el número de dígitos es impar
        if len(code) % 2:
            code = "0" + code

        # crear una nueva imágen
        im = Image.new("1",((len(code) * 3) * basewidth + (10 * narrow), height))

        # agregar códigos de inicio y final
        code = "::" + code.lower() + ";:" # A y Z en el original

        # crear un drawer
        draw = ImageDraw.Draw(im)

        # limpiar la imágen
        draw.rectangle(((0, 0), (im.size[0], im.size[1])), fill=256)

        xpos = 0    
        # dibujar los códigos de barras
        for i in range(0,len(code),2):
            # obtener el próximo par de dígitos
            bar = ord(code[i]) - ord("0")
            space = ord(code[i + 1]) - ord("0")
            # crear la sequencia barras (1er dígito=barras, 2do=espacios)
            seq = ""
            for s in range(len(bars[bar])):
                seq = seq + bars[bar][s] + bars[space][s]

            for s in range(len(seq)):
                if seq[s] == "n":
                    width = narrow
                else:
                    width = wide

                # dibujar barras impares (las pares son espacios)
                if not s % 2:
                    draw.rectangle(((xpos,0),(xpos+width-1,height)),fill=0)
                xpos = xpos + width 
       
    # guardar en un archivo la imágen generada
    response.headers['Content-Type']='image/png'
    im.save(response.body, extension.upper())
    return response.body.getvalue()
    
def miniatura():
    
    from PIL import Image 
    from cStringIO import StringIO 
    if request.vars:
        
        personaid= request.vars['personaid']
        persona = db(db.personas.personaid==personaid).select(db.personas.foto).first()
        #code = str(persona.dni)
        #busco el registro con el campo upload
        ruta_foto = os.path.join(request.folder, "uploads", persona.foto) 
        img= Image.open(ruta_foto) #abro la imagen
        img.thumbnail((100,100), Image.ANTIALIAS)
        salida= StringIO()
        img.save(salida,'PNG', quality=86)
        salida.seek(0)
        response.headers['Content-Type']= "image/png"
        
        return salida.getvalue(), response.body.getvalue()
        
def tarjeta():
    # genero tarjetas
    # busco qe haya registros en la bd
    q= db.personas.id>0
    personas = db(q).select(db.personas.nombre, db.personas.personaid) #traigo el id y nombres
        
    return dict (personas = personas)
    
def tarjeta_personal():
    # genero tarjetas
    # busco qe haya registros en la bd
    q= db.personas.id>0
    personas = db(q).select(db.personas.nombre, db.personas.personaid) #traigo el id y nombres

        
    return dict (personas = personas)

import pyttsx
            
def alta_persona():
    subtitulo= T ('Complete el formulario por favor...')
    form=SQLFORM(db.personas)
    if form.accepts(request.vars,session):
        engine= pyttsx.init() #inicio el patron de voz
        engine.setProperty('voice', 'spanish-latin-american') #doy propiedad de audio en español latino
        engine.say('Solicitud aceptada') #indico lo qe se debe ejecutar al iniciar el audio
        engine.runAndWait() #ejecuto la voz
        response.flash='Usted fue agregado...'
        #http://127.0.0.1:8000/control/control/tarjeta_personal
        #redirect(URL(f='tarjeta_personal'))
        
    elif form.errors: 
        engine= pyttsx.init() #inicio el patron de voz
        engine.setProperty('voice', 'spanish-latin-american') #doy propiedad de audio en español latino
        engine.say('Complete el formulario por favor') #indico lo qe se debe ejecutar al iniciar el audio
        engine.runAndWait() #ejecuto la voz
        response.flash='Hay errores en el formulario'
    else:
        response.flash='Por favor, complete el formulario'
        
    return dict (form=form, sub=subtitulo)
def listar():
    movimiento = db().select(db.movimientos.ALL)
    listado=[]
    listado.append(TABLE(TR(TH('ID',_style='width:200px; color:black; background: LimeGreen; border:black solid'),
    TH('Nombre',_style='width:200px; color:black; background:LimeGreen ; border:black solid'), TH('Fecha',_style='width:200px; color:black; background:LimeGreen; border:black solid'), TH('Hora',_style='width:200px; color:black; background:LimeGreen; border:black solid'))))  
   
   #recorre la tupla de datos obtenidos de la consulta sql y la agrega a listado: 
    for x in movimiento:
        
       listado.append(TABLE(TR(TD (x.id,_style='width:200px; color:black; background:white ; border: 2px solid black'),
       TD(x.personaid.nombre,_style='width:200px; color:black; background: white; border: 2px solid black'),TD(x.fecha,_style='width:200px; color:black; background: white; border: 2px solid black'),TD(x.hora,_style='width:200px; color:black; background: white; border: 2px solid black')))) 

    #retorna en una variable los datos insertados en una tabla html formateada con web2py:
    a = DIV(listado)
    return dict (a=a)
