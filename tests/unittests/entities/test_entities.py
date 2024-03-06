from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID


def test_entities_are_equal_when_ids_are_equal() -> None:
    id_ = UUIDID.create()
    a = Entity(id_=id_)
    b = Entity(id_=id_)

    assert a == b


def test_entities_are_hashable() -> None:
    assert len({Entity(), Entity()}) == 2
