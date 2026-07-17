import re

with open("cloudformation-ecs-networking.yml", "r") as f:
    content = f.read()

services_block = """  IdentityService:
    Type: AWS::ECS::Service
    DependsOn:
      - HttpListener
      - AuthPathRule
      - EseAdminPathRule
    Properties:
      Cluster: !Ref ClusterName
      ServiceName: identity-platform
      TaskDefinition: !Ref IdentityTaskDefinition
      DesiredCount: 1
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets:
            - !Ref PublicSubnet1
            - !Ref PublicSubnet2
          SecurityGroups:
            - !Ref EcsIdentitySecurityGroup
          AssignPublicIp: ENABLED
      LoadBalancers:
        - ContainerName: identity-platform
          ContainerPort: 9000
          TargetGroupArn: !Ref IdentityTargetGroup
        - ContainerName: identity-platform
          ContainerPort: 9090
          TargetGroupArn: !Ref EseAdminTargetGroup

  LendingService:
    Type: AWS::ECS::Service
    DependsOn:
      - HttpListener
      - CustomersPathRule
      - ConsentPathRule
      - GstPathRule
      - AaPathRule
      - FhcPathRule
      - CreditPathRule
      - CamPathRule
      - OcenPathRule
      - CkycPathRule
      - McaPathRule
      - EpfoPathRule
    Properties:
      Cluster: !Ref ClusterName
      ServiceName: lending-intelligence
      TaskDefinition: !Ref LendingTaskDefinition
      DesiredCount: 1
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets:
            - !Ref PublicSubnet1
            - !Ref PublicSubnet2
          SecurityGroups:
            - !Ref EcsPlatformSecurityGroup
          AssignPublicIp: ENABLED
      LoadBalancers:
        - ContainerName: lending-intelligence
          ContainerPort: 9001
          TargetGroupArn: !Ref LendingTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9002
          TargetGroupArn: !Ref ConsentTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9003
          TargetGroupArn: !Ref GstTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9004
          TargetGroupArn: !Ref AaTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9005
          TargetGroupArn: !Ref FhcTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9006
          TargetGroupArn: !Ref CreditTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9007
          TargetGroupArn: !Ref CamTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9008
          TargetGroupArn: !Ref OcenTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9011
          TargetGroupArn: !Ref CkycTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9012
          TargetGroupArn: !Ref McaTargetGroup
        - ContainerName: lending-intelligence
          ContainerPort: 9013
          TargetGroupArn: !Ref EpfoTargetGroup

  ExecutiveService:
    Type: AWS::ECS::Service
    DependsOn:
      - HttpListener
      - ExecPathRule
      - RmWorkspacePathRule
    Properties:
      Cluster: !Ref ClusterName
      ServiceName: executive-intelligence
      TaskDefinition: !Ref ExecutiveTaskDefinition
      DesiredCount: 1
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets:
            - !Ref PublicSubnet1
            - !Ref PublicSubnet2
          SecurityGroups:
            - !Ref EcsPlatformSecurityGroup
          AssignPublicIp: ENABLED
      LoadBalancers:
        - ContainerName: executive-intelligence
          ContainerPort: 9009
          TargetGroupArn: !Ref ExecutiveTargetGroup
        - ContainerName: executive-intelligence
          ContainerPort: 9010
          TargetGroupArn: !Ref RmWorkspaceTargetGroup
"""

# Replace the empty `  IdentityService:` with the full block
content = content.replace("  IdentityService:\n", services_block)
# In case there are trailing spaces
content = re.sub(r'  IdentityService:\s*$', services_block, content)

with open("cloudformation-ecs-networking.yml", "w") as f:
    f.write(content)
