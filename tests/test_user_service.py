import pytest
from unittest.mock import MagicMock
from app.services.user_service import UserService
from app.models.user_model import User
from app.schemas.user_schema import UserRequest

# Sample fixture for mocked DB session
@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_repo(monkeypatch):
    # Create a mocked repository
    mock_repo_instance = MagicMock()
    monkeypatch.setattr("app.services.user_service.UserRepository", lambda: mock_repo_instance)
    return mock_repo_instance

@pytest.fixture
def service(mock_repo):
    return UserService()

# --- Test create_user ---
def test_create_user(service, mock_db, mock_repo):
    user_request = UserRequest(name="Alice")
    mock_repo.save.return_value = User(id=1, name="Alice")

    result = service.create_user(mock_db, user_request)

    mock_repo.save.assert_called_once()
    assert result.name == "Alice"
    assert result.id == 1

# --- Test update_user ---
def test_update_user(service, mock_db, mock_repo):
    user = User(id=1, name="Bob")
    mock_repo.save.return_value = user

    result = service.update_user(mock_db, user)

    mock_repo.save.assert_called_once_with(mock_db, user)
    assert result.name == "Bob"

# --- Test delete_user ---
def test_delete_user(service, mock_db, mock_repo):
    user = User(id=1, name="Charlie")
    mock_repo.deleteUser.return_value = True

    result = service.delete_user(mock_db, user)

    mock_repo.deleteUser.assert_called_once_with(mock_db, user)
    assert result is True

# --- Test get_user success ---
def test_get_user_success(service, mock_db, mock_repo):
    user = User(id=1, name="David")
    mock_repo.find_by_id.return_value = user

    result = service.get_user(mock_db, 1)

    mock_repo.find_by_id.assert_called_once_with(mock_db, 1)
    assert result.name == "David"

# --- Test get_user not found ---
def test_get_user_not_found(service, mock_db, mock_repo):
    mock_repo.find_by_id.return_value = None

    with pytest.raises(Exception) as excinfo:
        service.get_user(mock_db, 99)
    assert str(excinfo.value) == "User not found"

# --- Test getAllUsers success ---
def test_get_all_users_success(service, mock_db, mock_repo):
    users = [User(id=1, name="Alice"), User(id=2, name="Bob")]
    mock_repo.find_All.return_value = users

    result = service.getAllUsers(mock_db)

    mock_repo.find_All.assert_called_once_with(mock_db)
    assert len(result) == 2

# --- Test getAllUsers not found ---
def test_get_all_users_not_found(service, mock_db, mock_repo):
    mock_repo.find_All.return_value = None

    with pytest.raises(Exception) as excinfo:
        service.getAllUsers(mock_db)
    assert str(excinfo.value) == "User not found"