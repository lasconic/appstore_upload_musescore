from apiclient import sample_tools
from oauth2client import client
from os.path import expanduser

home = expanduser("~")
descriptionPath = home + "/player-qt/promotion"
imagesPath = home + "/Google Drive/MuseScore App Design/v1/Artwork"

# extract description, short description, etc... from player checkout
def extractDescription(language, os, appName):
    fname = descriptionPath + "/" + "description_" + language + ".txt"
    with open(fname) as f:
        content = f.readlines()


    inFree = False
    inAndroid = False
    inIOS = False

    inTitle = False
    inShortDescription = False
    inDescription = False
    inWhatsNew = False

    title = ""
    shortDescription = ""
    description = ""
    whatsNew = ""
    for line in content:
        if line.startswith("-- APP 2"):
            inFree = True
            if appName != "com.musescore.playerlite":
                break
        if appName == "com.musescore.playerlite" and not inFree:
            continue
        if line.startswith("---- Title"):
            inTitle = True
        if line.startswith("---- Short"):
            inShortDescription = True
            inTitle = False
        if line.startswith("--- Description"):
            inDescription = True
            inShortDescription = False
            inTitle = False
        if line.startswith("--- What"):
            inWhatsNew = True
            inDescription = False
            inShortDescription = False
            inTitle = False

        if line.startswith("--"):
            if line.startswith("-- Android"):
                inAndroid = not inAndroid
            if line.startswith("-- iOS"):
                inIOS = not inIOS
            continue

        if inAndroid and os != "android":
            continue
        if inIOS and os != "ios":
            continue
        if inTitle:
            title += line
        if inShortDescription:
            shortDescription += line
        if inDescription:
            description += line
        if inWhatsNew:
            whatsNew += line

    title = title.strip()
    shortDescription = shortDescription.strip()
    description = description.strip()
    whatsNew = whatsNew.strip()

    print "-- Title --"
    print title
    print "-- Short Description --" 
    print shortDescription
    print "-- Description --" 
    print description
    print "-- What's New? --"
    print whatsNew
    return {'title': title, 'shortDescription': shortDescription, 'description': description, 'whatsNew': whatsNew}

def changeDescriptionAndroid(package_name, language, title, shortDescription, description):
    myList = []
    # Authenticate and construct service.
    service, flags = sample_tools.init(
      myList,
      'androidpublisher',
      'v2',
      __doc__,
      __file__, parents=[],
      scope='https://www.googleapis.com/auth/androidpublisher')

    try:
        edit_request = service.edits().insert(body={}, packageName=package_name)
        result = edit_request.execute()
        edit_id = result['id']

        if (len(title) > 30):
            titleArray = title.split("-")
            title = titleArray[0].strip()

        listing_response_us = service.edits().listings().update(
            editId=edit_id, packageName=package_name, language=language,
            body={'fullDescription': description,
                'shortDescription': shortDescription,
                'title': title}).execute()

        print ('Listing for language %s was updated.' % listing_response_us['language'])

        commit_request = service.edits().commit(editId=edit_id, packageName=package_name).execute()

        print 'Edit "%s" has been committed' % (commit_request['id'])

    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the application to re-authorize')

def sendDescriptionToDeliver(package_name, language, title, shortDescription, description, whatsNew):
    directory = "deliver-player/metadata"
    if appName == "com.musescore.playerlite":
        directory = "deliver-playerlite/metadata"
    directory += "/" + language

    fNameTitle = directory + "/title.txt"
    with open(fNameTitle, 'w') as f:
        f.write(title)
    
    fNameDescription = directory + "/description.txt"
    with open(fNameDescription, 'w') as f:
        f.write(description)

    fNameWhatsNew = directory + "/version_whats_new.txt"
    with open(fNameWhatsNew, 'w') as f:
        f.write(whatsNew)
        

android = { "en": ["en-US"], "nl": ["nl-NL"], "fr": ["fr-FR"], "de": ["de-DE"], "it": ["it-IT"], "ja": ["ja-JP"], "es": ["es-419", "es-ES"], "cs": ["cs-CZ"], "pt_BR": ["pt-BR"]}
ios = { "en": ["en-US"], "nl": ["nl-NL"], "fr": ["fr-FR"], "de": ["de-DE"], "it": ["it-IT"], "ja": ["ja-JP"], "es": ["es-ES"], "pt_BR": ["pt-BR"]}

#android or ios
os = "android" 
languages = android if (os == "android") else ios

# free or paid
appNames = ["com.musescore.playerlite", "com.musescore.player"]

for appName in appNames:
    for language in languages.keys():
        languagesAppStore = languages[language]
        for languageAppStore in languagesAppStore:
            info = extractDescription(language, os, appName)
            #if (os == "android"):
            #    changeDescriptionAndroid(appName, languageAppStore, info['title'], info['shortDescription'], info['description'])
            #else:
            #    sendDescriptionToDeliver(appName, languageAppStore, info['title'], info['shortDescription'], info['description'], info['whatsNew'])

