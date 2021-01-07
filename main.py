from flask import Flask
from threading import Thread
import os
import discord
from dotenv import load_dotenv

load_dotenv()
Token = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord')
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Liv's Orders"))

@client.event
async def on_guild_join(guild):
  with open('Guild.' + str(guild.id), 'a') as a_writer:
    a_writer.write("\n" + "Guild Joined with id: " + str(guild.id) + "\n")

@client.event
async def on_message(message):
  with open('Guild.' + str(message.guild.id), 'r') as reader:
    info = reader.readlines()
  global msg
  global fieldName
  global embedColor
  if(message.author.bot):
    return
  elif client.user in message.mentions:
    msg = "\nHere are some commands you can use!\nUse >channel (type) to designate a channel type\nTypes include suggestions and bugs (or adminsuggestions/adminbugs to log them)\nUse >bug (bug) or >suggest (suggestion) in their respective channels to report a bug or make a suggestion!\nUser >confirm or >deny to confirm and deny suggestions and bugs"
    fieldName = "Help:"
    embedColor = 3447003
    await message.delete()
    await message.author.send(embed=embedtext())
  elif message.content.startswith(">boop"):
    msg = "You have been booped by Liv's Bot :P"
    fieldName = "Easter Egg:"
    embedColor = 16580705
    await message.delete()
    await message.channel.send(embed=embedtext())
  elif message.content.startswith(">channel"):
    for Permissions in message.author.guild_permissions:
      if("administrator" in Permissions):
        arg = message.content.split(' ',1)[1]
        if arg == "suggestions":
          with open ('Guild.' + str(message.guild.id), 'a') as a_writer:
            a_writer.write("\n" + "suggestions: " + str(message.channel.id) + "\n")
            await message.channel.send("This Channel is now a Suggestions Channel")
        elif arg == "adminsuggestions":
          with open ('Guild.' + str(message.guild.id), 'a') as a_writer:
            a_writer.write("\n" + "adminsuggestions: " + str(message.channel.id) + "\n")
            await message.channel.send("This Channel is now an Admin Suggestions Channel")
        elif arg == "bugs":
          with open ('Guild.' + str(message.guild.id), 'a') as a_writer:
            a_writer.write("\n" + "bugs: " + str(message.channel.id) + "\n")
            await message.channel.send("This Channel is now a Bugs Channel")
        elif arg == "adminbugs":
          with open ('Guild.' + str(message.guild.id), 'a') as a_writer:
            a_writer.write("\n" + "adminbugs: " + str(message.channel.id) + "\n")
            await message.channel.send("This Channel is now an Admin Bugs Channel")
  elif message.content.startswith(">bug") and ("bugs: " + str(message.channel.id) + "\n") in info:
    s2 = message.content.split(' ', 1)[1]
    await message.delete()
    msg = str(message.author) + " Reported:\n" + s2 + "\n"
    fieldName = "Bug Report:"
    embedColor = 12745742
    await message.channel.send(embed=embedtext())
    for line in info:
      if ("adminbugs:" in line):
        msg = str(message.author) + " Reported:\n" + s2 + "\n"
        fieldName = "Bug Report:"
        embedColor = 12745742
        for line in info:
          if line.startswith("adminbugs: "):
            adminid = line.split(' ',1)[1].rstrip()
            newchannel = client.get_channel(int(adminid))
            await newchannel.send(embed=embedtext())
  elif message.content.startswith(">suggest") and ("suggestions: " + str(message.channel.id) + "\n") in info:
    s2 = message.content.split(' ', 1)[1]
    await message.delete()
    msg = str(message.author) + " Suggested:\n\n" + s2 + "\n"
    fieldName = "Suggestion:"
    embedColor = 12745742
    newmsg = await message.channel.send(embed=embedtext())
    await newmsg.add_reaction('✅')
    await newmsg.add_reaction('❌')
    for line in info:
      if ("adminsuggestions:" in line):
        msg = str(message.author) + " Suggested:\n\n" + s2 + "\n"
        fieldName = "Suggestion:"
        embedColor = 12745742
        for line in info:
          if line.startswith("adminsuggestions: "):
            adminid = line.split(' ', 1)[1].rstrip()
            newchannel = client.get_channel(int(adminid))
            await newchannel.send(embed=embedtext())
  elif message.content.startswith(">confirm"):
    for Permissions in message.author.guild_permissions:
      if("administrator" in Permissions):
        s2 = message.content.split(' ', 1)[1]
        await message.delete()
        oldone = await message.channel.fetch_message(int(s2))
        await oldone.delete()
        msg = (str(oldone.embeds[0].fields[0].value) + "\n\n Your Suggestion or Bug has been Accepted and dealt with!")
        fieldName = "Response:"
        embedColor = 3066993 
        await message.channel.send(embed=embedtext())
  elif message.content.startswith(">deny"):
    for Permissions in message.author.guild_permissions:
      if("administrator" in Permissions):
        s2 = message.content.split(' ', 1)[1]
        await message.delete()
        oldone = await message.channel.fetch_message(int(s2))
        await oldone.delete()
        msg = (str(oldone.embeds[0].fields[0].value) + "\n\n Your Suggestion or Bug has been Denied and dealt with!")
        fieldName = "Response:"
        embedColor = 15158332 
        await message.channel.send(embed=embedtext())

##############################
def embedtext():
  embed = discord.Embed(title="Kami Bot", color=embedColor)
  embed.add_field(name=fieldName, value = msg)
  embed.set_footer(text = "Made by Liv_Kami!")
  return embed
##############################

app = Flask('')

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
   app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

botid = "Nzk2NzY2ODgzNDA3NTkzNDgy.X_cs_A.CEhmnAsarkb8-3Rh3cap3O8KGCs"

keep_alive()
client.run(botid)
#boooooops from liv