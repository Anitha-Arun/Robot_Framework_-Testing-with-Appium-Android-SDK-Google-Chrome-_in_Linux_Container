*** Settings ***
Resource    ../resources/keywords/common.robot

*** Keywords ***
Verify home screen page
    [Arguments]     ${device}
    verify_home_screen_tiles    ${device}
    verify_home_screen_time_dates    ${device}

Verify device setting page from Home Screen enable page and come back
    [Arguments]     ${device}
    Navigate to device setting page from Home Screen enable page    ${device}
    Device setting back     ${device}
    Come back to home screen    ${device}

Navigate to calls tab from home screen
    [Arguments]     ${device}
    navigate_calls_tab_from_home_screen    ${device}
