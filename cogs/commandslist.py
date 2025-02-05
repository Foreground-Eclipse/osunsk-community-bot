from disnake.ext import commands
import disnake
from internal.storage.sqlite import getInfoByCommandName, getAllCommandNames, getCommandsWithLimit


class SelectCommand(disnake.ui.Select):
    def __init__(self, options, page):
        self.options = options
        self.page = page
        super().__init__(placeholder="Выберите команду для превью", options=self.options)

    async def callback(self, interaction: disnake.MessageInteraction):
        if self.values[0] == "nextpage":
            self.page +=1
            selectoptions = []
            for info in getCommandsWithLimit(self.page):
                selectoptions.append(disnake.SelectOption(label=info[0], value = info[0], description = f"превью команды {info[0]}"))
            if len(selectoptions) != 0:
                selectoptions[len(selectoptions)]= disnake.SelectOption(label="Следующая страница", value="nextpage", description="следующая страница)")
            else:
                await interaction.response.send_message("команды кончились бро", ephemeral=True)
                return
            view = disnake.ui.View(timeout=300)
            view.add_item(SelectCommand(selectoptions, self.page))
            await interaction.response.send_message(view=view, ephemeral=True)
        embed = disnake.Embed()
        data = getInfoByCommandName(self.values[0])
        content = ""
        if data[0][1] != None:
            content = data[0][1]
        if data[0][2] != None:
            embed.set_image(data[0][2])
        await interaction.response.send_message(embed=embed, content = content, ephemeral=True)

class Commandslist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("commandslist cog loaded")

    @commands.slash_command(description="Список всех команд")
    async def commandslist(self, interaction: disnake.CommandInteraction):
        selectoptions = []
        for info in getCommandsWithLimit(0):
            selectoptions.append(disnake.SelectOption(label=info[0], value = info[0], description = f"превью команды {info[0]}"))
        selectoptions.append("")
        selectoptions[len(selectoptions)-1]= disnake.SelectOption(label="Следующая страница", value="nextpage", description="следующая страница)")
        view = disnake.ui.View(timeout=300)
        view.add_item(SelectCommand(selectoptions, 0))
        await interaction.response.send_message(view=view, ephemeral=True)
        


def setup(bot):
    bot.add_cog(Commandslist(bot))