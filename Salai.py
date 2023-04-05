import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SERVER_ID = os.environ.get('SERVER_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
SALAI_TOKEN = os.environ.get('SALAI_TOKEN')
APPLICATION_ID = "936929561302675456"  # added a constant variable for app ID
APPLICATION_DATA_VERSION = "1077969938624553050" # added a constant variable for app data Version
APPLICATION_DATA_ID = "938956540159881230" # added a constant variable for app data id
INTERACTION_URL = "https://discord.com/api/v9/interactions"

# Combined the repetitive code into one function with customizable parameters
def PassPromptToSelfBot(prompt : str):
    payload = {
        "type": 2,
        "guild_id": SERVER_ID,
        "channel_id": CHANNEL_ID,
        "message_flags": 0,
        "application_id": APPLICATION_ID,
        "session_id": "2fb980f65e5c9a77c96ca01f2c242cf6",
        # customized parameters
        "data": {
            "version": APPLICATION_DATA_VERSION,
            "id": APPLICATION_DATA_ID,
            "name": "imagine",
            "type": 1,
            "options": [
                {
                    "type": 3,
                    "name": "prompt",
                    "value": prompt
                }
            ],
            "application_command": {
                "id": APPLICATION_DATA_ID,
                "application_id": APPLICATION_ID,
                "version": APPLICATION_DATA_VERSION,
                "default_permission": True,
                "default_member_permissions": None,
                "type": 1,
                "nsfw": False,
                "name": "imagine",
                "description": "Create images with Midjourney",
                "dm_permission": True,
                "options": [
                    {
                    "type": 3,
                    "name": "prompt",
                    "description": "The prompt to imagine",
                    "required": True
                    }
                ]
            }
        }
    }

    header = {
        'authorization' : SALAI_TOKEN
    }
    response = requests.post(INTERACTION_URL, json=payload, headers=header)
    return response



def Upscale(index : int, messageId : str, messageHash : str):
    payload = {
        "type": 3,
        "guild_id": SERVER_ID,
        "channel_id": CHANNEL_ID,
        "message_flags": 0,
        "message_id": messageId,
        "application_id": APPLICATION_ID,
        "session_id": "45bc04dd4da37141a5f73dfbfaf5bdcf",
        "data": {
            "component_type": 2,
            "custom_id": "MJ::JOB::upsample::{}::{}".format(index, messageHash)
        }
    }  
    
    header = {
        'authorization' : SALAI_TOKEN
    }
    response = requests.post(INTERACTION_URL, json=payload, headers=header)
    return response


def Variation(index : int,messageId : str, messageHash : str):
    payload = {
        "type": 3,
        "guild_id": SERVER_ID,
        "channel_id": CHANNEL_ID,
        "message_flags": 0,
        "message_id": messageId,
        "application_id": APPLICATION_ID,
        "session_id": "1f3dbdf09efdf93d81a3a6420882c92c",
        "data": {
            "component_type": 2,
            "custom_id": "MJ::JOB::variation::{}::{}".format(index,
            messageHash)
        }
    }

    header = {
        'authorization' : SALAI_TOKEN
    }
    response = requests.post(INTERACTION_URL, json=payload, headers=header)
    return response


def MaxUpscale(messageId : str, messageHash : str):
    payload = {
        "type": 3,
        "guild_id": SERVER_ID,
        "channel_id": CHANNEL_ID,
        "message_flags": 0,
        "message_id": messageId,
        "application_id": APPLICATION_ID,
        "session_id": "1f3dbdf09efdf93d81a3a6420882c92c",
        "data": {
            "component_type": 2,
            "custom_id": "MJ::JOB::upsample_max::1::{}::SOLO".format(messageHash)
        }
    }

    header = {
        'authorization' : SALAI_TOKEN
    }
    response = requests.post(INTERACTION_URL, json=payload, headers=header)
    return response





  