import os
#os.system("python -m pip install youtube_dl discord")
import discord
import random
import time
import datetime
import asyncio
from discord.ext import commands




bot = commands.Bot(('franto ',"Franto ","f ", "F "),  
intents=discord.Intents.all(),
help_command=None)






@bot.command()
async def help(ctx):
    em = discord.Embed(title="Seznam dostupných příkazů:")
    em.add_field(name="hello", value="Says hello to you.")
    em.add_field(name="invite", value="Creates invite and sends you a link.", )
    em.add_field(name="list", value="Embedded list of servers that bot is in.")
    em.add_field(name="moudro", value="Writes something clever. (Czech)")
    em.add_field(name="ban", value="Bans specified user.")
    em.add_field(name="unban", value="Unbans specified user")
    em.add_field(name="kick", value="Kicks specified user.")
    em.add_field(name="ping", value="Tells you the bots latency.")
    em.add_field(name="track", value="Shows the song which is user listening on Spotify right now.")
    em.add_field(name="clear", value="Clears specified messages from the channel.")
    em.add_field(name="members", value="List of members on this server.")
    em.add_field(name="deprese", value="Has depression with you.")
    em.add_field(name="role", value="Shows your top role.")
    em.add_field(name="aclear", value="Clears specified messages from the channel. (Admin only)")
    em.add_field(name="uptime", value="Shows how long the bot has been running.")
    em.add_field(name="say", value="Says what you want.")
    


    
    await ctx.send(embed = em)

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="track")
    async def track(self, ctx, user: discord.Member = None):
        """Shows the song which is user listening on Spotify right now."""
        user = user or ctx.author
        spotify_result = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)


        if spotify_result is None:

            em = discord.Embed(title=f"{user.name} momentálně neposlouchá Spotify!")
            await ctx.send(embed = em)

        em = discord.Embed(title=f"{user.name} právě poslouchá: ")
        
        em.set_thumbnail(url=spotify_result.album_cover_url)
        em.add_field(name="Název:", value=f"{spotify_result.title}")
        em.add_field(inline=False, name="Autor:", value=f"{spotify_result.artist}")
        em.add_field(inline=False, name="Odkaz:", value=f"https://open.spotify.com/track/{spotify_result.track_id}")
        

        await ctx.send(embed = em)




