import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.fixture
def scu():
    mocked_dao = mock.MagicMock(spec=DAO)
    controller = UserController(dao=mocked_dao)
    return controller, mocked_dao

@pytest.mark.unit
@pytest.mark.parametrize(
    "email, dao_return, expected_output, expect_expection, warning_message",
    [
        # Valid
        ("user@test.com", [{"_id": 1, "email": "user@test.com"}], {"_id": 1, "email": "user@test.com"}, None, None),
        ("no@test.com", [], None, None, None),
    ]
)
def test_get_user_by_email(scu, email, dao_return, expected_output, expect_expection, warning_message, capsys):
    controller, mocked_dao = scu
    mocked_dao.find.return_value = dao_return
    result = controller.get_user_by_email(email=email)
    assert result == expected_output
