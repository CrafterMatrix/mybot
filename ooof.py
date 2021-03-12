import discord
from discord.ext import commands
import re
import asyncio
import json
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all(), case_insensitive=True)

with open(r"C:\Users\nakul\Documents\GitHub\mybot\py.json", 'r') as f:
    bot.data = json.load(f)

async def save():
    await bot.wait_until_ready()
    while not bot.is_closed():
        with open(r"C:\Users\nakul\Documents\GitHub\mybot\py.json", 'w') as f:
            json.dump(bot.data, f, indent=4)

        await asyncio.sleep(1)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
bot.admin_roles = ["staff", "Mods"]
bot.server_developer_role = "Server Developers"
bot.TICK_MARK = "<:tick_mark:814801884358901770>"
bot.CROSS_MARK = "<:cross_mark:814801897138815026>"
ban_reason = ""
kicks = False
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["to"])
@commands.has_permissions(manage_messages=True)
async def ticketoption(context, param=None, emoji: discord.Emoji=None, *, op=None):
    print(emoji)
    if param.upper() == 'ADD':
        if emoji == None:
            em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide an emoji/option!\n Usage- `$ticketoption add (emoji) (option line)`")
            await context.send(embed=em)
            return
        if op == None:
            em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide an emoji/option!\n Usage- `$ticketoption add (emoji) (option line)`")
            await context.send(embed=em)
            return
        bot.data['ticket']['op'][str(context.guild.id)][str(emoji)] = str(op)
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully added Emoji-Option pair to ticketing!\n {str(emoji)} - {op}")
        mes = await context.send(embed=em)
        await asyncio.sleep(5)
        await mes.delete()
        
    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def suggest(context, *, msg=None):
    chn = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    num = bot.data['suggest']['count'][str(context.guild.id)]
    if bot.data['suggest']['chn'][str(context.guild.id)] == "":
        em = discord.Embed(description=f"{bot.CROSS_MARK} This server doesn't have a suggestion channel set up!\n Ask the moderators to run the `$setsuggest` command!")
        await context.send(embed=em)
        return
    else:
        if msg != None:
            em = discord.Embed(title=f"Suggestion #{num}", description=msg)
            em.set_author(name=context.message.author, icon_url=context.message.author.avatar_url)
            m1 =  await chn.send(embed=em)
            await m1.add_reaction(f"{bot.TICK_MARK}")
            await m1.add_reaction(f"{bot.CROSS_MARK}")
            await context.message.delete()
            em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully sent suggestion!")
            mes = await context.send(embed=em)
            await asyncio.sleep(5)
            await mes.delete()
            bot.data['suggest']['val'][str(context.guild.id)][str(num)] = {}
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['author'] = str(context.message.author)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['msg'] = str(msg)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['icon'] = str(context.message.author.avatar_url)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['link'] = str(m1.jump_url)
            bot.data['suggest']['count'][str(context.guild.id)] = bot.data['suggest']['count'][str(context.guild.id)] + 1
        else:
            em = discord.Embed(description=f"{bot.TICK_MARK} Please type your suggestion now!")
            mess = await context.send(embed=em)
            def check(m):
                return m.author == context.message.author and m.channel == context.channel
            try:
                msgg = await bot.wait_for('message', timeout= 30, check=check)
                await mess.delete()
            except asyncio.TimeoutError:
                em = discord.Embed(description=f"{bot.CROSS_MARK} You ran out of time! Please re-type the command!")
                await context.channel.send(embed=em)
                return
            msg = msgg.content
            em = discord.Embed(title=f"Suggestion #{num}", description=msg)
            em.set_author(name=context.message.author, icon_url=context.message.author.avatar_url)
            m1 =  await chn.send(embed=em)
            await m1.add_reaction(f"{bot.TICK_MARK}")
            await m1.add_reaction(f"{bot.CROSS_MARK}")
            await context.message.delete()
            await msgg.delete()
            em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully sent suggestion!")
            mes = await context.send(embed=em)
            await asyncio.sleep(5)
            await mes.delete()
            bot.data['suggest']['val'][str(context.guild.id)][str(num)] = {}
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['author'] = str(context.message.author)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['msg'] = str(msg)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['icon'] = str(context.message.author.avatar_url)
            bot.data['suggest']['val'][str(context.guild.id)][str(num)]['link'] = str(m1.jump_url)
            bot.data['suggest']['count'][str(context.guild.id)] = bot.data['suggest']['count'][str(context.guild.id)] + 1

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def approve(context, no=None, *, reason=None):
    log_chat = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    if str(no) in bot.data['suggest']['val'][str(context.guild.id)]:
        em = discord.Embed(title=f'Approved suggestion #{str(no)}', color=discord.Color.green())
        em.add_field(name=f"Suggestion content", value=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['msg'] + f" - [Suggestion!]({bot.data['suggest']['val'][str(context.guild.id)][str(no)]['link']})", inline=False)
        em.add_field(name=f"Reason from {context.message.author.name}", value=reason, inline=False)
        em.set_author(name=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['author'], icon_url=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['icon'])
        await log_chat.send(embed=em)
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Approved suggestion #{str(no)} for reason - {reason}!")
        ems = await context.send(embed=em)
        await context.message.delete()
        await asyncio.sleep(5)
        await ems.delete()
        return
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> Please provide a valid suggestion ID!")
        await context.channel.send(embed=em)
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def deny(context, no=None, *, reason=None):
    log_chat = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    if str(no) in bot.data['suggest']['val'][str(context.guild.id)]:
        em = discord.Embed(title=f'Denied suggestion #{str(no)}', color=discord.Color.red())
        em.add_field(name=f"Suggestion content", value=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['msg'] + f" - [Suggestion!]({bot.data['suggest']['val'][str(context.guild.id)][str(no)]['link']})", inline=False)
        em.add_field(name=f"Reason from {context.message.author.name}", value=reason, inline=False)
        em.set_author(name=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['author'], icon_url=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['icon'])
        await log_chat.send(embed=em)
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Denied suggestion #{str(no)} for reason - {reason}!")
        ems = await context.send(embed=em)
        await context.message.delete()
        await asyncio.sleep(5)
        await ems.delete()
        return
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> Please provide a valid suggestion ID!")
        await context.channel.send(embed=em)
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def consider(context, no=None, *, reason=None):
    log_chat = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    if str(no) in bot.data['suggest']['val'][str(context.guild.id)]:
        em = discord.Embed(title=f'Considered suggestion #{str(no)}', color=discord.Color.blue())
        em.add_field(name=f"Suggestion content", value=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['msg'] + f" - [Suggestion!]({bot.data['suggest']['val'][str(context.guild.id)][str(no)]['link']})", inline=False)
        em.add_field(name=f"Reason from {context.message.author.name}", value=reason, inline=False)
        em.set_author(name=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['author'], icon_url=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['icon'])
        await log_chat.send(embed=em)
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Considered suggestion #{str(no)} for reason - {reason}!")
        ems = await context.send(embed=em)
        await context.message.delete()
        await asyncio.sleep(5)
        await ems.delete()
        return
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> Please provide a valid suggestion ID!")
        await context.channel.send(embed=em)
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def implement(context, no=None, *, reason=None):
    log_chat = bot.get_channel(bot.data['suggest']['chn'][str(context.guild.id)])
    if str(no) in bot.data['suggest']['val'][str(context.guild.id)]:
        em = discord.Embed(title=f'Implemented suggestion #{str(no)}', color=discord.Color.purple())
        em.add_field(name=f"Suggestion content", value=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['msg'] + f" - [Suggestion!]({bot.data['suggest']['val'][str(context.guild.id)][str(no)]['link']})", inline=False)
        em.add_field(name=f"Reason from {context.message.author.name}", value=reason, inline=False)
        em.set_author(name=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['author'], icon_url=bot.data['suggest']['val'][str(context.guild.id)][str(no)]['icon'])
        await log_chat.send(embed=em)
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Implemented suggestion #{str(no)} for reason - {reason}!")
        ems = await context.send(embed=em)
        await context.message.delete()
        await asyncio.sleep(5)
        await ems.delete()
        return
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> Please provide a valid suggestion ID!")
        await context.channel.send(embed=em)
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def setl(context, channel: discord.TextChannel=None):
    if channel == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide a channel for this command!")
        await context.send(embed=em)
    else:
        bot.data['logs'][str(context.guild.id)] = channel.id
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully set logs channel as - {channel.mention}!")
        mes = await context.send(embed=em)
        await asyncio.sleep(5)
        await context.message.delete()
        await mes.delete()


    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['setwidt'])
