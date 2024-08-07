*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  3
${action_time} =  5

*** Test Cases ***
TC1:[HDMI]Verify DUT user is not getting HDMI option in meeting when disabled from General settings
    [Tags]     344615        P1         sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    navigate to teams admin settings page   device=device_1
    Enable and disable hdmi content sharing     device=device_1     state=off
    Come back from admin settings page     device_list=device_1
    Join Meeting    device=device_1           meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1         state=Connected
    verify share content hdmi is not present    device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure     AND     disable hdmi content sharing   device=device_1   AND     Come back to home screen    device_list=device_1


*** Keywords ***
navigate to teams admin settings page
    [Arguments]    ${device}
    Click on more option   ${device}
    Click on settings page   ${device}
    Navigate to meetings option in device settings page      ${device}

Navigate back from the device settings page
    [Arguments]     ${device}
    Click close btn    device_list=${device}
    device setting back     ${device}
    device setting back     ${device}
    Click close btn    device_list=${device}

disable hdmi content sharing
    [Arguments]     ${device}
    navigate to teams admin settings page      ${device}
    Enable and disable hdmi content sharing     device=device_1     state=on
    Come back from admin settings page      device_list=${device}
