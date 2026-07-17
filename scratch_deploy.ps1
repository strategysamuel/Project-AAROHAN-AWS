Remove-Item Env:\AWS_ACCESS_KEY_ID -ErrorAction SilentlyContinue
Remove-Item Env:\AWS_SECRET_ACCESS_KEY -ErrorAction SilentlyContinue
Remove-Item Env:\AWS_SESSION_TOKEN -ErrorAction SilentlyContinue

$ErrorActionPreference = "Stop"

Write-Host "Authenticating to ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 905417996641.dkr.ecr.ap-south-1.amazonaws.com

Write-Host "Building Lending Container..."
docker build -f Dockerfile.lending -t aarohan/lending:latest .

Write-Host "Tagging and Pushing..."
docker tag aarohan/lending:latest 905417996641.dkr.ecr.ap-south-1.amazonaws.com/aarohan/lending:latest
docker push 905417996641.dkr.ecr.ap-south-1.amazonaws.com/aarohan/lending:latest

Write-Host "Registering Task Definition..."
aws ecs register-task-definition --cli-input-json file://ecs-task-lending.json --region ap-south-1

Write-Host "Updating CloudFormation Stack..."
aws cloudformation update-stack --stack-name aarohan-platform --template-body file://cloudformation-ecs-networking.yml --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

Write-Host "Updating ECS Service..."
aws ecs update-service --cluster aarohan-hackathon-cluster --service aarohan-platform-LendingService-U9S3O9hdumuS --force-new-deployment

Write-Host "Deployment Commands Executed Successfully."
