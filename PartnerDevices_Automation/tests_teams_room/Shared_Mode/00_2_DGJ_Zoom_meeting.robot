*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

Suite Setup         Enable third party meetings
Suite Teardown    Run Keywords   Suite Failure Capture    AND   Disable third party meetings    device=device_1

*** Variables ***

*** Test Cases ***
TC1:[Meeting ID] Join Zoom meeting successfully
    [Tags]   454369     P0      exclude_ftp_sm
    [Setup]    Testcase Setup for Meeting User   count=1
    verify join with an meeting id options after enabling third party meetings      device=device_1
    join with an meeting id   device=device_1   meeting_type=zoom
    Verify meeting state   device_list=device_1    state=Connected
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


TC2:[Meeting Id] Verify Teams Enter code working
    [Tags]   454372     P0      exclude_ftp_sm
    [Setup]    Testcase Setup for Meeting User   count=1
    join with an meeting id   device=device_1
    Verify meeting state   device_list=device_1    state=Connected
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC3:[Meeting ID] Join Zoom meeting with incorrect meeting detail
    [Tags]   454370    P1       exclude_ftp_sm
    [Setup]    Testcase Setup for Meeting User   count=1
    Verify join meeting with incorrect meeting detail   device=device_1     meeting_type=zoom
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC4:[DGJ]Zoom Meeting Should be displayed in Home screen
    [Tags]   327956     bvt_sm   sanity_sm      exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify meeting display on home screen     device=device_1
    Zoom Meeting Should be displayed in Home screen
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC5:[DGJ]DUT user should be able to join Zoom Meeting from Teams
    [Tags]  327957    bvt_sm   sanity_sm        exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1    meeting=zoom_meeting
    Verify meeting state   device_list=device_1    state=Connected
    End meeting      device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC6: [DGJ]In Zoom Meeting Both Call Controls should be in SYNC
    [Tags]      327960   bvt_sm   sanity_sm     exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1    meeting=zoom_meeting
    Verify meeting state   device_list=device_1    state=Connected
    verify the docked ubar when third party meeting joins    device=device_1
    verify third party meeting both call controls should be in sync     device=device_1     mute_state=mute     video_state=off
    verify third party meeting both call controls should be in sync     device=device_1     mute_state=unmute    video_state=on
    End meeting      device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


TC8:[DGJ]DUT user should be able to join Zoom Meeting from Teams and See call control options
    [Tags]      327958   P1     sanity_sm   exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1     meeting=zoom_meeting
    Verify meeting state   device_list=device_1    state=Connected
    verify the docked ubar when third party meeting joins    device=device_1
    End meeting      device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


TC9:[DGJ zoom]DUT user Video should be enabled by default while Joining the meeting
    [Tags]     327961      P1         sanity_sm     exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1      meeting=zoom_meeting
    Verify meeting state   device_list=device_1    state=Connected
    verify video should be enabled by default while Joining the meeting   device=device_1
    End meeting      device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


TC10:[DGJ]DUT user Mute and unmute during Zoom Meeting
    [Tags]      327967   P1  sanity_sm      exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1    meeting=zoom_meeting
    Verify meeting state   device_list=device_1    state=Connected
    verify the docked ubar when third party meeting joins    device=device_1
    verify third party meeting both call controls should be in sync     device=device_1     mute_state=mute     video_state=off
    verify third party meeting both call controls should be in sync     device=device_1     mute_state=unmute    video_state=on
    End meeting      device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


TC11:[DGJ]Zoom icon should be displayed for the meeting created with Zoom Link on Calendar
    [Tags]      327973     P1   sanity_sm       exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify meeting display on home screen     device=device_1
    verify zoom icon on calendar tab     device=device_1
    Zoom Meeting Should be displayed in Home screen
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


TC12:[DGJ]DUT should display connecting screen with Cancel button
    [Tags]      345686     P1   sanity_sm       exclude_ftp_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify meeting display on home screen     device=device_1
    verify connecting screen with Cancel button when we join the meeting
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

Enable third party meetings
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    Enable and disable third party meetings zoom toggle  device=device_1    state=on
    Come back from admin settings page    device_list=device_1

Disable third party meetings
    [Arguments]     ${device}
    Navigate to app settings page     ${device}
    navigate to meetings option in device settings page      ${device}
    Enable and disable third party meetings zoom toggle   ${device}    state=off
    Come back from admin settings page    device_list=${device}

Zoom Meeting Should be displayed in Home screen
    Join meeting   device=device_1    meeting=zoom_meeting
    Verify meeting state   device_list=device_1    state=Connected
    End meeting      device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected

verify connecting screen with Cancel button when we join the meeting
    Join meeting   device=device_1    meeting=zoom_meeting   dgj=true
    Verify meeting state   device_list=device_1    state=Connected
    End meeting      device=device_1

