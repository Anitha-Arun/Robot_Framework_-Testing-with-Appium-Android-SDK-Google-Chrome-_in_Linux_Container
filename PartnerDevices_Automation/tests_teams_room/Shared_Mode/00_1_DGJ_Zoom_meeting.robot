*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Test Cases ***
TC1:[Meeting Id] Disable Zoom in meeting settings
    [Tags]   454371     P0      exclude_ftp_sm
    [Setup]    Testcase Setup for Meeting User   count=1
    verify that third party meetings is Disabled default    device=device_1
    Verify the join by id on home seceen when zoom meeting toggle is disabled      device=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC2:[DGJ]DUT user should have option to enable Zoom meeting
    [Tags]   327955      bvt_sm   sanity_sm     exclude_ftp_sm
    [Setup]    Testcase Setup for Meeting User   count=1
    DUT user should have option to enable Zoom meeting    device=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

verify that third party meetings is Disabled default
    [Arguments]     ${device}
    Navigate to app settings page     ${device}
    navigate to meetings option in device settings page      ${device}
    verify third party zoom meetings toggle disable default   ${device}
    Come back from admin settings page    device_list=${device}

DUT user should have option to enable Zoom meeting
    [Arguments]     ${device}
    Navigate to app settings page     ${device}
    navigate to meetings option in device settings page      ${device}
    Enable and disable third party meetings zoom toggle  ${device}  state=on
    click back    ${device}
    Enable and disable third party meetings zoom toggle  ${device}  state=off
    Come back from admin settings page    device_list=${device}
