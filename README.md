# cdk-codepipeline
cdk project with codepipeline to deploy aws resources to stage accounts

## project strucure

## setup project

### provision pipeline
toolchain

with toolchain credentials
cdk bootstrap aws://803379787620/eu-west-1 - on tooling account.

npx cdk bootstrap     [--profile admin-profile-1]     --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess     aws://111111111111/us-east-1


other accounts
with dev credentials
cdk bootstrap --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess --trust 803379787620 aws://805448283132/eu-west-1

npx cdk bootstrap     [--profile admin-profile-2]     --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess     --trust 11111111111     aws://222222222222/us-east-2


## tests


