# Custom::KMSGrant
The `Custom::KMSGrant` create a KMS grant

## Syntax
The custom resource takes the same arguments as the create_grant API call, with the addition that you can specify
a KeyAliasArn and Version instead of the KeyId.

```yaml
  Type : "Custom::KMSGrant",
  Properties:
    Name: ''
    KeyId: ''
    KeyAliasArn: ''
    Version: ''
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
When you specify a KeyAliasArn, the key will be looked up and passed in as KeyId. When you change the alias to point to 
a different key, it will not automatically be picked up. Specify a Version to force an update.

After creation, the GrantId is returned.  The GrantToken is returned as an attribute.

The custom resource wraps the KMS [create-grant](https://docs.aws.amazon.com/cli/latest/reference/kms/create-grant.html) function.
