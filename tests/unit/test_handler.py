import json
import pytest
from web_ocr import app


@pytest.fixture()
def apigw_url_path():
    """ Generates API GW Event"""

    with open('./events/lambda/event_url_path.json') as f:
        data = json.load(f)

    return data

def test_url_path(apigw_url_path, mocker):
    ret = app.lambda_handler(apigw_url_path, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == 'Se não\npuder fazer\ntudo,\n\nfaça tudo\nque puder.\n\x0c'


@pytest.fixture()
def apigw_image64():
    """ Generates API GW Event"""

    with open('./events/lambda/event_image64.json') as f:
        data = json.load(f)

    return data

def test_image64(apigw_image64, mocker):
    ret = app.lambda_handler(apigw_image64, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    print(repr(data["message"]))
    assert data["message"] == 'Ela\n\nnão é forte,\nforte mesmo é\no Deus que nela\nhabita.\n\x0c'



@pytest.fixture()
def apigw_non_formated():
    """ Generates API GW Event"""

    with open('./events/lambda/event_non_formated.json') as f:
        data = json.load(f)

    return data

def test_non_formated(apigw_non_formated, mocker):
    ret = app.lambda_handler(apigw_non_formated, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 400
    assert "message" in ret["body"]
    print(data["message"])
    assert data["message"] == 'You must pass a least one of the arguments: url_pah or image64'


@pytest.fixture()
def apigw_non_configuration():
    """ Generates API GW Event"""

    with open('./events/lambda/event_pass_configuration.json') as f:
        data = json.load(f)

    return data

def test_non_configuration(apigw_non_configuration, mocker):
    ret = app.lambda_handler(apigw_non_configuration, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == 'Ela\n\nnao é forte,\nforte mesmo €\n0 Deus que nela\nhabita.\n\x0c'








