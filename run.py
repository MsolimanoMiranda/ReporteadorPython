import os
import json
from flask import Flask
from flask import render_template, request, redirect, url_for, send_file
from flask import jsonify
from werkzeug.utils import secure_filename
from config.db import metodos 
from flask_mail import Message, Mail
from datetime import date
from flask_cors import CORS
import sys

reload(sys)
sys.setdefaultencoding("UTF-8")
sys.getdefaultencoding()
app = Flask(__name__)
CORS(app)
# Carpeta de subida
app.config['UPLOAD_FOLDER'] = './archivos'
app.config['HOST'] = 'localhost'
app.config['USER'] = 'root'
app.config['PASSWORD'] = 'Dj5xjbZHcmUvquAh8etQ'
app.config['DB'] = 'kpi'
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='mail.cloudsystems.com.pe',
	MAIL_PORT=587,
	MAIL_USE_TLS = True,
       MAIL_USE_SSL = False,
	MAIL_USERNAME = 'sistemas@cloudsystems.com.pe',
	MAIL_PASSWORD = 'a6NWfDGhEb'
	)

    
mail = Mail(app)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(ruta_file,correos,plantilla):
       try:   
             
              today = date.today()
              ruta='./reportes/'+str(today)+ruta_file
              msg = Message("Reporte del dia",
                     sender=("Departamento de Sitemas","sistemas@cloudsystems.com.pe"),
                     recipients=correos)
              msg.html = plantilla
              with app.open_resource(ruta) as fp:
                     msg.attach(ruta_file,'text/xlsx', fp.read())       
              mail.send(msg)
              return 'Mail sent!'
       except Exception,e:
              return(str(e)) 

@app.route("/", methods=["GET", "POST"])
def lista():
       return render_template('formulario.html')


@app.route("/report/<int:post_id>/", methods=["GET", "POST"])
def lista_report(post_id=None):
      
       x = 'call kpi.sp_reports(1,'+str(post_id)+')'
       rv = metodos.set_list(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       
       if rv != None :
              content = rv.json
              today = date.today()
              ruta_plantilla = content['data'][0]['ruta_plantilla']
              correos = content['data'][0]['correos'].split(",") if content['data'][0]['correos'] != None else []
              html = content['data'][0]['plantilla'].replace("@NOMBRE_CLIENTE",content['data'][0]['Razon'])
              html = html.replace("@DIA_REPORTE",str(today))
              html = html.replace("@NOMBRE_REPORTE",content['data'][0]['reporte'])
              html = html.replace("@CORREO_CLIENTE",content['data'][0]['correos'])
              plantilla = ''+html.encode('utf-8') if content['data'][0]['plantilla'] != None else ''
              sql='call sp_reports(2,'+str(content['data'][0]['Id'])+')' 
              metodos.modificar_Excel(sql,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'],ruta_plantilla)
              send_email(ruta_plantilla,correos,plantilla)
              return rv
       return jsonify({"type":"error","status":401,"data":None})
@app.route("/reports", methods=["GET", "POST"])
def lista_report_init():
      
       x = 'call kpi.sp_reports(1,0)'
       rv = metodos.set_list(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
             
              return rv
       return jsonify({"type":"error","status":401,"data":None})

@app.route("/detalleReports/<int:post_id>/", methods=["GET", "POST"])
def lista_report_detail(post_id=None):
      
       x = 'call kpi.sp_reports(2,'+str(post_id)+')'
       rv = metodos.set_list(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
             
              return rv
       return jsonify({"type":"error","status":401,"data":None})

@app.route("/deleteReports/<int:post_id>/", methods=["GET", "POST"])
def delete_reports(post_id=None):
       x = 'delete from kpi.kpi_cabecera  where  Id='+str(post_id)
       rv = metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       x = 'delete from kpi.kpi_detalle where id_kpi='+str(post_id)
       rv = metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})

@app.route("/deleteDetalleReports/<int:post_id>/", methods=["GET", "POST"])
def delete_detalle_reports(post_id=None):
       x = 'delete from kpi.kpi_detalle where Id='+str(post_id)
       rv = metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})

@app.route("/duplicate_reporte/<int:post_id>/", methods=["GET", "POST"])
def duplicate_reports(post_id=None):
       x = 'call duplicate_report('+str(post_id)+');'
       print x
       rv = metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})

@app.route("/archi")
def upload_file():
 # renderiamos la plantilla "formulario.html"
 return render_template('formulario.html')


