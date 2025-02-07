from .entidades import Compania
from seedwork.dominio.repositorios import Mapeador
from seedwork.dominio.fabricas import Fabrica
from seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class FabricaCompanias(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            compania: Compania = mapeador.dto_a_entidad(obj)
            return compania