@commands.has_permissions(manage_messages=True)
async def setw(context, channel: discord.TextChannel=None):
    if channel == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide a channel for this command!")
        await context.send(embed=em)
    else:
        bot.data['widt'][str(context.guild.id)] = channel.id
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully set widt channel as - {channel.mention}!")
        mes = await context.send(embed=em)
        await asyncio.sleep(5)
        await context.message.delete()
        await mes.delete()

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['setsuggest'])
@commands.has_permissions(manage_messages=True)
async def sets(context, channel: discord.TextChannel=None):
    if channel == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide a channel for this command!")
        await context.send(embed=em)
    else:
        bot.data['suggest']['chn'][str(context.guild.id)] = channel.id
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully set suggestions channel as - {channel.mention}!")
        mes = await context.send(embed=em)
        await asyncio.sleep(5)
        await context.message.delete()
        await mes.delete()

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['setticket'])
@commands.has_permissions(manage_messages=True)
async def sett(context, channel: discord.TextChannel=None):
    if channel == None:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You must provide a channel for this command!")
        await context.send(embed=em)
    else:
        bot.data['ticket']['chn'][str(context.guild.id)] = channel.id
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully set ticket channel as - {channel.mention}!")
        mes = await context.send(embed=em)
        em = discord.Embed(title="Create ticket!", description="React 📩 to create a ticket!")
        msg = await channel.send(embed=em)
        await msg.add_reaction('📩')
        await channel.set_permissions(context.guild.default_role, send_messages = False, read_messages = True)
        bot.data['ticket']['msg'][str(context.guild.id)] = msg.id
        await asyncio.sleep(5)
        await context.message.delete()
        await mes.delete()

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['resetsuggest'])
@commands.has_permissions(manage_messages=True)
async def resets(context):
    em = discord.Embed(description=f"{bot.CROSS_MARK} Are you sure you want to reset the suggestion count?\n Type yes to proceed!")
    msgg = await context.send(embed=em)
    def check(m):
        return m.author == context.message.author and m.channel == context.channel
    try:
        msg = await bot.wait_for('message', timeout= 30, check=check)
    except asyncio.TimeoutError:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You ran out of time! Please re-type the command!")
        await context.channel.send(embed=em)
        return
    if msg.content.upper() == 'YES':
        bot.data['suggest']['count'][str(context.guild.id)] = 1
        bot.data['suggest']['val'][str(context.guild.id)] = {}
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully reset suggestion count!")
        mes = await context.send(embed=em)
        await context.message.delete()
        await msg.delete()
        await asyncio.sleep(5)
        await mes.delete()
        await msgg.delete()
    else:
        em = discord.Embed(description=f"{bot.CROSS_MARK} Process cancelled!")
        mes = await context.channel.send(embed=em)
        await context.message.delete()
        await msg.delete()
        await asyncio.sleep(5)
        await mes.delete()
        await msgg.delete()
        return

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['resetticket'])
@commands.has_permissions(manage_messages=True)
async def resett(context):
    em = discord.Embed(description=f"{bot.CROSS_MARK} Are you sure you want to reset the ticket count?\n Type yes to proceed!")
    msgg = await context.send(embed=em)
    def check(m):
        return m.author == context.message.author and m.channel == context.channel
    try:
        msg = await bot.wait_for('message', timeout= 30, check=check)
    except asyncio.TimeoutError:
        em = discord.Embed(description=f"{bot.CROSS_MARK} You ran out of time! Please re-type the command!")
        await context.channel.send(embed=em)
        return
    if msg.content.upper() == 'YES':
        bot.data['ticket']['count'][str(context.guild.id)] = 1
        bot.data['ticket']['val'][str(context.guild.id)] = {}
        bot.data['ticket']['msg'][str(context.guild.id)] = ""
        bot.data['ticket']['op'][str(context.guild.id)] = {}
        em = discord.Embed(description=f"{bot.TICK_MARK} Succesfully reset ticket count!")
        mes = await context.send(embed=em)
        await context.message.delete()
        await msg.delete()
        await asyncio.sleep(5)
        await mes.delete()
        await msgg.delete()
    else:
        em = discord.Embed(description=f"{bot.CROSS_MARK} Process cancelled!")
        mes = await context.channel.send(embed=em)
        await context.message.delete()
        await msg.delete()
        await asyncio.sleep(5)
        await mes.delete()
        await msgg.delete()
        return

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# on message event handler - handles a lot of the anti blocking, logging. - Even Recieves all messages,
# including DMs and from itself
@bot.event
async def on_message(msg):

    # ignore it if its the bots own message
    if msg.author.id == bot.user.id:
        return

    log_save_id = bot.data['logs'][str(msg.guild.id)]
    if not isinstance(msg.channel, discord.channel.DMChannel):
        if msg.guild.id == log_save_id:
            return

    # get main log channel
    try:
        chn = bot.data['logs'][str(msg.guild.id)]
    except AttributeError:
        # It is a DM channel message - It has no guild
        pass
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # TICKET LOGGER
    try:
        # get all currently open tickets
        curr_open_tickets = bot.tickets_collection.find({"GUILD_ID": msg.guild.id, "STATUS": "OPEN"})
        # get the channel ids of those tickets
        currtickids = [i["CHN_ID"] for i in curr_open_tickets]

        # check if the channel id of the message was in this list
        if msg.channel.id in currtickids:
            # log the message with details into mongodb
            d = {"time": msg.created_at, "authorid": msg.author.id,
                 "authorname": f'{msg.author.name}#{msg.author.discriminator}', 'content': msg.content}
            if msg.attachments:
                d["attachments"] = True
            else:
                d["attachments"] = False

            bot.tickets_collection.update_one({"GUILD_ID": msg.guild.id, "CHN_ID": msg.channel.id},
                                              {"$addToSet": {"CHAT_LOG": d}})
    except AttributeError:
        # DM channel - it has no guild attribute.
        pass
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ATTACHMENT LOGGER
    if msg.attachments and not isinstance(msg.channel, discord.channel.DMChannel):  # only log non DMs
        if msg.channel.id != chn.id and msg.channel.id != log_save_id:  # If the message is not in log channel - done to prevent infinite loop

            # get date time of message creation
            t = datetime.strftime(msg.created_at + timedelta(hours=5, minutes=30),
                                  '%d/%m/%Y, %H:%M:%S hrs IST/GMT+5:30')

            # send a new log message for each attachment in the msg
            for i in msg.attachments:
                # usually len 1, just in case...

                # generate message
                em = discord.Embed(description=f"**Attachment sent in {str(msg.channel.mention)}** - [Message]({msg.jump_url})", color=discord.Color.blue())
                em.add_field(name='Author', value=msg.author, inline=False)
                em.add_field(name='Message', value=msg.content)
                em.add_field(name='Channel', value=msg.channel)
                em.add_field(name='Server', value=msg.guild)
                em.add_field(name='Link', value=i.url, inline=False)
                await chn.send(embed=em)

                msge = f"**ORACLE ATTACHMENT LOGGING**\n" + \
                      f"FROM: {msg.author.name}#{msg.author.discriminator} " \
                      f"[{msg.author.id}]\n" + \
                      f"Created IST Timestamp: {t}\n"
                msge += f"Not a DM channel (I do not log DM Channels for Privacy),\nID: {msg.channel.id}" \
                        f"\nNAME: {msg.channel.name}" \
                        f"\nON SERVER: {msg.guild.name}"
                msge += f"\nMessage was:\n```{msg.content}```\n"

                if i.size < 8000000:  # 8 MB in bytes
                    # can send attachment
                    fi = await i.to_file()
                    lgsvchannel = bot.get_channel(log_save_id)
                    await lgsvchannel.send(msge, file=fi)
                    await chn.send(msge, file=fi)
                else:
                    # cant send attachment, too large!
                    await chn.send(msge+"\n**Couldn't Log attachment - Too large (Larger than 8000000 Bytes)**\n")
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # INVITE BLOCKER
    if msg.content.find("discord.gg") != -1 and not isinstance(msg.channel, discord.channel.DMChannel):
        # if message has discord.gg type invite
        ind = msg.content.find("discord.gg")
        if msg.content[ind + len("discord.gg"):] == "/jDMYEV5":
            # if the message is an invite for The Matrix, ignore it.
            pass
        else:
            # Delete the message since invite has been found
            em = discord.Embed(description=f"{bot.CROSS_MARK}  You can not send invite links!")
            await msg.channel.send(embed=em) 
            await chn.send(f"{msg.author.mention} | {msg.author.id} did a invite in {msg.channel}.")
            await msg.delete()
            return
    elif msg.content.find("discordapp.com/invite") != -1 and not isinstance(msg.channel, discord.channel.DMChannel):
        # if message has discordapp.com/invite type invite
        ind = msg.content.find("discordapp.com/invite")
        if msg.content[ind + len("discordapp.com/invite"):] == "/jDMYEV5":
            # if the message is an invite for The Matrix, ignore it.
            pass
        else:
            # Delete the message since invite has been found
            em = discord.Embed(description=f"{bot.CROSS_MARK}  You can not send invite links!")
            await msg.channel.send(embed=em) 
            await chn.send(f"{msg.author.mention} | {msg.author.id} did a invite in {msg.channel}.")
            await msg.delete()
            return
    elif msg.content.find("discord.com/invite") != -1 and not isinstance(msg.channel, discord.channel.DMChannel):
        # if message has discord.com/invite type invite
        ind = msg.content.find("discord.com/invite")
        if msg.content[ind + len("discord.com/invite"):] == "/jDMYEV5":
            # if the message is an invite for The Matrix, ignore it.
            pass
        else:
            # Delete the message since invite has been found
            em = discord.Embed(description=f"{bot.CROSS_MARK}  You can not send invite links!")
            await msg.channel.send(embed=em) 
            await chn.send(f"{msg.author.mention} | {msg.author.id} did a invite in {msg.channel}.")
            await msg.delete()
            return
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # return prefix if bot is tagged (tag must be first in the msg)
    if msg.content.startswith(f"<@!{bot.user.id}>"):
        await msg.channel.send(f"Hey there, my prefix is {bot.command_prefix}")

    # process the message normally (as in command)
    await bot.process_commands(msg)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# The edit event - all message edits are detected here
