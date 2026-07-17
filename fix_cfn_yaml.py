import yaml
import copy

# Use a custom loader to preserve !Ref and other AWS tags (as simple strings or dicts)
class AwsLoader(yaml.SafeLoader):
    pass
class AwsDumper(yaml.SafeDumper):
    pass

def construct_aws_ref(loader, node):
    return {"Ref": loader.construct_scalar(node)}
AwsLoader.add_constructor('!Ref', construct_aws_ref)

def represent_aws_ref(dumper, data):
    if isinstance(data, dict) and 'Ref' in data and len(data) == 1:
        return dumper.represent_scalar('!Ref', data['Ref'])
    return dumper.represent_dict(data)
AwsDumper.add_representer(dict, represent_aws_ref)

with open('cloudformation-ecs-networking.yml', 'r') as f:
    template = yaml.load(f, Loader=AwsLoader)

resources = template.get('Resources', {})

# 1. Update LendingService LoadBalancers to use nginx-proxy on port 80
if 'LendingService' in resources:
    props = resources['LendingService'].get('Properties', {})
    props['LoadBalancers'] = [
        {
            'ContainerName': 'nginx-proxy',
            'ContainerPort': 80,
            'TargetGroupArn': {'Ref': 'LendingTargetGroup'}
        }
    ]

# 2. Update LendingTargetGroup to port 80
if 'LendingTargetGroup' in resources:
    props = resources['LendingTargetGroup'].get('Properties', {})
    props['Port'] = 80
    props['HealthCheckPort'] = '80'
    props['HealthCheckPath'] = '/livez'

# 3. For all path rules that point to Lending services, redirect to LendingTargetGroup
target_groups_to_replace = [
    'ConsentTargetGroup', 'GstTargetGroup', 'AaTargetGroup', 'FhcTargetGroup',
    'CreditTargetGroup', 'CamTargetGroup', 'OcenTargetGroup', 'CkycTargetGroup',
    'McaTargetGroup', 'EpfoTargetGroup', 'RbiTargetGroup'
]

for res_name, res_val in resources.items():
    if res_val.get('Type') == 'AWS::ElasticLoadBalancingV2::ListenerRule':
        props = res_val.get('Properties', {})
        actions = props.get('Actions', [])
        for action in actions:
            if action.get('Type') == 'forward':
                tg_arn = action.get('TargetGroupArn', {})
                if isinstance(tg_arn, dict) and tg_arn.get('Ref') in target_groups_to_replace:
                    action['TargetGroupArn'] = {'Ref': 'LendingTargetGroup'}

# 4. Delete the unused TargetGroup resources
for tg in target_groups_to_replace:
    if tg in resources:
        del resources[tg]

# 5. Remove Name property from ALL remaining TargetGroups
for res_name, res_val in resources.items():
    if res_val.get('Type') == 'AWS::ElasticLoadBalancingV2::TargetGroup':
        props = res_val.get('Properties', {})
        if 'Name' in props:
            del props['Name']

with open('cloudformation-ecs-networking.yml', 'w') as f:
    yaml.dump(template, f, Dumper=AwsDumper, default_flow_style=False, sort_keys=False)
print("Updated CFN via YAML")
