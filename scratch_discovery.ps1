Remove-Item Env:\AWS_ACCESS_KEY_ID -ErrorAction SilentlyContinue
Remove-Item Env:\AWS_SECRET_ACCESS_KEY -ErrorAction SilentlyContinue
Remove-Item Env:\AWS_SESSION_TOKEN -ErrorAction SilentlyContinue

$results = @{}

Write-Host "Discovering Services..."
$services = aws ecs list-services --cluster aarohan-hackathon-cluster --output json | ConvertFrom-Json
$results.services = $services.serviceArns

Write-Host "Discovering Target Groups..."
$tgs = aws elbv2 describe-target-groups --output json | ConvertFrom-Json
$results.targetGroups = $tgs.TargetGroups

Write-Host "Discovering Listeners..."
$listeners = aws elbv2 describe-listeners --load-balancer-arn arn:aws:elasticloadbalancing:ap-south-1:905417996641:loadbalancer/app/aarohan-alb/a8a0ed97070b0da7 --output json | ConvertFrom-Json
$results.listeners = $listeners.Listeners

$results.rules = @()
foreach ($listener in $listeners.Listeners) {
    Write-Host "Discovering Rules for Listener: $($listener.ListenerArn)"
    $rules = aws elbv2 describe-rules --listener-arn $listener.ListenerArn --output json | ConvertFrom-Json
    $results.rules += $rules.Rules
}

Write-Host "Discovering Tasks..."
$results.tasks = @{}
foreach ($serviceArn in $services.serviceArns) {
    $serviceName = ($serviceArn -split "/")[-1]
    $tasks = aws ecs list-tasks --cluster aarohan-hackathon-cluster --service-name $serviceName --output json | ConvertFrom-Json
    
    if ($tasks.taskArns.Count -gt 0) {
        $taskDetails = aws ecs describe-tasks --cluster aarohan-hackathon-cluster --tasks $tasks.taskArns --output json | ConvertFrom-Json
        $results.tasks[$serviceName] = $taskDetails.tasks
    } else {
        $results.tasks[$serviceName] = @()
    }
}

Write-Host "Discovering Task Definitions..."
$results.taskDefs = @{}
foreach ($serviceArn in $services.serviceArns) {
    $serviceName = ($serviceArn -split "/")[-1]
    $serviceDetails = aws ecs describe-services --cluster aarohan-hackathon-cluster --services $serviceName --output json | ConvertFrom-Json
    $taskDefArn = $serviceDetails.services[0].taskDefinition
    $taskDefDetails = aws ecs describe-task-definition --task-definition $taskDefArn --output json | ConvertFrom-Json
    $results.taskDefs[$serviceName] = $taskDefDetails.taskDefinition
}

$results | ConvertTo-Json -Depth 10 | Out-File "discovery.json"
Write-Host "Discovery complete. Saved to discovery.json"
