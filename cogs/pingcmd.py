import discord
from discord import app_commands
from discord.ext import commands
from database.database import setpingroleid, getpingroleid


class pingcmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.command(name="setpingrole", description="Admin command to set ping role")
    async def setpingrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            await setpingroleid(interaction.guild.id, role.id)
            await interaction.response.send_message(content=f"""Ping role has been set to {role.name}""", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)
    @app_commands.command(name="ping", description="Slash command to add people to the Ping role.")
    async def ping(self, interaction: discord.Interaction):
        try:
            prole = await getpingroleid(interaction.guild.id)
            role = discord.utils.get(interaction.guild.roles, id=prole[0])
            if role:
                if role in interaction.user.roles:

                    await interaction.response.send_message(
                        content=f"""You're already in the role {role.name}.""",
                        ephemeral=True)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(
                        content=f"""You have been added to role {role.name}.""",
                        ephemeral=True)
            else:
                await interaction.response.send_message(content=f"""No ping role exists.""",
                                                        ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=f"""Something went wrong.""", ephemeral=True)



async def setup(bot):
    await bot.add_cog(pingcmd(bot))