*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  3
${action_time} =  5

*** Test Cases ***
TC1:[Automatic Framing] Verify the Room Cemara under the Teams App Settings.
    [Tags]      381002      bvt_sm     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    navigate to teams admin settings page   device=device_1
    verify the room camera under the teams app settings     device=device_1
    Come back from admin settings page     device_list=device_1
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

Navigate back from the device settings page
    [Arguments]     ${device}
    device setting back     ${device}
    device setting back     ${device}
    come back to home screen  ${device}
