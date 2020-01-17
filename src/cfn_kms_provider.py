import os
import logging
from copy import copy
import boto3
from cfn_resource_provider import ResourceProvider


request_schema = {
    "type": "object",
    "required": ["KeyId", "GranteePrincipal", "Operations"],
    "properties": {
        "KeyId": {"type": "string"},
        "GranteePrincipal": {"type": "string"},
        "RetiringPrincipal": {"type": "string"},
        "Operations": {"type": "array", "items": {"type": "string"}},
        "Constraints": {
            "type": "object",
            "properties": {
                "EncryptionContextSubset": {"type": "object"},
                "EncryptionContextEquals": {"type": "object"},
            },
        },
        "GrantTokens": {"type": "array", "items": {"type": "string"}},
        "Name": {"type": "string"},
    },
}


class KMSGrantProvider(ResourceProvider):
    def __init__(self):
        super(KMSGrantProvider, self).__init__()
        self._kms = boto3.client("kms")

    def create(self):
        kwargs = copy(self.properties)
        if "ServiceToken" in kwargs:
            kwargs.pop("ServiceToken")
        response = self._kms.create_grant(**kwargs)
        self.physical_resource_id = response["GrantId"]
        self.set_attribute("GrantId", response["GrantId"])
        self.set_attribute("GrantToken", response["GrantToken"])

    def update(self):
        self.create()

    def delete(self):
        if self.physical_resource_id != "could-not-create":
            self._kms.revoke_grant(
                KeyId=self.get("KeyId"), GrantId=self.physical_resource_id
            )


provider = KMSGrantProvider()


def handler(request, context):
    log = logging.getLogger()
    log.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    return provider.handle(request, context)
