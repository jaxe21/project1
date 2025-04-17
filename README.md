# Project 1 CS 178: Spring 2025
## James Axe

## Introduction
In this project, users are able to create a profile and then select the countries they want in their top 10 list of the most populated cities in those countries. Users can select an infinite number of countries. If a user changes their name, they're able to do so using the update user function. If they enter an invalid email, they're sent back to the home page and told the update failed and to try again. Additionally, users are able to delete their accounts if they don't want their data stored anymore. Users are also able to sign in after making an account. This makes it much simpler for returning users.


## How to Install/Run
Download all parts of the repository to a folder. You will then need to create a creds file and enter the RDS username, password, database name, and link to the RDS containing the dataset. In terminal type python3 flashapp.py. Then click on the provided link. You should be directed to the Flash site. Continue reading to learn how to use the website.

If you prefer not to download the files, it is still usable! Users are able to run the file by going to the following link: http://44.204.169.238:8080/. Users can create a profile by clicking create new user and then entering their first and last name along with their email. Then the user will be able to sign in and select the countries they want to see the top 10 most populated cities of. To select multiple countries, hold down the control key on Windows or the command key on Mac while clicking on the countries. After pressing submit, you will be presented with a chart of the cities, countries, and populations. If you wish to return home and log out, just simply press the logout button. If you wish to update your name, simply press the update user button and type your email and new first and last name. If you wish to delete your data from the site, press Delete user, type in your email, and then press submit.

## Dependencies
This code relies on the user having Flask, pymysql, and boto3 installed on their terminal. The requirements file is included in the repository, so you just need to download Flask, pymysql, and boto3 as they're imported through the dbcode file. Having a strong internet connection is also a must for this code to run. 


#### Credits
ChatGPT helped me create the selection's HTML page. I described some of the features I wanted it to have, such as being able to select multiple countries, having it autofill, and also displaying the table. Having never used HTML before, I wasn't quite sure how to do this request, and ChatGPT was able to guide me in the right direction for it.
