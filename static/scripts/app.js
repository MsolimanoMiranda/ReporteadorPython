
const distritos='<option value="">Seleccione</option>'+
'<option value="">LIMA</option>'+
'<option value="">ANCON</option>'+
'<option value="">ATE</option>'+
'<option value="">BARRANCO</option>'+
'<option value="">BREÑA</option>'+
'<option value="">CARABAYLLO</option>'+
'<option value="">CHACLACAYO</option>'+
'<option value="">CHORRILLOS</option>'+
'<option value="">CIENEGUILLA</option>'+
'<option value="">COMAS</option>'+
'<option value="">EL AGUSTINO</option>'+
'<option value="">INDEPENDENCIA</option>'+
'<option value="">JESUS MARIA</option>'+
'<option value="">LA MOLINA</option>'+
'<option value="">LA VICTORIA</option>'+
'<option value="">LINCE</option>'+
'<option value="">LOS OLIVOS</option>'+
'<option value="">LURIGANCHO</option>'+
'<option value="">LURIN</option>'+
'<option value="">MAGDALENA DEL MAR</option>'+
'<option value="">MIRAFLORES</option>'+
'<option value="">PACHACAMAC</option>'+
'<option value="">PUCUSANA</option>'+
'<option value="">PUEBLO LIBRE</option>'+
'<option value="">PUENTE PIEDRA</option>'+
'<option value="">PUNTA HERMOSA</option>'+
'<option value="">PUNTA NEGRA</option>'+
'<option value="">RIMAC</option>'+
'<option value="">SAN BARTOLO</option>'+
'<option value="">SAN BORJA</option>'+
'<option value="">SAN ISIDRO</option>'+
'<option value="">SAN JUAN DE LURIGANCHO</option>'+
'<option value="">SAN JUAN DE MIRAFLORES</option>'+
'<option value="">SAN LUIS</option>'+
'<option value="">SAN MARTIN DE PORRES</option>'+
'<option value="">SAN MIGUEL</option>'+
'<option value="">SANTA ANITA</option>'+
'<option value="">SANTA MARIA DEL MAR</option>'+
'<option value="">SANTA ROSA</option>'+
'<option value="">SANTIAGO DE SURCO</option>'+
'<option value="">SURQUILLO</option>'+
'<option value="">VILLA EL SALVADOR</option>'+
'<option value="">VILLA MARIA DEL TRIUNFO</option>';

const vias='<option value="">Seleccione</option>'+
'<option value="AL">ALAMEDA</option>'+
'<option value="AV">AVENIDA</option>'+
'<option value="BJ">BAJADA</option>'+
'<option value="BL">BOULEVARD</option>'+
'<option value="CL">CALLE</option>'+
'<option value="N">CALLEJÓN</option>'+
'<option value="CA">CARRETERA</option>'+
'<option value="R">COOPERATIVA</option>'+
'<option value="E">ESQUINA</option>'+
'<option value="F">FUNDO</option>'+
'<option value="GA">GALERIA</option>'+
'<option value="H">HACIENDA</option>'+
'<option value="JR">JIRON</option>'+
'<option value="KM">KILOMETRO</option>'+
'<option value="ML">MALECON</option>'+
'<option value="MZ">MZ</option>'+
'<option value="OT">OTROS</option>'+
'<option value="OV">OVALO</option>'+
'<option value="PQ">PARQUE</option>'+
'<option value="PJ">PASAJE</option>'+
'<option value="PS">PASEO</option>'+
'<option value="PL">PLAZA</option>'+
'<option value="Z">PLAZUELA</option>'+
'<option value="PR">PROLONGACION</option>'+
'<option value="Y">PUEBLOJOVEN</option>'+
'<option value="PT">PUENTE</option>'+
'<option value="K">TAMBO</option>'+
'<option value="I">VILLA</option>';

const estudios='<option value="0">Seleccione Grado de Estudio</option>'+
              '<option value="masculino">Primaria Completa</option>'+
              '<option value="femenino">Secundaria Completa</option>'+
              '<option value="femenino">Tecnico</option>'+
              '<option value="femenino">Universitario</option>';
