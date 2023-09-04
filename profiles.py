import random, os, json, shutil
from datetime import datetime


userProfilePath = os.getcwd() + "/profiles/users"
defaultProfilePath = os.getcwd() + "/profiles/default"

def save_config(directory, account_id, data):
    with open(os.path.join(userProfilePath + "/" + account_id + ".json"), "w") as file:
        json.dump(data, file, indent=2)

def create_response(profile_data, profile_id, rvn):
    #print("profile data: " + str(profile_data))
    rvn = int(rvn)
    response_data = {
        "profileRevision": rvn + 1 if rvn else 1,
        "profileId": profile_id,
        "profileChangesBaseRevision": rvn + 1 if rvn else 1,
        "profileChanges": [
            {
                "changeType": "fullProfileUpdate",
                "profile": profile_data
            }
        ],
        "profileCommandRevision": rvn + 1 if rvn else 1,
        "serverTime": datetime.now().isoformat(),
        "responseVersion": 1
    }
    return json.dumps(response_data, indent=4)  # Convert dictionary to JSON with proper indentation

def loadProfile(profileId):
    
    try:
        with open(f'{defaultProfilePath}/profile_{profileId}.json') as file:
            config = json.load(file)
            return config
    except Exception as error:
        print("[Profiles] load profile error, error:", error)
    

def loadConfig(accountId):
    check_and_create_profile(accountId)
    try:
        with open(f'{userProfilePath}/{accountId}.json') as file:
            config = json.load(file)
            return config
    except Exception as error:
        print("[Profiles] load config error, error:", error)
      


def check_and_create_profile(account_id):
    if not os.path.exists(f"./profiles/users/{account_id}.json"):
        shutil.copy(os.getcwd() + "/profiles/default/config.json", userProfilePath + f"/{account_id}.json")


def createTheater0(accountId, profile):
    profile['accountId'] = accountId
    profile['profileId'] = "theater0"
    profile['created'] = datetime.now().isoformat()
    profile['updated'] = datetime.now().isoformat()
    return profile

def createCollections(config, accountId, profile):
    profile["items"]['Currency']["quantity"] = config.vbucks
    profile['_id'] = accountId
    profile['accountId'] = accountId
    profile['profileId'] = 'athena'
    profile['created'] = datetime.now().isoformat()
    profile['updated'] = datetime.now().isoformat()
    return profile

def createCreative(accountId, profile):
    profile['accountId'] = accountId
    profile['profileId'] = 'creative'
    profile['created'] = datetime.now().isoformat()
    profile['updated'] = datetime.now().isoformat()
    return profile

def createCommonPublic(accountId, profile):
    profile['accountId'] = accountId
    profile['profileId'] = 'athena'
    profile['created'] = datetime.now().isoformat()
    profile['updated'] = datetime.now().isoformat()
    return profile



def createCommonCore(config, accountId, profile):
    if config.get('banned') is True:
        profile["stats"]["attributes"]
        bannedJSON = "{\"bRequiresUserAck\": true, \"banReasons\": [\"VixenFN\"], \"bBanHasStarted\": true, \"banStartTimeUtc\": \"2023-08-10T17:44:09.878Z\", \"banDurationDays\": 696969.0, \"exploitProgramName\": \"\", \"additionalInfo\": \"Don't worry, you aren't actually banned! This is just a test message!\", \"competitiveBanReason\": \"None\" }"
        profile["stats"]["attributes"]["ban_status"] = bannedJSON
    profile["items"]['Currency']['quantity'] = config['vbucks']
    profile['_id'] = accountId
    profile['accountId'] = accountId
    profile['profileId'] = 'athena'

    profile['created'] = datetime.now().isoformat()
    profile['updated'] = datetime.now().isoformat()
    return profile

def getGiftJSON(GiftType, ItemType, ItemID):

    giftJSON = {
   "templateId":"GiftBox:" + GiftType,
   "attributes":{
      "max_level_bonus":0,
      "fromAccountId":"VixenFN",
      "lootList":[
         {
            "itemProfile":"athena",
            "itemType": ItemType + ":" + ItemID,
            "itemGuid": ItemType + ":" + ItemID,
            "quantity":1
         }
      ],
      "level":1,
      "item_seen":False,
      "xp":0,
      "giftedOn":"2022-01-01T00:00:00.000Z",
      "params":{
         "userMessage":"Thanks for using VixenFN!"
      },
      "favorite":False
   },
   "quantity":1
}
    return giftJSON

