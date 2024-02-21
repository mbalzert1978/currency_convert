import uuid

import pydantic
import pytest

from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID


def test_create_uuidid_using_create_default() -> None:
    # Arrange / Act
    id_ = UUIDID.create()

    # Assert
    assert isinstance(id_, UUIDID)
    assert isinstance(id_.value, uuid.UUID)


def test_create_uuidid_using_create_value() -> None:
    # Arrange
    expected = "test_space"

    # Act
    id_ = UUIDID.create(expected)

    # Assert
    assert isinstance(id_, UUIDID)
    assert id_.value == expected


def test_imutability() -> None:
    # Arrange
    id_ = UUIDID.create()

    # Act / Assert
    with pytest.raises(pydantic.ValidationError, match="frozen"):
        id_.value = "new"