class Management(commands.Cog):


    @commands.command(name="join")
    async def join(self, ctx):
        """Joins the voice channel."""
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()


    @commands.command(name="leave")
    async def leave(self, ctx):
        """Leaves the voice channel."""
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        """Shows how long the bot has been running."""
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        embed = discord.Embed(title="Uptime", description=f"Bot has been running for: {uptime}", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name="role")
    async def nitro(self, ctx,  user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(user.top_role)
        
        if user.premium_since == None:
            await ctx.send(f"{user.display_name} nemá žádné vylepšení.")

        else:
            await ctx.send(f"{user.display_name}{user.premium_since}")
        

    
    async def is_admin(ctx):
        return ctx.author.id == 205691205034573824
    @commands.check(is_admin)

    @commands.command(name="aclear")
    async def aclear(self, ctx, number):
        """Clears specified messages from the channel."""
        if int(number) > 1000:
            await ctx.send("Maximální počet zpráv je 1000 :)")
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=2)
            return

        await ctx.channel.purge(limit=int(number)+1)
        

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages = True)
    async def _clear(self, ctx, number):
        """Clears specified messages from the channel."""
        if int(number) > 1000:
            await ctx.send("Maximální počet zpráv je 1000 :)")
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=2)
            return

        await ctx.channel.purge(limit=int(number)+1)


    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """Kicks specified user from the server."""
        
        await member.kick(reason=reason)        
        
        em = discord.Embed(title="Uživatel vyhozen!", description=f"{ctx.author.mention} vyhodil uživatele {member.mention}!")
        await ctx.send(embed = em)  

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """Bans specified user from the server."""       
               
        em = discord.Embed(title="Uživatel zabanován!", description=f"{ctx.author.mention} zabanoval uživatele ```{member}```")
        await ctx.send(embed = em)
        await member.ban(reason=reason) 


    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user=None):
        """Unbans specified user from the server."""

        try:
            user = await commands.converter.UserConverter().convert(ctx, user)
        except:
            await ctx.send("Error: user could not be found!")
            return

        try:
            bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
            if user in bans:
                await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
            else:
                await ctx.send("User not banned!")
                return

        except discord.Forbidden:
            await ctx.send("I do not have permission to unban!")
            return

        except:
            await ctx.send("Unbanning failed!")
            return

        em = discord.Embed(title="Uživatel odbanován!", description=f"{ctx.author.mention} odbanoval uživatele ```{user}```")
        await ctx.send(embed = em)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Napíše latenci bota."""
        #time_1 = time.perf_counter()
        #await ctx.trigger_typing()
        #time_2 = time.perf_counter()
        #ping = round(bot.latency *1000)
        #em = discord.Embed(title=f":ping_pong: ***Pong!***  {ping}ms")
        #await ctx.send(embed = em)
        before = time.monotonic()
        message = await ctx.send("** **")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")

class Basic(commands.Cog):

    @commands.command(name="say")
    async def say(self, ctx, message):
        """Says what you want."""
        await ctx.send(message)


    @commands.command(name='hello')
    async def hello(self, ctx: commands.Context):
        """Says hello to you!"""
        await ctx.send(f"Zdravím tě {ctx.author.mention}" )

    @commands.command(name="invite")
    @commands.has_permissions(create_instant_invite = True)
    async def invite(self, ctx):
        """Creates server invite."""
        link = await ctx.channel.create_invite(max_uses = 0, unique = False)
        em = discord.Embed(title=f"Tu máš invite **{ctx.author.name}**")
        em.add_field(name="Odkaz: ", value=f"{link}")
        await ctx.send(embed = em)

    @commands.command(name="list")
    async def list(self, ctx):
        """Embedded list of servers that bot is in."""

        for guild in bot.guilds:
            name = guild.name
            chunk = str(guild.chunked)
            owner = guild.owner
            count = guild.member_count
            response = (f"```Server name = {name}" + f" \nChunked = {chunk}```")

            embed = discord.Embed(title=name, description=f"Chunked: {chunk} \nOwner: **{owner}** \nMembers: {count}")
            await ctx.send(embed=embed)


    @commands.command(name="members")
    async def members(self, ctx):
        """List of members on this server."""
        em = discord.Embed(title="Seznam členů tohoto serveru:")
        for guild in bot.guilds:
            for member in guild.members:

                em.add_field(name= '\u200b' , value=f"{member}", inline=True)
        await ctx.send(embed = em)
        
        
        """
        em = discord.Embed(title="Seznam členů tohoto serveru:")
        for guild in bot.guilds:
            for member in guild.members:

                em.add_field(name= '\u200b' , value=f"{member}", inline=False)
        await ctx.send(embed = em)
        """


    @commands.command(name="deprese")
    async def deprese(self, ctx):
        """Has depression with you."""
        await bot.change_presence(activity=discord.Game(name=f"deprese s {ctx.author}"))
        await ctx.send(f"{ctx.author.mention} feeluju :(")
        await asyncio.sleep(300)
        await bot.change_presence(activity=discord.Game(name="franto help"))
                

    @commands.command(name="moudro")
    async def moudro(self, ctx: commands.Context):
        """Writes something clever. (Czech)"""

        write_response = [
        "Bez peněz do hospody nelez.",
        ("Bez práce nejsou koláče."),
        ("Co je doma, to se počítá."),
        ("Co můžeš udělat dnes, neodkládej na zítřek."),
        ("Dobrá rada nad zlato."),
        ("Dvakrát měř, jednou řež."),
        ("Hloupý kdo dává, hloupější kdo nebere."),
        ("Hněv je špatný rádce."),
        ("Host do domu, Bůh do domu."),
        ("Host do domu, hůl do ruky."),
        ("Když kocour není doma, myši mají pré."),
        ("Líná huba, holé neštěstí."),
        ("Není kouře bez ohně."),
        ("V noci každá kočka černá."),
        ("Vyhni se opilému, jakož i bláznu."),
        ("Na každém šprochu pravdy trochu."),
        ("Mluviti stříbro, mlčeti zlato."),
        ("Starého psa novým kouskům nenaučíš."),
        ("Kdo se moc ptá, moc se dozví."),


        ]
        response = write_response
        await ctx.send(random.choice(response))




@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 762354312717533185:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        
        

        if payload.emoji.name == "head":
            role = discord.utils.get(guild.roles, name="👻Mentals👻")
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 762354312717533185:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        

        if payload.emoji.name == "head":
            role = discord.utils.get(guild.roles, name="👻Mentals👻")
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)


class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

@bot.event
async def on_ready():
    print('{0.user} has connected to Discord!'.format(bot))
    global startTime #global variable to be used later in cog
    startTime = time.time()# snapshot of time when listener sends on_ready
    await bot.change_presence(activity=discord.Game("franto help"))
    channel = bot.get_channel(762366971291238402)
    response = "Jsem ready!"
    await channel.send(response)


asyncio.run(bot.add_cog(Basic(bot)))
asyncio.run(bot.add_cog(Spotify(bot)))
asyncio.run(bot.add_cog(Management(bot)))


bot.run("TOKEN")
