*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Test Cases ***
#TC1: [Admin Settings] DUT to have "Calling" options to customize incoming calls in settings.
#    [Tags]  237873   p1
#    [Setup]    Testcase Setup for Meeting User   count=1
#    Navigate to app settings page  device=device_1
#    navigate calling option  device=device_1
#    verify options in device settings calling    device=device_1
#    device setting back  device=device_1
#    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1

TC2: [Admin Settings]Microsoft Teams device Admin Only settings are password protected
     [Tags]  237642   bvt_sm    sanity_sm   
    [Setup]    Testcase Setup for Meeting User   count=1
    Navigate to app settings page  device=device_1
    Teams device Admin settings are password protected     device=device_1
    come back from admin settings page  device_list=device_1
    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1


TC3:[Admin Settings] DUT user verify Protected apps are available under Admin settings for Shared account
     [Tags]  303547     P2
    [Setup]    Testcase Setup for Meeting User   count=1
    Navigate to app settings page  device=device_1
    navigate to teams admin settings     device=device_1
    verify protected apps are available under admin settings    device=device_1
    device setting back  device=device_1
    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1

TC4:[Admin Settings] User to have admin sign-out option behind admin settings.
    [Tags]      409967     P2
    [Setup]    Testcase Setup for Meeting User   count=1
    Navigate to app settings page  device=device_1
    navigate to teams admin settings     device=device_1
    verify admin sign-out option behind admin settings       device=device_1
    Navigate back from the device settings page  device=device_1
    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1


*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

navigate calling option
    [Arguments]       ${device}
    navigate to teams admin settings   ${device}
    verify calling option in device settings page     ${device}

Teams device Admin settings are password protected
   [Arguments]       ${device}
   navigate to teams admin settings   ${device}

verify admin sign-out option behind admin settings
    [Arguments]       ${device}
    verify protected apps are available under admin settings    ${device}

Navigate back from the device settings page
    [Arguments]     ${device}
    Click close btn    device_list=${device}
    device setting back     ${device}
    device setting back     ${device}
    Click close btn    device_list=${device}
