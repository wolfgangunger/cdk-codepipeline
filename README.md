# cdk-codepipeline
cdk project with codepipeline to deploy aws resources to stage accounts

## project strucure

## setup project

### bootstrap
toolchain

with toolchain credentials
cdk bootstrap aws://12345678912/eu-west-1 - on tooling account (change account number)

cdk bootstrap     [--profile admin-profile-1]     --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess     aws://111111111111/us-east-1


other accounts (dev, int , qa)
with stage credentials
cdk bootstrap --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess --trust 12345678912 aws://12345678915/eu-west-1

cdk bootstrap     [--profile admin-profile-2]     --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess     --trust 11111111111     aws://222222222222/us-east-2


## tests
### infrastructure tests
pytest -vvvv -s generic/infrastructure/tests
pytest -vvvv -s infrastructure/tests
### lambda tests 
pytest -vvvv -s infrastructure/lambdas/tests



