from pymongo import MongoClient
from settings import DBLINK
from settings import DB
import datetime,time


mdb=MongoClient(DBLINK)[DB]

def searchorsave(mdb,effective_user,message):
    user=mdb.users.find_one({"user_id":effective_user.id})
    if not user:
        user={
            "user_id":effective_user.id,
            "first_name":effective_user.first_name,
            "username":effective_user.username,
            "chat_id":message.chat.id,
            "time":message.chat.time
        }
        mdb.users.insert_one(user)
    return user

def saveBloodLevel(mdb,effective_user,sugar_level,timem):
    mdb.sugarlevel.insert_one({"user_id":effective_user.id,
                               "sugarLevel":sugar_level,
                               'date': timem})

