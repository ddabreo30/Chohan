from mysql.connector.connection import MySQLConnection
from invalidInputException import InvalidInputException
import random
import mysql.connector
from mysql.connector import Error
from flask import Flask
from flask import jsonify
from flask import request


HOST_NAME = "localhost"


app = Flask(__name__)
# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route("/")
def main():

    # f = open("input.txt", "r+")
    # sql = create_connection(HOST_NAME, 'root')
    # cursor = sql.cursor()

    

    data = f.read()
    lst = []
    results = []
    data = data.split("\n")
    cont = True

    for line in data:
        line_items = line.split(',')
        dic = {
            "name": line_items[0],
            "play": line_items[1],
            "bet": line_items[2],
            "balance": 100
        }
        lst.append(dic)
    
    check_valid(lst)

    

    while cont:

        # print(lst)


        dice = random.randrange(1,7)
        print("dice roll", dice)

        lst = decrement_from_dictionary(lst)

        lst = calculate_winnings(lst, dice)

        for item in lst:
            print(item)
            results.append(item.copy())
        
    #     for item in lst:
    #         cursor.execute("INSERT INTO Players VALUES (\"" + item['name'] + "\"," + str(item['balance']) + ');')
    #     sql.commit()
        
        cont = check_has_money(lst)
    # cursor.close()
    # sql.close()
    return jsonify(results)


def check_has_money(lst):
    for item in lst:
        if item['balance'] == 0:
            print("done with game!")
            return False
    
    return True

def calculate_winnings(lst, dice):
    for item in lst: # loop each
        if dice % 2 == 0: # if dice is even
            if item['play'].lower() == 'cho': # if player bet even
                winnings = int(item['bet']) * 2 # double the input
                item['balance'] += int(winnings)
        else:
            if item['play'].lower() == 'han':
                winnings = int(item['bet']) * 2 # double the input
                item['balance'] += int(winnings)
    return lst


def decrement_from_dictionary(lst):
    for item in lst:
        item['balance'] -= int(item['bet'])
    return lst

def check_valid(lst):
    total = 0
    for item in lst:
        if item['play'].lower() == 'cho':
            total += int(item['bet'])
        else:
            total -= int(item['bet'])
    if total != 0:
        raise InvalidInputException

def create_connection(host_name, user_name, user_password=None) -> MySQLConnection:
    connection = None
    try:
        if user_name is not None:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                database="ChoHan",
                passwd=user_password
            )
        else:
            connection = mysql.connector.connect(
                host=host_name,
                database="ChoHan",
                user=user_name
            )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection("localhost", "root", "")

if __name__ == '__main__':
    # main()
    app.run(port=8000,debug=True)