@bot.event
async def on_message_edit(before, after):

    try:
        chn = bot.get_channel(bot.common_server_info_collection.find_one({"SERVER_ID": after.guild.id})["LOG_CHANNEL"])
    except AttributeError:
        # DM channel - there is none guild attribute for Message
        pass

    # Invite block for edits
    if after.content.find("discord.gg") != -1 and not isinstance(after.channel, discord.channel.DMChannel):
        # found discord.gg!
        ind = after.content.find("discord.gg")
        if after.content[ind + len("discord.gg"):] \
                == "/jDMYEV5":
            pass
        else:
            # found discord.gg!
            em = discord.Embed(description=f"{bot.CROSS_MARK}  You can not send invite links!")

            await after.channel.send(embed=em)
            await chn.send(f"{after.author.mention} | {after.author.id} did a EDIT invite in {after.channel}.")
            await after.delete()
    elif after.content.find("discordapp.com/invite") != -1 and not isinstance(after.channel, discord.channel.DMChannel):
        # found "discordapp.com/invite"
        ind = after.content.find("discordapp.com/invite")
        if after.content[ind + len("discordapp.com/invite"):] == "/jDMYEV5":
            pass
        else:
            # found discord.gg!
            em = discord.Embed(description=f"{bot.CROSS_MARK}  You can not send invite links!")
            await after.channel.send(embed=em)    
            await chn.send(f"{after.author.mention} | {after.author.id} did a EDIT invite in {after.channel}.")
            await after.delete()
    elif after.content.find("discord.com/invite") != -1 and not isinstance(after.channel, discord.channel.DMChannel):
        # found "discord.com/invite"
        ind = after.content.find("discord.com/invite")
        if after.content[ind + len("discord.com/invite"):] == "/jDMYEV5":
            pass
        else:
            # found discord.gg!
            em = discord.Embed(description=f"{bot.CROSS_MARK}  You can not send invite links!")
            await after.channel.send(embed=em) 
            await chn.send(f"{after.author.mention} | {after.author.id} did a EDIT invite in {after.channel}.")
            await after.delete()

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Master command ERROR HANDLER!
@bot.event
async def on_command_error(ctx, error):
    # ignore command not found errors
    ignored = commands.CommandNotFound
    if isinstance(error, ignored):
        return

    # handle Cooldown's
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f'You must wait {int(s)} second(s) to use this command')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f'You must wait {int(m)} minute(s) and {int(s)} second(s) to use this command')
        else:
            await ctx.send(
                f'You must wait {int(h)} hour(s), {int(m)} minute(s) and {int(s)} second(s) to use this command')
        return
    # Handle wrong user input - missing arguments etc.
    elif isinstance(error, commands.UserInputError):
        await ctx.send(f'Please use the command properly:\n```{error}```')
        return
    # Handle permission issues (check failures)
    elif isinstance(error, commands.CheckFailure):
        em = discord.Embed(description=f"{bot.CROSS_MARK}  You lack the required permissions!")
        await ctx.send(embed=em)
        return
    # handle unhandled errors - just raise it and send to discord.
    else:
        await ctx.send(f"Internal Error!\n```{error}```\nPlease inform the moderators immediately.")
        raise error

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="whoami")
async def whoami(context):
    channel = context.message.channel
    author = context.message.author
    await channel.send("Hi, you are " + str(author.mention) + " and you are talking to **The Oracle** a bot made for **The Matrix**!! You are currently in the channel : " + str(channel.mention))
    await context.message.author.send("You can not let the other members on the server know about this... Its top secret stuff - you are an amazing person!! : )")

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="ONION")
async def onion(context):
    await context.send("https://cdn.discordapp.com/attachments/774156001993162793/814833307836481576/images.png")

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="kick", pass_context = True)
async def kick(context, member: discord.Member, *, reason=None):
    global kicks
    kicks = True
    for_reason = "For reason - "
    log_chat = bot.get_channel(bot.data['logs'][str(context.guild.id)])
    if reason == None:
        reason = "No reason provided! by moderator " + str(context.message.author)
    if reason != "No reason provided! by moderator " + str(context.message.author):
        reason = reason + "! by moderator " + str(context.message.author)
    if context.message.author != member:
        if kicks == True:
            await member.kick(reason=reason)
            emk = discord.Embed(description=f"**Member kicked**\n {member.mention}", color=discord.Color.red())
            emk.add_field(name="Reason", value=reason)
            emk.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
            emk.set_thumbnail(url=member.avatar_url)
        await log_chat.send(embed=emk)
        if reason == "No reason provided! by moderator " + str(context.message.author):
            for_reason = ""
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Succesfully Kicked {member.mention} \n{for_reason} {str(reason)}")
        await context.send(embed=em)
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> You cannot kick yourself!")
        await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="ban", pass_context = True)
