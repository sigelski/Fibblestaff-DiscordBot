import discord
from discord.ext import commands
from openai import AsyncOpenAI
import Constants

client = AsyncOpenAI(api_key = Constants.OPENAI_API_TOKEN)

# Set up command prefix to utilize commands, and allow all intents.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Shows when the bot is being launched.
@bot.event
async def on_ready():
    print(f'Logged in as Bot: {bot.user.name} | Bot User ID: {bot.user.id}')
    print('Bot is now live!\n')
    channel = bot.get_channel(1173451431114723500)
    await channel.send("Bot is now live!")
    
# Displays ANY message sent in the server. Can be used for debugging.    
@bot.event
async def on_message(message):
    print(f"!!!Message Received!!! \nContent = {message.content} \nAuthor = {message.author} \nUser ID = {message.author.id} \nChannel = {message.channel} \nChannel ID = {message.channel.id}\n")
    await bot.process_commands(message)
    
# How OpenAI and Discord work together.    
@bot.command()
async def talkAI(ctx, *, user_input):
    user_id = ctx.author.id
    converted_userid = str(user_id)
    input = converted_userid + " " + user_input
    try:
        print(f"Command received: {input}")

        # Use the OpenAI API to generate a response
        response = await client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
            {
                "role": "system",
                "content": "About Yourself:\nYour name is Mr. James Fibblestaff."
            },
            {
                "role": "user",
                "content": user_input
            }
            ],
        temperature = 1.1,
        max_tokens = 500,
        top_p = 0.9,
        frequency_penalty = 0.2,
        presence_penalty = 0.2
        )
              
        print("\n!!!OpenAI API Request Sent!!!")

        # Print the OpenAI API request details to the console
        print(f"OpenAI API Response: {response}\n")

        # Send the generated formatted response to the Discord channel, and prints out a copy to the terminal.
        response_message = response.choices[0].message.content
        await ctx.send(response_message)
        print(f"Response sent to Discord Server: {response_message}\n\n!!!Success!!!\n")
        
    # Error Catching, cause that keeps happening -_-
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("Sorry, an error occurred.") 
        
# Adds a way to shutdown the bot via a discord message in case of emergency.
@bot.command()
async def shutdown(ctx):
    await ctx.send("Bot is shutting down. Goodbye!")
    await bot.close()
    
# Runs the bot using the Bot's API Token    
bot.run(Constants.DISCORD_BOT_TOKEN)