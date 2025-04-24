import pytest
import pymongo
import os
import json
from src.util.dao import DAO
from unittest.mock import patch
from pymongo.errors import WriteError
from bson.objectid import ObjectId


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
def test_create(dao):
    user_data = {
        "firstName": "Mark",
        "lastName": "Henrry",
        "email":"mark@henry.com",
    }

    user = dao.create(user_data)

    assert "_id" in user

