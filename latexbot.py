import discord
import os 
import requests
from PIL import Image as img
import PIL.ImageOps

from random import randint as rnd

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

#discord converts any picture link into a picture file in the chat
def fetchLatexImage(latexCode):
    latexCode = latexCode.replace("!latex-dark", "")
    latexCode = latexCode.replace("!latex", "")
    latexCode = latexCode.replace(" ", "&space;")
    latexCode = latexCode.replace("(", "\left\(")
    latexCode = latexCode.replace(")", r"\right\)")
    #this bot utilizes CodeCogs' LATEX api
    url = r"https://latex.codecogs.com/png.latex?\bg_white&space;" + latexCode
    return url

def invertImage(url):
    fetchedImage = requests.get(url)
    fileName = f"{rnd(10, 15)}.png"
    file = open(fileName, "wb")
    file.write(fetchedImage.content)
    file.close()

    imageToInvert = img.open(fileName).convert("RGB")
    invertedImage = PIL.ImageOps.invert(imageToInvert)
    invertedImage.save(fileName)
    return fileName
    
@client.event
async def on_ready():
    serverCount = 0

    for server in client.guilds:
        serverCount += 1
        print(f"{serverCount}. {server.name}")
    
    print(f"LATEX bot is in {serverCount} servers!")

@client.event
async def on_message(message):
    code = message.content
    
    if code.startswith("!latex-dark"):
        imageURLToInvert = fetchLatexImage(code)
        fileNameOfImage = invertImage(imageURLToInvert)
        await message.channel.send(file=discord.File(fileNameOfImage))

    elif code.startswith("!latex"):
        imageURLToSend = fetchLatexImage(code)
        await message.channel.send(imageURLToSend)

client.run(token)
