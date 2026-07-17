import re

with open('cloudformation-ecs-networking.yml', 'r') as f:
    content = f.read()

# 1. Update LendingTargetGroup Port to 80
content = re.sub(r'(LendingTargetGroup:.*?Port: )9001', r'\g<1>80', content, flags=re.DOTALL)
content = re.sub(r'(LendingTargetGroup:.*?HealthCheckPort: \')9001(\')', r'\g<1>80\g<2>', content, flags=re.DOTALL)
content = re.sub(r'(LendingTargetGroup:.*?HealthCheckPath: )/api/livez', r'\g<1>/livez', content, flags=re.DOTALL)

# 2. In LendingService, replace LoadBalancers list with just one pointing to port 80
new_load_balancers = """      LoadBalancers:
        - ContainerName: nginx-proxy
          ContainerPort: 80
          TargetGroupArn: !Ref LendingTargetGroup"""

content = re.sub(r'      LoadBalancers:\n(?:        - ContainerName: lending-intelligence\n          ContainerPort: \d+\n          TargetGroupArn: !Ref \w+\n)+', new_load_balancers + '\n', content)

# 3. For all PathRules that used to point to ConsentTargetGroup, GstTargetGroup, etc., point them to LendingTargetGroup
target_groups_to_replace = [
    'ConsentTargetGroup', 'GstTargetGroup', 'AaTargetGroup', 'FhcTargetGroup',
    'CreditTargetGroup', 'CamTargetGroup', 'OcenTargetGroup', 'CkycTargetGroup',
    'McaTargetGroup', 'EpfoTargetGroup', 'RbiTargetGroup'
]

for tg in target_groups_to_replace:
    content = content.replace(f'TargetGroupArn: !Ref {tg}', 'TargetGroupArn: !Ref LendingTargetGroup')

# 4. Remove the TargetGroup definitions for the ones we just replaced
for tg in target_groups_to_replace:
    pattern = rf'  {tg}:\n    Type: AWS::ElasticLoadBalancingV2::TargetGroup\n    Properties:.*?(?=\n  [A-Z]|\Z)'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

with open('cloudformation-ecs-networking.yml', 'w') as f:
    f.write(content)
print("Updated cloudformation-ecs-networking.yml")
