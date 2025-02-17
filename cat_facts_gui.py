import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import requests

# Cat Facts API base URL for GET
CAT_FACTS_URL = "https://catfact.ninja/fact"

# Mock API base URL for POST, PUT, DELETE
MOCK_API_URL = "https://httpbin.org/anything"

class CatFactsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat Facts App")
        self.root.geometry("500x500")

        # Title Label
        tk.Label(root, text="Cat Facts Generator", font=("Arial", 16, "bold")).pack(pady=10)

        # Buttons for API Actions
        tk.Button(root, text="Fetch a Single Cat Fact", command=self.get_single_fact, width=30).pack(pady=5)
        tk.Button(root, text="Fetch Multiple Cat Facts", command=self.get_multiple_facts, width=30).pack(pady=5)
        tk.Button(root, text="Simulate Creating a Fact (POST)", command=self.create_mock_fact, width=30).pack(pady=5)
        tk.Button(root, text="Simulate Updating a Fact (PUT)", command=self.update_mock_fact, width=30).pack(pady=5)
        tk.Button(root, text="Simulate Deleting a Fact (DELETE)", command=self.delete_mock_fact, width=30).pack(pady=5)

        # Text Box for Displaying Output
        self.output_box = scrolledtext.ScrolledText(root, width=60, height=15, wrap=tk.WORD)
        self.output_box.pack(pady=10)

    def get_single_fact(self):
        """Fetch and display a single cat fact."""
        try:
            response = requests.get(CAT_FACTS_URL)
            response.raise_for_status()
            fact = response.json().get("fact", "No fact found.")
            self.display_output(f"Cat Fact: {fact}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch cat fact: {str(e)}")

    def get_multiple_facts(self):
        """Fetch multiple cat facts based on user input."""
        try:
            count = simpledialog.askinteger("Fetch Facts", "Enter number of facts:", minvalue=1, maxvalue=10)
            if count:
                facts = []
                for _ in range(count):
                    response = requests.get(CAT_FACTS_URL)
                    response.raise_for_status()
                    facts.append(response.json().get("fact", "No fact found."))
                self.display_output("\n".join(f"Fact {i+1}: {fact}" for i, fact in enumerate(facts)))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch multiple cat facts: {str(e)}")

    def create_mock_fact(self):
        """Simulate creating a new cat fact using POST."""
        fact = simpledialog.askstring("Create Fact", "Enter a new cat fact:")
        if fact:
            try:
                response = requests.post(MOCK_API_URL, json={"fact": fact, "type": "cat_fact"})
                response.raise_for_status()
                self.display_output(f"POST Response: {response.json()}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to create mock fact: {str(e)}")

    def update_mock_fact(self):
        """Simulate updating a cat fact using PUT."""
        resource_id = simpledialog.askstring("Update Fact", "Enter the ID of the fact to update:")
        updated_fact = simpledialog.askstring("Update Fact", "Enter the updated cat fact:")
        if resource_id and updated_fact:
            try:
                response = requests.put(f"{MOCK_API_URL}/{resource_id}", json={"fact": updated_fact, "type": "cat_fact"})
                response.raise_for_status()
                self.display_output(f"PUT Response: {response.json()}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to update mock fact: {str(e)}")

    def delete_mock_fact(self):
        """Simulate deleting a cat fact using DELETE."""
        resource_id = simpledialog.askstring("Delete Fact", "Enter the ID of the fact to delete:")
        if resource_id:
            try:
                response = requests.delete(f"{MOCK_API_URL}/{resource_id}")
                response.raise_for_status()
                self.display_output(f"DELETE Response: {response.status_code}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to delete mock fact: {str(e)}")

    def display_output(self, text):
        """Display text output in the scrollable text box."""
        self.output_box.insert(tk.END, text + "\n\n")
        self.output_box.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CatFactsApp(root)
    root.mainloop()
