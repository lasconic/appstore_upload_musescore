from apiclient import sample_tools
from oauth2client import client
from os.path import expanduser

home = expanduser("~")
descriptionPath = home + "/player-qt/promotion"


# extract description, short description, etc... from player checkout
def extractDescription(language, appName):
    fname = descriptionPath + "/" + "description_" + language + ".txt"
    with open(fname) as f:
        content = f.readlines()

    inFree = False
    inWhatsNew = False
    whatsNew = ""
    for line in content:
        if line.startswith("-- APP 2"):
            inFree = True
            if appName != "com.musescore.playerlite":
                break
        if appName == "com.musescore.playerlite" and not inFree:
            continue
        if line.startswith("--- What"):
            inWhatsNew = True

        if line.startswith("--"):
            continue
        if inWhatsNew:
            whatsNew += line

    whatsNew = whatsNew.strip()

    print "-- What's New? --"
    print whatsNew
    return whatsNew

languages = { "en": ["en-US"], "nl": ["nl-NL"], "fr": ["fr-FR"], "de": ["de-DE"], "it": ["it-IT"], "ja": ["ja-JP"], "es": ["es-419", "es-ES"], "cs": ["cs-CZ"], "pt_BR": ["pt-BR"]}

# free or paid
#appNames = {"com.musescore.playerlite": "/Users/lasconic/Dropbox/Public/APK/mplayerlite-1.9-73.apk", 
#  "com.musescore.player" : "/Users/lasconic/Dropbox/Public/APK/mplayer-1.9-73.apk"}

appNames = {"com.musescore.playerlite": "/Users/lasconic/Dropbox/Public/APK/mplayerlite-1.9-73.apk"}

TRACK = "production"
for appName in appNames.keys():
    # Authenticate and construct service.
    myList = []
    service, flags = sample_tools.init(
      myList,
      'androidpublisher',
      'v2',
      __doc__,
      __file__, parents=[],
      scope='https://www.googleapis.com/auth/androidpublisher')

    # Process flags and read their values.
    package_name = appName
    apk_file = appNames[appName]

    try:
        edit_request = service.edits().insert(body={}, packageName=package_name)
        result = edit_request.execute()
        edit_id = result['id']

        apk_response = service.edits().apks().upload(
          editId=edit_id,
          packageName=package_name,
          media_body=apk_file).execute()

        print 'Version code %d has been uploaded' % apk_response['versionCode']

        track_response = service.edits().tracks().update(
          editId=edit_id,
          track=TRACK,
          packageName=package_name,
          body={u'versionCodes': [apk_response['versionCode']]}).execute()

        print 'Track %s is set for version code(s) %s' % (
          track_response['track'], str(track_response['versionCodes']))

        for language in languages.keys():
            whatsNew = extractDescription(language, appName)
            for l in languages[language]:
                listing_response = service.edits().apklistings().update(
                  editId=edit_id, packageName=package_name, language=l,
                  apkVersionCode=apk_response['versionCode'],
                  body={'recentChanges': whatsNew}).execute()

                print ('Listing for language %s was updated.'
                  % listing_response['language'])

        commit_request = service.edits().commit(
          editId=edit_id, packageName=package_name).execute()

        print 'Edit "%s" has been committed' % (commit_request['id'])

    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the '
          'application to re-authorize')