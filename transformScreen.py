#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap
import os
import codecs

def transform(inFile, text, outFile, bgColor, language="en"):
    factor = 0.15
    img = Image.open(inFile)
    largeSize = img.size

    # create an image the same size
    newImage = Image.new("RGB", largeSize, bgColor)

    draw = ImageDraw.Draw(newImage)

    width, height = img.size
    newWidth = width - (width * factor)
    newHeight = int(height * newWidth/width)
    newWidth = int(newWidth)

    print str(width) + "," + str(height)
    print str(newWidth) + "," + str(newHeight)

    imgResized = img.resize((newWidth, newHeight), Image.ANTIALIAS)

    x = int(width * factor/2)
    y = int(height - newHeight - width * factor/4)
    print str(x) + "," + str(y)
    newImage.paste(imgResized, (x, y))

    # draw the text
    font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 28 * height/960)

    lines = textwrap.wrap(text, 40 if language != "ja" else 16)
    y = 5
    for line in lines:
        xline, yline = draw.textsize(line, font=font)
        x = (width - xline) / 2
        draw.text((x, y), line, "white", font=font)
        y = y + yline

    newImage.save(outFile)

android = { "en": ["en-US"], "nl": ["nl-NL"], "fr": ["fr-FR"], "de": ["de-DE"], "it": ["it-IT"], "ja": ["ja-JP"], "es": ["es-419", "es-ES"], "cs": ["cs-CZ"], "pt_BR": ["pt-BR"]}
ios = { "en": ["en-US"], "nl": ["nl-NL"], "fr": ["fr-FR"], "de": ["de-DE"], "it": ["it-IT"], "ja": ["ja-JP"], "es": ["es-ES"], "pt_BR": ["pt-BR"]}

devices = ["iPad-Retina", "iPhone-4s", "iPhone-5s", "iPhone-6", "iPhone-6-Plus"]

bgColor = "#383E49"

screenshots = {"discover": "2", "mixer":"5", "scoreview_page":"3", "discover_free":"7", "scoreview_bigger":"4", "sidemenu_loggedin":"6", "downloads":"1", "sidemenu_loggedin_free":"6"}

screenOrderFree = ["scoreview_page", "mixer", "discover_free", "sidemenu_loggedin_free", "scoreview_bigger"]
screenOrderPaid = ["scoreview_page", "mixer", "discover", "sidemenu_loggedin", "scoreview_bigger"]

apps = ["com.musescore.player", "com.musescore.playerlite"]

currentOs = "android"

if currentOs == "android":
    rootDir = "android_screenshot"
    languages = android
    imageTypes = ["phoneScreenshots", "sevenInchScreenshots", "tenInchScreenshots"]
    devices = ["iPhone-4s", "iPhone-6-Plus", "iPad-Retina"]
else:
    rootDir = "."
    languages = ios

for app in apps:
    screenOrder = screenOrderPaid
    if app == "com.musescore.playerlite":
        screenOrder = screenOrderFree

    if currentOs == "ios":
        outDir = rootDir+"/deliver-player/screenshots"
        if app == "com.musescore.playerlite":
            outDir = rootDir+"/deliver-playerlite/screenshots"
    else:
        outDir = rootDir+"/player"
        if app == "com.musescore.playerlite":
            outDir = rootDir+"/playerlite"
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for language in languages.keys():
        screenshotFile = "/Users/lasconic/player-qt/promotion/screenshots_" + language + ".txt"
        f = codecs.open(screenshotFile, 'r', "utf-8")
        lines = f.readlines()
        index = 1
        for name in screenOrder:
            for device in devices:
                i = int(screenshots[name])
                text = lines[i].strip()
                print text
                inFile = "/Users/lasconic/player-qt/promotion/" + device + "/" + language + "/" + name + ".png"
                print inFile
                for l in languages[language]:
                    outDir2 = outDir + "/" + l
                    if not os.path.exists(outDir2):
                        os.makedirs(outDir2)
                    if currentOs == "ios":
                        outDevice = device
                    else:
                        outDevice = imageTypes[devices.index(device)]
                    outFile = outDir2 + "/" + str(index) + "_" + outDevice + "_" + name + ".png"
                    print outFile
                    transform(inFile, text, outFile, bgColor, language)
            index = index + 1
