#!/bin/bash
# Project AAROHAN - Local Hackathon Testing Script
# Test 3-container architecture locally before AWS deployment

set -e

echo "🧪 Project AAROHAN - Local Hackathon Test"
echo "=========================================="

# Step 1: Start services
echo ""
echo "🚀 Starting 3-container architecture..."
docker-compose -f docker-compose.hackathon.yml up -d

# Step 2: Wait for services to start
echo ""
echo "⏳ Waiting 30 seconds for services to initialize..."
sleep 30

# Step 3: Test all endpoints
echo ""
echo "🔍 Testing Container 1 (Identity Platform)..."
curl -f http://localhost:9000/livez && echo "✅ auth-service (9000) OK" || echo "❌ auth-service (9000) FAILED"
curl -f http://localhost:9090/livez && echo "✅ ese-admin-service (9090) OK" || echo "❌ ese-admin-service (9090) FAILED"

echo ""
echo "🔍 Testing Container 2 (Lending Intelligence)..."
curl -f http://localhost:9001/livez && echo "✅ onboarding-service (9001) OK" || echo "❌ onboarding-service (9001) FAILED"
curl -f http://localhost:9003/livez && echo "✅ gst-service (9003) OK" || echo "❌ gst-service (9003) FAILED"
curl -f http://localhost:9004/livez && echo "✅ aa-service (9004) OK" || echo "❌ aa-service (9004) FAILED"
curl -f http://localhost:9005/livez && echo "✅ fhc-service (9005) OK" || echo "❌ fhc-service (9005) FAILED"
curl -f http://localhost:9006/livez && echo "✅ credit-engine (9006) OK" || echo "❌ credit-engine (9006) FAILED"
curl -f http://localhost:9007/livez && echo "✅ cam-service (9007) OK" || echo "❌ cam-service (9007) FAILED"
curl -f http://localhost:9011/livez && echo "✅ ckyc-service (9011) OK" || echo "❌ ckyc-service (9011) FAILED"
curl -f http://localhost:9012/livez && echo "✅ mca-service (9012) OK" || echo "❌ mca-service (9012) FAILED"
curl -f http://localhost:9013/livez && echo "✅ epfo-service (9013) OK" || echo "❌ epfo-service (9013) FAILED"

echo ""
echo "🔍 Testing Container 3 (Executive Intelligence)..."
curl -f http://localhost:9009/livez && echo "✅ exec-service (9009) OK" || echo "❌ exec-service (9009) FAILED"

echo ""
echo "📊 Container Status:"
docker-compose -f docker-compose.hackathon.yml ps

echo ""
echo "✅ Local testing complete!"
echo ""
echo "To view logs: docker-compose -f docker-compose.hackathon.yml logs -f [service-name]"
echo "To stop: docker-compose -f docker-compose.hackathon.yml down"