def createAthena(accountId, config, profile):
    print("acc id: " + str(accountId))
    try:
        with open(f'{userProfilePath}/{accountId}.json') as file:
            config = json.load(file)
    except Exception as error:
        print("[Profiles] Create athena: error when parsing config, error:", error)

    profile['_id'] = accountId
    profile['accountId'] = accountId

    profile['created'] = datetime.now().isoformat()
    profile['updated'] = datetime.now().isoformat()

    profile['version'] = 'VixenFN'
    profile['profileId'] = 'athena'

    # Loadout
    shouldSetGifts = True
    locker = profile['items']['sandbox_loadout']['attributes']['locker_slots_data']['slots']

    locker['MusicPack']['items'][0] = config['MusicPack']['ID']
    locker['MusicPack']['activeVariants'] = config['MusicPack']['Variants']

    locker['Character']['items'][0] = config['Character']['ID']
    locker['Character']['activeVariants'] = config['Character']['Variants']

    # Continue updating locker for other items

    # Banner
    profile['items']['sandbox_loadout']['attributes']['banner_icon_template'] = config['BannerIconTemplate']
    profile['items']['sandbox_loadout']['attributes']['banner_color_template'] = config['BannerColorTemplate']

    profile['items']['sandbox_loadout']['attributes']['locker_slots_data']['slots'] = locker

    # Stats 
    stats = profile['stats']['attributes']

    stats['book_level'] = int(config['level'])
    stats['book_purchased'] = True
    stats['level'] = int(config['level'])
    stats['battlestars'] = int(config['battlestars'])
    stats['battlestars_season_total'] = int(config['battlestars'])
    stats['accountLevel'] = int(config['level'])
    stats['season_num'] = 25  # Change this for new seasons
    if(len(config["gifts"]) != 0):
         gifts = getGiftJSON(config["gifts"][0]["giftId"], config["gifts"][0]["ItemType"], config["gifts"][0]["ItemID"])
         profile['items']
         profile['items']["GiftBox:" + config["gifts"][0]["giftId"]] = gifts
    # crowns
    profile['items']['VictoryCrown:defaultvictorycrown']['attributes']['data_is_valid_for_mcp'] = True
    profile['items']['VictoryCrown:defaultvictorycrown']['attributes']['has_victory_crown'] = True
    profile['items']['VictoryCrown:defaultvictorycrown']['attributes']['total_victory_crowns_bestowed_count'] = config['crowns']
    profile['items']['VictoryCrown:defaultvictorycrown']['attributes']['total_royal_royales_achieved_count'] = config['crowns']

    profile['stats']['attributes'] = stats

    
        

    # Favorite
    items = profile['items']

    for item in config['favorites']:
        items[item['id']]['attributes']['favorite'] = True
    for item in config['archived']:
        items[item['id']]['attributes']['archived'] = True

    profile['items'] = items
    print("sending")
    return profile

def updateVbucks(accountId, config, newAmount):
   check_and_create_profile(accountId)
   vbucks = config['vbucks']
   if(newAmount is None):
      return "Invalid Vbuck count!"
   if(newAmount > 9999999):
     return "Vbuck total cannot be more than 9999999!"
   vbucks = newAmount
   save_config(userProfilePath + "/", accountId, config)
   return config
   
def updateLevel(accountId, config, newAmount):
   check_and_create_profile(accountId)
   level = config['level']
   if(newAmount is None):
      return "Invalid level count!"
   if(newAmount > 9999999):
     return "Level count cannot be more than 9999999!"
   level = newAmount
   save_config(userProfilePath + "/", accountId, config)
   return config

def updateCrowns(accountId, config, newAmount):
   check_and_create_profile(accountId)
   crowns = config['crowns']
   if(newAmount is None):
      return "Invalid crowns count!"
   if(newAmount > 9999999):
     return "Crowns count cannot be more than 9999999!"
   crowns = newAmount
   save_config(userProfilePath + "/", accountId, config)
   return config


def addCustomBan(accountId, config, theBanReason, theBanMessage):
   check_and_create_profile(accountId)
   IsBanned = config['banned']
   IsBanned = True
   banMessage = config['banMessage']
   banMessage = ""
   banReason = config['banReason']
   banReason = ""
   banMessage = theBanMessage
   banReason = theBanReason
   save_config(userProfilePath + "/", accountId, config)
   return config

def addVixenBan(accountId, config):
   check_and_create_profile(accountId)
   IsBanned = config['banned']
   IsBanned = True
   banMessage = config['banMessage']
   banMessage = ""
   banReason = config['banReason']
   banReason = ""
   banMessage = "Don't worry, you aren't actually banned! This is only a test!"
   banReason = "VixenFN"
   save_config(userProfilePath + "/", accountId, config)
   return config


def removeBan(accountId, config):
   check_and_create_profile(accountId)
   config['banned'] = False
   banMessage = config['banMessage']
   banMessage = ""
   banReason = config['banReason']
   banReason = ""
   save_config(userProfilePath + "/", accountId, config)
   return config

def updateBackground(accountId, config, newBackgroundUrl):
   check_and_create_profile(accountId)
   backgroundUrl = config['backgroundUrl']
   if(backgroundUrl is None):
      return "Invalid backgroundurl!"
   if("http://" or "https://" not in backgroundUrl):
     return "Background url is invalid!"
   backgroundUrl = newBackgroundUrl
   save_config(userProfilePath + "/", accountId, config)
   return config
  