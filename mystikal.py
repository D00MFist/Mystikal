#!/usr/bin/python3
import sys
from pathlib import Path
from Modules.Installer_Package import *
from Modules.Installer_Package_Python import *
from Modules.Installer_Package_with_LD import *
from Modules.Installer_Plugins import *
from Modules.Installer_JS import *
from Modules.Installer_JS_Script import *
from Modules.Mobile import *
from Modules.Webloc import *
from Modules.Macro_Word import *
from Modules.Macro_Excel import *
from Modules.Macro_PowerPoint import *
from Modules.Macro_SYLK_Excel import *
from Modules.DMG import *
from Modules.PDF import *

print("""\
 _______               __   __ __           __
|   |   |.--.--.-----.|  |_|__|  |--.---.-.|  |
|       ||  |  |__ --||   _|  |    <|  _  ||  |
|__|_|__||___  |_____||____|__|__|__|___._||__|
         |_____|
""")

def main():
    print("Mystikal: macOS Initial Access Payload Generator")
    Path("./Payloads/").mkdir(parents=True, exist_ok=True)
    choice ='0'
    while choice =='0':
        print("Main Choice: Choose 1 of 8 choices")
        print("Choose 1 for Installer Packages")
        print("Choose 2 for Mobile Configuration: Chrome Extension")
        print("Choose 3 for Mobile Configuration: Webloc File")
        print("Choose 4 for Office Macros: VBA")
        print("Choose 5 for Office Macros: XLM Macros in SYLK Files")
        print("Choose 6 for Disk Images")
        print("Choose 7 for Armed PDFs")
        print("Choose 8 to exit")

        choice = input ("Please make a choice: ")

        if choice == "8":
            print("Exiting")         
            sys.exit(1)
        elif choice == "7":
            print("Selected Armed PDF")
            pdf()
        elif choice == "6":
            print("Selected Disk Images")
            dmg()
        elif choice == "5":
            print("Selected Office Macros: XLM Macros in SYLK Files")
            sylk_macros_excel()
        elif choice == "4":
            print("Selected Office Macros: VBA")
            office_macros_menu()
        elif choice == "3":
            print("Selected Mobile Configuration: Webloc File")
            mobile_webloc()
        elif choice == "2":
            print("Selected Mobile Configuration: Chrome Extension")
            mobile_ext()
        elif choice == "1":
            print("Selected Installer Packages")
            install_pkg_menu()
        else:
            print("*******Pick an option 1-8*******")
            main()

def install_pkg_menu():
    choice ='0'
    while choice =='0':
        print("SubMenu Choice: Choose 1 of 5 choices")
        print("Choose 1 for Installer Package w/ only preinstall script")
        print("Choose 2 for Installer Package w/ Launch Daemon for Persistence")
        print("Choose 3 for Installer Package w/ Installer Plugin")
        print("Choose 4 for Installer Package w/ JavaScript Functionality")
        print("Choose 5 for Installer Package w/ Dylib")
        print("Choose 6 to exit")

        choice = input ("Please make a choice: ")

        if choice == "6":
            sys.exit(1)
        elif choice == "5":
            print("Selected Installer Package w/ Dylib")
            install_pkg_py() 
        elif choice == "4":
            print("Selected Installer Package w/ JavaScript Functionality")
            pkg_js_menu() 
        elif choice == "3":
            install_plug() 
        elif choice == "2":
            install_pkg_with_LD()
        elif choice == "1":
            install_pkg()
        else:
            print("*******Pick an option 1-4*******")
            install_pkg_menu()

def office_macros_menu():
    choice ='0'
    while choice =='0':
        print("SubMenu Choice: Choose 1 of 4 choices")
        print("Choose 1 for VBA Macros for Word")
        print("Choose 2 for VBA Macros for Excel")
        print("Choose 3 for VBA Macros for PowerPoint")
        print("Choose 4 to exit")

        choice = input ("Please make a choice: ")

        if choice == "4":
            sys.exit(1)
        elif choice == "3":
            macro_powerpoint()
        elif choice == "2":
            macro_excel()
        elif choice == "1":
            macro_word()
        else:
            print("*******Pick an option 1-4*******")
            office_macros_menu()
            
def pkg_js_menu():
    choice ='0'
    while choice =='0':
        print("SubMenu Choice: Choose 1 of 3 choices")
        print("Choose 1 for Installer Package w/ JavaScript Functionality embedded")
        print("Choose 2 for Installer Package w/ JavaScript Functionality in Script")
        print("Choose 3 to exit")

        choice = input ("Please make a choice: ")

        if choice == "3":
            sys.exit(1)
        elif choice == "2":
            install_js_script() 
        elif choice == "1":
            install_js() 
        else:
            print("*******Pick an option 1-3*******")
            pkg_js_menu()

main()
