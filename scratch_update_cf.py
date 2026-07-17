import re

with open("cloudformation-ecs-networking.yml", "r") as f:
    content = f.read()

# 1. Update EcsPlatformSecurityGroup
content = re.sub(
    r'FromPort: 9001\s+ToPort: 9013',
    'FromPort: 9001\n          ToPort: 9014',
    content
)

# 2. Add RbiTargetGroup
target_group = """  RbiTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-rbi-tg
      Port: 9014
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

"""
content = content.replace("  RmWorkspaceTargetGroup:", target_group + "  RmWorkspaceTargetGroup:")

# 3. Add RbiPathRule
path_rule = """  RbiPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 31
      Conditions:
        - Field: path-pattern
          Values:
            - /rbi/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref RbiTargetGroup

"""
content = content.replace("  ExecPathRule:", path_rule + "  ExecPathRule:")

# 4. Update LendingService DependsOn
content = content.replace(
    "- EpfoPathRule",
    "- EpfoPathRule\n      - RbiPathRule"
)

# 5. Update LendingService LoadBalancers
load_balancer = """        - ContainerName: lending-intelligence
          ContainerPort: 9014
          TargetGroupArn: !Ref RbiTargetGroup
"""
content = content.replace(
    "  ExecutiveService:",
    load_balancer + "\n  ExecutiveService:"
)

with open("cloudformation-ecs-networking.yml", "w") as f:
    f.write(content)
