*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  3
${action_time} =  5

*** Test Cases ***
TC1:[Norden][Wallpaper Theme]Verify Wallpapers is available under Admin Settings for shared accounts
    [Tags]     303470      bvt_sm     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    navigate to teams admin settings page   device=device_1
    verify wallpaper page in teams admin setting    device=device_1
    Click close btn     device_list=device_1
	come back from admin settings page  device_list=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}
navigate to teams admin settings page
    [Arguments]    ${device}
    Navigate to app settings page    ${device}
    navigate to teams admin settings      ${device}


