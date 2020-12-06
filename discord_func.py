import mysql.connector
import pymongo
import random
import api_func
import traceback
import time

myclient = pymongo.MongoClient("mongodb+srv://Jimmy:Chips@doobie.jsw33.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = myclient.test
print(myclient.list_database_names())
Database = myclient.get_database('ZaydsSwill') 
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
Zayd = Database.Zayd

#db = myclient["types"]
#print(myclient.list_database_names())
#dblist = myclient.list_database_names()
#if "types" in dblist:
#  print("The database exists.")
#words = db["POS"]
cnx = mysql.connector.connect(user='root', password='pissword',
                      host='127.0.0.1',
                      database='discord_bot')
                      
cursor = cnx.cursor(buffered = True)
print("Succesfully connected to discord_bot database!")



#DB_NAME = 'discord_bot'
#try:
#    cursor.execute("USE {}".format())
#except mysql.connector.Error as err:
 #   print('no worky mr jones')

def test():
    print("it prints!")

def add_on_message(message_id, user_id, message, length, channel_name, time):
    args = [message_id, user_id, message, length, channel_name, time]    
    updateMessages(args) #args: message_id, user_id message, length, channel_name, time
    

def create_new_user(id,name,pref_name,greeting):

    new_user = "INSERT INTO Users (ID, User_Name, Preferred_Name, Default_Greeting) VALUES ('{user_id}', '{nam}', '{pnam}', '{gret}')"
    add_user = new_user.format(user_id = id, nam = str(name), pnam = str(pref_name), gret = str(greeting))
    #data_user = (id, name, pref_name, greeting)
    print(add_user)
    try:
        cursor.execute(add_user)
        print('commit time')
        cnx.commit()
        return None, 0
    except Exception as inst:
        print((type(inst)))
        return "This user already exists everyone sucks", 1

def get_all_users():
    query = "SELECT ID FROM Users"
    cursor.execute(query)
    users = []
    for user in cursor:
        users.append(int(user[0]))
    return users

def set_preferred_name(pref_name,id):
    set_preferred_name = "UPDATE Users SET Preferred_Name = '{pnam}' WHERE ID = '{user_id}'"
    query = set_preferred_name.format(pnam = pref_name, user_id = id)
    try:
        cursor.execute(query)
        cnx.commit()
        return None, 0
    except:
        return "Error: There is no user with this ID to change the preferred name of", 1
    

def get_name(id):

    query = "SELECT User_Name FROM Users WHERE ID = '{user_id}'".format(user_id = id)
    print(query)
    try:
        cursor.execute(query)
        for name in cursor:
            return name[0], 0
    except:
        return "There is no user with this name", 1

def set_greeting(greeting,id):
    #print('whats')
    data = "UPDATE Users SET Default_Greeting = '{gret}' WHERE ID = '{user_id}'"
    query = data.format(gret = greeting, user_id = id)
    print(query)
    try:
        cursor.execute(query)
        cnx.commit()
        return None, 0
    except:
        return "Error: There is no User with this ID to change the greeting of", 1

def get_greeting(id):
    print("Getting greeting")
    query = "SELECT Default_Greeting FROM Users WHERE ID = '{user_id}'".format(user_id=id)
    try:
        cursor.execute(query)
        for gret in cursor:
            print(gret[0])
            return gret[0], 0
    except:
        return "Sad because this user doesn't exist so there is no greeting", 1
        
def delete_user(id):
    query = "Delete FROM Users WHERE ID = '{user_id}'".format(user_id=id)
    print(query)
    try:
        cursor.execute(query)
        cnx.commit()
        return None, 0
    except:
        return "Error: This user does not exist to be deleted", 1


def wordsearch(args, id): #channel is a list, wordsearch is the word you want to search, id is the id that you want to use
    arr = args.split()
    if (len(arr) != 3):
        return "Error: Correct format should be !wordsearch {channel 1} {channel 2} {word}", 1
    ch1 = arr[0]
    ch2 = arr[1]
    word_to_search = arr[2]
    #add each line in discord to the database as it is said with a user argument
    query = "Select User_Name FROM Messages join Users on Users.ID = Messages.User_ID WHERE (Messages.Channel_Name='{chan1}' or  Messages.Channel_Name = '{chan2}') and Messages.Message like '%{word}%' GROUP BY User_Name"
    data = query.format(chan1=ch1,chan2=ch2 , word = word_to_search)
    try:
        cursor.execute(data)
        users = []
        for u in cursor:
            print(u)
            users.append(u[0])
        cnx.commit()
        return users, 0 #messages in this case would be users that is selected from the channels
    except:
        return "Error: The wordsearch has failed", 1


def longmessage(args, id):
    arr = args.split()
    if (len(arr) != 2):
        return "Error: Correct format should be !longmessage [length]", 1
    ch1 = arr[0]
    message_length = arr[1]
    query = "SELECT User_Name, message FROM Messages join Users on Messages.User_ID = Users.ID  WHERE Messages.Length > '{length}' and Messages.Channel_Name = '{ch1}' GROUP BY User_Name, message"
    data = query.format(length = message_length, ch1 = ch1)
    users = []
    messages = []
    try:
        cursor.execute(data)
        for u in cursor:
            users.append(u[0])
            messages.append(u[1])
        cnx.commit()
        return (users, messages), 0 #x in this case would be users that is selected from the channels
    except:
        return "Error: The wordsearch has failed", 1

#advanced 1  done by davin the god king lord himself thank you davin sweetheart
def updateResponse(args):
    a = args[0] #id #primary key
    b = args[1] #response 
    c = args[2] #category
    d = args[3] #sentiment
    e = args[4] #entity
    f = args[5] #entity_setnimetn 
    g = args[6] #channel_name
    query = "INSERT INTO RESPONSES VALUES ('{a}', '{b}', '{c}', {d}, '{e}', {f}, '{g}')"
    data = query.format(a = a, b = b, c = c, d = d, e = e, f = f, g = g)
    #print("Inserting into table")
    try:
        cursor.execute(data)
        cnx.commit()
        return None, 0
    except:
        return "Error: The update failed for Responses table", 1

def getResponse(args):
    global cursor
    #cursor1 = cnx.cursor(buffered = True)
    a = args[0] #id #primary key
    b = args[1] #category
    c = args[2] #sentiment
    d = args[3] #entity
    e = args[4] #entity_setnimetn 
    args.append("")
    
    try:
        result = cursor.callproc("GetResponse", args)
        response = result[5]
        print(response)
        return response, 0
    except Exception:
        traceback.print_exc()
        return "Error: The grabing output failed for Responses table", 1

"""advanced 2
    - Need another no sql database, basically no primary key to get the data its all passed in
    - 
"""

def meany(message): #refers to typer of word, adj verb, noun
    #update the nosql database with the word and the type passed in
    #for example use adj as first index and noun is the last word of the setance and verb first 
    print('entering meany')
    listoftypes = api_func.get_pos(message.content)
    #print(listoftypes)

    for tup in listoftypes:
        word, pos = tup
        if pos == "NOUN" or pos == "VERB" or pos == "ADJ":
            myword = {"word": word.content, "partofspeech": pos}
            Zayd.insert_one(myword)
        else:
            continue    


def mad():
    #repeat the words that are in the nosql database in ascendiong order
    #adj, verb, noun
    #!mad -> you *verb* *adjective* *noun* -> 
    nouns = list(Zayd.find({"partofspeech":"NOUN"},{"_id":0, "partofspeech":0}))
    verbs = list(Zayd.find({"partofspeech":"VERB"}, {"_id": 0, "partofspeech": 0}))
    adjs = list(Zayd.find({"partofspeech":"ADJ"}, {"_id": 0, "partofspeech": 0}))
    return "you " + random.choice(verbs)["word"] + " a " + random.choice(adjs)["word"] + " " + random.choice(nouns)["word"]




def updateMessages(args):
    a = args[0] #message_id #primary key
    b = args[1] #user_id
    c = args[2] #message_data
    d = args[3] #length
    e = args[4] #channel_name
    f = args[5] #time
    query = "INSERT INTO MESSAGES  VALUES ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}')"
    data = query.format(a = a, b = b, c = c, d = d, e = e, f = f)
    try:
        cursor.execute(data)
        cnx.commit()
        return None, 0
    except:
        return "Error: The update failed for Messages table", 1



#
#get_all_users()
#create_new_user(554363,'hehe','haha','ono')
#cnx.close()e(verbs)["word"] + " a " + random.choice(adjs)["word"] + random.choice(nouns)["word"]
