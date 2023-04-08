# Imported necessary libraries and modules
import os
from dotenv import load_dotenv
import aiohttp
from typing import Dict, Any
# Load environment variables
load_dotenv()

# Set constants for environment variables
SERVER_ID = os.environ.get('SERVER_ID')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
SALAI_TOKEN = os.environ.get('SALAI_TOKEN')
APPLICATION_ID = "936929561302675456"
APPLICATION_DATA_VERSION = "1077969938624553050"
APPLICATION_DATA_ID = "938956540159881230"
INTERACTION_URL = "https://discord.com/api/v9/interactions"

# Create a function to prompt self bot
async def PassPromptToSelfBot(prompt: str) -> aiohttp.ClientResponse:
    # Define the payload to be sent to the server
    payload = {
        "type": 2,
        "guild_id": SERVER_ID,
        "channel_id": CHANNEL_ID,
        "message_flags": 0,
        "application_id": APPLICATION_ID,
        "session_id": "2fb980f65e5c9a77c96ca01f2c242cf6",
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

    # Set the authorization header with necessary token  
    headers = {
        'authorization' : SALAI_TOKEN
    }
    
    # Send the request to the server via POST method with defined payload and header in JSON format
    async with aiohttp.ClientSession() as session:
        async with session.post(INTERACTION_URL, json=payload, headers=headers) as response:
            return response

# Create a function to upscale image
async def Upscale(index: int, messageId: str, messageHash: str) -> aiohttp.ClientResponse:
    # Define the payload to be sent to server
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
            "custom_id": f"MJ::JOB::upsample::{index}::{messageHash}"
        }
    }  
    
    # Set the authorization header with necessary token
    headers = {
        'authorization' : SALAI_TOKEN
    }

    # Send the request to the server via POST method with defined payload and header in JSON format
    async with aiohttp.ClientSession() as session:
        async with session.post(INTERACTION_URL, json=payload, headers=headers) as response:
            return response

# Create a function to generate image variation
async def Variation(index: int, messageId: str, messageHash: str) -> aiohttp.ClientResponse:
    # Define the payload to be sent to server
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
            "custom_id": f"MJ::JOB::variation::{index}::{messageHash}"
        }
    }

    # Set the authorization header with necessary token
    headers = {
        'authorization' : SALAI_TOKEN
    }

    # Send the request to the server via POST method with defined payload and header in JSON format
    async with aiohttp.ClientSession() as session:
        async with session.post(INTERACTION_URL, json=payload, headers=headers) as response:
            return response

# Create a function to upscale image to maximum 
async def MaxUpscale(messageId: str, messageHash: str) -> aiohttp.ClientResponse:
    # Define the payload to be sent to server
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
            "custom_id": f"MJ::JOB::upsample_max::1::{messageHash}::SOLO"
        }
    }

    # Set the authorization header with necessary token
    headers = {
        'authorization' : SALAI_TOKEN
    }
    
    # Send the request to the server via POST method with defined payload and header in JSON format
    async with aiohttp.ClientSession() as session:
        async with session.post(INTERACTION_URL, json=payload, headers=headers) as response:
            return response
        
