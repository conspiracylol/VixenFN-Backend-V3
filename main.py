from flask import Flask, request, Response
import random, os, json, shutil, time, requests, threading
from datetime import datetime
from profiles import *


app = Flask(__name__)


userProfilePath = os.getcwd() + "/profiles/users"
defaultProfilePath = os.getcwd() + "/profiles/default"


@app.route("/", methods= ['GET'])
def mainpage():
  return "why are you looking here man.?"

@app.route("/v5/dashboard/user/<string:accountId>/experiments", methods = ['GET'])
def experimentsCheck(accountId):
  if(accountId):
        check_and_create_profile(accountId)
        config = loadConfig(accountId)
        
        response = Response()  # Create a response object
        
        # Modify CORS headers for the response
        response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
        
        
        if config["experimentsEnabled"] == True:
              response.status_code = 200
        elif config["experimentsEnabled"] == False:
              response.status_code = 204
        
        return response

  else:
        response = Response(status=204)
        response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
        return response
    
@app.route("/v5/api/internal/public/user/<string:accountId>/backgroundUrl", methods = ['GET'])
def external_client_usercommand_background(accountId):
  if accountId is None or len(accountId) != 32:
      return Response("Sorry, the user you are trying to find cannot be found.", status=404)
  else:
    check_and_create_profile(accountId)
    config = loadConfig(accountId)
    if config["backgroundUrl"] is None or config["backgroundUrl"] != "":
      return Response("https://cdn.vixenfn.lol/assets/img/lobbybackground", status=204);
    else:
      return Response(config["backgroundUrl"], status=200);
    
    
    

@app.route("/v5/dashboard/user/<string:accountId>/experiments/toggle", methods = ['GET'])
def ToggleExperiments(accountId):
  if(accountId):
        check_and_create_profile(accountId)
        config = loadConfig(accountId)
        
        response = Response()  # Create a response object
        
        # Modify CORS headers for the response
        response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
        if config["experimentsEnabled"] == True:
            config["experimentsEnabled"] = False
            save_config(userProfilePath + "/", accountId, config)
            response.status_code = 204
            return response
        elif config["experimentsEnabled"] == False:
            config["experimentsEnabled"] = True
            save_config(userProfilePath + "/", accountId, config)
            response.status_code = 200
            return response
       

  else:
        response = Response(status=204)
        response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
        return response
    

def UpdateCosmetics():
  os.system("node updater.js")

@app.route("/vixen/dashboard/<string:accountId>/stats/<string:command>", methods = ['POST'])
def dashboard_route(accountId, command):
  
     req = request.get_json(force=True, silent=True)
     if req is None:
      return Response("No body was provided!", status=400)
     if(accountId):
        if(len(accountId) != 32):
             return Response("Malformed account Id", status=400)
        else:
             if(command):
                  check_and_create_profile(accountId)
                  config = loadConfig(accountId)
                  if(command == "vbucks"):
                    amount = request.args.get('amount')
                    if amount is None or len(amount) == 0:
                      return Response("No " + command + " count was specified.", status=400)
                    if len(amount) > 999999:
                      return Response("Invalid " + command + " amount.", status=413)
                    else:
                      if(amount < 0):
                        return Response("The " + command + " amount cannot be negative.", status=400)
                      else:
                        config["vbucks"] = amount;
                        save_config(userProfilePath + "/", accountId, config)
                        return Response("Changed " + command + " amount to: " + amount + "! Restart your game to see the change!", status=200)
                  elif(command == "level"):
                    amount = request.args.get('amount')
                    if amount is None or len(amount) == 0:
                      return Response("No " + command + " count was specified.", status=400)
                    if len(amount) > 999999:
                      return Response("Invalid " + command + " amount.", status=413)
                    else:
                      if(amount < 0):
                        return Response("The " + command + " amount cannot be negative.", status=400)
                      else:
                        config["level"] = amount;
                        save_config(userProfilePath + "/", accountId, config)
                        return Response("Changed " + command + " amount to: " + amount + "! Change an item to see the change!", status=200)
                  elif command == "background":
                    
                    amount = request.get_json()["backgroundurl"]
                    if "https" not in amount and "http" not in amount and "/" not in amount and ":" not in amount and "." not in amount or amount is None:
                      return Response("Invalid Request! Command parameter: " + command + " was not valid! ", status=400)
                    else:
                      config["backgroundUrl"] = amount
                      save_config(userProfilePath + "/", accountId, config)
                      return Response("Changed " + command + " Successfully! Restart your game to see the change!", status=200)
                  elif(command == "crowns"):
                    amount = request.args.get('amount')
                    if amount is None or len(amount) == 0:
                      return Response("No " + command + " count was specified.", status=400)
                    if len(amount) > 999999:
                      return Response("Invalid " + command + " amount.", status=413)
                    else:
                      if(amount < 0):
                        return Response("The " + command + " amount cannot be negative.", status=400)
                      else:
                        config["crowns"] = amount;
                        save_config(userProfilePath + "/", accountId, config)
                        return Response("Changed " + command + " amount to: " + amount + "! Change an item to see the change!", status=200)
                  elif(command == "gold"):
                    amount = request.args.get('amount')
                    if amount is None or len(amount) == 0:
                      return Response("No " + command + " count was specified.", status=400)
                    if len(amount) > 999999:
                      return Response("Invalid " + command + " amount.", status=413)
                    else:
                      if(amount < 0):
                        return Response("The " + command + " amount cannot be negative.", status=400)
                      else:
                        #config["gold"] = amount;
                        save_config(userProfilePath + "/", accountId, config)
                        return Response("Changed " + command + " amount to: " + amount + "! Change an item to see the change!", status=200)
                  else:
                    print("Unknown command: " + command);
                    return "Unknown command: " + command;
                  
                       
             else:
                  return "NoCommand"
     else:
        return "NoAccount"


