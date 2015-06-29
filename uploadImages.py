from apiclient import sample_tools
from oauth2client import client
from os.path import expanduser
import os
import fnmatch

languages = { "en": ["en-US"], "nl": ["nl-NL"], "fr": ["fr-FR"], "de": ["de-DE"], "it": ["it-IT"], "ja": ["ja-JP"], "es": ["es-419", "es-ES"], "cs": ["cs-CZ"], "pt_BR": ["pt-BR"]}
#languages = { "en": ["en-US"] }

# free or paid
#appNames = {"com.musescore.playerlite", "com.musescore.player" ]

appNames = ["com.musescore.player"]

imageTypes = ["phoneScreenshots", "sevenInchScreenshots", "tenInchScreenshots"]

for appName in appNames:
    if appName == "com.musescore.playerlite":
        screenDir = "./android_screenshot/playerlite"
    else:
        screenDir = "./android_screenshot/player"
    myList = []
    # Authenticate and construct service.
    service, flags = sample_tools.init(
      myList,
      'androidpublisher',
      'v2',
      __doc__,
      __file__, parents=[],
      scope='https://www.googleapis.com/auth/androidpublisher')
    package_name = appName
    try:
        edit_request = service.edits().insert(body={}, packageName=package_name)
        result = edit_request.execute()
        edit_id = result['id']

        for language in languages.keys():
            for l in languages[language]:
                for imageType in imageTypes:
                    deleteall_response = service.edits().images().deleteall(
                      editId=edit_id, packageName=package_name, language=l, imageType=imageType
                      ).execute()

                    print ('Delete all images for language %s in %s' % (l, imageType))
                    languageDir = screenDir + "/" + l
                    for file in os.listdir(languageDir):
                        if fnmatch.fnmatch(file, '*.png') and imageType in file:
                            filePath = languageDir + "/" + file
                            add_image = service.edits().images().upload(
                              editId=edit_id, packageName=package_name, language=l, imageType=imageType,
                              media_body=filePath).execute()
                            print '--> Add "%s"' % (filePath)

        commit_request = service.edits().commit(editId=edit_id, packageName=package_name).execute()

        print 'Edit "%s" has been committed' % (commit_request['id'])

    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the application to re-authorize')