import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import json
import os

load_dotenv()

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def save_data(data, file_path):
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)  # Crea la cartella se non esiste

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

class ResourceLock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.resources = {}

    def ensure_resources(self, guild_id):
        file_path = f"{os.getenv('RES_DIR')}/{guild_id}_resources.json"
        if guild_id not in self.resources:
            self.resources[guild_id] = load_data(file_path)

    @app_commands.command(name="res_list", description="List resources and their status")
    async def res_list(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        self.ensure_resources(guild_id)

        resources = self.resources.get(guild_id, {})
        if not resources:
            await interaction.response.send_message("No resources. Add one with `/res_add`.", ephemeral=True)
            return

        resources_msg = "\n".join(
            f'🔒 "{r}" locked by {u}' if u else f'✅ "{r}" available'
            for r, u in resources.items()
        )

        await interaction.response.send_message(resources_msg)

    @app_commands.command(name="res_add", description="Adds a new resource")
    async def res_add(self, interaction: discord.Interaction, resource: str):
        guild_id = interaction.guild.id
        self.ensure_resources(guild_id)

        if resource in self.resources[guild_id]:
            await interaction.response.send_message(f'❌ Resource "{resource}" already exists.', ephemeral=True)
        else:
            self.resources[guild_id][resource] = None
            save_data(self.resources[guild_id], f"{os.getenv('RES_DIR')}/{guild_id}_resources.json")
            await interaction.response.send_message(f'✅ Resource "{resource}" added.')

    @app_commands.command(name="res_remove", description="Removes a resource")
    async def res_remove(self, interaction: discord.Interaction, resource: str):
        guild_id = interaction.guild.id
        self.ensure_resources(guild_id)

        if resource not in self.resources[guild_id]:
            await interaction.response.send_message(f'❌ Resource "{resource}" not found.', ephemeral=True)
        else:
            del self.resources[guild_id][resource]
            save_data(self.resources[guild_id], f"{os.getenv('RES_DIR')}/{guild_id}_resources.json")
            await interaction.response.send_message(f'✅ Resource "{resource}" removed.')

    @app_commands.command(name="res_lock", description="Locks a resource if available")
    async def res_lock(self, interaction: discord.Interaction, resource: str):
        guild_id = interaction.guild.id
        self.ensure_resources(guild_id)

        if resource not in self.resources[guild_id]:
            await interaction.response.send_message(f'❌ Resource "{resource}" not found.', ephemeral=True)
        elif self.resources[guild_id][resource] is not None:
            await interaction.response.send_message(f'❌ Resource "{resource}" is already locked.', ephemeral=True)
        else:
            self.resources[guild_id][resource] = interaction.user.name
            save_data(self.resources[guild_id], f"{os.getenv('RES_DIR')}/{guild_id}_resources.json")
            await interaction.response.send_message(f'🔒 Resource "{resource}" locked by {interaction.user.name}.')

    @app_commands.command(name="res_unlock", description="Unlocks a resource if you are the owner")
    async def res_unlock(self, interaction: discord.Interaction, resource: str):
        guild_id = interaction.guild.id
        self.ensure_resources(guild_id)

        if resource not in self.resources[guild_id]:
            await interaction.response.send_message(f'❌ Resource "{resource}" not found.', ephemeral=True)
        elif self.resources[guild_id][resource] != interaction.user.name:
            await interaction.response.send_message(f'❌ You cannot unlock a resource you did not lock.', ephemeral=True)
        else:
            self.resources[guild_id][resource] = None
            save_data(self.resources[guild_id], f"{os.getenv('RES_DIR')}/{guild_id}_resources.json")
            await interaction.response.send_message(f'🔓 Resource "{resource}" unlocked.')

    @app_commands.command(name="res_status", description="Shows a resource status")
    async def res_status(self, interaction: discord.Interaction, resource: str):
        guild_id = interaction.guild.id
        self.ensure_resources(guild_id)

        if resource not in self.resources[guild_id]:
            await interaction.response.send_message(f'❌ Resource "{resource}" not found.', ephemeral=True)
        elif self.resources[guild_id][resource] is None:
            await interaction.response.send_message(f'✅ Resource "{resource}" is **available**.')
        else:
            await interaction.response.send_message(f'🔒 Resource "{resource}" is locked by {self.resources[guild_id][resource]}.')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(ResourceLock(bot))
    try:
        commands = await bot.tree.sync()
        print(f"✅ {len(commands)} Slash commands successfully synchronized!")
    except Exception as e:
        print(f"❌ Synchronization error: {e}")

    print(f'🔹 Logged in as {bot.user}')

TOKEN = os.getenv('APP_TOKEN')
bot.run(TOKEN)