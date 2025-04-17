from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone


#This just is the home page for my website. It has the buttons to the rest of my website.
@app.route('/')
def home():
    return render_template('home.html')

#This code is used for testing the connection to the database. It send the query of getting the first 10 countries.
@app.route("/index")
def index():
    countries = get_list_of_dictionaries()
    print("Countries:", countries)
    return render_template("index.html", results = countries)

 
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Takes the data from the submission and stores it as variables. 
        email = request.form['email']
        firstname= request.form['first_name']
        lastname = request.form['last_name']
        
        #Takes the variables and uses the add new user function to add them to the databae.
        try:
            add_new_user(email, firstname, lastname)
            flash('User added successfully!', 'success')
        
        #If the addition fails this code block runs and asks the user to try again.
        except Exception:
            print("Something went wrong. Please Try again")
        #The user is returned to the home page
        return redirect(url_for('home'))
    else:
        #The user is brought back to the create_user page to try again
        return render_template('create_user.html')
    

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    #Takes user input to delete the given email from the database.
    if request.method == 'POST':
        email = request.form['email']

        try:
            user = get_user_email(email)
            #If the user is not in the database this runs and redirects to home and displays the warning. If they are then next block does and deletes the user

            if not user:
                flash("Something went wrong. Please Try again", 'warning')
                return redirect(url_for('home'))
            #If the user is in the database this runs. If not then next block does and redirects to home and displays the warning.
            delete_user_email(email)
            flash('User deleted successfully!', 'success')
        except Exception:
            flash("Something went wrong. Please Try again")

        return redirect(url_for('home'))
    else:
        return render_template('delete_user.html')

@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    #Gets the users inputs and saves them.
    if request.method == 'POST':
        email = request.form['email']
        firstname= request.form['first_name']
        lastname = request.form['last_name']

        try:
            #Uses the update name function to update the user.
            result = update_name(email, firstname, lastname)
            if result.get('success'):
                flash('User updated successfully!', 'success')
            else:
                flash("User update failed, please try again", 'warning')
        
        except Exception:
            print("Something went wrong. Please Try again")

        return redirect(url_for('home'))
    else:
        return render_template('update_user.html')

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    #This gets the email from the sign in page, and checks if its in the table.
    if request.method == 'POST':
        email = request.form['email']
        user = table.get_item(Key = {'email': email})
        #If the user is in the table then this code runs and finds the first name of the user and if no first name then it uses guest.
        if 'Item' in user:
            firstname = user['Item'].get('First_Name', 'Guest')
            return redirect(url_for('selections', name=firstname))
        #If no user is found in the table with that email this runs.
        else:
            flash("User does not exist. Please create an account", "warning")
            return render_template('sign-in.html')
    
    return render_template('sign-in.html')
    
@app.route('/display_users')
def printallemails():
    #This just prints all the users.
    users = print_users()
    return render_template('show_user.html', users = users)

@app.route('/selections', methods=['GET', 'POST'])
def selections():
    if request.method == 'POST':
        #Takes the selected countries and puts them into a list.
        selected_countries = request.form.getlist("countries")
        #This gets the name of the user after sign in. If they somehow skip the login, then they're given guest.
        name = request.form.get("name", "Guest")
        #if countries are selected then it looks for cities within that country if not empty list.
        if selected_countries:
            city_matches = get_cities_by_country(selected_countries)
        else:
            city_matches = []

        #This takes those selected and allows for the welcome ______. It takes the selcted countries and seperates them with commas and sends the cities to the selections html.
        return render_template(
            "selections.html",
            success=True,
            name=name,
            selected_countries=", ".join(selected_countries),
            city_matches=city_matches,
            countries=get_countries()
        )
    #This gets the name from the url, gets all the countries from the data, and renders the selections html with the new selections.
    name = request.args.get("name", "Guest")
    countries = get_countries()
    return render_template('selections.html', countries=countries, name = name)

#This code starts a flash app server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

