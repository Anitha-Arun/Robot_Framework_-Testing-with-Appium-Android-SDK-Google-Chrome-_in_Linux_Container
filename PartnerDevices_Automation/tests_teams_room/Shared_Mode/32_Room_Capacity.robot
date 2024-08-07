*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  3
${action_time} =  5

*** Test Cases ***
TC1:[Room Capacity] Norden DUT to have Max room occupancy notification in Meetings
    [Tags]      303854      P1    sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    navigate to teams admin settings page   device=device_1
    verify Max room occupancy notification toggle in Meetings     device=device_1
    Come back from admin settings page     device_list=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


*** Keywords ***

navigate to teams admin settings page
    [Arguments]    ${device}
    Click on more option   device=device_1
    Click on settings page       device=device_1
    navigate to meetings option in device settings page      device=device_1

Navigate back from the device settings page
    [Arguments]     ${device}
    Click close btn    device_list=${device}
    device setting back     ${device}
    device setting back     ${device}
    Click close btn    device_list=${device}

verify Max room occupancy notification toggle in Meetings
    [Arguments]     ${device}
    enable and disable the max room occupancy notification toggle button      ${device}   state=off
    enable and disable the max room occupancy notification toggle button  ${device}   state=on
