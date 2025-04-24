import pytest
import pymongo
import os
import json
from src.util.dao import DAO
from unittest.mock import patch
from pymongo.errors import WriteError


@pytest.fixture
def dao():
    """Fixure for setting upp MongoDB and ter it down during testing"""
    test_collection_name = "user_test"
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    client = pymongo.MongoClient(mongo_url)
    database = client.edutask

    validator_json = """
    {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["firstName", "lastName", "email"],
            "properties": {
                "firstName": {
                    "bsonType": "string",
                    "description": "the first name of a user must be determined"
                }, 
                "lastName": {
                    "bsonType": "string",
                    "description": "the last name of a user must be determined"
                },
                "email": {
                    "bsonType": "string",
                    "description": "the email address of a user must be determined",
                    "uniqueItems": true
                },
                "tasks": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId"
                    }
                }
            }
        }
    }
    """
    validator = json.loads(validator_json)

    with patch('src.util.dao.getValidator', autospec=True) as mockedValidator:
        mockedValidator.return_value = validator
        dao = DAO(test_collection_name)

        yield dao

        database.drop_collection(test_collection_name)
        client.close()


@pytest.mark.integration
@pytest.mark.parametrize(
    "user_data, expected_output",
    [
        # Valid
        ({"firstName": "Mark", "lastName": "Henry", "email":"mark@henry.com"}, None),

        # Invalid
        ({"firstName": "Mark", "lastName": "", "email":"shuifh@sefsef.com"}, WriteError),
        ({"firstName": "", "lastName": "Henry", "email":"awd@sef.com"}, WriteError),
        ({"firstName": "Mark", "lastName": "Henry", "email":""}, WriteError),

        ({"firstName": "Mark", "email":"room@djaam.com"}, WriteError),
        ({"lastName": "Henry", "email":"Mikl@boom.com"}, WriteError),
        ({"firstName": "Mark", "lastName": "Henry"}, WriteError),
        
    ]
)
def test_create_user(dao, user_data, expected_output):
    """ Test create user """
    if expected_output is not None:
        with pytest.raises(expected_output):
            dao.create(user_data)
    else:
        user = dao.create(user_data)
        assert user is not None
        assert "_id" in user
        assert user["firstName"] == user_data["firstName"]
        assert user["lastName"] == user_data["lastName"]
        assert user["email"] == user_data["email"]


@pytest.mark.integration
def test_create_with_duplicate_email(dao):
    """ Test create two users with the same email """
    user_data = {
        "firstName": "Mark",
        "lastName": "Henry",
        "email":"mark@henry.com",
    }

    user_data1 = {
        "firstName": "Maison",
        "lastName": "Martines",
        "email":"mark@henry.com",
    }

    dao.create(user_data)

    with pytest.raises(WriteError):
        dao.create(user_data1)