function getParametersSendPost(paquete){

  var res="{";
$.each(paquete, function(key, value) {  

var valor="";  
  if(value.type=="text"){
     valor=$("#"+key).val();
  }else if (value.type=="select"){
    valor=$("#"+key+" option:selected").val();
  }
  var postsend=value.send;

  str = '"'+value.send+'"'+':'+'"'+valor+'"'+',';
  if(valor!=="" && valor!=="0"){res = res.concat($.trim(str));}

  });

texto=res;
texto = texto.substring(0,texto.length-1).concat("}");
if(texto=="}"){texto="{}";}

return JSON.parse(texto);
}

const arryaAlumno={
  cmb_programa:{type:'select',send:'programa'},
  cmb_Subprograma:{type:'select',send:'sub_progrma'},
  sexo_hijo:{type:'text',send:'sexo'},
  dni_hijo:{type:'text',send:'dni'},
  nombres_hijo:{type:'text',send:'nombres'},
  apellidos_hijo:{type:'text',send:'apellidos'},
  fch_nacimiento_hijo:{type:'text',send:'fch_nacimiento'},
  alergias_hijo:{type:'text',send:'alergias'},
};

const arrayPersona={
  dni:{type:'text',send:'dni'},
  grado_estudios:{type:'select',send:'grado_estudios'},
  nombres:{type:'text',send:'nombres'},
  apellidos:{type:'text',send:'apellidos'},
  celular:{type:'text',send:'celular'},
  profesion:{type:'text',send:'profesion'},
  oficio:{type:'text',send:'oficio'},
  centro_trabjo:{type:'text',send:'centro_trabjo'},
  fch_nacimiento:{type:'text',send:'fch_nacimiento'},
  telefono:{type:'text',send:'telefono'},
  provincia:{type:'select',send:'provincia'},
  distrito:{type:'select',send:'distrito'},
  via:{type:'select',send:'via'},
  nro_via:{type:'text',send:'nro_via'},
  referencia:{type:'text',send:'referencia'},
}



const headers = {
  'Content-Type': 'application/json',
  'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1ODI2MDQ3NjAsImlzcyI6IjEwNzc1NjU1NDc1IiwiaWF0IjoxNTgwMDEyNzYwfQ.i4mpD4n588ESCFG-Lb0MQ6TU8lVoeGL5CgJvg_Gd56o'
}

 init();

async function init(){
  getParametersSendPost(arryaAlumno);
  
  $("#papaDistrito,#mamaDistrito,#apoderadoDistrito").html(distritos);
  $("#papavias,#mamavias,#apoderadovias").html(vias);
  $("#papaestudios,#mamaestudios,#apoderadoestudios").html(estudios);
  

  await axios.get("http://192.99.145.229/wsDinamic/api/3", {
    headers: headers
  }).then((x) => {
    const data=x.data.data; 
    let html='<option value="0">Seleccione Programa</option>';

   for(key in data){
     html +='<option value="'+data[key].Id+'" >'+data[key].descripcion+'</option>'
  }
  $("#cmb_programa").html(html);

  
  })
  .catch((error) => {
    console.log(error);
  })

}



$("#cmb_programa").change(function() {
  loadSubPrograma(parseInt(this.value));
});


async function loadSubPrograma(idprograma){
await axios.post("http://192.99.145.229/wsDinamic/api/4",{idprograma:idprograma}, {
  headers: headers
}).then((x) => {
  const data=x.data.data; 
  let html='<option value="0">Seleccione Sub Programa</option>'
for(key in data){
   html +='<option value="'+data[key].Id+'" >'+data[key].descripcion+'</option>'
}
$("#cmb_Subprograma").html(html);

})
.catch((error) => {
  let html='<option value="0">Seleccione Sub Programa</option>'
  $("#cmb_Subprograma").html(html);
  console.log(error);
})
}





