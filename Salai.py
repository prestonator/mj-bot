import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SERVER_ID = os.environ.get('SERVER_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
SALAI_TOKEN = os.environ.get('SALAI_TOKEN')
APPLICATION_ID = "936929561302675456"  # added a constant variable for application ID


# Combined the repetitive code into one function with customizable parameters
def make_request(data, custom_id):
    payload = {
        "type": 3,
        "guild_id": SERVER_ID,
        "channel_id": CHANNEL_ID,
        "message_flags": 0,
        "application_id": APPLICATION_ID,
        "session_id": "45bc04dd4da37141a5f73dfbfaf5bdcf",  # changed to a constant variable
    
        # customized parameters
        "data": {
            "component_type": 2,
            "custom_id": custom_id,
            "options": [{"type": 3, "name": "prompt", "value": data}]  # added custom prompt value
        }
    }

    header = {'authorization': SALAI_TOKEN}
    response = requests.post("https://discord.com/api/v9/interactions", json=payload, headers=header)
    return response


# Updated function to use the make_request function
def PassPromptToSelfBot(prompt):
    custom_id = f"MJ::JOB::imagine::{prompt}"  # made custom ID dynamic using prompt value
    
    # calls make_request function with customized parameters and returns response
    return make_request(data=prompt, custom_id=custom_id)


# Updated function to use the make_request function
def Upscale(index, messageId, messageHash):
    custom_id = f"MJ::JOB::upsample::{index}::{messageHash}"
    
    # calls make_request function with customized parameters and returns response
    return make_request(data="", custom_id=custom_id)


# Updated function to use the make_request function
def Variation(index, messageId, messageHash):
    custom_id = f"MJ::JOB::variation::{index}::{messageHash}"
    
    # calls make_request function with customized parameters and returns response
    return make_request(data="", custom_id=custom_id)


def MaxUpscale(messageId : str, messageHash : str):
  payload = {"type":3,
          "guild_id":SERVER_ID,
          "channel_id":CHANNEL_ID,
             "message_flags":0,
             "message_id": messageId,
             "application_id":"936929561302675456",
             "session_id":"1f3dbdf09efdf93d81a3a6420882c92c","data": 
       {"component_type":2,"custom_id":"MJ::JOB::upsample_max::1::{}::SOLO".format(messageHash)}}
  header = {
        'authorization' : SALAI_TOKEN
    }
  response = requests.post("https://discord.com/api/v9/interactions",
  json = payload, headers = header)
  return response



# Updated function to use the make_request function
def MaxUpscale(messageId, messageHash):
    custom_id = f"MJ::JOB::upsample_max::1::{messageHash}::SOLO"

    # calls make_request function with customized parameters and returns response
    return make_request(data="", custom_id=custom_id)



  