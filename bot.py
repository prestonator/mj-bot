import discord
from discord.ext import commands
from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation
from helpers import handle_response, get_channel_id
import os

DAVINCI_TOKEN = os.getenv("DAVINCI_TOKEN")
USE_MESSAGED_CHANNEL = bool(os.getenv("USE_MESSAGED_CHANNEL"))
CHANNEL_ID = os.getenv("CHANNEL_ID")
MID_JOURNEY_ID = os.getenv("MID_JOURNEY_ID")
target_info = {"targetID": "", "targetHash": ""}

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Using a decorator to print the bot username when it is authenticated and ready for interaction.
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# Creating a command that accepts a text prompt and passes it to the PassPromptToSelfBot function for creating an image.
@bot.command(description="This command is a wrapper of MidJourneyAI")
async def create_image_from_prompt(ctx, prompt: discord.Option(str)):
    CHANNEL_ID = get_channel_id(ctx, USE_MESSAGED_CHANNEL)

    response = await PassPromptToSelfBot(prompt)

    success = await handle_response(ctx, response)
    if not success:
        return


# Creating a command that accepts the index of a prompt image and uses the Upscale function to upscale it.
@bot.command(description="Upscale one of images generated by MidJourney")
async def upscale_generated_image(ctx, message, index: int):
    if index <= 0 or index > 4:
        await ctx.send("Invalid index. Please choose an index between 1 and 4.")
        return

    response = await Upscale(
        index,
        str(message.id),
        str(message.attachments[0].url.split("_")[-1].split(".")[0]),
    )
    success = await handle_response(ctx, response)
    if not success:
        return


# Creating a command that upscales the target image to its maximum resolution.
@bot.command(
    description="Upscale to max targeted image (should be already upscaled using mj_upscale)"
)
async def upscale_image_to_max(ctx):
    if target_info["targetID"] == "":
        await ctx.send(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    CHANNEL_ID = get_channel_id(ctx, USE_MESSAGED_CHANNEL)

    response = await MaxUpscale(target_info["targetID"], target_info["targetHash"])
    target_info["targetID"] = ""
    success = await handle_response(ctx, response)
    if not success:
        return


# Creating a command that accepts an index and generates a variation image based on the target image.
@bot.command(description="Make variation given index after target has been set")
async def create_image_variation(
    ctx, index: discord.Option(int), reset_target: discord.Option(bool) = True
):
    if index <= 0 or index > 4:
        await ctx.send("Invalid index. Please choose an index between 1 and 4.")
        return

    if target_info["targetID"] == "":
        await ctx.send(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    CHANNEL_ID = get_channel_id(ctx, USE_MESSAGED_CHANNEL)

    response = await Variation(
        index, target_info["targetID"], target_info["targetHash"]
    )
    if reset_target:
        target_info["targetID"] = ""
    success = await handle_response(ctx, response)
    if not success:
        return


# Using an event listener to check if a new message is sent, if the message is a targeted message it sets the targetID and targetHash for use in image manipulation commands.
@bot.event
async def on_message(message):
    if message.content == "":
        return

    for attachment in message.attachments:
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            ctx = await bot.get_context(message)
            await upscale_generated_image(
                ctx, message, 1
            )  # Change the index according to your requirement
            break

    await bot.process_commands(message)

def run_bot():
    bot.run(DAVINCI_TOKEN)
