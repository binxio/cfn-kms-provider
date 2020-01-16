# Custom::KMSGrant
The `Custom::KMSGrant` create a KMS grant

## Syntax
The custom resource takes the same arguments as the create_grant API call:

```yaml
  Type : "Custom::KMSGrant",
  Properties:
    Name: ''
    KeyId: ''
    GranteePrincipal: ''
    RetiringPrincipal: ''
    Operations:
      - ''
    Constraints:
      EncryptionContextSubset:
        KeyName: ''
      EncryptionContextEquals:
        KeyName: ''
    GrantTokens:
      - ''
    !Sub 'arn:aws:lambda:${AWS::Region}:${AWS::AccountId}:function:binxio-cfn-kms-provider'
```

After creation, the GrantId is returned.  The GrantToken is returned as an attribute.

The custom resource wraps the KMS [create-grant](https://docs.aws.amazon.com/cli/latest/reference/kms/create-grant.html) function.
