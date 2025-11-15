"""
Simple test script to verify the API endpoints work correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_heatmap_data():
    """Test the heatmap data endpoint"""
    print("Testing /api/v1/heatmap_data...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/heatmap_data")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Received {len(data.get('features', []))} heatmap points")
            print(f"  Average temperature: {data.get('metadata', {}).get('avg_temperature', 'N/A')}°C")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_simulation():
    """Test the simulation endpoint"""
    print("\nTesting /api/v1/simulate_intervention...")
    try:
        payload = {
            "interventions": [
                {
                    "type": "trees",
                    "count": 20,
                    "area": 0,
                    "location": [18.5204, 73.8567],
                    "base_temperature": 35
                }
            ]
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/simulate_intervention",
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Temperature reduction: {data.get('temperature_reduction', 0)}°C")
            print(f"  Energy saving: {data.get('energy_saving', 0)} MWh")
            print(f"  CO2 reduction: {data.get('co2_reduction', 0)} kg")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_recommendations():
    """Test the recommendations endpoint"""
    print("\nTesting /api/v1/recommendations...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/recommendations")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Received {len(data)} recommendations")
            if data:
                print(f"  First recommendation: {data[0].get('action', 'N/A')}")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_health_precautions():
    """Test the health precautions endpoint"""
    print("\nTesting /api/v1/health_precautions...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health_precautions")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Received {len(data)} health precautions")
            if data:
                print(f"  First precaution: {data[0].get('title', 'N/A')}")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("=" * 50)
    print("UHI Mitigation API Test Suite")
    print("=" * 50)
    
    results = []
    results.append(("Heatmap Data", test_heatmap_data()))
    results.append(("Simulation", test_simulation()))
    results.append(("Recommendations", test_recommendations()))
    results.append(("Health Precautions", test_health_precautions()))
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print("\n" + "=" * 50)
    if all_passed:
        print("All tests passed! ✓")
    else:
        print("Some tests failed. Please check the errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main()


