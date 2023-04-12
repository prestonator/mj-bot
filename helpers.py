# Helpers.py - create this file in the same directory as the current file
import os

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


# async def is_desired_image_message(message):
#     for attachment in message.attachments:
#         if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
#             return True
#     return False
