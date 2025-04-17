import pymysql
import pymysql.cursors
import creds
import boto3

TABLE_NAME = "Project1"

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

def get_conn():
    #This code connects VScode to the SQL database.
    return pymysql.connect(
        host = creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )


def execute_query(query, args = ()):
    #This code uses that connection from get_conn and sends and query and returns the results.
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, args)
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()

def get_list_of_dictionaries():
    #This is a simple sql query that helps test the connection to the database.
    query = "SELECT Name, Population FROM country LIMIT 10;"
    return execute_query(query)


def add_new_user(email, firstname, lastname):
    #This code takes responses from the flashapp and creat_user.html file and puts them into the noSQL database in dyanmoDB. It returns the result of the response.
    response = table.put_item(
        Item ={
            'email': email,
            'First_Name' : firstname,
            'Last_Name' : lastname
        }
    )
    return response

def update_name(email, firstname, lastname):
    #This code checks to see if the user is in the database, takes a new name and then updates that in the noSQL database in dynamoDB.

    existing_user = table.get_item(Key={'email': email})
    if 'Item' not in existing_user:
        print("User not found.")

        return {"success": False, "reason": "User not found"}

    response = table.update_item(
        Key={'email': email},
        UpdateExpression= 'SET First_Name = :f, Last_Name = :l',
        ExpressionAttributeValues = {
            ':f': firstname,
            ':l': lastname         
        }
    )
    print("Update response:", response)

    return {"success": True}


def delete_user_email(email):
    #This code finds the given email and deletes it from the noSQL database in dynamoDB,
    response = table.delete_item(Key={
        'email': email})
    return response



def print_users():
    #This takes all the users in the dyanmo db database and returns them back to the flashapp.
    response = table.scan()
    users = response.get('Items', [])
    return users


def get_cities_by_country(country_names):
   #This sends a SQL query based on the countries selected and stores them in the placeholder variable. It executes the query and returns it to flashapp.
    placeholders = ','.join(['%s'] * len(country_names))

    query = f"""
        SELECT city.name AS City,
               country.name AS Country,
               city.population AS Population
        FROM city
        JOIN country ON city.countrycode = country.code
        WHERE country.name IN ({placeholders})
        ORDER BY city.population DESC
        LIMIT 10;
    """
    return execute_query(query, country_names)

def get_countries():
    #This gets all the countries in the database and returns them to the flashapp allowing them to be selected on the selections page.
    query = "SELECT Name FROM country ORDER BY NAME;"
    rows = execute_query(query)
    return [row['Name'] for row in rows]
