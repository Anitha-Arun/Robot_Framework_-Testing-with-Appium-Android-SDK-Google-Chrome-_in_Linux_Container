*** Settings ***
Library     tr_app_settings_keywords
Library     tr_settings_keywords
Library    tr_device_settings_keywords
Library   settings_keywords
Resource    ../resources/keywords/common.robot

*** Keywords ***
Enable proximity join button
    [Arguments]     ${device}
    Select proximity join button  device_list=${device}   state=ON

Disable proximity join button
    [Arguments]     ${device}
    Select proximity join button  device_list=${device}   state=OFF

Validate different options inside settings page
    [Arguments]     ${device}
    Click on settings page    ${device}
    Verify option inside settings page  ${device}
    Click close btn    device_list=${device}