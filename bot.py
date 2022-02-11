from pickle import FALSE
import discord
import http.client
import json

from datetime import date

client = discord.Client()

isLink = False

def numOfDays(date1, date2):
    return (date2-date1).days

async def printConso(message):
    if isLink == FALSE:
        await message.reply('Not link with your Bouygues Telecom account', mention_author=True)
        return
    data = getConso()[0]
    data = data["mainDataUsage"]
    strResult = "["
    consoTotal = int(data["limitBytes"])
    conso = int(data["usageBytes"])
    data = data["renewDate"].split("T")
    actualDate = data[0]
    date1 = date(2018, 12, 13)
    date2 = date(2019, 2, 25)
    resultDate = numOfDays(date1, date2)
    strDate = "Restart " + actualDate + " (" + str(resultDate) + " days)\n"
    pourcentage = (conso / consoTotal) * 100
    for i in range (50):
        if i < pourcentage / 2:
            strResult += '■'
        else:
            strResult += '   '
    strResult += "]"
    await message.reply(strDate + 'Actual consommation: ' + str(pourcentage)[:5] + '%\n' + strResult, mention_author=True)

async def printInfo(message):
    await message.reply('All commands:\n\tconso\n\tdebit\n\tlink\n\tchange', mention_author=False)

async def printDebit(message):
    if isLink == FALSE:
        await message.reply('Not link with your Bouygues Telecom account', mention_author=True)
        return
    channel = client.get_channel(941335733636038656)
    await channel.send(file=discord.File('screen_exemple/speed_test.png'))

async def isLinkAccount(message):
    global isLink

    if isLink == True:
        await message.reply('You are already link with your Bouygues Telecom account ;)', mention_author=True)
    else:
        con = validEmail(getToken(), "OLGA.GORSHKOVA1_AP4@GMAIL.COM")
        if con == False:
            await message.reply('Not link with your Bouygues Telecom account', mention_author=True)
        else:
            await message.reply('You are know link with your Bouygues Telecom account ;)', mention_author=True)
            isLink = True                

async def makeChange(message):
    if isLink == FALSE:
        await message.reply('Not link with your Bouygues Telecom account', mention_author=True)
        return
    await message.reply('Possible API où on pourrait changer d\'abonnement(passer d\'un forfais 50Go a 100Go) ou bine ajouter des limites()ne pas dépasser 10Go', mention_author=False)

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
    token = json.loads(data.decode("utf-8"))["access_token"]
    return token

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

def getConso():
    conn = http.client.HTTPSConnection("api.sandbox.bouyguestelecom.fr")
    payload = ''
    headers = {
      'Authorization': 'Bearer at-583ca345-e387-4d17-9e1d-3fc0788d7e5e'
    }
    conn.request("GET", "/ap4/customer-management/v1/usage-consumptions/mobile-data", payload, headers)
    res = conn.getresponse()
    data = res.read()
    token = json.loads(data.decode("utf-8"))["usages"]
    return token

class MyClient(discord.Client):
    async def on_ready(self):
        global isLink

        isLink = validEmail(getToken(), "OLGA.GORSHKOVA1_AP4@GMAIL.COM")
        if validEmail(getToken(), "OLGA.GORSHKOVA1_AP4@GMAIL.COM") == False:
            exit()
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if message.content.startswith('!hello'):
            #mail = message.author.name
            #print(discord.ClientUser.email)
            #print(dir(message.author))
            #await message.reply(mail, mention_author=True)
            await message.reply('Hello!', mention_author=True)
        elif message.content.startswith('!conso'):
            await printConso(message)
        elif message.content.startswith('!debit'):
            await printDebit(message)
        elif message.content.startswith('!link'):
            await isLinkAccount(message)
        elif message.content.startswith('!change'):
            await makeChange(message)
        elif message.content.startswith('!h'):
            await printInfo(message)

client = MyClient()
client.run(open('botLogin').read())