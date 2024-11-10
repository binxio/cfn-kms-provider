# cfn-kms-provider
A CloudFormation custom resource provider for creating KMS grants.

Read about the usefulness of this provider on [how to start auto scaling group instances using a cross account encrypted AMI](https://binx.io/blog/2020/01/20/how-to-start-autoscaling-groups-using-a-cross-account-encrypted-ami/).

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

This CloudFormation template will use our pre-packaged provider from `463637877380.dkr.ecr.eu-central-1.amazonaws.com/xebia/cfn-kms-provider:1.0.1`.


## Demo
To install the simple sample of the Custom Resource, type:

```sh
aws cloudformation deploy --stack-name cfn-kms-provider-demo \
	--template-file ./cloudformation/demo-stack.json
```
