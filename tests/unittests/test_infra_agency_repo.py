import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm.session import Session
from currency_convert.domain.agency.entities.agency import Agency
from currency_convert.infrastructure.agency.repository import AgencyRepo


@pytest.fixture
def agency_repo() -> tuple[AgencyRepo, MagicMock]:
    session = MagicMock(spec=Session)
    return AgencyRepo(session), session


@pytest.fixture
def agency() -> Agency:
    return Agency.create(
        name="Test Agency",
        base="USD",
        address="https://test.com",
        country="Test Country",
    ).unwrap()


@pytest.mark.parametrize(
    "mock_into_db_side_effect, mock_merge_side_effect, mock_commit_side_effect, expected_error",
    [
        (Exception("Into DB error"), None, None, "Into DB error"),
        (None, Exception("Merge error"), None, "Merge error"),
        (None, None, Exception("Commit error"), "Commit error"),
    ],
    ids=[
        "save_when_into_db_fails_should_roll_back_and_return_error",
        "save_when_merge_fails_should_roll_back_and_return_error",
        "save_when_commit_fails_should_roll_back_and_return_error",
    ],
)
@patch("currency_convert.infrastructure.agency.mapper.AgencyMapper.into_db")
def test_save_when_error_occurs_should__roll_back_and_return_error(
    mock_into_db: MagicMock,
    agency_repo: tuple[AgencyRepo, MagicMock],
    agency: Agency,
    mock_into_db_side_effect: Exception,
    mock_merge_side_effect: Exception,
    mock_commit_side_effect: Exception,
    expected_error: str,
) -> None:
    repo, session = agency_repo
    mock_into_db.side_effect = mock_into_db_side_effect
    session.merge.side_effect = mock_merge_side_effect
    session.commit.side_effect = mock_commit_side_effect

    result = repo.save(agency)

    assert result.is_err()
    assert str(result.unwrap_err()) == expected_error
    session.rollback.assert_called_once()
