from email import message
from pickle import FALSE
import discord
import http.client
import json

async def printConso(message, link):
    if link == FALSE:
        await message.reply('Compte pas lié avec Bouygues', mention_author=True)
        return
    str = "["
    consoTotal = 100
    conso = 50
    pourcentage = (conso / consoTotal) * 100
    for i in range (50):
        if i < pourcentage / 2:
            str += '+'
        else:
            str += '   '
    str += "]"
    await message.reply('Voici t\'a conso bg:\n' + str, mention_author=False)

async def printInfo(message):
    await message.reply('Voici les commandes:\n\tconso\n\tdebit\n\tlink\n\tchange', mention_author=False)

async def printDebit(message, link):
    if link == FALSE:
        await message.reply('Compte pas lié avec Bouygues', mention_author=True)
        return
    await message.reply('Voici t\'on debit bg', mention_author=False)

async def isLink(message, link):
    if link == True:
        await message.reply('Compte Discord lié avec compte Bouygues ;)', mention_author=False)
    else:
        await message.reply('Ton compte n\'est pas lié mon reuf', mention_author=False)

async def makeChange(message, link):
    if link == FALSE:
        await message.reply('Compte pas lié avec Bouygues', mention_author=True)
        return
    await message.reply('Voici t\'on debit bg', mention_author=False)

def getToken():
    conn = http.client.HTTPSConnection("oauth2.sandbox.bouyguestelecom.fr")
    payload = 'grant_type=client_credentials'
    headers = {
      'Authorization': 'Basic cGFydGVuYWlyZS5lbGJhLmJvdXlndWVzdGVsZWNvbS5mcjpuazZYRnNtREpTNmRtZVBy',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/ap4/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    lol = json.loads(data.decode("utf-8"))["access_token"]
    return lol

def validEmail(token, mail):
    conn = http.client.HTTPSConnection("open.api.sandbox.bouyguestelecom.fr")
    payload = json.dumps({
        "emailAddress": mail
    })
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/ap4/v1/customer-management/email-addresses/check", payload, headers)
    res = conn.getresponse()
    data = res.read()
    if data.decode("utf-8").count("true") != 2:
        #print('Bad customer')
        return False
    else:
        #print('Good customer')
        return True

class MyClient(discord.Client):
    async def on_ready(self):
        if validEmail(getToken(), "OLGA.GORSHKOVA1_AP4@GMAIL.COM") == False:
            exit()
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        link = validEmail(getToken(), "OLGA.GORSHKOVA1_AP4@GMAIL.COM")
        if message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author=True)
        elif message.content.startswith('!conso'):
            await printConso(message, link)
        elif message.content.startswith('!debit'):
            await printDebit(message, link)
        elif message.content.startswith('!link'):
            await isLink(message, link)
        elif message.content.startswith('!change'):
            await makeChange(message, link)
        elif message.content.startswith('!h'):
            await printInfo(message)

client = MyClient()
client.run('OTQxMzY2MTc5NTM1MTQyOTgy.YgU5kg.Jch0PTsGVUKjMt11AdJV12kQNqw')