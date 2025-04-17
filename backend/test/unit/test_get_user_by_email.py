import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.fixture
def sut():
    mocked_dao = mock.MagicMock(spec=DAO)
    controller = UserController(dao=mocked_dao)
    return controller, mocked_dao

@pytest.mark.unit
@pytest.mark.parametrize(
    "email, dao_return, expected_output, expect_expection",
    [
        # Valid Email
        # Found user
        ("user@test.com", [{"_id": 1, "email": "user@test.com"}], {"_id": 1, "email": "user@test.com"}, None),
        ("many@test.com", [{"_id": 1, "email": "many@test.com"}, {"_id": 2, "email": "many@test.com"}], {"_id": 1, "email": "many@test.com"}, None),
        # No user
        ("no@test.com", [], None, None),

        # Invalid Email
        # ("user.com", None, None, ValueError),
        # ("test@test", None, None, ValueError),
        # ("test@", None, None, ValueError),
        # ("test @test.com", None, None, ValueError),
        # ("@test.com", None, None, ValueError),
        # ("test", None, None, ValueError),
        # ("@test", None, None, ValueError),
        # ("@", None, None, ValueError),
    ]
)
def test_get_user_by_email(sut, email, dao_return, expected_output, expect_expection):
    controller, mocked_dao = sut
    if expect_expection:
        with pytest.raises(expect_expection):
            controller.get_user_by_email(email=email)
    else:
        mocked_dao.find.return_value = dao_return
        result = controller.get_user_by_email(email=email)
        assert result == expected_output

@pytest.mark.unit
def test_get_user_by_email_error(sut):
    controller, mocked_dao = sut
    mocked_dao.find.side_effect = Exception
    with pytest.raises(Exception):
        controller.get_user_by_email('user@test.com')
