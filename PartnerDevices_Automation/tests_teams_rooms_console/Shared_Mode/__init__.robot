*** Settings ***
Resource    ../../resources/keywords/common.robot
Suite Setup    Teams Console Setup For Shared Mode


*** Variables ***


*** Keywords ***
Teams Console Setup For Shared Mode
    Sign Out Console
    Sign Out
    Sign In    user_list=meeting_user,user,user
    Sign In Console    user_list=meeting_user
    Get device pairing code    device_list=device_1    console_list=console_1     user_list=meeting_user
