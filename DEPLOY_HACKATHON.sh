#!/bin/bash
# Project AAROHAN - AWS Hackathon Deployment Script
# 3-Container Optimized Architecture

set -e

REGION="ap-south-1"
ACCOUNT_ID="905417996641"
CLUSTER_NAME="aarohan-hackathon-cluster"
VPC_ID=""  # Replace with your VPC ID
SUBNET_1="" # Replace with your Subnet 1 ID
SUBNET_2="" # Replace with your Subnet 2 ID

echo "🚀 Project AAROHAN - AWS Hackathon Deployment"
echo "=============================================="

# Step 1: Create ECR Repositories
echo ""
echo "📦 Step 1: Creating ECR repositories..."
aws ecr create-repository --repository-name aarohan/identity --region $REGION || echo "Repository aarohan/identity already exists"
aws ecr create-repository --repository-name aarohan/lending --region $REGION || echo "Repository aarohan/lending already exists"
aws ecr create-repository --repository-name aarohan/executive --region $REGION || echo "Repository aarohan/executive already exists"

# Step 2: Authenticate Docker to ECR
echo ""
echo "🔐 Step 2: Authenticating Docker to ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Step 3: Build and Push Container Images
echo ""
echo "🏗️  Step 3: Building and pushing Container 1 (Identity Platform)..."
docker build -f Dockerfile.identity -t aarohan/identity:latest .
docker tag aarohan/identity:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/aarohan/identity:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/aarohan/identity:latest

echo ""
echo "🏗️  Step 3: Building and pushing Container 2 (Lending Intelligence)..."
docker build -f Dockerfile.lending -t aarohan/lending:latest .
docker tag aarohan/lending:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/aarohan/lending:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/aarohan/lending:latest

echo ""
echo "🏗️  Step 3: Building and pushing Container 3 (Executive Intelligence)..."
docker build -f Dockerfile.executive -t aarohan/executive:latest .
docker tag aarohan/executive:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/aarohan/executive:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/aarohan/executive:latest

# Step 4: Create CloudWatch Log Groups
echo ""
echo "📊 Step 4: Creating CloudWatch log groups..."
aws logs create-log-group --log-group-name /ecs/aarohan-identity-platform --region $REGION || echo "Log group already exists"
aws logs create-log-group --log-group-name /ecs/aarohan-lending-intelligence --region $REGION || echo "Log group already exists"
aws logs create-log-group --log-group-name /ecs/aarohan-executive-intelligence --region $REGION || echo "Log group already exists"

# Step 5: Create ECS Cluster
echo ""
echo "🎯 Step 5: Creating ECS Fargate cluster..."
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION || echo "Cluster already exists"

# Step 6: Register Task Definitions
echo ""
echo "📝 Step 6: Registering ECS task definitions..."
aws ecs register-task-definition --cli-input-json file://ecs-task-identity.json --region $REGION
aws ecs register-task-definition --cli-input-json file://ecs-task-lending.json --region $REGION
aws ecs register-task-definition --cli-input-json file://ecs-task-executive.json --region $REGION

# Step 7: Create Application Load Balancer
echo ""
echo "⚖️  Step 7: Creating Application Load Balancer..."
echo "⚠️  MANUAL STEP REQUIRED:"
echo "1. Go to AWS Console > EC2 > Load Balancers"
echo "2. Create Application Load Balancer named 'aarohan-alb'"
echo "3. Select VPC and at least 2 subnets"
echo "4. Create Security Group allowing inbound 80, 443, 9000-9013, 9090"
echo "5. Create Target Groups for each port (9000, 9001, 9003-9007, 9009, 9011-9013, 9090)"
echo "6. Configure path-based routing or port-based listeners"
echo ""
read -p "Press Enter after creating ALB and Target Groups..."

# Step 8: Create ECS Services
echo ""
echo "🚢 Step 8: Creating ECS services..."
echo "⚠️  Replace SUBNET_IDS and SECURITY_GROUP_ID with your values"
echo ""
echo "Command for Identity Platform service:"
echo "aws ecs create-service \\"
echo "  --cluster $CLUSTER_NAME \\"
echo "  --service-name identity-platform \\"
echo "  --task-definition aarohan-identity-platform \\"
echo "  --desired-count 1 \\"
echo "  --launch-type FARGATE \\"
echo "  --network-configuration \"awsvpcConfiguration={subnets=[$SUBNET_1,$SUBNET_2],securityGroups=[YOUR_SG_ID],assignPublicIp=ENABLED}\" \\"
echo "  --load-balancers targetGroupArn=YOUR_TG_ARN_9000,containerName=identity-platform,containerPort=9000 \\"
echo "  --region $REGION"
echo ""
echo "Command for Lending Intelligence service:"
echo "aws ecs create-service \\"
echo "  --cluster $CLUSTER_NAME \\"
echo "  --service-name lending-intelligence \\"
echo "  --task-definition aarohan-lending-intelligence \\"
echo "  --desired-count 1 \\"
echo "  --launch-type FARGATE \\"
echo "  --network-configuration \"awsvpcConfiguration={subnets=[$SUBNET_1,$SUBNET_2],securityGroups=[YOUR_SG_ID],assignPublicIp=ENABLED}\" \\"
echo "  --load-balancers targetGroupArn=YOUR_TG_ARN_9001,containerName=lending-intelligence,containerPort=9001 \\"
echo "  --region $REGION"
echo ""
echo "Command for Executive Intelligence service:"
echo "aws ecs create-service \\"
echo "  --cluster $CLUSTER_NAME \\"
echo "  --service-name executive-intelligence \\"
echo "  --task-definition aarohan-executive-intelligence \\"
echo "  --desired-count 1 \\"
echo "  --launch-type FARGATE \\"
echo "  --network-configuration \"awsvpcConfiguration={subnets=[$SUBNET_1,$SUBNET_2],securityGroups=[YOUR_SG_ID],assignPublicIp=ENABLED}\" \\"
echo "  --load-balancers targetGroupArn=YOUR_TG_ARN_9009,containerName=executive-intelligence,containerPort=9009 \\"
echo "  --region $REGION"

echo ""
echo "✅ Deployment preparation complete!"
echo ""
echo "📋 DEPLOYMENT SUMMARY"
echo "====================="
echo "Container 1 (Identity): auth-service (9000), ese-admin-service (9090)"
echo "Container 2 (Lending): 9 services on ports 9001, 9003-9007, 9011-9013"
echo "Container 3 (Executive): exec-service (9009)"
echo ""
echo "🔗 Next Steps:"
echo "1. Complete ALB and Target Group setup in AWS Console"
echo "2. Create ECS services using the commands above"
echo "3. Update frontend API_URL to point to ALB DNS name"
echo "4. Test all endpoints: /livez on each port"
