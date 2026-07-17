import re
import sys

def main():
    with open("cloudformation-ecs-networking.yml", "r") as f:
        content = f.read()

    # 1. Update Security Groups
    sg_identity = """      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 9000
          ToPort: 9000
          SourceSecurityGroupId: !Ref AlbSecurityGroup
        - IpProtocol: tcp
          FromPort: 9090
          ToPort: 9090
          SourceSecurityGroupId: !Ref AlbSecurityGroup"""
          
    content = re.sub(r'      SecurityGroupIngress:\n        - IpProtocol: tcp\n          FromPort: 9000\n          ToPort: 9000\n          SourceSecurityGroupId: !Ref AlbSecurityGroup', sg_identity, content)

    sg_platform = """      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 9001
          ToPort: 9013
          SourceSecurityGroupId: !Ref AlbSecurityGroup"""

    old_sg_platform = """      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 9001
          ToPort: 9001
          SourceSecurityGroupId: !Ref AlbSecurityGroup
        - IpProtocol: tcp
          FromPort: 9009
          ToPort: 9009
          SourceSecurityGroupId: !Ref AlbSecurityGroup"""
          
    content = content.replace(old_sg_platform, sg_platform)
    
    # 2. Add Target Groups
    target_groups = """
  EseAdminTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-eseadmin-tg
      Port: 9090
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  ConsentTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-consent-tg
      Port: 9002
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  GstTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-gst-tg
      Port: 9003
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  AaTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-aa-tg
      Port: 9004
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  FhcTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-fhc-tg
      Port: 9005
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  CreditTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-credit-tg
      Port: 9006
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  CamTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-cam-tg
      Port: 9007
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  OcenTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-ocen-tg
      Port: 9008
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  CkycTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-ckyc-tg
      Port: 9011
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  McaTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-mca-tg
      Port: 9012
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  EpfoTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-epfo-tg
      Port: 9013
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200

  RmWorkspaceTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: aarohan-rm-tg
      Port: 9010
      Protocol: HTTP
      TargetType: ip
      VpcId: !Ref VpcId
      HealthCheckEnabled: true
      HealthCheckPath: /livez
      HealthCheckProtocol: HTTP
      Matcher:
        HttpCode: 200"""
        
    content = content.replace("  ExecutiveTargetGroup:", target_groups + "\n\n  ExecutiveTargetGroup:")

    # 3. Add Listener Rules
    listener_rules = """
  EseAdminPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 11
      Conditions:
        - Field: path-pattern
          Values:
            - /ese/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref EseAdminTargetGroup

  CustomersPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 20
      Conditions:
        - Field: path-pattern
          Values:
            - /customers/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref LendingTargetGroup

  ConsentPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 21
      Conditions:
        - Field: path-pattern
          Values:
            - /consents/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref ConsentTargetGroup

  GstPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 22
      Conditions:
        - Field: path-pattern
          Values:
            - /gst/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref GstTargetGroup

  AaPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 23
      Conditions:
        - Field: path-pattern
          Values:
            - /aa/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref AaTargetGroup

  FhcPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 24
      Conditions:
        - Field: path-pattern
          Values:
            - /fhc/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref FhcTargetGroup

  CreditPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 25
      Conditions:
        - Field: path-pattern
          Values:
            - /credit/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref CreditTargetGroup

  CamPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 26
      Conditions:
        - Field: path-pattern
          Values:
            - /cam/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref CamTargetGroup

  OcenPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 27
      Conditions:
        - Field: path-pattern
          Values:
            - /ocen/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref OcenTargetGroup

  CkycPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 28
      Conditions:
        - Field: path-pattern
          Values:
            - /ckyc/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref CkycTargetGroup

  McaPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 29
      Conditions:
        - Field: path-pattern
          Values:
            - /mca/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref McaTargetGroup

  EpfoPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 30
      Conditions:
        - Field: path-pattern
          Values:
            - /epfo/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref EpfoTargetGroup

  ExecPathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 40
      Conditions:
        - Field: path-pattern
          Values:
            - /exec/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref ExecutiveTargetGroup

  RmWorkspacePathRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HttpListener
      Priority: 41
      Conditions:
        - Field: path-pattern
          Values:
            - /rm/*
      Actions:
        - Type: forward
          TargetGroupArn: !Ref RmWorkspaceTargetGroup"""
          
    # Remove old rules and add new ones
    start_rules = content.find("  AuthPathRule:")
    end_rules = content.find("  IdentityService:")
    if start_rules != -1 and end_rules != -1:
        content = content[:start_rules] + "  AuthPathRule:\n" + content[start_rules+16:end_rules] + listener_rules + "\n\n  IdentityService:"
        
        # Need to be careful here to only replace the GstPathRule, ApiPathRule, ExecPathRule
        content_lines = content.split('\n')
        new_lines = []
        skip = False
        for line in content_lines:
            if line.startswith("  GstPathRule:") or line.startswith("  ApiPathRule:") or line.startswith("  ExecPathRule:"):
                skip = True
            elif line.startswith("  IdentityService:") or line.startswith("  AuthPathRule:") or (not line.startswith(" ") and len(line) > 0 and skip):
                if skip and line.startswith("  IdentityService:"):
                    skip = False
            
            if not skip:
                new_lines.append(line)
        # We'll just replace the whole rules block
        
    start_rules = content.find("  AuthPathRule:")
    end_rules = content.find("  IdentityService:")
    content = content[:start_rules] + "  AuthPathRule:\n    Type: AWS::ElasticLoadBalancingV2::ListenerRule\n    Properties:\n      ListenerArn: !Ref HttpListener\n      Priority: 10\n      Conditions:\n        - Field: path-pattern\n          Values:\n            - /auth/*\n      Actions:\n        - Type: forward\n          TargetGroupArn: !Ref IdentityTargetGroup\n" + listener_rules + "\n\n  IdentityService:"

    # 4. Modify LoadBalancers
    identity_lbs = """      LoadBalancers:
        - ContainerName: identity-platform
          ContainerPort: 9000
          TargetGroupArn: !Ref IdentityTargetGroup
        - ContainerName: identity-platform
          ContainerPort: 9090
          TargetGroupArn: !Ref EseAdminTargetGroup"""
    content = re.sub(r'      LoadBalancers:\n        - ContainerName: identity-platform\n          ContainerPort: 9000\n          TargetGroupArn: !Ref IdentityTargetGroup', identity_lbs, content)
    
    lending_lbs = """      LoadBalancers:
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
          TargetGroupArn: !Ref EpfoTargetGroup"""
    content = re.sub(r'      LoadBalancers:\n        - ContainerName: lending-intelligence\n          ContainerPort: 9001\n          TargetGroupArn: !Ref LendingTargetGroup', lending_lbs, content)

    exec_lbs = """      LoadBalancers:
        - ContainerName: executive-intelligence
          ContainerPort: 9009
          TargetGroupArn: !Ref ExecutiveTargetGroup
        - ContainerName: executive-intelligence
          ContainerPort: 9010
          TargetGroupArn: !Ref RmWorkspaceTargetGroup"""
    content = re.sub(r'      LoadBalancers:\n        - ContainerName: executive-intelligence\n          ContainerPort: 9009\n          TargetGroupArn: !Ref ExecutiveTargetGroup', exec_lbs, content)

    # Output dependencies fixes
    content = content.replace("DependsOn:\n      - HttpListener\n      - AuthPathRule", "DependsOn:\n      - HttpListener\n      - AuthPathRule\n      - EseAdminPathRule")
    content = content.replace("DependsOn:\n      - HttpListener\n      - ApiPathRule", "DependsOn:\n      - HttpListener\n      - CustomersPathRule\n      - ConsentPathRule\n      - GstPathRule\n      - AaPathRule\n      - FhcPathRule\n      - CreditPathRule\n      - CamPathRule\n      - OcenPathRule\n      - CkycPathRule\n      - McaPathRule\n      - EpfoPathRule")
    content = content.replace("DependsOn:\n      - HttpListener\n      - ExecPathRule", "DependsOn:\n      - HttpListener\n      - ExecPathRule\n      - RmWorkspacePathRule")

    with open("cloudformation-ecs-networking-new.yml", "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
