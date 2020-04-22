import os
import logging
from copy import copy
import boto3
from typing import Optional
from cfn_resource_provider import ResourceProvider


request_schema = {
    "type": "object",
    "oneOf": [
        {"required": ["KeyId", "GranteePrincipal", "Operations"]},
        {"required": ["KeyAliasArn", "GranteePrincipal", "Operations"]},
    ],
    "properties": {
        "KeyId": {"type": "string"},
        "KeyAliasArn": {"type": "string"},
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
        "Version": {"type": "string", "default": "v1"},
    },
}


class KMSGrantProvider(ResourceProvider):
    def __init__(self):
        super(KMSGrantProvider, self).__init__()
        self._kms = boto3.client("kms")

    def create_api_args(self) -> Optional[dict]:
        result = copy(self.properties)
        if "Version" in result:
            result.pop("Version")
        if "ServiceToken" in result:
            result.pop("ServiceToken")

        alias_arn = result.get("KeyAliasArn")
        if alias_arn:
            paginator = self._kms.get_paginator("list_aliases")
            for response in paginator.paginate():
                alias = next(
                    iter(
                        filter(
                            lambda r: r["AliasArn"] == alias_arn, response["Aliases"]
                        )
                    ),
                    None,
                )
                if alias:
                    break

            key_id = alias.get("TargetKeyId") if alias else None

            if not key_id:
                self.fail(f"alias '{alias_arn}' does not resolve to a KMS key")
                return None

            result.pop("KeyAliasArn")
            result["KeyId"] = alias_arn.replace(
                f":{alias['AliasName']}", f":key/{key_id}"
            )

        return result

    def create(self):
        kwargs = self.create_api_args()
        if kwargs:
            response = self._kms.create_grant(**kwargs)
            self.physical_resource_id = response["GrantId"]
            self.set_attribute("GrantId", response["GrantId"])
            self.set_attribute("GrantToken", response["GrantToken"])

    def update(self):
        self.create()

    def delete(self):
        if self.physical_resource_id != "could-not-create":
            args = self.create_api_args()
            self._kms.revoke_grant(
                KeyId=args.get("KeyId"), GrantId=self.physical_resource_id
            )


provider = KMSGrantProvider()


def handler(request, context):
    log = logging.getLogger()
    log.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    return provider.handle(request, context)
