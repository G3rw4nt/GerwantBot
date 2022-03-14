import requests
class Stream:
  client_id = 0
  client_secret = 0
  streamer_name = "name"

  def __init__(self,id,secret,name): #constructor
    self.client_id = id
    self.client_secret = secret
    self.streamer_name = name
  def getStreamData(self):  #parse json data about stream, like title, actual game, streamer's nick etc.
    body = {
    'client_id': self.client_id,
    'client_secret': self.client_secret,
    "grant_type": 'client_credentials'
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)

    
    keys = r.json()
    
    
    headers = {
        'Client-ID': self.client_id,
        'Authorization': 'Bearer ' + keys['access_token']
    }
    
    
    stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + self.streamer_name, headers=headers)
    
    stream_data = stream.json()
    
    return stream_data
  
  
  def isOnline(self):  #if data from getStreamData() exists, it returns True
    
    stream_data = self.getStreamData()
    if len(stream_data['data']) == 1:
        return True
    else:
        return False
    
    