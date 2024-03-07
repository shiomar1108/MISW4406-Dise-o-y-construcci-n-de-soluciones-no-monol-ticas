import seedwork.presentacion.api as api
from seedwork.dominio.excepciones import ExcepcionDominio
from modulos.companias.aplicacion.mapeadores import MapeadorCompaniaDTOJson
from modulos.companias.aplicacion.comandos.crear_compania import CrearCompania
from modulos.companias.aplicacion.queries.obtener_todas_companias import ObtenerTodasCompanias
from modulos.companias.aplicacion.comandos.rollback import RollbackCompania
from seedwork.aplicacion.queries import ejecutar_query
from seedwork.aplicacion.comandos import ejecutar_commando
import json
from flask import Response
from flask import request


bp = api.crear_blueprint('compania', '/compania')

@bp.route('/crear', methods=['POST',])
def crear():
    try:
        compania_dict = request.json
        map_compania = MapeadorCompaniaDTOJson()
        compania_dto = map_compania.externo_a_dto(compania_dict)

        comando = CrearCompania(
           nombre_compania = compania_dto.nombre_compania,
            representante_legal = compania_dto.representante_legal,
            email_contacto = compania_dto.email_contacto,
            telefono_contacto = compania_dto.telefono_contacto,
            estado = compania_dto.estado,
            documento_identidad_numero_identificacion = compania_dto.documento_identidad_numero_identificacion,
            documento_identidad_tipo = compania_dto.documento_identidad_tipo,
            tipo_industria = compania_dto.tipo_industria,
            direccion = compania_dto.direccion,
            latitud = compania_dto.tipo_industria,
            longitud = compania_dto.tipo_industria,
            ciudad = compania_dto.ciudad,
            pais = compania_dto.pais
        )

        ejecutar_commando(comando)
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    
@bp.route('', methods=('GET',))
def dar_compania_usando_query():
    map_compania = MapeadorCompaniaDTOJson()
    query_resultado = ejecutar_query(ObtenerTodasCompanias())
    resultados = []
    
    for compania in query_resultado.resultado:
        resultados.append(map_compania.dto_a_externo(compania))
    
    return resultados
    
@bp.route('/rollback', methods=('POST',))
def rollback_creacion():
    try:
        rollback_id = request.json.get("id")

        comando = RollbackCompania(
            id_compania= rollback_id
        )
        ejecutar_commando(comando)
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')