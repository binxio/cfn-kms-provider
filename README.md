# cfn-kms-provider
A CloudFormation custom resource provider for creating KMS grants.

## Installation
To install this custom resource, type:

```sh
aws cloudformation create-stack \
	--capabilities CAPABILITY_IAM \
	--stack-name cfn-kms-provider \
	--template-body file://cloudformation/cfn-kms-provider.json 

aws cloudformation wait stack-create-complete  --stack-name cfn-kms-provider 
```

This CloudFormation template will use our pre-packaged provider from `s3://binxio-public-${AWS_REGION}/lambdas/cfn-kms-provider-0.1.4.zip`.


## Demo
To install the simple sample of the Custom Resource, type:

```sh
aws cloudformation create-stack --stack-name cfn-kms-provider-demo \
	--template-body file://cloudformation/demo-stack.json
aws cloudformation wait stack-create-complete  --stack-name cfn-kms-provider-demo
```
