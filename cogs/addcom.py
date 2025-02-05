from disnake.ext import commands
import disnake
from internal.storage.sqlite import addcom, checkIfCommandNameTaken

async def validateCommandInput(name: str, text: str, picture: str, interaction: disnake.ModalInteraction) -> bool:
    if "@everyone" in name or "@here" in name :
        await interaction.response.send_message("евриван и хир нельзя в команды добавлять, шиз", ephemeral=True)
        return False
    if "@everyone" in text or "@here" in text :
        await interaction.response.send_message("евриван и хир нельзя в команды добавлять, шиз", ephemeral=True)
        return False
    if "@everyone" in picture or "@here" in picture :
        await interaction.response.send_message("евриван и хир нельзя в команды добавлять, шиз", ephemeral=True)
        return False
    if picture == "" and text == "":
        await interaction.response.send_message("у тебя инпут пустой мужик)", ephemeral=True)
        return False
    if "https://" not in picture:
        await interaction.response.send_message("невалидная ссылка мужик)", ephemeral=True)
        return False
    return True
    

class ButtonsAcceptAddcom(disnake.ui.View):
    def __init__(self, name, text, picture):
        super().__init__(timeout=300)
        self.name = name
        self.text = text
        self.picture = picture
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        self.stop()
    @disnake.ui.button(label='Подтвердить', style=disnake.ButtonStyle.green) 
    async def accept(self, button, interaction: disnake.Interaction):
        addcom(self.name, self.text, self.picture, interaction.user.id)
        await self.disable_all_items()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("команда добавлена", ephemeral=True)
        
    @disnake.ui.button(label='Отклонить', style=disnake.ButtonStyle.red) 
    async def decline(self, button, interaction: disnake.Interaction):
        await self.disable_all_items() 
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("команда не добавлена", ephemeral=True)
        
        
    

class AddcomModal(disnake.ui.Modal):
    def __init__(self,interid):
        self.interid = interid
        title = "Заполнение данных"
        components = [
            disnake.ui.TextInput(label="Название команды", placeholder="фрики", custom_id=f"name{self.interid}"),
            disnake.ui.TextInput(label="Текст", placeholder="МОЖНО ОСТАВИТЬ ПУСТЫМ", custom_id=f"text{self.interid}", required=False),
            disnake.ui.TextInput(label="Ссылка на пикчу", placeholder="Тут просто ссылку на пикчу с дса", custom_id=f"picture{self.interid}", required=False)
        ]
        super().__init__(title=title, components=components, custom_id=f"modal{self.interid}")
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name = interaction.text_values[f"name{self.interid}"]
        text = interaction.text_values[f"text{self.interid}"]
        picture = interaction.text_values[f"picture{self.interid}"]
        if checkIfCommandNameTaken(name):
            await interaction.response.send_message("название команды уже занято", ephemeral=True)
            return
        print(f"Modal callback: name={name}, text={text}, picture={picture}")
        if await validateCommandInput(name, text, picture, interaction):
            if text == "" and "https://" in picture:
                embed = disnake.Embed(title = "превью команды")
                embed.set_image(url=picture)
                await interaction.response.send_message(view=ButtonsAcceptAddcom(name = name, text = None, picture=picture), embed=embed, ephemeral=True)
            elif picture == "" and text != "":
                await interaction.response.send_message(view=ButtonsAcceptAddcom(name = name ,text = text ,picture = None), content=f"превью команды \n\n\n\n\n {text}", ephemeral=True)
            embed = disnake.Embed(title = "превью команды")
            embed.set_image(picture)
            await interaction.response.send_message(view=ButtonsAcceptAddcom(name = name ,text = text ,picture = picture), content=f"превью команды \n\n\n\n\n {text}", embed = embed, ephemeral=True)

class Addcom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("addcom cog loaded")

    @commands.slash_command(description="Добавить команду")
    async def addcom(self, interaction: disnake.CommandInteraction):
        await interaction.response.send_modal(AddcomModal(interaction.id))


def setup(bot):
    bot.add_cog(Addcom(bot))