*** Settings ***
Documentation   Meeting created as prerequisite before test execution make sure that  Webex meeting is created
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Test Cases ***
TC1:[DGJ]DUT user should have option to enable Webex meeting
    [Tags]     328326        bvt_sm       sanity_sm     exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    DUT user should have option to enable Webex meeting     device=device_1  state=off
    Come back from admin settings page    device_list=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   device=device_1
    Click on settings page   device=device_1

DUT user should have option to enable Webex meeting
    [Arguments]       ${device}   ${state}
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    Enable and disable third party meetings webex toggle    device=device_1     state=off
    Come back from admin settings page    device_list=device_1