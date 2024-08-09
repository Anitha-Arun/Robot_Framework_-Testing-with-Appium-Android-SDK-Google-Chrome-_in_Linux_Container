*** Settings ***
Documentation   Meeting created as prerequisite before test execution make sure that  Webex meeting is created
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

Suite Setup         Enable third party webex meetings
Suite Teardown    Run Keywords   Suite Failure Capture    AND   Disable third party meetings    device=device_1


*** Variables ***
${wait_time} =  3
${action_time} =  5

*** Test Cases ***

TC1:[DGJ]Webex Meeting Should be displayed in Home screen
    [Tags]     445043        bvt_sm       sanity_sm     exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify Webex Meeting Should be displayed in Home screen
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC2:[DGJ]DUT user should be able to join Webex Meeting from Teams
    [Tags]     445044        bvt_sm       sanity_sm     exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Join Meeting    device=device_1      meeting=webex_meeting
    Wait for Some Time    time=${action_time}
    Verify meeting state   device_list=device_1     state=Connected
    verify the docked ubar when third party meeting joins    device=device_1        meetting_mode=webex
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC3:[DGJ]DUT user should be able to join Webex Meeting from Teams and See call control options
    [Tags]     328329        bvt_sm       sanity_sm     exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Join Meeting    device=device_1      meeting=webex_meeting
    Wait for Some Time    time=${action_time}
    Verify meeting state   device_list=device_1     state=Connected
    verify the docked ubar when third party meeting joins    device=device_1        meetting_mode=webex
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC4:[DGJ]Webex icon should be displayed for the meeting created with Webex Link on Calendar
     [Tags]    445051      bvt_sm       sanity_sm       exclude_ftp_sm
     [Setup]  Testcase Setup for Meeting User     count=1
    Verify meeting display on home screen     device=device_1
    verify webex icon on calendar tab     device=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


TC5:[DGJ webex]DUT user Video should be enabled by default while Joining the meeting
     [Tags]        445046      bvt_sm       sanity_sm       exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Join Meeting    device=device_1      meeting=webex_meeting
    Wait for Some Time    time=${action_time}
    Verify meeting state   device_list=device_1     state=Connected
    Check video call On state   device_list=device_1
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1



*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   device=device_1
    Click on settings page   device=device_1

Enable third party webex meetings
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    Enable and disable third party meetings webex toggle    device=device_1     state=on
    Come back from admin settings page    device_list=device_1

Verify Webex Meeting Should be displayed in Home screen
    Join Meeting    device=device_1     meeting=webex_meeting
    Wait for Some Time    time=${action_time}
    Verify meeting state   device_list=device_1     state=Connected
    End meeting     device=device_1

Disable third party meetings
    [Arguments]     ${device}
    Navigate to app settings page     ${device}
    navigate to meetings option in device settings page      ${device}
    Enable and disable third party meetings webex toggle    device=device_1       state=off
    Come back from admin settings page    device_list=${device}
