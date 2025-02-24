from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Cat Facts API base URL for GET
CAT_FACTS_URL = "https://catfact.ninja/fact"

# Mock API base URL for POST, PUT, DELETE
MOCK_API_URL = "https://httpbin.org/anything"

@app.route('/')
def home():
    return render_template('index.html', fact=None, facts=[], response=None)

@app.route('/get_single_fact', methods=['POST'])
def get_single_fact():
    try:
        response = requests.get(CAT_FACTS_URL)
        response.raise_for_status()
        fact = response.json().get("fact", "No fact found.")
        return render_template('index.html', fact=fact, facts=[], response=None)
    except requests.exceptions.RequestException as e:
        flash(f"Error fetching single cat fact: {str(e)}")
        return redirect(url_for('home'))

@app.route('/get_multiple_facts', methods=['POST'])
def get_multiple_facts():
    try:
        count = int(request.form.get('count', 1))
        facts = []
        for _ in range(count):
            response = requests.get(CAT_FACTS_URL)
            response.raise_for_status()
            facts.append(response.json().get("fact", "No fact found."))
        return render_template('index.html', fact=None, facts=facts, response=None)
    except requests.exceptions.RequestException as e:
        flash(f"Error fetching multiple cat facts: {str(e)}")
        return redirect(url_for('home'))

@app.route('/create_fact', methods=['POST'])
def create_mock_fact():
    fact = request.form.get('new_fact')
    if not fact:
        flash("Please enter a fact to create.")
        return redirect(url_for('home'))
    try:
        response = requests.post(MOCK_API_URL, json={"fact": fact, "type": "cat_fact"})
        response.raise_for_status()
        return render_template('index.html', fact=None, facts=[], response=response.json())
    except requests.exceptions.RequestException as e:
        flash(f"Error creating mock fact: {str(e)}")
        return redirect(url_for('home'))

@app.route('/update_fact', methods=['POST'])
def update_mock_fact():
    resource_id = request.form.get('update_id')
    updated_fact = request.form.get('updated_fact')
    if not resource_id or not updated_fact:
        flash("Please provide both Resource ID and Updated Fact.")
        return redirect(url_for('home'))
    try:
        response = requests.put(f"{MOCK_API_URL}/{resource_id}", json={"fact": updated_fact, "type": "cat_fact"})
        response.raise_for_status()
        return render_template('index.html', fact=None, facts=[], response=response.json())
    except requests.exceptions.RequestException as e:
        flash(f"Error updating mock fact: {str(e)}")
        return redirect(url_for('home'))

@app.route('/delete_fact', methods=['POST'])
def delete_mock_fact():
    resource_id = request.form.get('delete_id')
    if not resource_id:
        flash("Please enter the Resource ID to delete.")
        return redirect(url_for('home'))
    try:
        response = requests.delete(f"{MOCK_API_URL}/{resource_id}")
        response.raise_for_status()
        return render_template('index.html', fact=None, facts=[], response={"status": response.status_code})
    except requests.exceptions.RequestException as e:
        flash(f"Error deleting mock fact: {str(e)}")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
