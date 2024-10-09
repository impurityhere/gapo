from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()  
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready and logged in as {bot.user}')
    await bot.tree.sync()  

positive_words = ['happy', 'good', 'awesome', 'great', 'love', 'fantastic']
negative_words = ['sad', 'bad', 'angry', 'terrible', 'hate', 'awful']

@bot.tree.command(name="rate_vibe", description="Rate the vibe of the server!")
async def rate_vibe(interaction: discord.Interaction):
    channel = interaction.channel
    messages = []

    async for message in channel.history(limit=100):
        messages.append(message.content)  

    positive_count = 0
    negative_count = 0

    for msg in messages:
        for word in msg.lower().split():
            if word in positive_words:
                positive_count += 1
            elif word in negative_words:
                negative_count += 1

    if positive_count > negative_count:
        vibe = 'positive!'
        suggestion = 'Maybe start a fun game or share something exciting!'
    elif negative_count > positive_count:
        vibe = 'negative.'
        suggestion = 'How about a chill conversation or some supportive words?'
    else:
        vibe = 'neutral.'
        suggestion = 'Maybe start a casual conversation or ask for suggestions!'

    await interaction.response.send_message(f"The vibe is {vibe} Positive words: {positive_count}, Negative words: {negative_count}")
    await interaction.followup.send(suggestion)

bot.run(TOKEN)
