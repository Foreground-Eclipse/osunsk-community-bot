from disnake.ext import commands
import disnake



class SelectRoles(disnake.ui.Select):
    def __init__(self):
        self.options = [
            disnake.SelectOption(label="Новосибирская область", value="1178222735919423588", description="Взять / убрать роль Новосибирской области "), 
            disnake.SelectOption(label="Республика Алтай", value="1178223393573699705", description="Взять / убрать роль Республики Алтай "), 
            disnake.SelectOption(label="Республика Тыва", value="1178224116692684861", description="Взять / убрать роль Республики Тыва"),
            disnake.SelectOption(label="Республика Хакасия", value="1178224717883248670", description="Взять / убрать роль Республики Хакассия "), 
            disnake.SelectOption(label="Алтайский край", value="1178225113687142400", description="Взять / убрать роль Алтайского края "),
            disnake.SelectOption(label="Красноярский край", value="1178225853860151336", description="Взять / убрать роль Красноярского края"),
            disnake.SelectOption(label="Иркутская область", value="1178228217904115792", description="Взять / убрать роль Иркутской области"),
            disnake.SelectOption(label="Кемеровская область - Кузбасс", value="1178228394186518558", description="Взять / убрать роль Кемеровской области"),
            disnake.SelectOption(label="Омская область", value="1178228468379557898", description="Взять / убрать роль Омской области "),
            disnake.SelectOption(label="Томская область", value="1178228663632801802", description="Взять / убрать роль Томской области"),
            disnake.SelectOption(label="Снести выбор)", value="11", description="Сносит меню выбора ролей к исходному виду")
        ]
        super().__init__(placeholder="Выберите роль", options=self.options, custom_id="rolesselectmenu")

    async def callback(self, interaction: disnake.MessageInteraction):
        if self.values[0] != "11":
            roles = [role.id for role in interaction.user.roles]
            if int(self.values[0]) in roles:
                await interaction.user.remove_roles(interaction.guild.get_role(int(self.values[0])))
                await interaction.response.send_message("роль убрана", ephemeral=True)
            else:
                await interaction.user.add_roles(interaction.guild.get_role(int(self.values[0])))
                await interaction.response.send_message("роль выдана", ephemeral=True)
        if self.values[0] == "11":
            await interaction.response.send_message("Выбор обнулен)", ephemeral = True)
            return

            

class RolesAdder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("roles cog loaded")
        guild = self.bot.get_guild(961264891723915374)
        channel = guild.get_channel(1178248381391454268)
        messages = 0 
        async for message in channel.history(limit=1):
            messages+=1
        if messages == 0:
            embed = disnake.Embed(title="Тут можно пикнуть роли в зависимости от вашего местоположения")
            embed.set_image("https://media.discordapp.net/attachments/961268157052506172/1003995967256797264/ezgif.com-gif-maker_3.gif?ex=67a3fbdb&is=67a2aa5b&hm=52e40adede3ef4bf83cc46f41c94cc8eeead6da479f19994d85b1654d79424e6&")
            view = disnake.ui.View(timeout=None)
            view.add_item(SelectRoles())
            await channel.send(embed=embed, view=view)
        view = disnake.ui.View(timeout=None)
        view.add_item(SelectRoles())
        self.bot.add_view(view = view, message_id = 1336649934400655435)
        self.persistent = True

    

        


def setup(bot):
    bot.add_cog(RolesAdder(bot))