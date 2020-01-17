import uuid
from copy import copy
import botocore
from botocore.stub import Stubber, ANY
from cfn_kms_provider import handler, provider

create_grant_request = {
    "KeyId": "arn:aws:kms:eu-central-1:123123123123:key/84c80a6b-bab5-4259-88e7-80dee36f5a94",
    "GranteePrincipal": "arn:aws:iam::123123123123:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling",
    "RetiringPrincipal": "arn:aws:iam::123123123123:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling",
    "Operations": [
        "Encrypt",
        "Decrypt",
        "ReEncryptFrom",
        "ReEncryptTo",
        "GenerateDataKey",
        "GenerateDataKeyWithoutPlaintext",
        "DescribeKey",
        "CreateGrant",
    ],
    "Constraints": {
        "EncryptionContextSubset": {"KeyName": "bla"},
        "EncryptionContextEquals": {"KeyName": "boo"},
    },
    "GrantTokens": ["123132123123123123123123123123123123123132"],
    "Name": "my grant",
}


def test_create_grant():
    create_grant_response = {
        "GrantId": "abbbb",
        "GrantToken": "AQpAYWJkOWJiNDRjZDcyNDliNTY",
    }

    kms = botocore.session.get_session().create_client("kms")
    stubber = Stubber(kms)
    stubber.add_response("create_grant", create_grant_response, create_grant_request)
    stubber.activate()
    provider._kms = kms

    request = Request("Create", create_grant_request)
    response = handler(request, ())
    assert response["Status"] == "SUCCESS", response["Reason"]
    assert response["PhysicalResourceId"] == create_grant_response["GrantId"]
    assert response["Data"] == create_grant_response
    stubber.assert_no_pending_responses()
    stubber.deactivate()


def test_update_grant():
    update_grant_response = {
        "GrantId": "abbbbcdsasdf",
        "GrantToken": "sjhdfkahsdfkahskdjfhskadf",
    }
    kms = botocore.session.get_session().create_client("kms")
    stubber = Stubber(kms)
    stubber.add_response("create_grant", update_grant_response, create_grant_request)
    stubber.activate()
    provider._kms = kms
    request = Request(
        "Update",
        create_grant_request,
        physical_resource_id="sdfkjaslkdfjsalkdjfslkdfjskldfjsdf",
    )
    response = handler(request, ())
    assert response["Status"] == "SUCCESS", response["Reason"]
    assert response["PhysicalResourceId"] == update_grant_response["GrantId"]
    assert response["Data"] == update_grant_response

    stubber.assert_no_pending_responses()
    stubber.deactivate()


def test_delete_grant():
    kms = botocore.session.get_session().create_client("kms")
    stubber = Stubber(kms)
    revoke_grant_response = {}
    revoke_grant_request = {"GrantId": "12312312312", "KeyId": "234123112234234243"}
    stubber.add_response("revoke_grant", revoke_grant_response, revoke_grant_request)
    stubber.activate()
    provider._kms = kms
    request = Request(
        "Delete",
        revoke_grant_request,
        physical_resource_id=revoke_grant_request["GrantId"],
    )
    response = handler(request, ())
    assert response["Status"] == "SUCCESS", response["Reason"]
    stubber.assert_no_pending_responses()
    stubber.deactivate()


class Request(dict):
    def __init__(self, request_type, properties: dict = {}, physical_resource_id=None):
        request_id = "request-%s" % uuid.uuid4()
        self.update(
            {
                "RequestType": request_type,
                "ResponseURL": "https://httpbin.org/put",
                "StackId": "arn:aws:cloudformation:us-west-2:EXAMPLE/stack-name/guid",
                "RequestId": request_id,
                "ResourceType": "Custom::KMSGrant",
                "LogicalResourceId": "VerifiedIdentity",
            }
        )
        self["ResourceProperties"] = properties

        if physical_resource_id:
            self["PhysicalResourceId"] = physical_resource_id


class CreateGrantReponse(dict):
    def __init__(self, attributes=None, metadata=None):
        if attributes:
            self.update(attributes)
        if not metadata:
            metadata = {
                "RequestId": "2c7bd3fe-730c-4d24-b9a5-1942193a091a",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "x-amzn-requestid": "2c7bd3fe-730c-4d24-b9a5-1942193a091a",
                    "content-type": "text/xml",
                    "content-length": "275",
                    "date": "Sat, 16 Nov 2019 17:58:29 GMT",
                },
                "RetryAttempts": 0,
            }
        self["ResponseMetadata"] = metadata
