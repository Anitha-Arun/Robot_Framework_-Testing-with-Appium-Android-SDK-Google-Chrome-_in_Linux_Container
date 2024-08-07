*** Settings ***
Resource    ../resources/keywords/common.robot

*** Keywords ***
Verify HD timeout
    [Arguments]     ${device}
    Verify hot desking mode  ${device}

Validate username after signed out from settings page
     [Arguments]     ${device}
     Validate username after signed out from hot desking     ${device}


Sign out from settings page
    [Arguments]     ${device}
    sign out from HD mode    ${device}