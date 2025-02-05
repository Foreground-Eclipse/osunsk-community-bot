import disnake
from disnake.ext.commands import InteractionBot
import os
from internal.storage.sqlite import initializeDatabaseSchema, getInfoByCommandName,checkIfCommandNameTaken
intents = disnake.Intents.all()
bot = InteractionBot(intents=intents)

@bot.event
async def on_ready():
    initializeDatabaseSchema()
    print("Im ready")

@bot.event
async def on_message(message: disnake.Message):
    if message.content.startswith("!"):
        if checkIfCommandNameTaken(message.content[1:]):
            channel = message.channel
            data = getInfoByCommandName(message.content[1:])[0]
            if data[1] == "" and data[2] != "":
                embed = disnake.Embed()
                embed.set_image(data[2])
                await channel.send(embed)
                return
            if data[1] != "" and data[2] == "":
                await channel.send(content=data[1])
                return
            embed = disnake.Embed()
            embed.set_image(data[2])
            await channel.send(content=data[1], embed=embed)
            



for file in os.listdir(r"./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(os.getenv("OSUNSK_TOKEN"))