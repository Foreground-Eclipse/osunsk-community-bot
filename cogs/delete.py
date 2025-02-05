from disnake.ext import commands
import disnake
from internal.storage.sqlite import getCommandOwner, deleteCommand, checkIfCommandNameTaken




class Deletecom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("deletecom cog loaded")

    @commands.slash_command(description="Удалить команду")
    async def deletecom(self, interaction: disnake.CommandInteraction, name: str):
        if checkIfCommandNameTaken(name):
            if getCommandOwner(name) == str(interaction.user.id):
                deleteCommand(name)
                await interaction.response.send_message("команда удалена", ephemeral=True)
            else:
                await interaction.response.send_message(f"овнер этой команды не вы, а <@{getCommandOwner(name)}>", ephemeral=True)
        else:
            await interaction.response.send_message("такой команды нет)", ephemeral=True)

    @commands.slash_command(description="Удалить команду(админ мод)")
    async def deletecomadmin(self, interaction: disnake.CommandInteraction, name: str):
        if checkIfCommandNameTaken(name):
            deleteCommand(name)
            await interaction.response.send_message("команда удалена", ephemeral=True)
        else:
            await interaction.response.send_message("такой команды нет)", ephemeral=True)

        


def setup(bot):
    bot.add_cog(Deletecom(bot))