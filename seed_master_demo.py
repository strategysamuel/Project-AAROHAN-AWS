import urllib.request
import urllib.error
import json
import time

def post(url, payload=None):
    if payload:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    else:
        req = urllib.request.Request(url, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Failed POST {url}: {e.code} - {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Failed POST {url}: {e}")
        return None

def put(url, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='PUT')
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Failed PUT {url}: {e.code} - {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Failed PUT {url}: {e}")
        return None

def seed_data():
    print("====================================================")
    print("PHASE 4: MASTER SEED ORCHESTRATOR (DYNAMIC IDs)")
    print("====================================================")
    
    # We will seed one persona: Priya Textile Works
    persona_name = "Priya Textile Works"
    print(f"\n--- 1. Loading Persona: {persona_name} ---")
    persona_res = post("http://localhost:9001/customers/load-persona", {"persona_name": persona_name})
    if not persona_res or "persona" not in persona_res:
        print("Failed to load persona. Is onboarding-service running?")
        return
    
    persona = persona_res["persona"]
    
    # Create Customer via Onboarding
    print("\n--- 2. Registering Customer ---")
    customer_payload = {
        "legal_name": persona["legal_name"],
        "mobile_number": persona["mobile_number"],
        "email": persona["email"],
        "pan": persona["pan"],
        "aadhaar_masked": persona["aadhaar_masked"],
        "district": persona["district"],
        "persona_name": persona["persona_name"],
        "onboarding_status": "SUBMITTED",
        "addresses": [
            {
                "address_type": "REGISTERED",
                "address_line1": "123 Market St",
                "address_line2": "",
                "city": persona.get("district", "Mumbai"),
                "state": "MH",
                "pincode": "400001"
            }
        ],
        "businesses": [
            {
                "trade_name": persona["business"]["trade_name"],
                "gstin": persona["business"]["gstin"],
                "udyam_number": persona["business"]["udyam_number"],
                "constitution_type": persona["business"]["constitution_type"],
                "annual_turnover": persona["business"]["annual_turnover"],
                "industry_segment": persona["business"]["industry_segment"],
                "business_vintage_years": persona["business"]["business_vintage_years"],
                "employee_count": persona["business"]["employee_count"],
                "existing_banking": persona["business"]["existing_banking"],
                "lifecycle_state": "ACTIVE",
                "directors": [
                    {
                        "full_name": persona["legal_name"],
                        "pan": persona["pan"],
                        "aadhaar_masked": persona["aadhaar_masked"],
                        "mobile": persona["mobile_number"]
                    }
                ]
            }
        ]
    }
    
    customer = post("http://localhost:9001/customers", customer_payload)
    if not customer:
        print("Failed to create customer. Exiting.")
        return
        
    customer_id = customer["id"]
    pan = customer["pan"]
    gstin = customer["businesses"][0]["gstin"]
    print(f"✅ Created Customer! ID: {customer_id} | PAN: {pan} | GSTIN: {gstin}")

    # Start Workflow
    print("\n--- 3. Starting MSME Lending Journey Workflow ---")
    wf_res = post(f"http://localhost:9001/customers/{customer_id}/start-workflow")
    if wf_res:
        print(f"✅ Workflow Started: {wf_res.get('workflow_id')}")

    # GST
    print("\n--- 4. Seeding GST ---")
    gst_res = post(f"http://localhost:9003/gst/sync/{customer_id}", {"gstin": gstin})
    if gst_res: print("✅ GST Synced")

    # CKYC
    print("\n--- 5. Seeding CKYC ---")
    ckyc_search = post("http://localhost:9011/ckyc/search", {"pan": pan})
    ckyc_payload = {
        "customer_id": customer_id,
        "ckyc_number": "30049281726355",
        "full_name": persona["legal_name"],
        "dob": "12-08-1988",
        "pan": pan,
        "aadhaar_masked": persona["aadhaar_masked"],
        "address": "123 Demo St",
        "mobile": persona["mobile_number"],
        "email": persona["email"],
        "kyc_status": "CLEAN"
    }
    ckyc_res = post("http://localhost:9011/ckyc/records", ckyc_payload)
    if ckyc_res: print("✅ CKYC Seeded")

    # AA
    print("\n--- 6. Seeding Account Aggregator ---")
    aa_discover = post(f"http://localhost:9004/aa/discover/{customer_id}", {"customer_mobile": persona["mobile_number"]})
    aa_link = [
        {
            "account_ref_num": "REF123456",
            "masked_acc_num": "XXXX-XXXX-1234",
            "bank_name": "HDFC Bank",
            "account_type": "CURRENT",
            "balance": 250000.00
        }
    ]
    aa_link_res = post(f"http://localhost:9004/aa/link/{customer_id}", aa_link)
    aa_replay = post(f"http://localhost:9004/aa/replay/{customer_id}")
    if aa_replay: print("✅ AA Linked and Replayed")

    # EPFO
    print("\n--- 7. Seeding EPFO ---")
    epfo_sync = post(f"http://localhost:9013/epfo/sync/{customer_id}", {"uan": "100123456789", "establishment_id": "MHBAN0000012000"})
    post(f"http://localhost:9013/epfo/analytics/{customer_id}/re-run")
    if epfo_sync: print("✅ EPFO Synced")

    # MCA
    print("\n--- 8. Seeding MCA ---")
    mca_sync = post(f"http://localhost:9012/mca/sync/{customer_id}", {"cin": persona["business"].get("cin", "U12345MH2020P123456")})
    post(f"http://localhost:9012/mca/analytics/{customer_id}/re-run")
    if mca_sync: print("✅ MCA Synced")

    # FHC
    print("\n--- 9. Generating Financial Health Card ---")
    fhc_gen = post(f"http://localhost:9005/fhc/generate/{customer_id}")
    if fhc_gen: print("✅ Financial Health Card Generated")

    # Credit Engine
    print("\n--- 10. Credit Decision ---")
    credit_gen = post(f"http://localhost:9006/credit/evaluate/{customer_id}")
    if credit_gen: print("✅ Credit Evaluated")

    # CAM Service
    print("\n--- 11. CAM Service ---")
    cam_gen = post(f"http://localhost:9007/cam/generate/{customer_id}")
    if cam_gen: print("✅ CAM Generated")
    
    print("\n[SUCCESS] Master Seeding Completed using Dynamic IDs.")

if __name__ == "__main__":
    seed_data()
