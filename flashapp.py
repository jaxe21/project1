from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/index")
def index():
    countries = get_list_of_dictionaries()
    print("Countries:", countries)
    return render_template("index.html", results = countries)


@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Extract form data
        firstname= request.form['first_name']
        lastname = request.form['last_name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("First Name:", firstname, " ", lastname)
        
        flash('User added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('create_user.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('sign-in.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

