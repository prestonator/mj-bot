import discord
from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import multiprocessing
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
DAVINCI_TOKEN = os.getenv('DAVINCI_TOKEN')
USE_MESSAGED_CHANNEL = bool(os.getenv('USE_MESSAGED_CHANNEL'))
CHANNEL_ID = os.getenv('CHANNEL_ID')
MID_JOURNEY_ID = os.getenv('MID_JOURNEY_ID')
SERVICE_URL = os.getenv('YOUR_SERVICE_URL')
target_info = {'targetID': '', 'targetHash': ''}

def get_channel_id(ctx, use_messaged_channel):
    if use_messaged_channel:
        return ctx.channel.id
    else:
        return CHANNEL_ID

async def handle_response(ctx, response):
    if response.status >= 400:
        await ctx.respond("Request has failed; please try later")
        return False
    else:
        await ctx.respond("Your image is being prepared, please wait a moment...")
        return True

bot = discord.Bot(intents=discord.Intents.all())

async def get_image_url(url: str, filename) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                logging.info(f"Image URL: {response.url}")
                return response.url

async def send_image_url_to_service(url: str, image_url: str):
    json_data = {"url": image_url}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            if response.status == 200:
                logging.info("Image URL sent successfully")
            else:
                logging.error("Error sending Image URL")

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")


@bot.command(description="Make DaVinci say something")
async def hello(ctx, sentence: discord.Option(str)):
    await ctx.respond(sentence)


@bot.command(description="This command is a wrapper of MidJourneyAI")
async def create_image_from_prompt(ctx, prompt: discord.Option(str)):
    CHANNEL_ID = get_channel_id(ctx, USE_MESSAGED_CHANNEL)

    response = await PassPromptToSelfBot(prompt)

    success = await handle_response(ctx, response)
    if not success:
        return
    

#Creating a command that accepts the index of a prompt image and uses the Upscale function to upscale it.
@bot.command(description="Upscale one of images generated by MidJourney")
async def upscale_generated_image(ctx, index: discord.Option(int), reset_target : discord.Option(bool) =True):
    if (index <= 0 or index > 4):
        await ctx.respond("Invalid index. Please choose an index between 1 and 4.")
        return

    if target_info['targetID'] == "":
        await ctx.respond(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    CHANNEL_ID = get_channel_id(ctx, USE_MESSAGED_CHANNEL)

    response = await Upscale(index, target_info['targetID'], target_info['targetHash'])
    if reset_target:
        target_info['targetID'] = ""
    success = await handle_response(ctx, response)
    if not success:
        return


# Creating a command that upscales the target image to its maximum resolution.
@bot.command(description="Upscale to max targeted image (should be already upscaled using mj_upscale)")
async def upscale_image_to_max(ctx):
    if target_info['targetID'] == "":
        await ctx.respond(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    CHANNEL_ID = get_channel_id(ctx, USE_MESSAGED_CHANNEL)

    response = await MaxUpscale(target_info['targetID'], target_info['targetHash'])
    target_info['targetID'] = ""
    success = await handle_response(ctx, response)
    if not success:
        return


# Creating a command that accepts an index and generates a variation image based on the target image.
@bot.command(description = "Make variation given index after target has been set")
async def create_image_variation(ctx, index: discord.Option(int), reset_target : discord.Option(bool) =True):
    if (index <= 0 or index > 4):
        await ctx.respond("Invalid index. Please choose an index between 1 and 4.")
        return

    if target_info['targetID'] == "":
        await ctx.respond(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    CHANNEL_ID = get_channel_id(ctx, USE_MESSAGED_CHANNEL)

    response = await Variation(index, target_info['targetID'], target_info['targetHash'])
    if reset_target:
        target_info['targetID'] = ""
    success = await handle_response(ctx, response)
    if not success:
        return


@bot.command(name="mj_target", description="Set target message for image operations")
async def set_target(ctx: commands.Context):
    if not ctx.message.reference:
        await ctx.send("You must reply to a MidJourney message to set the target.")
        return

    target_message = await ctx.fetch_message(ctx.message.reference.message_id)

    if str(target_message.author.id) != MID_JOURNEY_ID:
        await ctx.send("Use the command only when you reply to MidJourney")
        return

    target_info['targetID'] = str(target_message.id)
    target_info['targetHash'] = str((target_message.attachments[0].url.split("_")[-1]).split(".")[0])

    await ctx.send("Target set successfully")

    # Get image URL
    for attachment in target_message.attachments:
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            image_url = await get_image_url(attachment.url, attachment.filename)
            logging.info(f"Image URL: {image_url}")

            # Send image URL to the service
            await send_image_url_to_service(SERVICE_URL, image_url)


class Prompt(BaseModel):
    prompt: str

app = FastAPI()

@app.post("/send_prompt")
async def send_prompt(prompt_data: Prompt):
    prompt = prompt_data.prompt
    response = await PassPromptToSelfBot(prompt)
    return {"message": "Image creation initiated"}

def start_bot():
    bot.run(DAVINCI_TOKEN)

def start_fastapi_server():
    uvicorn.run("main:app", host="0.0.0.0", port=8269, log_level="info", reload=True)

if __name__ == "__main__":
    bot_process = multiprocessing.Process(target=start_bot)
    fastapi_process = multiprocessing.Process(target=start_fastapi_server)

    bot_process.start()
    fastapi_process.start()

    bot_process.join()
    fastapi_process.join()