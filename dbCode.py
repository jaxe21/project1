import pymysql
import pymysql.cursors
import creds
import boto3

TABLE_NAME = "Project1"

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

def get_conn():
    return pymysql.connect(
        host = creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )


def execute_query(query, args = ()):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, args)
            rows = cur.fetchall()
            return rows
    finally:
        conn.close()

def get_list_of_dictionaries():
    query = "SELECT Name, Population FROM country LIMIT 10;"
    return execute_query(query)


def add_new_user(email, firstname, lastname):
    response = table.put_item(
        Item ={
            'email': email,
            'First_Name' : firstname,
            'Last_Name' : lastname
        }
    )
    return response

def update_name(email, firstname, lastname):
    print(f"Received request to update user: {email} -> {firstname} {lastname}")

    existing_user = table.get_item(Key={'email': email})
    print("Existing user response:", existing_user)

    if 'Item' not in existing_user:
        print("User not found.")

        #This line of code runs if the user doesn't exist.
        return {"success": False, "reason": "User not found"}

    # If the user exists, then this code will run and update their name
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
    response = table.delete_item(Key={
        'email': email})
    return response

def get_top_10_of_city():
    query = ""
    return execute_query(query)