@app.route("/index", methods=['GET'])
def login():
 # renderiamos la plantilla "formulario.html"
 return render_template('formulario.html')


##APIS SERVIDORES
@app.route("/getServidores", methods=['GET'])
def get_servidores(post_id=None):
       x = 'SELECT s.*,s.Id as codigo,s.name_servidor as valor FROM kpi.ws_servidores s;'
       rv = metodos.set_list(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
             
              return rv
       return jsonify({"type":"error","status":401,"data":None})
@app.route("/actualizarSevidores", methods=["POST"])
def update_servidores():
       x="call sp_save_servidores("+str(request.form['id'])+",'"+request.form['db']+"','"+request.form['host']+"','"+request.form['user']+"','"+request.form['password']+"','"+request.form['name_servidor']+"')"
       rv=metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})

@app.route("/deleteServer/<int:post_id>/", methods=["GET", "POST"])
def delete_server(post_id=None):
       x = 'delete from kpi.ws_servidores where Id='+str(post_id)
       rv = metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})





@app.route("/getPlantilla", methods=['GET'])
def get_plantillas(post_id=None):
       x = 'SELECT Id as codigo,name_plantilla as valor FROM kpi.kpi_plantillas'
       rv = metodos.set_list(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
            return rv
       return jsonify({"type":"error","status":401,"data":None})
##APIS CORREO
@app.route("/getCorreos", methods=['GET'])
def get_correos(post_id=None):
       x = 'SELECT c.*,c.Id as codigo,c.name_correo as valor FROM kpi.kpi_correos c'
       rv = metodos.set_list(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
            return rv
       return jsonify({"type":"error","status":401,"data":None})

@app.route("/actualizarCorreos", methods=["POST"])
def update_correo():
       print request.form
       x="call sp_save_correo("+str(request.form['id'])+",'"+request.form['correos']+"','"+request.form['plantilla'].decode('utf8')+"','"+request.form['name_correo']+"')"
       rv=metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})

@app.route("/deleteCorreo/<int:post_id>/", methods=["GET", "POST"])
def delete_correo(post_id=None):
       x = 'delete from kpi.kpi_correos where Id='+str(post_id)
       rv = metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})
@app.route("/actualizarReportes", methods=["POST"])
def update_reporte():
       x="call sp_save_reportes("+str(request.form['id'])+",'"+request.form['ruc']+"','"+request.form['razon']+"','"+request.form['name_reporte']+"','"+request.form['plantilla']+"','"+request.form['id_correo']+"')"
       rv=metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})


@app.route("/actualizarDetalleReport", methods=["POST"])
def update_reporte_detalle():
       print request.form
       x="call sp_save_detalleReport("+str(request.form['id'])+","+str(request.form['id_kpi'])+",'"+request.form['hoja']+"','"+request.form['col']+"','"+request.form['fil']+"','"+request.form['query'].decode('utf8')+"','"+request.form['id_servidor']+"','"+request.form['nivel_2']+"','"+request.form['query_nivel2']+"','"+request.form['table_temp']+"','"+request.form['id_servidor_2']+"')"
       rv=metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})




@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files['archivo']
  filename = secure_filename(f.filename)
  x = "insert into kpi.kpi_plantillas(name_plantilla)values('"+filename+"');"
  rv = metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  # Retornamos una respuesta satisfactoria
  return render_template('formulario.html') 



@app.route("/download/<string:archivo>", methods=['GET'])
def downloadFile(archivo=None):
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = os.path.join(app.config['UPLOAD_FOLDER'], str(archivo))
    return send_file(path, as_attachment=True)

@app.route("/deleteplantilla/<int:post_id>/", methods=["GET", "POST"])
def delete_plantilla(post_id=None):
       x = 'delete from kpi.kpi_plantillas where Id='+str(post_id)
       rv = metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
       if rv != None :
              return rv
       return jsonify({"type":"error","status":401,"data":None})



# @app.route("/removeFile", methods=['POST'])
# def uploader():
#  if request.method == 'POST':
#   # obtenemos el archivo del input "archivo"
#   f = request.files['archivo']
#   filename = secure_filename(f.filename)
#   x = "insert into kpi.kpi_plantillas(name_plantilla)values('"+filename+"');"
#   rv = metodos.set_insert(x,app.config['HOST'] ,app.config['USER'] ,app.config['PASSWORD'],app.config['DB'])
#   f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#   # Retornamos una respuesta satisfactoria
#   return render_template('formulario.html') 


#   if os.path.exists("demofile.txt"):
#   os.remove("demofile.txt")
