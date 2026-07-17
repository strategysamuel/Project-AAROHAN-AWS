param(
  [string]$ProjectId = $env:PROJECT_ID,
  [string]$Region = 'asia-south1',
  [string]$ServiceName = 'aarohan-portal',
  [string]$ImageName,
  [string]$ApiBaseUrl = $(if ([string]::IsNullOrWhiteSpace($env:VITE_API_BASE_URL)) { 'https://aarohan-demo-platform-679889922969.asia-south1.run.app' } else { $env:VITE_API_BASE_URL }),
  [string]$AuthApiBaseUrl = $(if ([string]::IsNullOrWhiteSpace($env:VITE_AUTH_API_BASE_URL)) { 'https://aarohan-demo-platform-679889922969.asia-south1.run.app' } else { $env:VITE_AUTH_API_BASE_URL })
)

if ([string]::IsNullOrWhiteSpace($ProjectId) -or [string]::IsNullOrWhiteSpace($ApiBaseUrl) -or [string]::IsNullOrWhiteSpace($AuthApiBaseUrl)) {
  throw 'Set ProjectId, ApiBaseUrl, and AuthApiBaseUrl before running this script.'
}

if ([string]::IsNullOrWhiteSpace($ImageName)) {
  $ImageName = "$Region-docker.pkg.dev/$ProjectId/aarohan/$ServiceName:latest"
}

$ErrorActionPreference = 'Stop'

gcloud config set project $ProjectId | Out-Null
gcloud auth configure-docker "$Region-docker.pkg.dev" --quiet | Out-Null

docker build `
  -f Dockerfile.portal `
  --build-arg VITE_API_BASE_URL=$ApiBaseUrl `
  --build-arg VITE_AUTH_API_BASE_URL=$AuthApiBaseUrl `
  -t $ImageName .

docker push $ImageName

gcloud run deploy $ServiceName `
  --image=$ImageName `
  --region=$Region `
  --platform=managed `
  --allow-unauthenticated `
  --port=8080
