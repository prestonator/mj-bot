# Importing the necessary modules for the discord bot, including the Salai module that has useful image processing functions.
import discord
from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation
import os
from dotenv import load_dotenv

load_dotenv()

DAVINCI_TOKEN = os.getenv('DAVINCI_TOKEN')
USE_MESSAGED_CHANNEL = bool(os.getenv('USE_MESSAGED_CHANNEL'))
CHANNEL_ID = os.getenv('CHANNEL_ID')
MID_JOURNEY_ID = os.getenv('MID_JOURNEY_ID')
target_info = {'targetID': '', 'targetHash': ''}

# Function to get the channel ID and reuse it
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


# Using a decorator to print the bot username when it is authenticated and ready for interaction.
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# Creating a command to make the bot say something from a given sentence.
@bot.command(description="Make DaVinci say something")
async def hello(ctx, sentence: discord.Option(str)):
    await ctx.respond(sentence)


# Creating a command that accepts a text prompt and passes it to the PassPromptToSelfBot function for creating an image.
@bot.command(description="This command is a wrapper of MidJourneyAI")
async def mj_imagine(ctx, prompt: discord.Option(str)):
    CHANNEL_ID = get_channel_id(ctx, USE_MESSAGED_CHANNEL)

    response = await PassPromptToSelfBot(prompt)

    success = await handle_response(ctx, response)
    if not success:
        return


#Creating a command that accepts the index of a prompt image and uses the Upscale function to upscale it.
@bot.command(description="Upscale one of images generated by MidJourney")
async def mj_upscale(ctx, index: discord.Option(int), reset_target : discord.Option(bool) =True):
    if (index <= 0 or index > 4):
        await ctx.respond("Invalid argument, pick from 1 to 4")
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
async def mj_upscale_to_max(ctx):
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
async def mj_variation(ctx, index: discord.Option(int), reset_target : discord.Option(bool) =True):
    if (index <= 0 or index > 4):
        await ctx.respond("Invalid argument, pick from 1 to 4")
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


# Using an event listener to check if a new message is sent, if the message is a targeted message it sets the targetID and targetHash for use in image manipulation commands.
@bot.event
async def on_message(message):
    if message.content == "": return
    if "$mj_target" in message.content and message.content[0] == '$':
        try:
            target_info['targetID'] = str(message.reference.message_id)
            target_info['targetHash'] = str((message.reference.resolved.attachments[0].url.split("_")[-1]).split(".")[0])
        except:
            await message.channel.send(
                "Exception has occurred, maybe you didn't reply to MidJourney message"
            )
            await message.delete()
            return
        if str(message.reference.resolved.author.id) != MID_JOURNEY_ID:
            await message.channel.send(
                "Use the command only when you reply to MidJourney")
            await message.delete()
            return
        await message.channel.send("Done")
        await message.delete()


# Running the bot using the token provided in the .env file.
bot.run(DAVINCI_TOKEN)