@app.route("/vixen/dashboard/<string:accountId>/gift/<string:giftType>", methods = ['POST'])
def gift_route(accountId, giftType):
     req = request.json
     if(accountId):
        if(len(accountId) != 32):
             return Response("Malformed account Id", status=400)
        else:
             if(giftType):
                  check_and_create_profile(accountId)

                  actualGiftType = ""
                  if(giftType == "Quest"):
                    actualGiftType = "ChallengeCompleteLightweight"
                  if(giftType == "LevelUp"):
                    actualGiftType = "BattlePassPurchased"
                  elif(giftType == "Support"):
                    actualGiftType = "Restoration"
                  elif(giftType == "Default"):
                    actualGiftType = "Default"
                  elif(giftType == "Report"):
                    actualGiftType = "BanAssist_Athena"
                  elif(giftType == "Reward"):
                    actualGiftType = "Winterfestreward"
                  elif(giftType == "Merge"):
                    actualGiftType = "AccountMerge"
                  elif(giftType == "Rebaf"):
                    actualGiftType = "Rebaf"
                  elif(giftType == "Tournament"):
                    actualGiftType = "Tournament"
                  elif(giftType == "Remove"):
                    actualGiftType = "Ungiftbox"
                  elif(giftType == "Crew"):
                       actualGiftType = "Subscription_Purchased"
                  elif(giftType == "Vbuck"):
                       actualGiftType = "Default"

                  if(req["GiftType"]):
                        if(req["ItemType"]):
                            if(req["ItemID"]):
                                itemType = req["ItemType"]
                                itemId = req["ItemId"]
                                if(itemType == "AthenaCharacter" or itemType == "AthenaDance" or itemType == "AthenaPickaxe"):
                                     giftConfigJson = getGiftJSON("GB_" + actualGiftType, itemType, itemId)
                                     config = loadConfig(accountId)
                                     config["gifts"] = giftConfigJson
                                     save_config(userProfilePath + "\\", accountId + config)
                                     return "ok"
                       
             else:
                  return Response("Malformed gift specification", status=400)
     else:
        return Response("No account id was specified!", status=400)
     










