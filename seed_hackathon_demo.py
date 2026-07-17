import urllib.request
import urllib.error
import json
import time

def post(url, payload=None):
    if payload:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    else:
        req = urllib.request.Request(url, method='POST')
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

def get(url):
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Failed GET {url}: {e.code} - {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Failed GET {url}: {e}")
        return None


def seed_data():
    print("Seeding AAROHAN Hackathon Demo Data...")
    
    # 2. CKYC Service (Port 9011)
    print("\n--- Seeding CKYC ---")
    ckyc_search_payload = {"pan": "ABCDE1234F"}
    post("http://localhost:9011/ckyc/search", ckyc_search_payload)
    
    # Create record for 99 manually to ensure it exists
    ckyc_99_payload = {
        "customer_id": 99,
        "ckyc_number": "30049281726355",
        "full_name": "Priya Textile Works",
        "dob": "12-08-1988",
        "pan": "ABCDE1234G",
        "aadhaar_masked": "XXXXXXXX1234",
        "address": "123 Demo St",
        "mobile": "9876543210",
        "email": "info@ckyc.gov.in",
        "kyc_status": "CLEAN"
    }
    post("http://localhost:9011/ckyc/records", ckyc_99_payload)
    put("http://localhost:9011/ckyc/records/125", {"kyc_status": "CLEAN"})

    # 3. Account Aggregator Service (Port 9004)
    print("\n--- Seeding Account Aggregator ---")
    aa_discover = {"customer_mobile": "9876543210"}
    post("http://localhost:9004/aa/discover/99", aa_discover)
    
    aa_link = [
        {
            "account_ref_num": "REF123456",
            "masked_acc_num": "XXXX-XXXX-1234",
            "bank_name": "HDFC Bank",
            "account_type": "CURRENT",
            "balance": 250000.00
        }
    ]
    post("http://localhost:9004/aa/link/99", aa_link)
    post("http://localhost:9004/aa/replay/99")

    # 4. GST Service (Port 9003)
    print("\n--- Seeding GST ---")
    post("http://localhost:9003/gst/sync/99", {"gstin": "27AADCB2230M1Z2"})

    # 5. EPFO Service (Port 9013)
    print("\n--- Seeding EPFO ---")
    epfo_sync = {"uan": "100123456789", "establishment_id": "MHBAN0000012000"}
    post("http://localhost:9013/epfo/sync/99", epfo_sync)
    post("http://localhost:9013/epfo/analytics/99/re-run")

    # 6. MCA Service (Port 9012)
    print("\n--- Seeding MCA ---")
    mca_sync = {"cin": "U12345MH2020P123456"}
    post("http://localhost:9012/mca/sync/99", mca_sync)
    post("http://localhost:9012/mca/analytics/99/re-run")

    # 7. Financial Health Card (Port 9005)
    print("\n--- Seeding Financial Health Card ---")
    post("http://localhost:9005/fhc/generate/99")

    # 8. Credit Decision (Port 9006)
    print("\n--- Seeding Credit Decision ---")
    post("http://localhost:9006/credit/evaluate/99")
    
    # 9. CAM Service (Port 9007)
    print("\n--- Seeding CAM ---")
    post("http://localhost:9007/cam/generate/99")

    print("\n[SUCCESS] Data Seeding Completed!")

if __name__ == "__main__":
    seed_data()
