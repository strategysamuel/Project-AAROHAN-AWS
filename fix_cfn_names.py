import re

with open('cloudformation-ecs-networking.yml', 'r') as f:
    content = f.read()

# Remove the Name: property from TargetGroups to allow CloudFormation to auto-generate names and avoid "already exists" errors during replacement
content = re.sub(r'(\s+)Type: AWS::ElasticLoadBalancingV2::TargetGroup\n\1Properties:\n\1  Name: [a-zA-Z0-9-]+\n', r'\1Type: AWS::ElasticLoadBalancingV2::TargetGroup\n\1Properties:\n', content)

with open('cloudformation-ecs-networking.yml', 'w') as f:
    f.write(content)
print("Removed Name property from TargetGroups")
