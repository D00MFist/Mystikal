### Settings for Mythic Login & C2 Settings
### Change from Defaults to match your desired settings

# Mythic Settings
mythic_username="mythic_admin"
mythic_password="mythic_pass"
mythic_server_ip="172.16.113.149"
mythic_server_port="7443"
mythic_ssl=True

# C2 Settings HTTP
mythic_http_callback_host="http://172.16.113.149"
mythic_http_callback_interval=4
mythic_http_callback_port=80

# C2 Settings Websocket / Leviathan 
mythic_ws_callback_host="ws://192.168.100.200"
mythic_ws_callback_interval=4
mythic_ws_callback_port=8081

### Leviathan / Payload Host Server (Webloc/MobileConfig)

# Mobile Config
mythic_update_url="http://172.16.113.141/manifest.xml"
mythic_extension_file="http://172.16.113.141/extension.crx"

# Webloc
mythic_bookmark_link="http://172.16.113.141/simple.pkg"

# Office Payload URL
mythic_payload_url="http://172.16.113.141"

# Office Payload URL
mythic_dlopendylib_payload="http://172.16.113.141/dlopen.dylib"
mythic_tcldylib_payload="http://172.16.113.141/tclconfig.dylib"