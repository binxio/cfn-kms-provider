# cfn-kms-provider
A CloudFormation custom resource provider for creating KMS grants.

## How do I create a KMS grant?
It is quite easy: you specify a CloudFormation resource of the [Custom::KMSGrant](docs/KMSGrant.md), as follows:

```yaml
KMSGrant:
  Type: Custom::KMSGrant
  Properties:
    KeyId: !GetAtt EncryptionKey.Arn
    GranteePrincipal: !Sub 'arn:aws:iam::${AWS::AccountId}:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling'
    Operations:
      - 'Encrypt'
      - 'Decrypt'
      - 'ReEncryptFrom'
      - 'ReEncryptTo'
      - 'GenerateDataKey'
      - 'GenerateDataKeyWithoutPlaintext'
      - 'DescribeKey'
      - 'CreateGrant'
    ServiceToken: !Sub 'arn:aws:lambda:${AWS::Region}:${AWS::AccountId}:function:binxio-cfn-kms-provider'
```

It will return the GrantId and the GrantToken as attribute. Referencing the resource will return the grant id.

## Installation
To install this custom resource, type:

```sh
aws cloudformation deploy \
	--capabilities CAPABILITY_IAM \
	--stack-name cfn-kms-provider \
	--template-file ./cloudformation/cfn-kms-provider.yaml
```

This CloudFormation template will use our pre-packaged provider from `s3://binxio-public-${AWS_REGION}/lambdas/cfn-kms-provider-0.1.1.zip`.


## Demo
To install the simple sample of the Custom Resource, type:

```sh
aws cloudformation deploy --stack-name cfn-kms-provider-demo \
	--template-file ./cloudformation/demo-stack.json
```
