from flask import Flask
from flask import jsonify
from flask import request
import mysql.connector
from mysql.connector import Error
import datetime
import logging.config

##################################
# DB Details. We can read it from separate config
##################################
DBHOST="XXX.XXX.XXX.XXX"
DBNAME="test"
DBUSER="test"
DBPASSWORD="test"

###############################
# Logging related work and can be tuned here.Change level as per your requirement
###############################
logging.basicConfig(filename='birthday_service.log',filemode='a',format='%(asctime)s | %(levelname)s | %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = Flask(__name__)

def user_sanity_check(username, dob):
    print("Entered in user_sanity_check()...")
    #Check for digit test in username
    if username.isdigit() == True or username.isalpha() == False:
        print("Error: Incorrect Username format as it includes digits and provided username is:{1}".format(username.isdigit(),username))
        return 1

    #Check for DOB sanity
    try:
        datetime.datetime.strptime(dob, '%Y-%m-%d')
        today_date = datetime.datetime.today().date()
        if dob == datetime.datetime.strftime(today_date, '%Y-%m-%d'):
            print("Error: Mentioned DOB can't be Today's date.Entered DOB:{0} and Today Date:{1}!".format(dob, datetime.datetime.today().date()))
            return 1
    except ValueError as error:
        print("Error: Incorrect data format found for DOB as it should be [YYYY-MM-DD]!".format(error))
        return 1

    return 0

def get_birthday_days(dob,today):
    logger.debug("Entered in get_birthday_days()...")
    if (
            today.month == dob.month
            and today.day >= dob.day
            or today.month > dob.month
    ):
        nextBirthdayYear = today.year + 1
    else:
        nextBirthdayYear = today.year

    nextBirthday = datetime.date(nextBirthdayYear, dob.month, dob.day)
    diff = nextBirthday - today
    logger.debug("Next Birthday Year:{0}, Day:{1} and Days left for Birthday are:{2}".format(nextBirthdayYear,nextBirthday,diff.days))
    return diff.days

@app.route('/hello/<username>', methods=['PUT'])
def insert_user_birthday(username):
    try:
        dob = request.json['dateOfBirth']
        logger.debug("Received username:{0} and DOB in HTTP JSON request is:{1}".format(username, dob))

        sanity_status = user_sanity_check(username, dob)

        if sanity_status == 0:
            logger.debug("Sanity passed!")
        else:
            logger.debug("Sanity Failed!")
            return '', 404
    except Error as error:
        logger.error("Exception while json parsing.Username:{0} and DOB:{1}! Exception: {2}".format(username,dob,error))
        return '', 404

    try:
        connection = mysql.connector.connect(host=DBHOST, database=DBNAME, user=DBUSER, passwd=DBPASSWORD)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            logger.debug("Connected to Shared SRE MariaDB database... MySQL Server version on ".format(db_Info))
            cursor = connection.cursor()

            select_user_details_string = "select count(*) from user_details where username = '" + username + "'"
            insert_user_details_string = "insert into user_details (username, dob) values ('" + username + "','" + dob + "')"
            update_user_details_string = "update user_details set dob = '" + dob + "' where username = '" + username + "'"

            logger.debug("Select user details string is:{0}".format(select_user_details_string))
            logger.debug("Update query is:{0}".format(update_user_details_string))

            cursor.execute(select_user_details_string)
            result = cursor.fetchone()
            number_of_rows = result[0]

            logger.debug("Number of user exist with given name[Verificaiton Step]: Result:{0}".format(result[0]))
            if number_of_rows == 1:
                logger.debug("User already exist in DB so updating.Number of rows updated: {0}".format(number_of_rows))
                cursor.execute(update_user_details_string)
                if cursor.rowcount >= 1:
                   connection.commit()
                   return '', 204
                else:
                   logger.debug("Error while user update. Possibility that user already exist! Result:{0}".format(cursor.rowcount))
                   return '', 404
            else:
                logger.debug("User details not found for username: {0} as returned row count is :{1}".format(username,number_of_rows))
                cursor.execute(insert_user_details_string)
                if cursor.rowcount == 1:
                    connection.commit()
                    logger.debug("New User Successfully Inserted.{0}".format(cursor.rowcount))
                    return '', 204
                else:
                    logger.debug("Error while user details insertion.Result:{0}".format(number_of_rows))
                    return '', 404
    except Error as error:
        logger.error("Error while connecting to MySQL".format(error))
        return '', 404
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            logger.debug("MySQL connection is closed after user DB update[PUT fn()]!")


@app.route('/hello/<username>', methods=['GET'])
def get_birthday_message(username):
    try:
        connection = mysql.connector.connect(host=DBHOST, database=DBNAME, user=DBUSER, passwd=DBPASSWORD)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            logger.debug("Connected to Shared SRE MariaDB database... MySQL Server version is:{0}".format(db_Info))
            cursor = connection.cursor()
            select_user_details_string = "select dob from user_details where username = '" + username + "'"
            logger.debug("[GET BIRTHDAY]Select user details string is:{0}".format(select_user_details_string))
            cursor.execute(select_user_details_string)
            result = cursor.fetchone()

            logger.debug("Number of user exist with given name[Get DOB].Result:{0}".format(cursor.rowcount))
            if cursor.rowcount >= 1:
                logger.debug("User exists in DB so get DOB.Number of rows returned:{0}".format(cursor.rowcount))
                dob = result[0]
                logger.debug("Returned DOB for GET request is:{0}".format(dob))
            else:
                    logger.error("Error:User doesn't exist! Result:{0}".format(cursor.rowcount))
                    return '', 404

            days = get_birthday_days(dob, datetime.date.today())
            if int(days) == 0:
                message_value = "Hello, " + username + "!Happy Birthday!"
            else:
                message_value = "Hello, " + username + "!Your birthday is in " + str(days) + " day(s)"

            return jsonify({'message': message_value})
    except Error as error:
        logger.error("Error while connecting to MySQL during get for username:{0}.Exception:".format(username,error))
        return '', 404
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            logger.debug("MySQL connection is closed after user DB update[GET fn()]!")

# EB looks for an 'application' callable by default.


############### Main Programm #############
if __name__ == "__main__":
    logger.debug("*************************************************")
    logger.debug("** Starting Birthday API Service built by Shailender **")
    logger.debug("*************************************************")
	app.run()
    #app.run(host='127.0.0.1',debug=True, port=5001)
    #app.run(host='0.0.0.0',debug=True, port=5001)
