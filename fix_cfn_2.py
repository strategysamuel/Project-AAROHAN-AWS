import re

with open('cloudformation-ecs-networking.yml', 'r') as f:
    content = f.read()

# Make sure only one LoadBalancer remains for LendingService
pattern = r'(LendingService:\s+Type: AWS::ECS::Service.*?LoadBalancers:).*?(?=      ServiceRegistries:|      NetworkConfiguration:)'
replacement = r'\1\n        - ContainerName: nginx-proxy\n          ContainerPort: 80\n          TargetGroupArn: !Ref LendingTargetGroup\n'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('cloudformation-ecs-networking.yml', 'w') as f:
    f.write(content)
print("Updated load balancers")
