### Settings for Mythic Login & C2 Settings
### Change from Defaults to match your desired settings

# Mythic Settings
mythic_username = "mythic_admin"
mythic_password = "mythic_password"
mythic_server_ip = "172.16.113.149"
mythic_server_port = "7443"
mythic_ssl = True

# C2 Settings HTTP
mythic_http_callback_host = f"http://{mythic_server_ip}"
mythic_http_callback_interval = 4
mythic_http_callback_port = 80
mythic_http_callback_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
}
mythic_http_callback_killdate = 365  # number of days from now
mythic_http_callback_query_name = "q"
mythic_http_callback_get_uri = "index"
mythic_http_callback_post_uri = "data"
mythic_http_callback_encryption_type = "aes256_hmac"
mythic_http_callback_encrypted_key_exchange = True

# C2 Settings Websocket / Leviathan 
mythic_ws_callback_host = f"ws://192.168.100.200"
mythic_ws_callback_interval = 4
mythic_ws_callback_port = 8081

### Leviathan / Payload Host Server (Webloc/MobileConfig)

# Mobile Config
mythic_update_url = f"http://{mythic_server_ip}/manifest.xml"
mythic_extension_file = f"http://{mythic_server_ip}/extension.crx"

# Webloc
mythic_bookmark_link = f"http://{mythic_server_ip}/simple.pkg"

# Office Payload URL
mythic_payload_url = f"http://{mythic_server_ip}"

# Office Payload URL
mythic_dlopendylib_payload = f"http://{mythic_server_ip}/dlopen.dylib"
mythic_tcldylib_payload = f"http://{mythic_server_ip}/tclconfig.dylib"
