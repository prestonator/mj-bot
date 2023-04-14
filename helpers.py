# Helpers.py - create this file in the same directory as the current file
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

IMAGE_WEBHOOK_URL = os.getenv('IMAGE_WEBHOOK_URL')
CHANNEL_ID = os.getenv("CHANNEL_ID")


# Function to get the channel ID and reuse it
async def get_channel_id(ctx, use_messaged_channel):
    if use_messaged_channel:
        return ctx.channel.id
    else:
        return CHANNEL_ID


async def handle_response(ctx, response):
    if response.status >= 400:
        await ctx.send("Request has failed; please try later")
        return False
    else:
        await ctx.send("Your image is being prepared, please wait a moment...")
        return True


async def get_image_url(url):
    data = {"url": url}
    headers = {"Content-Type": "application/json"}
    webhook = "https://n8n.jenkinsremote.com/webhook-test/7841daf9-7619-4428-80b5-19ed870bf207"
    response = requests.post(webhook, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print(f"Image URL sent to webhook: {url}")
    else:
        print(f"Failed to send image URL to webhook: {response.content}")


async def send_to_webhook(url):
    await get_image_url(url)