@commands.has_permissions(ban_members=True)
async def ban(context, member: discord.User, *, reason=None):
    global ban_reason
    for_reason = "For reason - "
    if reason == None:
        reason = "No reason provided! by moderator " + str(context.message.author)
    if reason != "No reason provided! by moderator " + str(context.message.author):
        reason = reason + "! by moderator " + str(context.message.author)
    ban_reason = str(reason)
    if context.message.author != member:
        await member.ban(reason=reason)
        if reason == "No reason provided! by moderator " + str(context.message.author):
            for_reason = ""
        em = discord.Embed(description=f"<:tick_mark:814801884358901770> Succesfully Banned {member.mention} \n{for_reason}{str(reason)}")
        await context.send(embed=em)
    else:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> You cannot ban yourself!")
        await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['ui', 'info', 'i'])
async def userinfo(context, *, user: discord.Member = None):
    if isinstance(context.channel, discord.DMChannel):
        return    
    if user is None:
        user = context.author
    date_format = "%a, %d %b %Y %I:%M %p"
    em = discord.Embed(title=str(user.display_name) + "'s User Information", color=discord.Color.blue(), description=user.mention)
    em.set_thumbnail(url=user.avatar_url)
    em.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(context.guild.members, key=lambda m: m.joined_at)
    em.add_field(name="Join position", value=str(members.index(user)+1))
    em.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
    m = 16
    if len(user.roles) > m:
        role_string = "Too many to list! <:whathasyoudone:796680789881389146>"
    em.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string)
    em.add_field(name="Bot", value=user.bot)
    verified = not user.pending
    em.add_field(name="Verified", value=str(verified))
    em.set_footer(text='USER ID: ' + str(user.id))
    await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=['si', 'gi', 'guildinfo'])
async def serverinfo(context):
    name = str(context.guild.name)
    owner = str(context.guild.owner)
    id = str(context.guild.id)
    memberCount = str(context.guild.member_count)
    roleCount = str(len(context.guild.roles))
    channelCount = str(len(context.guild.channels))
    textCount = str(len(context.guild.text_channels))
    voiceCount = str(len(context.guild.voice_channels))
    icon = str(context.guild.icon_url)  
    em = discord.Embed(title=name + " Server Information",color=discord.Color.blue())
    em.set_thumbnail(url=icon)
    em.add_field(name="Owner", value=owner, inline=True)
    em.add_field(name="Level", value=f"{context.guild.premium_tier} ({context.guild.premium_subscription_count}/30)", inline=True)
    em.add_field(name="The Oracle", value="<:tick_mark:814801884358901770> True", inline=True)
    em.add_field(name="Member Count", value=memberCount, inline=True)
    em.add_field(name="Role Count", value=roleCount, inline=True)
    em.add_field(name="Channel Count", value=f"{channelCount} (<:text:812696450684551199>{textCount}, <:voice:812696440114774096>{voiceCount})", inline=True)
    em.add_field(name="Rules", value=f"{context.guild.rules_channel.mention}", inline=True)
    em.add_field(name="Moderation", value=f"[Click here!](https://discord.com/channels/297301054930944011/745958042486702123/812302504330526741)", inline=True)
    em.add_field(name="Leveling", value=f"[Click here!](https://discord.com/channels/297301054930944011/745958042486702123/747274838900736040)", inline=True)
    em.set_image(url=context.guild.banner_url)
    em.set_footer(text="Server ID : " + id)
    await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["ci", "channeli", "cinfo"])
async def channelinfo(context, *, channel: discord.TextChannel=None):
    date_format = "%a, %d %b %Y %I:%M %p"
    roles = ""
    if channel == None:
        channel = context.channel
    if isinstance(context.channel, discord.DMChannel):
        return
    em = discord.Embed(title=channel.name + " Channel Information", color=discord.Color.blue())
    em.add_field(name="Category", value=channel.category)
    em.add_field(name="Created at", value=channel.created_at.strftime(date_format))
    em.add_field(name="Position", value=channel.position)
    if channel.category != None:
        em.add_field(name="Synced", value=channel.permissions_synced)   
    em.add_field(name="Slowmode", value=channel.slowmode_delay)
    for role in channel.changed_roles:
        roles += f"{str(role.mention)}\n"
    if roles != "":
        em.add_field(name="Overwritten Roles", value=str(roles))
    else:
        em.add_field(name="Overwritten Roles", value="None")
    em.set_thumbnail(url=context.guild.icon_url)
    await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["ri", "rolei", "rinfo"])
async def roleinfo(context, *, role: discord.Role=None):
    tagss = role.tags
    date_format = "%a, %d %b %Y %I:%M %p"
    if role == None:
        eme = discord.Embed(description=f"<:cross_mark:814801897138815026> You must provide a role for this command!")
        await context.send(embed=eme)
    else:
        em = discord.Embed(title=role.name + " Role Information", color=discord.Color.blue())
        em.add_field(name="Color", value=str(role.color))
        em.add_field(name="Created at", value=str(role.created_at.strftime(date_format)))
        em.add_field(name="Position", value=str(role.position))
        em.add_field(name="Members", value=str(len(role.members)))
        em.add_field(name="Displayed", value=str(role.hoist))
        if hasattr(tagss, 'is_premium_subscriber') == True and hasattr(tagss, 'is_bot_managed') == True:
                em.add_field(name="Boost role/Bot role", value=str(role.tags.is_premium_subscriber()) + "/" + str(role.tags.is_bot_managed()))
        em.set_thumbnail(url=context.guild.icon_url)
    await context.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def purge(context, limit=5, member: discord.Member=None):
    await context.message.delete()
    msg = []
    try:
        limit = int(limit)
    except:
        return await context.send("Please pass in an integer as limit")
    if not member:
        await context.channel.purge(limit=limit)
        return await context.send(f"Purged {limit} messages", delete_after=5)
    async for m in context.channel.history():
        if len(msg) == limit:
            break
        if m.author == member:
            msg.append(m)
    await context.channel.delete_messages(msg)
    await context.send(f"Purged {limit} messages of {member.mention}", delete_after=3)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["a", "av"])
async def avatar(context, member: discord.Member=None):
    if member == None:
        member = context.message.author 
    em = discord.Embed(title="Avatar", color=discord.Color.blue())
    em.set_image(url=member.avatar_url)
    em.set_author(name=str(member), icon_url=member.avatar_url)
    em.set_footer(text="USER ID: " + str(member.id))
    await context.channel.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["servericon"])
async def icon(context):
    em = discord.Embed(title="Icon", color=discord.Color.blue())
    em.set_image(url=context.guild.icon_url)
    em.set_author(name=str(context.message.author), icon_url=context.message.author.avatar_url)
    em.set_footer(text="SERVER ID: " + str(context.guild.id))
    await context.channel.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["serverbanner"])
async def banner(context):
    em = discord.Embed(title="Banner", color=discord.Color.blue())
    em.set_image(url=context.guild.banner_url)
    em.set_author(name=str(context.message.author), icon_url=context.message.author.avatar_url)
    em.set_footer(text="SERVER ID: " + str(context.guild.id))
    await context.channel.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(aliases=["owo"])
