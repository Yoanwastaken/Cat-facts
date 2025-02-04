import requests

# Cat Facts API base URL for GET
CAT_FACTS_URL = "https://catfact.ninja/fact"

# Mock API base URL for POST, PUT, DELETE
MOCK_API_URL = "https://httpbin.org/anything"


def get_single_fact():
    """Fetch a single random cat fact."""
    try:
        response = requests.get(CAT_FACTS_URL)
        response.raise_for_status()
        data = response.json()
        print("Cat Fact:", data.get("fact"))
    except requests.exceptions.RequestException as e:
        print("Error in GET request:", str(e))


def get_multiple_facts(count):
    """Fetch multiple random cat facts."""
    for _ in range(count):
        get_single_fact()


def create_mock_fact(data):
    """Simulate creating a resource using POST."""
    try:
        response = requests.post(MOCK_API_URL, json=data)
        response.raise_for_status()
        print("POST Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error in POST request:", str(e))


def update_mock_fact(resource_id, data):
    """Simulate updating a resource using PUT."""
    try:
        response = requests.put(f"{MOCK_API_URL}/{resource_id}", json=data)
        response.raise_for_status()
        print("PUT Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error in PUT request:", str(e))


def delete_mock_fact(resource_id):
    """Simulate deleting a resource using DELETE."""
    try:
        response = requests.delete(f"{MOCK_API_URL}/{resource_id}")
        response.raise_for_status()
        print("DELETE Response:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error in DELETE request:", str(e))


def main():
    """Main menu for interacting with the program."""
    print("Welcome to the Advanced Cat Facts Program!")
    while True:
        print("\nMenu:")
        print("1. Fetch a single cat fact")
        print("2. Fetch multiple cat facts")
        print("3. Simulate creating a new fact (POST)")
        print("4. Simulate updating a fact (PUT)")
        print("5. Simulate deleting a fact (DELETE)")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            get_single_fact()
        elif choice == "2":
            try:
                count = int(input("How many facts would you like to fetch? "))
                if count <= 0:
                    print("Please enter a positive number.")
                else:
                    get_multiple_facts(count)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == "3":
            fact = input("Enter a new fact to simulate creation: ")
            create_mock_fact({"fact": fact, "type": "cat_fact"})
        elif choice == "4":
            resource_id = input("Enter the ID of the fact to update: ")
            updated_fact = input("Enter the updated fact: ")
            update_mock_fact(resource_id, {"fact": updated_fact, "type": "cat_fact"})
        elif choice == "5":
            resource_id = input("Enter the ID of the fact to delete: ")
            delete_mock_fact(resource_id)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
