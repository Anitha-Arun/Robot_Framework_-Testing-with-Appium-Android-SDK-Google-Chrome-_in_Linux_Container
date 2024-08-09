*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  10
${wait_for_time} =  5

*** Test Cases ***
TC1: [Home screen] User to check for the volume button
    [Tags]      304007  P1
    [Setup]  Testcase Setup for Meeting User     count=1
    Navigate to app settings  device=device_1
    Adjust volume button  device=device_1   state=UP
    Adjust volume button  device=device_1   state=Down
    Dismiss the popup screen       device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1

TC2: [Home screen] DUT displays the current time on the screen
    [Tags]  313022   P2
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify current time display on home screen    device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1

TC3: [Home screen] User to verify the DPI set on the device
    [Tags]  237947  bvt_sm   sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify dp set on device  device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1

TC4: [Home screen] Check Teams App supports 1080p UI
    [Tags]   237946    bvt_sm  sanity_sm    smoke_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Check teams app supported UI   device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen   device_list=device_1

TC5: [Home screen] DUT on the home screen to display current meeting or next upcoming meeting
    [Tags]      304006    bvt_sm      sanity_sm     smoke_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify current or upcoming meetings displays on home screen      device=device_1
    Verify user details present on landing page   device=device_1:meeting_user
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen   device_list=device_1

TC6: [Home screen] User checks ellipsis on the home screen
    [Tags]      304008      P1
    [Setup]  Testcase Setup for Meeting User   count=1
    User check Ellipsis options On Home Screen    device=device_1
    [Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

TC7: [Home screen] Home screen display
     [Tags]      304130      P2
    [Setup]  Testcase Setup for Meeting User   count=1
    Verify home page screen    device=device_1
    [Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

TC8: [Home screen] Multiple meetings are scheduled at the same time slot
     [Tags]      312858     P2
    [Setup]  Testcase Setup for Meeting User   count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC9: [Home screen] No upcoming meetings
    [Documentation]  Precondition delete meetings and run separately
    [Tags]      304132    P1
    [Setup]  Testcase Setup for Meeting User   count=1
    Verify no meeting schedule on landing page    device=device_1
    [Teardown]   Run Keywords   Capture on Failure  AND   Come back to home screen     device_list=device_1

TC10: [Home UI] Verify the Home screen of the DUT screen.
	[Tags]    452222    P0
	[Setup]    Testcase Setup for Meeting User   count=1
	Verify home page screen    device=device_1
	verify user details present on landing page     device=device_1:meeting_user
	Verify the Help button functionality       device=device_1
    [Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

TC11: [Home UI] Verify the options once user taps on More from the DUT Home screen
	[Tags]    452223    P0
	[Setup]    Testcase Setup for Meeting User   count=1
	Click on more option      device=device_1
	Verify more options     console=device_1
	Verify the Help button functionality       device=device_1
	[Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

TC12: [Home UI] Verify the Help button [?] functionality in DUT home screen.
	[Tags]    452224    P0
	[Setup]    Testcase Setup for Meeting User   count=1
	Verify the Help button functionality       device=device_1
	[Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

*** Keywords ***
User check Ellipsis options On Home Screen
    [Arguments]     ${device}
    Click on more option    ${device}
    Verify app settings options    ${device}
