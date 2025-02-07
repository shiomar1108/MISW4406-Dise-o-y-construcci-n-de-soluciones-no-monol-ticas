from config.db import db
from modulos.companias.dominio.repositorios import RepositorioCompanias
from modulos.companias.infraestructura.dto import Compania
from modulos.companias.dominio.fabricas import FabricaCompanias
from .dto import Compania as CompaniaDTO
from .mapeadores import MappeadorCompania
from uuid import UUID

class RepositorioCompaniasPostgresSQL(RepositorioCompanias):
    def __init__(self):
        self._fabrica_companias: FabricaCompanias = FabricaCompanias()

    def agregar(self, compania: Compania):
            compania_dto = self._fabrica_companias.crear_objeto(compania, MappeadorCompania())
            db.session.add(compania_dto)
    
    def obtener_todos(self) -> list[Compania]:
        companias_list = db.session.query(Compania).all()
        return companias_list
    
    def obtener_tipo(self) -> type:
        return Compania.__class__
    
    def obtener_por_id(self, id_compania: UUID) -> Compania:
        compania_dto = db.session.query(CompaniaDTO).filter_by(id=str(id_compania)).first()
        return self._fabrica_companias.crear_objeto(compania_dto, MappeadorCompania())
    
    def obtener_por_direccion(self, direccion: str) -> Compania:
        compania_dto = db.session.query(CompaniaDTO).filter_by(direccion=direccion).first()
        return self._fabrica_companias.crear_objeto(compania_dto, MappeadorCompania())    
    
    def eliminar(self, compania: Compania):
        db.session.query(CompaniaDTO).filter_by(id=str(compania.id_compania)).delete() 