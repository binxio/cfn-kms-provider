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

kms = boto3.client("kms")

class KMSGrantProvider(ResourceProvider):
    def __init__(self):
        super(KMSGrantProvider, self).__init__()

    def create(self):
        kwargs = copy(self.properties)
        kwargs.pop('ServiceToken')
        response = kms.create_grant(**kwargs)
        self.physical_resource_id = response["GrantId"]
        self.set_attribute("GrantToken", response["GrantToken"])

    def has_changes(self):
        for key in request_schema["properties"]:
            if self.get(key) != self.old_properties.get(key):
                return True
        return False

    def update(self):
        if self.has_changes():
            self.create()

    def delete(self):
        if self.physical_resource_id != "could-not-create":
            kms.revoke_grant(KeyId=self.get("KeyId"), GrantId=self.physical_resource_id)


provider = KMSGrantProvider()


def handler(request, context):
    log = logging.getLogger()
    log.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    return provider.handle(request, context)
