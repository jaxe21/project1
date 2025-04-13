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


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Extract form data
        email = request.form['email']
        firstname= request.form['first_name']
        lastname = request.form['last_name']

        try:
            add_new_user(email, firstname, lastname)
            flash('User added successfully!', 'success')
        
        except Exception:
            print("Something went wrong. Please Try again")

        return redirect(url_for('home'))
    else:

        return render_template('create_user.html')
    

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        email = request.form['email']

        try:
            delete_user_email(email)
            flash('User deleted successfully!', 'success')
        
        except Exception:
            print("Something went wrong. Please Try again")

        return redirect(url_for('home'))
    else:
        return render_template('delete_user.html')

@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        email = request.form['email']
        firstname= request.form['first_name']
        lastname = request.form['last_name']

        try:

            result = update_name(email, firstname, lastname)
            if result.get('success'):
                flash('User updated successfully!', 'success')
            else:
                flash("User update failed, please try again")
        
        except Exception:
            print("Something went wrong. Please Try again")

        return redirect(url_for('home'))
    else:
        return render_template('update_user.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('sign-in.html')

@app.route('/display_users')
def printallemails():
    users = print_users()
    return render_template('show_user.html', users = users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

