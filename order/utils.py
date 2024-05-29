from .models import user
import re

def getPrimaryUserId(new_user: user) -> int:
    fetched_users=user.objects.raw("select * from order_user where email = '{0}' or phoneNumber = '{1}' order by id asc Limit 1"  
                                   .format(new_user.email , new_user.phoneNumber) )
    parent_user = None
    print(fetched_users)
    for i in fetched_users:
        if(i.linkedId!=None):
            parent_user = i.linkedId
        else:
            parent_user = i.id
        break
    if parent_user!=None:
        return parent_user
    return -1

def getDbUser(new_user: user) -> user:
    existing_user = user.objects.filter(email = new_user.email, phoneNumber = new_user.phoneNumber).first()
    if existing_user != None:
        return existing_user
    return None

def getUserById(uid : int) -> user:
    return user.objects.get(id = uid)

def getAllAssociatedContacts(uid : int) -> list[user]:
    return user.objects.filter(linkedId = uid)

def updateUsersStatus(new_user: user , uid : int):
    secondary_users = user.objects.raw("select id from order_user where (email = '{0}' or phoneNumber = '{1}' ) and id != {2}"
                                       .format(new_user.email , new_user.phoneNumber,str(uid)) )
    secondary_users_db_string = ",".join(map(str, secondary_users))
    user.objects.raw(" update order_user set linkedId = {0} where ( id in ({1}) or linkedId in ({2}) ) "
                     .format(str(uid),secondary_users_db_string,secondary_users_db_string))
    
def getContact(primary_contact : user,secondary_contacts: list[user]) -> dict:
    cont = dict()
    cont['emails'] = set()
    cont['emails'].add(primary_contact.email)
    cont['primaryContatctId'] = primary_contact.id
    cont['phoneNumbers'] = set()
    cont['phoneNumbers'].add(primary_contact.phoneNumber)
    cont['secondaryContactIds'] = []
    for secondary_contact in secondary_contacts:
        cont['emails'].add(secondary_contact.email)
        cont['phoneNumbers'].add(secondary_contact.phoneNumber)
        cont['secondaryContactIds'].append(secondary_contact.id)
    cont['emails'] = list(cont['emails'])
    cont['phoneNumbers'] = list(cont['phoneNumbers'])
    return cont

def isEmailValid(email : str) -> bool:
    pat = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
    if re.fullmatch(pat, email):
        return True
    else:
        return False
    
def isPhoneValid(phone : str) -> bool:
    pat = re.compile(r"^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$")
    if re.fullmatch(pat, phone):
        return True
    else:
        return False