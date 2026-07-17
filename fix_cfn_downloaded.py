import yaml
import copy
import io

class AwsLoader(yaml.SafeLoader):
    pass
class AwsDumper(yaml.SafeDumper):
    pass

def construct_aws_ref(loader, node):
    return {"Ref": loader.construct_scalar(node)}
AwsLoader.add_constructor('!Ref', construct_aws_ref)

def construct_aws_getatt(loader, node):
    if isinstance(node, yaml.ScalarNode):
        return {"Fn::GetAtt": loader.construct_scalar(node).split(".")}
    elif isinstance(node, yaml.SequenceNode):
        return {"Fn::GetAtt": loader.construct_sequence(node)}
AwsLoader.add_constructor('!GetAtt', construct_aws_getatt)

def construct_aws_sub(loader, node):
    if isinstance(node, yaml.ScalarNode):
        return {"Fn::Sub": loader.construct_scalar(node)}
    elif isinstance(node, yaml.SequenceNode):
        return {"Fn::Sub": loader.construct_sequence(node)}
AwsLoader.add_constructor('!Sub', construct_aws_sub)

def represent_aws_ref(dumper, data):
    if isinstance(data, dict) and 'Ref' in data and len(data) == 1:
        return dumper.represent_scalar('!Ref', data['Ref'])
    return dumper.represent_dict(data)
AwsDumper.add_representer(dict, represent_aws_ref)

# Note: Downloaded AWS template will be in UTF-16 in powershell
with io.open('downloaded-cfn.yml', 'r', encoding='utf-16') as f:
    template = yaml.load(f, Loader=AwsLoader)

resources = template.get('Resources', {})

if 'LendingService' in resources:
    props = resources['LendingService'].get('Properties', {})
    props['LoadBalancers'] = [
        {
            'ContainerName': 'nginx-proxy',
            'ContainerPort': 80,
            'TargetGroupArn': {'Ref': 'LendingTargetGroup'}
        }
    ]

if 'LendingTargetGroup' in resources:
    props = resources['LendingTargetGroup'].get('Properties', {})
    props['Port'] = 80
    props['HealthCheckPort'] = '80'
    props['HealthCheckPath'] = '/livez'

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

for tg in target_groups_to_replace:
    if tg in resources:
        del resources[tg]

for res_name, res_val in resources.items():
    if res_val.get('Type') == 'AWS::ElasticLoadBalancingV2::TargetGroup':
        props = res_val.get('Properties', {})
        if 'Name' in props:
            del props['Name']

with io.open('cloudformation-ecs-networking.yml', 'w', encoding='utf-8') as f:
    yaml.dump(template, f, Dumper=AwsDumper, default_flow_style=False, sort_keys=False)
print("Updated CFN via YAML from downloaded template")