@app.route("/fortnite/api/game/v2/profile/<string:accountId>/client/<string:command>", methods = ['POST', 'GET'])
def client_route(accountId, command):
    req = request.get_json()
    profileId = request.args.get('profileId')
    check_and_create_profile(profileId)
    config = loadConfig(accountId)
    profile = loadProfile(profileId)
    
    if(profileId):
        rvn = request.args.get('rvn')
        if(rvn):
            if(command == "SetCosmeticLockerBanner"):
                if(req['templateId'] != 'None'):
                    config['bannerIconTemplateName'] = req['bannerIconTemplateName']
                    config['BannerColorTemplate'] = req['bannerColorTemplateName']
                    save_config(userProfilePath + "/", accountId, config)
                    createAthena(accountId, config, profile)
                    return Response(create_response(
						createAthena(accountId, config, profile),
						profileId,
						rvn
					), status=200, mimetype='application/json')
            elif(command == "ClientQuestLogin" or command == "QueryProfile"):
                if(profileId == "collections"):
                                 print("collections")
                if(profileId == "metadata"):
                                 print("metadata")
                if(profileId == "theater0"):
                                 print("theater0")
                if(profileId == "campaign"):
                                 print("campaign")
                if(profileId == "common_public"):
                                print("common_public")           
				
            elif(command == "SetMtxPlatform"):
                    return Response(create_response([ { "changeType": 'statModified', "name": 'current_mtx_platform', "value": req["platform"] }], profileId, rvn), status=200, mimetype='application/json')
            
            elif(command == "SetAffiliateName"):
                    return Response(create_response(createCommonCore(config, accountId, profile), profileId, rvn), status=200, mimetype='application/json')
        
            elif(command == "VerifyRealMoneyPurchase"):
                    return Response(create_response(createCommonCore(config, accountId, profile), profileId, rvn), status=200, mimetype='application/json')
            
            elif(command == "SetItemFavoriteStatusBatch"):
                    index = 0
                    for item in req.body['itemIds']:
                        if req.body['itemFavStatus'][index] == True:
                            is_already_favorized = False
                    for fav_item in config['favorites']:
                        if fav_item['id'] == req.body['itemIds'][index]:
                            is_already_favorized = True
                            break
                        if not is_already_favorized:
                            config['favorites'].append({'id': req.body['itemIds'][index]})
                        else:
                            index2 = 0
                            for fav_item in config['favorites']:
                                if fav_item['id'] == req.body['itemIds'][index]:
                                    config['favorites'].pop(index2)
                                    break
                                index2 += 1
                                index += 1
                                save_config(userProfilePath + "/", accountId, config)
                    return Response(create_response(createAthena(accountId, config, profile), profileId, rvn ), status=200, mimetype='application/json')


            elif(command == "RemoveGiftBox"):
                   config["gifts"] = {}
                   save_config(userProfilePath + "/", accountId, config)
                   if(profileId == "athena"):
                    return Response(create_response(createAthena(accountId, config, profile), profile, rvn ), status=200, mimetype='application/json')
                   if(profileId == "common_core"):
                    return Response(create_response(createCommonCore(config, profileId, profile), profileId, rvn ), status=200, mimetype='application/json')
                   
            elif(command == "SetCosmeticLockerSlot"):
                item_to_slot = req.get('itemToSlot')
                index_slot = req.get('slotIndex')
                slot_name = req.get('category')
                variant_updates = req.get('variantUpdates')

                if slot_name in ['Character', 'Backpack', 'Pickaxe', 'Glider', 'SkyDiveContrail', 'MusicPack', 'LoadingScreen']:
                    config[slot_name]['ID'] = item_to_slot
                    config[slot_name]['Variants'] = [{'variants': variant_updates}]
                elif slot_name == 'Dance':
                    config[slot_name]['ID'][index_slot] = item_to_slot
                    config[slot_name]['Variants'][index_slot] = [{'variants': variant_updates}]
                elif slot_name == 'ItemWrap':
                    if index_slot != -1:
                        config[slot_name]['ID'][index_slot] = item_to_slot
                        config[slot_name]['Variants'][index_slot] = [{'variants': variant_updates}]
                    else:
                        for i in range(7):
                            config[slot_name]['ID'][i] = item_to_slot
                            config[slot_name]['Variants'][i] = [{'variants': variant_updates}]
                            save_config(userProfilePath, accountId, config)

                new_athena = createAthena(accountId, config, profile)
                return Response(create_response(new_athena, profileId, rvn), status=200, mimetype='application/json')
            elif(command == "SetItemArchivedStatusBatch"):
                    index = 0
                    for item in req.body['itemIds']:
                        if req.body['archived'] == True:
                            is_already_archived = False
                    for archived_item in config['archived']:
                        if archived_item['id'] == req.body['itemIds'][index]:
                            is_already_archived = True
                            break
                        if not is_already_archived:
                            config['archived'].append({'id': req.body['itemIds'][index]})
                        else:
                            index2 = 0
                            for archived_item in config['archived']:
                                if archived_item['id'] == req.body['itemIds'][index]:
                                    config['archived'].pop(index2)
                                    break
                                index2 += 1
                                index += 1
                                save_config(userProfilePath + "/", accountId, config)
                    return Response(create_response(createAthena(accountId, config, profile), profile, rvn ), status=200, mimetype='application/json')
           
    else:
        noProfile= "{\"errorCode\": \"errors.com.epicgames.modules.profiles.invalid_payload\", \"errorMessage\": \"Unable to parse command com.epicgames.fortnite.core.game.commands." + command + ". Could not deserialize payload for com.epicgames.fortnite.core.game.commands" + command + "\", \"messageVars\": [\"com.epicgames.fortnite.core.game.commands." + command + "\", Could not deserialize payload for com.epicgames.fortnite.core.game.commands." + command + "\"], \"numericErrorCode\": 12806, \"originatingService\": \"fortnite\", \"intent\": \"prod-live\"}"    
        return noProfile








