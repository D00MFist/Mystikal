# Mystikal
macOS Initial Access Payload Generator

## Usage: 
1. Install Xcode on build machine (Required for Installer Package w/ Installer Plugin)
2. Install python requirements
```
sudo pip3 install -r requirements.txt
```
3. Change settings within the `Settings/MythicSettings.py` file to match your Mythic configs
4. Run mystikal
```
python3 mystikal.py
```
5. Select your desired payload from the options
```
 _______               __   __ __           __
|   |   |.--.--.-----.|  |_|__|  |--.---.-.|  |
|       ||  |  |__ --||   _|  |    <|  _  ||  |
|__|_|__||___  |_____||____|__|__|__|___._||__|
         |_____|
         
Mystikal: macOS Payload Generator
Main Choice: Choose 1 of 8 choices
Choose 1 for Installer Packages
Choose 2 for Mobile Configuration: Chrome Extension
Choose 3 for Mobile Configuration: Webloc File
Choose 4 for Office Macros: VBA
Choose 5 for Office Macros: XLM Macros in SYLK Files
Choose 6 for Disk Images
Choose 7 for Armed PDFs
Choose 8 to exit
```
### Note: 
Option 1, Option 1.4, and Option 4 have submenus shown below
```
Selected Installer Packages
SubMenu: Choose 1 of 5 choices
Choose 1 for Installer Package w/ only pre/postinstall scripts
Choose 2 for Installer Package w/ Launch Daemon for Persistence
Choose 3 for Installer Package w/ Installer Plugin
Choose 4 for Installer Package w/ JavaScript Functionality
Choose 5 to exit

Selected Installer Package w/ JavaScript Functionality
SubMenu Choice: Choose 1 of 3 choices
Choose 1 for Installer Package w/ JavaScript Functionality embedded
Choose 2 for Installer Package w/ JavaScript Functionality in Script
Choose 3 to exit

Selected Office Macros: VBA
SubMenu Choice: Choose 1 of 4 choices
Choose 1 for VBA Macros for Word
Choose 2 for VBA Macros for Excel
Choose 3 for VBA Macros for PowerPoint
Choose 4 to exit
```
### Behavior Modifications: 
To change the execution behavior (which binaries are called upon payload execution)
- Modifications will be required in either the specific payload file under the `Modules` folder or the related template file under the `Templates` folder.
