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
    
import Image, ImageFont, ImageDraw

def codigo_barras():
    "Generar una imágen con el código de barras Interleaved 2 of 5"
    # basado de:
    #  * http://www.fpdf.org/en/script/script67.php
    #  * http://code.activestate.com/recipes/426069/
    
    #im= Image.new("1",(0,0))
    #im = Image.new("1",((8 * 3) * 3 + (10 * 1), 30))
    if request.vars:
        
        personaid= request.vars['personaid']
        persona = db(db.personas.personaid==personaid).select(db.personas.dni).first()
        code = str(persona.dni)
        basewidth=3
        height=30
        extension = "PNG"
    
        wide = basewidth
        narrow = basewidth / 3

        # códigos ancho/angostos (wide/narrow) para los dígitos
        bars = ("nnwwn", "wnnnw", "nwnnw", "wwnnn", "nnwnw", "wnwnn", "nwwnn", 
            "nnnww", "wnnwn", "nwnwn", "nn", "w        personaid= 1n")

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
        img= Image.open(ruta_foto)
        img.thumbnail((100,100), Image.ANTIALIAS)
        salida= StringIO()
        img.save(salida,'PNG', quality=86)
        salida.seek(0)
        response.headers['Content-Type']= "image/png"
        
        return salida.getvalue(), response.body.getvalue()