@app.route("/v3/fortnite/api/game/v2/profile/<string:accountId>/client/<string:command>", methods = ['POST', 'GET'])
def client_routev2(accountId, command):
    req = request.get_json()
    print("Req found! accountId: " + accountId + " command: " + command)
    profileId = request.args.get('profileId')
    print("profile id: " + profileId)
    check_and_create_profile(accountId)
    print("check create for id: " + accountId)
    config = loadConfig(accountId)
    print("load profile for id: " + accountId)
    profile = loadProfile(profileId)
    print("loaded fn profile for id: " + profileId)
    if(profileId):
        print("has profile for id: " + profileId)
        rvn = request.args.get('rvn')
        if(rvn):
            print("has rvn")
            if(command == "SetCosmeticLockerBanner"):
                print("set banner operation")
                if(req['templateId'] != 'None'):
                    config['bannerIconTemplateName'] = req['bannerIconTemplateName']
                    config['BannerColorTemplate'] = req['bannerColorTemplateName']
                    save_config(userProfilePath + "/", accountId, config)
                    createAthena(accountId, config, profile)
                    return Response(create_response(
						createAthena(accountId, config, profile),
						profileId,
						rvn
					), status=200, mimetype='application/json')
            elif(command == "ClientQuestLogin" or command == "QueryProfile"):
                print("queryprofile operation")
                if(profileId == "collections"):
                                 response = Response(create_response(createCollections(config, accountId, profile), profileId, rvn), status=200, mimetype='application/json')
                if(profileId == "metadata"):
                                 print("metadata")
                if(profileId == "theater0"):
                                 print("theater0")
                if(profileId == "campaign"):
                                 print("campaign")
                if(profileId == "common_public"):
                                 response = Response(create_response(createCommonPublic(accountId, profile), profileId, rvn), status=200, mimetype='application/json')
                if(profileId == "common_core"):
                                response = Response(create_response(createCommonCore(config, accountId, profile), profileId, rvn), status=200, mimetype='application/json')
                                print("response: " + str(response))
                                return response
                  
                if(profileId == "athena"):
                                response = Response(create_response(createAthena(accountId, config, profile), profileId, rvn), status=200, mimetype='application/json')
                                print("response: " + str(response))
                                return response
          
            elif(command == "SetMtxPlatform"):
                    return Response(create_response([ { "changeType": 'statModified', "name": 'current_mtx_platform', "value": req["platform"] }], profileId, rvn), status=200, mimetype='application/json')
            
            elif(command == "SetAffiliateName"):
                    return Response(create_response(createCommonCore(config, accountId, profile), profileId, rvn), status=200, mimetype='application/json')
        
            elif(command == "VerifyRealMoneyPurchase"):
                    return Response(create_response(createCommonCore(config, accountId, profile), profileId, rvn), status=200, mimetype='application/json')
            
            elif(command == "SetItemFavoriteStatusBatch"):
                    index = 0
                    for item in req.body['itemIds']:
                        if req.body['itemFavStatus'][index] == True:
                            is_already_favorized = False
                    for fav_item in config['favorites']:
                        if fav_item['id'] == req.body['itemIds'][index]:
                            is_already_favorized = True
                            break
                        if not is_already_favorized:
                            config['favorites'].append({'id': req.body['itemIds'][index]})
                        else:
                            index2 = 0
                            for fav_item in config['favorites']:
                                if fav_item['id'] == req.body['itemIds'][index]:
                                    config['favorites'].pop(index2)
                                    break
                                index2 += 1
                                index += 1
                                save_config(userProfilePath + "/", accountId, config)
                    return Response(create_response(createAthena(accountId, config, profile), profile, rvn ), status=200, mimetype='application/json')


            elif(command == "RemoveGiftBox"):
                   config["gifts"] = {}
                   save_config(userProfilePath + "/", accountId, config)
                   if(profileId == "athena"):
                    return Response(create_response(createAthena(accountId, config, profile), profile, rvn ), status=200, mimetype='application/json')
                   if(profileId == "common_core"):
                    return Response(create_response(createCommonCore(config, profileId, profile), profile, rvn ), status=200, mimetype='application/json')
                   
            elif(command == "SetCosmeticLockerSlot"):
                item_to_slot = req.get('itemToSlot')
                index_slot = req.get('slotIndex')
                slot_name = req.get('category')
                variant_updates = req.get('variantUpdates')
                if slot_name in ['Character', 'Backpack', 'Pickaxe', 'Glider', 'SkyDiveContrail', 'MusicPack', 'LoadingScreen']:
                    config[slot_name]['ID'] = item_to_slot
                    config[slot_name]['Variants'] = [{'variants': variant_updates}]
                elif slot_name == 'Dance':
                    config[slot_name]['ID'][index_slot] = item_to_slot
                    config[slot_name]['Variants'][index_slot] = [{'variants': variant_updates}]
                elif slot_name == 'ItemWrap':
                    if index_slot != -1:
                        config[slot_name]['ID'][index_slot] = item_to_slot
                        config[slot_name]['Variants'][index_slot] = [{'variants': variant_updates}]
                    else:
                        for i in range(7):
                            config[slot_name]['ID'][i] = item_to_slot
                            config[slot_name]['Variants'][i] = [{'variants': variant_updates}]
                            
                save_config(userProfilePath, accountId, config)
                new_athena = createAthena(accountId, config, profile)
                return Response(create_response(new_athena, profileId, rvn), status=200, mimetype='application/json')
            elif(command == "SetItemArchivedStatusBatch"):
                    index = 0
                    for item in req.body['itemIds']:
                        if req.body['archived'] == True:
                            is_already_archived = False
                    for archived_item in config['archived']:
                        if archived_item['id'] == req.body['itemIds'][index]:
                            is_already_archived = True
                            break
                        if not is_already_archived:
                            config['archived'].append({'id': req.body['itemIds'][index]})
                        else:
                            index2 = 0
                            for archived_item in config['archived']:
                                if archived_item['id'] == req.body['itemIds'][index]:
                                    config['archived'].pop(index2)
                                    break
                                index2 += 1
                                index += 1
                                save_config(userProfilePath + "/", accountId, config)
                    return Response(create_response(createAthena(accountId, config, profile), profile, rvn ), status=200, mimetype='application/json')
           
    else:
        noProfile= "{\"errorCode\": \"errors.com.epicgames.modules.profiles.invalid_payload\", \"errorMessage\": \"Unable to parse command com.epicgames.fortnite.core.game.commands." + command + ". Could not deserialize payload for com.epicgames.fortnite.core.game.commands" + command + "\", \"messageVars\": [\"com.epicgames.fortnite.core.game.commands." + command + "\", Could not deserialize payload for com.epicgames.fortnite.core.game.commands." + command + "\"], \"numericErrorCode\": 12806, \"originatingService\": \"fortnite\", \"intent\": \"prod-live\"}"    
        return noProfile





if __name__ == '__main__':
    threading.Thread(target=UpdateCosmetics).start()
    flask_thread = threading.Thread(target=app.run(host="0.0.0.0"))
    flask_thread.start()
    threading.Thread(target=UpdateCosmetics()).start()
    # Start the auto-updater in the main thread
    