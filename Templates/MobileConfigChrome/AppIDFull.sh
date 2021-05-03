#!/bin/bash
openssl rsa -pubout -outform DER < /Users/student/Desktop/mystikal-D00MFist-dev/Payloads/MobileConfigChrome_Payload/temp/extension.pem | shasum -a 256 | head -c32 | tr 0-9a-f a-p > /Users/student/Desktop/mystikal-D00MFist-dev/Payloads/MobileConfigChrome_Payload/temp/AppIDValue
