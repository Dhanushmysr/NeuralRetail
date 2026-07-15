import requests
import time

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print(" NeuralRetail API Testing ")
print("=" * 60)


def test_endpoint(name, endpoint):
    start = time.time()

    response = requests.get(BASE_URL + endpoint)

    end = time.time()

    print(f"\n{name}")
    print("-" * 40)
    print("Status Code :", response.status_code)
    print("Response Time:", round((end - start) * 1000, 2), "ms")
    print("Response:")
    print(response.json())


# ----------------------------
# Test GET Endpoints
# ----------------------------

test_endpoint("Home", "/")

test_endpoint("Customers", "/customers")

test_endpoint("Revenue", "/revenue")

test_endpoint("Orders", "/orders")

test_endpoint("Top Country", "/top-country")

test_endpoint("Top Product", "/top-product")

test_endpoint("Monthly Sales", "/monthly-sales")

test_endpoint("Health", "/health")
print("\nPrediction API")
print("-" * 40)

payload = {
    "Total_Orders": 10,
    "Total_Revenue": 25000,
    "Average_Order_Value": 2500,
    "Purchase_Frequency": 8,
    "CLV": 30000,
    "Recency": 20,
    "Frequency": 10,
    "Monetary": 25000,
    "R_Score": 5,
    "F_Score": 4,
    "M_Score": 5
}

start = time.time()

response = requests.post(
    BASE_URL + "/predict-churn",
    json=payload
)

end = time.time()

print("Status Code :", response.status_code)
print("Response Time:", round((end-start)*1000,2), "ms")
print(response.json())

print("\nInvalid Prediction Request")
print("-"*40)

bad_payload = {
    "Total_Orders": 5
}

response = requests.post(
    BASE_URL + "/predict-churn",
    json=bad_payload
)

print("Status Code :", response.status_code)
print(response.json())