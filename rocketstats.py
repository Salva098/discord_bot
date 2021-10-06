import requests
from discord.embeds import Embed
import json

class Rocketstats:
    def stats(name):
        headers = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"}

        url="https://api.tracker.gg/api/v2/rocket-league/standard/profile/epic/{}".format(name)
        api=requests.get(url,headers=headers)


        if api.status_code==200:
            data = api.json()
            




        else:
            raise ValueError("no da señal el servidor")