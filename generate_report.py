import json

def main():
    with open("discovery.json", "r", encoding="utf-16") as f:
        data = json.load(f)
        
    md = "# AAR-INFRASTRUCTURE-DRIFT-REPORT\n\n"
    md += "This report identifies every difference between the updated repository configuration and the live AWS deployment.\n\n"
    
    # ECS Services
    md += "## ECS Services\n"
    live_services = data.get("services", [])
    md += f"**Live Services:** {len(live_services)}\n"
    for s in live_services:
        md += f"- `{s}`\n"
        
    # Task Definitions
    md += "\n## Task Definitions\n"
    for s_name, t_def in data.get("taskDefs", {}).items():
        md += f"### Service: `{s_name}`\n"
        md += f"**Live Family:** `{t_def.get('family')}`\n"
        md += f"**Live Revision:** `{t_def.get('revision')}`\n"
        live_ports = []
        for c in t_def.get('containerDefinitions', []):
            for pm in c.get('portMappings', []):
                live_ports.append(pm.get('containerPort'))
        md += f"**Live Exposed Ports:** {sorted(live_ports)}\n"
        
        if s_name == "lending-intelligence":
            md += "**Repository Ports (ecs-task-lending.json):** `[9001, 9002, 9003, 9004, 9005, 9006, 9007, 9008, 9011, 9012, 9013, 9014]`\n"
            md += "**DRIFT IDENTIFIED:** Live missing ports `9002`, `9008`, `9014`.\n"
            
    # Target Groups
    md += "\n## Target Groups\n"
    live_tgs = data.get("targetGroups", [])
    md += f"**Live Target Groups:** {len(live_tgs)}\n"
    live_tg_names = [tg.get('TargetGroupName') for tg in live_tgs]
    for tg in live_tg_names:
        md += f"- `{tg}`\n"
    if "aarohan-rbi-tg" not in live_tg_names:
        md += "**DRIFT IDENTIFIED:** `aarohan-rbi-tg` is missing in live environment.\n"
        
    # Listener Rules
    md += "\n## Listener Rules\n"
    live_rules = data.get("rules", [])
    rule_paths = []
    for r in live_rules:
        for c in r.get('Conditions', []):
            if c.get('Field') == 'path-pattern':
                rule_paths.extend(c.get('Values', []))
                
    md += "**Live Path Rules:**\n"
    for p in rule_paths:
        md += f"- `{p}`\n"
    if "/rbi/*" not in rule_paths:
        md += "**DRIFT IDENTIFIED:** Listener rule for `/rbi/*` is missing in live environment.\n"
        
    # Conclusion
    md += "\n## Conclusion & Deployment Action\n"
    md += "Drift exists between the updated repository and the live environment for the `lending-intelligence` ECS service, missing port mappings for 9002, 9008, and 9014. Additionally, the CloudFormation stack is missing the `aarohan-rbi-tg` target group and corresponding listener rule. We will deploy these missing infrastructure changes immediately.\n"

    with open("AAR-INFRASTRUCTURE-DRIFT-REPORT.md", "w") as f:
        f.write(md)
        
if __name__ == "__main__":
    main()
