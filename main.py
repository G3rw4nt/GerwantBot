import os
import discord
from discord.ext.tasks import loop
import stream
import time
import datetime
import tweepy



client_id = os.environ['client_id']            #creating stream object
client_secret = os.environ['client_secret']
streamer_name = os.environ['streamer_name']

gerwant = stream.Stream(client_id,client_secret,streamer_name)


#twitter API authentication stuff
auth = tweepy.OAuthHandler(os.environ['twitter_consumer_token'], os.environ['twitter_consumer_secret'])
auth.set_access_token(os.environ['twitter_key'], os.environ['twitter_secret'])

api = tweepy.API(auth)
#starting discord bot
client = discord.Client()
alreadyOnline = False
@client.event

async def on_ready():  #function running on bot's boot
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name='gerw4nt', url='https://www.twitch.tv/gerw4nt'))

    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    
    notifications.start()
  
@loop(seconds = 5) # it check if stream is online every 5 seconds, if it is, it sends discord notification and posts tweet
async def notifications():
  print(gerwant.getStreamData()["data"])
  global alreadyOnline
  if(gerwant.isOnline() == False):
    print("Stream offline!")
    alreadyOnline = False
  elif(gerwant.isOnline() == True and alreadyOnline == False):
    alreadyOnline = True
    channel = client.get_channel(829321267999670272)
    time.sleep(10)
    while(len(gerwant.getStreamData()["data"]) == 0):
      {
        print("waiting for stream data")
      }
    data = gerwant.getStreamData()
    await channel.send("@everyone Właśnie odpaliłem maśniutkiego streama, wbijaj wariacie! 🐺🐺🐺")
    
    embed = discord.Embed(title=data["data"][0]["title"], url="https://twitch.tv/gerw4nt", description="Stream online 🐺🐺🐺", color=0xb50c0f, timestamp=datetime.datetime.utcnow())
    icon = "https://static-cdn.jtvnw.net/jtv_user_pictures/d52d3af0-4dfb-4fdf-ac98-8daa53017859-profile_image-300x300.png"
    embed.set_author(name="gerw4nt", url="https://twitch.tv/gerw4nt", icon_url = icon)
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Gra: ", value=data["data"][0]["game_name"], inline = True)
    embed.set_image(url="https://static-cdn.jtvnw.net/previews-ttv/live_user_gerw4nt-480x270.jpg")
    embed.set_footer(text='https://twitch.com/gerw4nt', icon_url = icon)
    await channel.send(embed=embed)
    api.update_status("""#STREAM ONLINE! 🐺🐺🐺
Today we're playing: {} 
https://twitch.tv/gerw4nt
#twitchtv #twitch #goinglive #gaming""".format(data["data"][0]["game_name"]))
    print("Stream online!")

client.run(os.environ['bot_token'])