async def owofy(context, message: discord.Message=None):
    if message == None:
        em = discord.Embed(description=f"<:cross_mark:814801897138815026> You must provide text!")
        await context.send(embed=em)
    l = "l"
    ln = "w"
    r = "r"
    rn = "w"
    na = "na"
    nan = "nya"
    msg = str(message)
    if l in message:
        msg.replace(l, ln)
    if r in message:
        msg.replace(r, rn)
    if na in message:
        msg.replace(na, nan)
    await context.channel.send(msg)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("with the lives of RAIDERS"))
    print('Bot is now online!')

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_ban(guild, user):
    global ban_reason
    log_chat = bot.get_channel(bot.data['logs'][str(guild.id)])
    em = discord.Embed(description=f"**Member banned**\n {user.mention}", color=discord.Color.red())
    if ban_reason != "":
        em.add_field(name="Reason", value=str(ban_reason))
    em.set_author(name=user.name + "#" + user.discriminator, icon_url=user.avatar_url)
    em.set_thumbnail(url=user.avatar_url)
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_message_edit(payload):  
    before = payload.cached_message
    channel = bot.get_channel(payload.channel_id)
    after = await channel.fetch_message(payload.message_id)
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    bc = f'{bot.CROSS_MARK} Not in Memory!'
    if hasattr(before, 'content'):
        if len(before.content) > 1024:
            before.content = before.content[0:1020] + "\n..."
        if len(after.content) > 1024:
            after.content = before.content[0:1020] + "\n..."
        bc = before.content
    if str(after.content) == "":
        return
    if after.author == bot.user:
        return
    em = discord.Embed(description=f"**Message edited in {str(channel.mention)}** - [Message]({after.jump_url})", color=discord.Color.purple())
    em.add_field(name=f"**Before**", value=str(bc), inline=False)
    em.add_field(name=f"**After**", value=str(after.content), inline=False)
    em.set_author(name=str(after.author), icon_url=after.author.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(after.id))
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_message_delete(payload):
    message = payload.cached_message
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])  
    bc = f'{bot.CROSS_MARK} Not in Memory!'
    auth = ""
    if hasattr(message, 'content'):
        if len(message.content) > 1024:
            message.content = message.content[0:1020] + "\n..."
        if str(message.content) == "":
            return
        bc = message.content
    if hasattr(message, 'author'):
        auth =  f" - {message.author.mention}"
    channel = bot.get_channel(payload.channel_id)
    em = discord.Embed(description=f"**Message deleted in {str(channel.mention)}**\n{bc}{auth}", color=discord.Color.red())
    if hasattr(message, 'author'):
        em.set_author(name=str(message.author), icon_url=message.author.avatar_url)
    if hasattr(message, 'id'):
        em.set_footer(text="MESSAGE ID: " + str(message.id))
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_bulk_message_delete(payload):
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    messages = payload.cached_messages
    message_contents = "\n".join([str(message.author.mention)+" : "+message.content for message in messages])
    channel = bot.get_channel(int(payload.channel_id))
    em = discord.Embed(description=f"**Bulk message delete in {str(channel.mention)}** \n {str(message_contents)}", color=discord.Color.red())
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_join(member):
    log_chat = bot.get_channel(bot.data['logs'][str(member.guild.id)])
    date_format = "%a, %d %b %Y %I:%M %p"
    em = discord.Embed(description= f"**Member Joined** - {member.mention}", color=discord.Color.green())
    em.set_author(name=str(member), icon_url=member.avatar_url)
    em.add_field(name="Joined", value=member.joined_at.strftime(date_format))  
    members = sorted(member.guild.members, key=lambda m: m.joined_at)
    em.add_field(name="Join position", value=str(members.index(member)+1))
    em.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=False)
    em.set_footer(text="USER ID: " + str(member.id))
    await log_chat.send(embed=em)

    await save()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_remove(member):
    log_chat = bot.get_channel(bot.data['logs'][str(member.guild.id)])
    global kicks
    if kicks == True:
        kicks = False
        return
    else:
        date_format = "%a, %d %b %Y %I:%M %p"
        em = discord.Embed(description= f"**Member Left** - {member.mention}", color=discord.Color.red())
        em.set_author(name=str(member), icon_url=member.avatar_url)
        em.add_field(name="Joined", value=member.joined_at.strftime(date_format), inline=False)
        em.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=False)
        if len(member.roles) > 1:
            role_string = ' '.join([r.mention for r in member.roles][1:])
            em.add_field(name="Roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
        em.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_update(before, after):
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    if before.roles != after.roles:
        for role in before.roles:
            if role not in after.roles:
                em = discord.Embed(description=f"**Role removed from** {before.mention} \n**Role** - {role.mention}", color=discord.Color.red())
                em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
                em.set_footer(text="USER ID: " + str(after.id)) 
                em.set_thumbnail(url=after.avatar_url)
                await log_chat.send(embed=em)
        for role in after.roles:
            if role not in before.roles:
                em = discord.Embed(description=f"**Role added to** {after.mention} \n**Role** - {role.mention}", color=discord.Color.green())
                em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
                em.set_footer(text="USER ID: " + str(after.id))
                em.set_thumbnail(url=after.avatar_url)
                await log_chat.send(embed=em)

    elif before.nick != after.nick:
        if after.nick == None:
            before.nick = before.nick
            em = discord.Embed(description=f"**Nickname removed for** - {after.mention}", color=discord.Color.blue())
            em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
            em.add_field(name="Before", value=f"{before.nick}")
            em.add_field(name="After", value=f"{after.nick}")
            em.set_thumbnail(url=after.avatar_url)
            em.set_footer(text="USER ID: " + str(after.id))
        if before.nick == None:
            before.nick = before.nick
            em = discord.Embed(description=f"**Nickname added for** - {after.mention}", color=discord.Color.blue())
            em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
            em.add_field(name="Before", value=f"{before.nick}")
            em.add_field(name="After", value=f"{after.nick}")
            em.set_thumbnail(url=after.avatar_url)
            em.set_footer(text="USER ID: " + str(after.id))
        if after.nick != None:
            if before.nick != None:
                em = discord.Embed(description=f"**Nickname changed for** - {after.mention}", color=discord.Color.blue())
                em.set_author(name=str(before.name) + "#" + str(before.discriminator), icon_url=before.avatar_url)
                em.add_field(name="Before", value=f"{before.nick}")
                em.add_field(name="After", value=f"{after.nick}")
                em.set_thumbnail(url=after.avatar_url)
                em.set_footer(text="USER ID: " + str(after.id)) 
        await log_chat.send(embed=em)
    else:
        await save()
        return

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_invite_create(invite):
    log_chat = bot.get_channel(bot.data['logs'][str(invite.guild.id)])
    em = discord.Embed(title= "New invite created", color=discord.Color.green())
    em.add_field(name="Invite", value=str(invite), inline=False)
    em.add_field(name="Creater", value=str(invite.inviter.mention), inline=True)
    em.add_field(name="Channel", value=str(invite.channel.mention), inline=True)
    em.set_thumbnail(url=invite.guild.icon_url)
    em.set_footer(text="USER ID: " + str(invite.inviter.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_invite_delete(invite):
    log_chat = bot.get_channel(bot.data['logs'][str(invite.guild.id)])
    em = discord.Embed(title= "Old invite revoked", color=discord.Color.red())
    em.add_field(name="Invite", value=str(invite), inline=False)
    em.add_field(name="Channel", value=str(invite.channel), inline=True)
    em.set_thumbnail(url=invite.guild.icon_url)
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_channel_create(channel):
    log_chat = bot.get_channel(bot.data['logs'][str(channel.guild.id)])
    em = discord.Embed(title=f"Channel Created - #{channel}", color=discord.Color.green())
    em.add_field(name="Catrgory", value=f"`{channel.category}`")
    em.set_thumbnail(url=channel.guild.icon_url)
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_channel_delete(channel):
    log_chat = bot.get_channel(bot.data['logs'][str(channel.guild.id)])
    em = discord.Embed(title=f"Channel Deleted - #{channel}", color=discord.Color.red())
    em.add_field(name="Catrgory", value=f"`{channel.category}`")
    em.set_thumbnail(url=channel.guild.icon_url)
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_reaction_add(payload):
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    emoji = payload.emoji
    member = payload.member
    channel = bot.get_channel(payload.channel_id)
    guild = channel.guild
    message = await channel.fetch_message(payload.message_id)
    if member.id == 811243240836825099:
        return
    em = discord.Embed(description=f"**‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎Reaction added in {channel.mention}** - [Message]({message.jump_url})   ", color=discord.Color.green())
    em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
    em.add_field(name="Message by", value=f"{message.author.mention}", inline=True)
    em.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(message.id))
    await log_chat.send(embed=em)
    if message.id == bot.data['ticket']['msg'][str(guild.id)]:
        em = discord.Embed(description=f"{member.mention} Are you sure?")
        mes = await channel.send(embed=em)
        await mes.add_reaction(bot.TICK_MARK)
        await mes.add_reaction(bot.CROSS_MARK)
        def check(reaction, user):
            return reaction.message.id == mes.id and str(reaction.emoji) in [bot.TICK_MARK, bot.CROSS_MARK] and user.id == member.id
        try:
            r, u = await bot.wait_for('reaction_add', timeout= 30, check=check)
        except asyncio.TimeoutError:
            em = discord.Embed(description=f"{bot.CROSS_MARK} You ran out of time! Please re-type the command!")
            me = await channel.channel.send(embed=em)
            await asyncio.sleep(5)
            await mes.delete()
            await me.delete()
            return
        if str(r.emoji) == bot.CROSS_MARK:
            em = discord.Embed(description=f"{bot.CROSS_MARK} {member.mention} Cancelling process!")
            memm = await channel.send(embed=em)
            await asyncio.sleep(5)
            await mes.delete()
            await memm.delete()
            await message.remove_reaction(emoji, member)
            return
        if str(r.emoji) == bot.TICK_MARK:
            em = discord.Embed(description=f"{bot.TICK_MARK} {member.mention} Creating ticket!")
            memm = await channel.send(embed=em)
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True)}
        chn = await guild.create_text_channel(f"#{bot.data['ticket']['count'][str(guild.id)]}-{member.name}", overwrites=overwrites)
        em = discord.Embed(title=f"Ticket #{bot.data['ticket']['count'][str(guild.id)]}")
        em.add_field(name='Creator', value=member.mention)
        await chn.send(embed=em)
        await message.remove_reaction(emoji, member)
        bot.data['ticket']['count'][str(guild.id)] = bot.data['ticket']['count'][str(guild.id)] + 1
        await asyncio.sleep(5)
        await mes.delete()
        await memm.delete()

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_reaction_remove(payload):
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    emoji = payload.emoji
    user = payload.user_id
    member = bot.get_user(user)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    em = discord.Embed(description=f"**Reaction removed in {channel.mention}** - [Message]({message.jump_url})", color=discord.Color.red())
    em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
    em.add_field(name="Message by", value=f"{message.author.mention}", inline=False)
    em.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
    em.set_footer(text="MESSAGE ID: " + str(message.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_reaction_clear(payload):
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    em = discord.Embed(title=f"Reactions Cleared", color=discord.Color.red())
    em.add_field(name="Message", value=f"[Click Here!]({message.jump_url})", inline=False)
    em.set_thumbnail(url=channel.guild.icon_url)
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_raw_reaction_clear_emoji(payload):
    log_chat = bot.get_channel(bot.data['logs'][str(payload.guild_id)])
    emoji = payload.emoji
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    em = discord.Embed(title=f"Emoji Cleared", color=discord.Color.red())
    em.add_field(name="Emoji", value=f"{str(emoji)}", inline=False)
    em.add_field(name="Message", value=f"[Click Here!]({message.jump_url})", inline=False)
    em.set_thumbnail(url=channel.guild.icon_url)
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_channel_update(before, after):
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    valueb = ""
    valuea = ""
    em = discord.Embed(title=f'Channel "{before.name}" Updated', color=discord.Color.blue())
    if before.category != after.category:
        valueb += f"**Category** - {before.category}\n"
        valuea += f"**Category** - {after.category}\n"
    if before.name != after.name:
        valueb += f"**Name** - {before.name}\n"
        valuea += f"**Name** - {after.name}\n"
    if before.permissions_synced != after.permissions_synced:
        if before.permissions_synced == False:
            valueb += "None\n"
            valuea += f"**Synced with** {after.category}\n"
        if before.permissions_synced == True:
            valueb += "None\n"
            valuea += f"**Unsynced with** {after.category}\n"
    if before.changed_roles != after.changed_roles:
        if len(before.changed_roles) < len(after.changed_roles):
            for role in after.changed_roles:
                if role not in before.changed_roles: 
                    valueb += "None\n"
                    valuea += f"**Overwrite added - ** {role.mention}\n"
        if len(before.changed_roles) > len(after.changed_roles):
            for role in before.changed_roles:
                if role not in after.changed_roles: 
                    valueb += "None\n"
                    valuea += f"**Overwrite removed - ** {role.mention}\n"
    if before.topic != after.topic:
        if before.topic == "":
            valueb += "None\n"
            valuea += f"**Topic added - ** {after.mention}\n"
        if after.topic == "":
            valueb += "None\n"
            valuea += f"**Topic removed - ** {role.mention}\n"
    em.add_field(name="Before", value=valueb)
    em.add_field(name="After", value=valuea)
    em.set_thumbnail(url=before.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(before.id))
    if valuea != "" and valueb != "":
        await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_channel_pins_update(channel, last_pin):
    log_chat = bot.get_channel(bot.data['logs'][str(channel.guild.id)])
    status = "Pins Updated"
    pins = await channel.pins()
    pin = "\n".join(["[Click Here!](" + pin.jump_url + ")" for pin in pins])
    if pin == "":
        pin = None
        status = "Pins Removed"
    em = discord.Embed(title=status, color=discord.Color.blue())
    em.add_field(name="Channel", value=channel.mention)
    em.add_field(name="Pins", value=str(pin))
    em.set_thumbnail(url=channel.guild.icon_url)
    em.set_footer(text="CHANNEL ID: " + str(channel.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_update(before, after):
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    if before.banner != after.banner:
        emold = discord.Embed(title=f"{after.name}'s' Banner Changed", description="Before", color=discord.Color.blue())
        emold.set_image(url=before.banner_url)
        emold.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{after.name}'s Banner Changed", description="After", color=discord.Color.blue())
        emnew.set_image(url=after.banner_url)
        emnew.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    if before.name != after.name:
        em = discord.Embed(title="Server Name Changed", color=discord.Color.blue())
        em.add_field(name="Before", value=before.name, inline=False)
        em.add_field(name="After", value=after.name, inline=False)
        em.set_thumbnail(url=before.icon_url)
        em.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=em)
    if before.icon != after.icon:
        emold = discord.Embed(title=f"{after.name}'s Icon Changed", description="Before", color=discord.Color.blue())
        emold.set_image(url=before.icon_url)
        emold.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{after.name}'s Icon Changed", description="After", color=discord.Color.blue())
        emnew.set_image(url=after.icon_url)
        emnew.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    if before.owner != after.owner:
        em = discord.Embed(title="Server Owner Changed", color=discord.Color.blue())
        em.add_field(name="Before", value=before.owner.mention, inline=False)
        em.add_field(name="After", value=after.owner.mention, inline=False)
        em.set_thumbnail(url=before.icon_url)
        em.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=em)
    if before.splash != after.splash:
        emold = discord.Embed(title=f"{after.name}'s' Splash Changed", description="Before", color=discord.Color.blue())
        emold.set_image(url=before.spash_url)
        emold.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emold)
        emnew = discord.Embed(title=f"{after.name}'s Splash Changed", description="After", color=discord.Color.blue())
        emnew.set_image(url=after.spash_url)
        emnew.set_footer(text="SERVER ID: " + str(before.id))
        await log_chat.send(embed=emnew)
    if before.premium_subscription_count != after.premium_subscription_count:
        if before.premium_subscription_count > after.premium_subscription_count:
            em = discord.Embed(title=f"{after.name} lost boosts", color=discord.Color.red())
            em.add_field(name="Before", value=before.premium_subscription_count, inline=False)
            em.add_field(name="After", value=after.premium_subscription_count, inline=False)
            await log_chat.send(embed=em)
        else:
            em = discord.Embed(title=f"{after.name} gained boosts", color=discord.Color.green())
            em.add_field(name="Before", value=before.premium_subscription_count, inline=False)
            em.add_field(name="After", value=after.premium_subscription_count, inline=False)
            await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_role_create(role):
    log_chat = bot.get_channel(bot.data['logs'][str(role.guild.id)])
    em = discord.Embed(title=f'Role "{role.name}" Created', color=discord.Color.green())
    em.set_thumbnail(url=role.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(role.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_role_delete(role):
    log_chat = bot.get_channel(bot.data['logs'][str(role.guild.id)])
    em = discord.Embed(title=f'Role "{role.name}" Deleted', color=discord.Color.red())
    em.set_thumbnail(url=role.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(role.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_role_update(before, after):
    log_chat = bot.get_channel(bot.data['logs'][str(after.guild.id)])
    valueb = ""
    valuea = ""
    permissions = ""
    emoji = ""
    em = discord.Embed(title=f'Role "{before.name}" Updated', color=discord.Color.blue())
    if before.name != after.name:
        valueb += f"**Name** - {before.name}\n"
        valuea += f"**Name** - {after.name}\n"
    if before.color != after.color:
        valueb += f"**Color** - {str(before.color)}\n"
        valuea += f"**Color** - {str(after.color)}\n"
    if before.permissions.add_reactions != after.permissions.add_reactions:
        if after.permissions.add_reactions == True:
            emoji = bot.TICK_MARK
        if after.permissions.add_reactions == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**add_reactions** `{after.permissions.add_reactions}`\n"
    if before.permissions.administrator != after.permissions.administrator:
        if after.permissions.administrator == True:
            emoji = bot.TICK_MARK
        if after.permissions.administrator == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**administrator** `{after.permissions.administrator}`\n"
    if before.permissions.attach_files != after.permissions.attach_files:
        if after.permissions.attach_files == True:
            emoji = bot.TICK_MARK
        if after.permissions.attach_files == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**attach_files** `{after.permissions.attach_files}`\n"
    if before.permissions.ban_members != after.permissions.ban_members:
        if after.permissions.ban_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.ban_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**ban_members** `{after.permissions.ban_members}`\n"
    if before.permissions.change_nickname != after.permissions.change_nickname:
        if after.permissions.change_nickname == True:
            emoji = bot.TICK_MARK
        if after.permissions.change_nickname == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**change_nickname** `{after.permissions.change_nickname}`\n"
    if before.permissions.connect != after.permissions.connect:
        if after.permissions.connect == True:
            emoji = bot.TICK_MARK
        if after.permissions.connect == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**connect** `{after.permissions.connect}`\n"
    if before.permissions.create_instant_invite != after.permissions.create_instant_invite:
        if after.permissions.create_instant_invite == True:
            emoji = bot.TICK_MARK
        if after.permissions.create_instant_invite == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**create_instant_invite** `{after.permissions.create_instant_invite}`\n"
    if before.permissions.deafen_members != after.permissions.deafen_members:
        if after.permissions.deafen_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.deafen_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**deafen_members** `{after.permissions.deafen_members}`\n"
    if before.permissions.embed_links != after.permissions.embed_links:
        if after.permissions.embed_links == True:
            emoji = bot.TICK_MARK
        if after.permissions.embed_links == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**embed_links** `{after.permissions.embed_links}`\n"
    if before.permissions.external_emojis != after.permissions.external_emojis:
        if after.permissions.external_emojis == True:
            emoji = bot.TICK_MARK
        if after.permissions.external_emojis == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**external_emojis** `{after.permissions.external_emojis}`\n"
    if before.permissions.kick_members != after.permissions.kick_members:
        if after.permissions.kick_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.kick_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**kick_members** `{after.permissions.kick_members}`\n"
    if before.permissions.manage_channels != after.permissions.manage_channels:
        if after.permissions.manage_channels == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_channels == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_channels** `{after.permissions.manage_channels}`\n"
    if before.permissions.manage_emojis != after.permissions.manage_emojis:
        if after.permissions.manage_emojis == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_emojis == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_emojis** `{after.permissions.manage_emojis}`\n"
    if before.permissions.manage_guild != after.permissions.manage_guild:
        if after.permissions.manage_guild == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_guild == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_guild** `{after.permissions.manage_guild}`\n"
    if before.permissions.manage_messages != after.permissions.manage_messages:
        if after.permissions.manage_messages == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_messages == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_messages** `{after.permissions.manage_messages}`\n"
    if before.permissions.manage_nicknames != after.permissions.manage_nicknames:
        if after.permissions.manage_nicknames == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_nicknames == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_nicknames** `{after.permissions.manage_nicknames}`\n"
    if before.permissions.manage_permissions != after.permissions.manage_permissions:
        if after.permissions.manage_permissions == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_permissions == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_permissions** `{after.permissions.manage_permissions}`\n"
    if before.permissions.manage_roles != after.permissions.manage_roles:
        if after.permissions.manage_roles == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_roles == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_roles** `{after.permissions.manage_roles}`\n"
    if before.permissions.manage_webhooks != after.permissions.manage_webhooks:
        if after.permissions.manage_webhooks == True:
            emoji = bot.TICK_MARK
        if after.permissions.manage_webhooks == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**manage_webhooks** `{after.permissions.manage_webhooks}`\n"
    if before.permissions.mention_everyone != after.permissions.mention_everyone:
        if after.permissions.mention_everyone == True:
            emoji = bot.TICK_MARK
        if after.permissions.mention_everyone == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**mention_everyone** `{after.permissions.mention_everyone}`\n"
    if before.permissions.move_members != after.permissions.move_members:
        if after.permissions.move_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.move_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**move_members** `{after.permissions.move_members}`\n"
    if before.permissions.mute_members != after.permissions.mute_members:
        if after.permissions.mute_members == True:
            emoji = bot.TICK_MARK
        if after.permissions.mute_members == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**mute_members** `{after.permissions.mute_members}`\n"
    if before.permissions.priority_speaker != after.permissions.priority_speaker:
        if after.permissions.priority_speaker == True:
            emoji = bot.TICK_MARK
        if after.permissions.priority_speaker == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**priority_speaker** `{after.permissions.priority_speaker}`\n"
    if before.permissions.read_message_history != after.permissions.read_message_history:
        if after.permissions.read_message_history == True:
            emoji = bot.TICK_MARK
        if after.permissions.read_message_history == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**read_message_history** `{after.permissions.read_message_history}`\n"
    if before.permissions.read_messages != after.permissions.read_messages:
        if after.permissions.read_messages == True:
            emoji = bot.TICK_MARK
        if after.permissions.read_messages == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**read_messages** `{after.permissions.read_messages}`\n"
    if before.permissions.send_messages != after.permissions.send_messages:
        if after.permissions.send_messages == True:
            emoji = bot.TICK_MARK
        if after.permissions.send_messages == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**send_messages** `{after.permissions.send_messages}`\n"
    if before.permissions.send_tts_messages != after.permissions.send_tts_messages:
        if after.permissions.send_tts_messages == True:
            emoji = bot.TICK_MARK
        if after.permissions.send_tts_messages == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**send_tts_messages** `{after.permissions.send_tts_messages}`\n"
    if before.permissions.speak != after.permissions.speak:
        if after.permissions.speak == True:
            emoji = bot.TICK_MARK
        if after.permissions.speak == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**speak** `{after.permissions.speak}`\n"
    if before.permissions.stream != after.permissions.stream:
        if after.permissions.stream == True:
            emoji = bot.TICK_MARK
        if after.permissions.stream == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**stream** `{after.permissions.stream}`\n"
    if before.permissions.use_external_emojis != after.permissions.use_external_emojis:
        if after.permissions.use_external_emojis == True:
            emoji = bot.TICK_MARK
        if after.permissions.use_external_emojis == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**use_external_emojis** `{after.permissions.use_external_emojis}`\n"
    if before.permissions.use_voice_activation != after.permissions.use_voice_activation:
        if after.permissions.use_voice_activation == True:
            emoji = bot.TICK_MARK
        if after.permissions.use_voice_activation == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**use_voice_activation** `{after.permissions.use_voice_activation}`\n"
    if before.permissions.view_audit_log != after.permissions.view_audit_log:
        if after.permissions.view_audit_log == True:
            emoji = bot.TICK_MARK
        if after.permissions.view_audit_log == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**view_audit_log** `{after.permissions.view_audit_log}`\n"
    if before.permissions.view_guild_insights != after.permissions.view_guild_insights:
        if after.permissions.view_guild_insights == True:
            emoji = bot.TICK_MARK
        if after.permissions.view_guild_insights == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**view_guild_insights** `{after.permissions.view_guild_insights}`\n"
    if before.hoist != after.hoist:
        if after.hoist == True:
            emoji = bot.TICK_MARK
        if after.hoist == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**display_seperately** `{after.hoist}`\n"
    if before.mentionable != after.mentionable:
        if after.mentionable == True:
            emoji = bot.TICK_MARK
        if after.mentionable == False:
            emoji = bot.CROSS_MARK 
        permissions += f"{emoji}**mentionable** `{after.mentionable}`\n"
    if valuea == "":
        valuea = None
    if valueb == "":
        valueb = None
    em.add_field(name="Before", value=valueb)
    em.add_field(name="After", value=valuea)
    if permissions != "":
        em.add_field(name="Permissions", value=permissions)
    em.set_thumbnail(url=before.guild.icon_url)
    em.set_footer(text="ROLE ID: " + str(before.id))
    await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_voice_state_update(member, before, after):
    log_chat = bot.get_channel(bot.data['logs'][str(member.guild.id)])
    status = ""
    status2 = ""
    status3 = ""
    status4 = ""
    status5 = ""
    status6 = ""
    status7 = ""
    status8 = ""
    field_2 = False
    color = ""
    color2 = ""
    color3 = ""
    color4 = ""
    color5 = ""
    color6 = ""
    color7 = ""
    color8 = ""
    if before.channel != after.channel:
        if before.channel == None:
            status = "**Member joined voice channel**"
            color = discord.Color.green()
        if after.channel == None:
            status = "**Member left voice channel**"
            color = discord.Color.red()
        if before.channel != None and after.channel != None:
            status = "**Member changed voice channels**"
            field_2 = True
            color = discord.Color.blue()
        em = discord.Embed(description=f"{status} - {member.mention}", color=color)
        em.set_author(name=member, icon_url=member.avatar_url)
        if field_2 == True:
            em.add_field(name="Channel 1", value=before.channel)
            em.add_field(name="Channel 2", value=after.channel)
        else:
            if after.channel == None:
                em.add_field(name="Channel", value=before.channel)
            else:
                em.add_field(name="Channel", value=after.channel)
        em.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em)
    if before.mute != after.mute:
        if before.mute == False:
            status2 = "**Member muted**"
            color2 = discord.Color.red()
        if after.mute == False:
            status2 = "**Member unmuted**"
            color2 = discord.Color.green()
        em2 = discord.Embed(description=f"{status2} - {member.mention}", color=color2)
        em2.set_author(name=member, icon_url=member.avatar_url)
        em2.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em2)
    if before.deaf != after.deaf:
        if before.deaf == False:
            status3 = "**Member deafened**"
            color3 = discord.Color.red()
        if after.deaf == False:
            status3 = "**Member undefeaned**"
            color3 = discord.Color.green()
        em3 = discord.Embed(description=f"{status3} - {member.mention}", color=color3)
        em3.set_author(name=member, icon_url=member.avatar_url)
        em3.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em3)
    if before.self_mute != after.self_mute:
        if before.self_mute == False:
            status4 = "**Member self muted**"
            color4 = discord.Color.red()
        if after.self_mute == False:
            status4 = "**Member self unmuted**"
            color4 = discord.Color.green()
        em4 = discord.Embed(description=f"{status4} - {member.mention}", color=color4)
        em4.set_author(name=member, icon_url=member.avatar_url)
        em4.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em4)
    if before.self_deaf != after.self_deaf:
        if before.self_deaf == False:
            status5 = "**Member self deafened**"
            color5 = discord.Color.red()
        if after.self_deaf == False:
            status5 = "**Member self undefeaned**"
            color5 = discord.Color.green()
        em5 = discord.Embed(description=f"{status5} - {member.mention}", color=color5)
        em5.set_author(name=member, icon_url=member.avatar_url)
        em5.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em5)
    if before.self_stream != after.self_stream:
        if before.self_stream == False:
            status6 = "**Member started streaming**"
            color6 = discord.Color.green()
        if after.self_stream == False:
            status6 = "**Member stopped streaming**"
            color6 = discord.Color.red()
        em6 = discord.Embed(description=f"{status6} - {member.mention}", color=color6)
        em6.set_author(name=member, icon_url=member.avatar_url)
        em6.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em6)
    if before.self_video != after.self_video:
        if before.self_video == False:
            status7 = "**Member started sharing their video**"
            color7 = discord.Color.green()
        if after.self_video == False:
            status7 = "**Member stopped sharing their video**"
            color7 = discord.Color.red()
        em7 = discord.Embed(description=f"{status7} - {member.mention}", color=color7)
        em7.set_author(name=member, icon_url=member.avatar_url)
        em7.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em7)
    if before.self_video != after.self_video:
        if before.afk == False:
            status8 = "**Member now afk**"
            color8 = discord.Color.red()
        if after.afk == False:
            status8 = "**Member not afk**"
            color8 = discord.Color.green()
        em8 = discord.Embed(description=f"{status8} - {member.mention}", color=color8)
        em8.set_author(name=member, icon_url=member.avatar_url)
        em8.set_footer(text="USER ID: " + str(member.id))
        await log_chat.send(embed=em8)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_user_update(before, after):
    for guild in bot.data['logs']:
        log_chat = bot.get_channel(bot.data['logs'][str(guild)])
        if before.avatar != after.avatar:
            emold = discord.Embed(title=f"{before.display_name}'s Avatar Updated", description="Before", color=discord.Color.blue())
            emold.set_image(url=before.avatar_url)
            emold.set_footer(text="USER ID: " + str(before.id))
            await log_chat.send(embed=emold)
            emnew = discord.Embed(title=f"{before.display_name}'s Avatar Updated", description="After", color=discord.Color.blue())
            emnew.set_image(url=after.avatar_url)
            emnew.set_footer(text="USER ID: " + str(before.id))
            await log_chat.send(embed=emnew)
        else:
            em = discord.Embed(title=f"{before.display_name}'s Name/Discriminator Updated", color=discord.Color.blue())
            em.add_field(name="Before", value=f"`{before.name}#{before.discriminator}`", inline=False)
            em.add_field(name="After", value=f"`{after.name}#{after.discriminator}`", inline=False)
            em.set_footer(text="USER ID: " + str(before.id))
            em.set_thumbnail(url=before.avatar_url)
            await log_chat.send(embed=em)

    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_guild_join(guild):
    bot.data['logs'][str(guild.id)] = ""

    bot.data['widt'][str(guild.id)] = ""

    bot.data['suggest']['chn'][str(guild.id)] = ""
    bot.data['suggest']['count'][str(guild.id)] = 1
    bot.data['suggest']['val'][str(guild.id)] = {}
    bot.data['ticket']['op'][str(guild.id)] = {}

    bot.data['ticket']['chn'][str(guild.id)] = ""
    bot.data['ticket']['count'][str(guild.id)] = 1
    bot.data['suggest']['val'][str(guild.id)] = {}
    await save()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------








bot.run('ODExMjQzMjQwODM2ODI1MDk5.YCvXJA.koWM9mPBTB5iwhKmCwPS1KHu0H0')
