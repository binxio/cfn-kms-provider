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

create_grant_request_with_alias = {
    "KeyAliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/EBS",
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


def test_create_grant_with_alias():
    create_grant_response = {
        "GrantId": "abbbb",
        "GrantToken": "AQpAYWJkOWJiNDRjZDcyNDliNTY",
    }

    list_aliases_response = {
        "Aliases": [
            {
                "AliasName": "alias/aws/backup",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/backup",
                "TargetKeyId": "9ac35b02-191d-4b98-af4c-e5a344003ed0",
            },
            {
                "AliasName": "alias/aws/codecommit",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/codecommit",
                "TargetKeyId": "171fdf16-6858-4580-a54b-405a66975b14",
            },
            {
                "AliasName": "alias/aws/dynamodb",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/dynamodb",
            },
            {
                "AliasName": "alias/aws/ebs",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/ebs",
                "TargetKeyId": "85fff602-d2eb-42d9-b467-f68d5a19b8ef",
            },
            {
                "AliasName": "alias/aws/elasticfilesystem",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/elasticfilesystem",
                "TargetKeyId": "200f84e4-d4c5-49a1-b0c4-c5c2876c9c8d",
            },
            {
                "AliasName": "alias/aws/es",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/es",
            },
            {
                "AliasName": "alias/aws/fsx",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/fsx",
                "TargetKeyId": "5148c34a-9f22-40fc-b7b5-3f6411d85dfa",
            },
            {
                "AliasName": "alias/EBS",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/EBS",
                "TargetKeyId": "84c80a6b-bab5-4259-88e7-80dee36f5a94",
            },
            {
                "AliasName": "alias/aws/glue",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/glue",
            },
            {
                "AliasName": "alias/aws/kinesisvideo",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/kinesisvideo",
            },
            {
                "AliasName": "alias/aws/lambda",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/lambda",
                "TargetKeyId": "d8d83b5e-4d36-4705-8bde-079fe4205c06",
            },
            {
                "AliasName": "alias/aws/lightsail",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/lightsail",
                "TargetKeyId": "a2788a12-d685-4a3d-91b6-a2a135e999fd",
            },
            {
                "AliasName": "alias/aws/rds",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/rds",
            },
            {
                "AliasName": "alias/aws/redshift",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/redshift",
            },
            {
                "AliasName": "alias/aws/s3",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/s3",
                "TargetKeyId": "e695c083-7da2-4e13-bb60-748c1fc4563a",
            },
            {
                "AliasName": "alias/aws/ssm",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/ssm",
            },
            {
                "AliasName": "alias/aws/xray",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/aws/xray",
            },
            {
                "AliasName": "alias/cmk/backup",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/cmk/backup",
                "TargetKeyId": "27018d53-9296-4c55-b158-58e4f7656d2c",
            },
            {
                "AliasName": "alias/sm",
                "AliasArn": "arn:aws:kms:eu-central-1:123123123123:alias/sm",
                "TargetKeyId": "64720673-3541-40e9-a08a-175e5f3a02a5",
            },
        ]
    }
    kms = botocore.session.get_session().create_client("kms")
    stubber = Stubber(kms)
    stubber.add_response("list_aliases", list_aliases_response, {})
    stubber.add_response("create_grant", create_grant_response, create_grant_request)
    stubber.activate()
    provider._kms = kms

    request = Request("Create", create_grant_request_with_alias)
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
