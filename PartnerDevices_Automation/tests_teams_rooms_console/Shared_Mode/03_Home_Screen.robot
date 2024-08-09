*** Settings ***
Documentation   Validating the functionality of console Home Screen feature.
Force Tags    sm_home_screen    sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Home screen] User to check for the volume button
     [Tags]  314970        sanity_sm  P1
     [Setup]   Testcase Setup for shared User     count=1
     Tap on more option  console=console_1
     Verify functionality of volume button    console=console_1   button=UP
     Verify functionality of volume button    console=console_1   button=Down
     [Teardown]   Run Keywords    Capture Failure  AND    Test Case Teardown    console=console_1

TC2: [Home screen]Touch Console displays the current time on the screen
    [Tags]      314976  P1
    [Setup]   Testcase Setup for shared User     count=1
    Verify time display on home screen   console=console_1
    [Teardown]   Run Keywords    Capture Failure

TC3: [Home screen]User to verify the DPI set on the device
    [Tags]  314962      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User     count=1
    Verify dpi set on device  console=console_1
    Verify dp set on device  device=device_1
    [Teardown]  Run Keywords    Capture Failure      AND     Come back to home screen page   console_list=console_1

TC4: [Home screen] Verify DUT supports1080p UI
    [Tags]   314960     bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User     count=1
    Check app supported UI      console=console_1
    Check teams app supported UI   device=device_1
    [Teardown]   Run Keywords    Capture Failure    AND       Come back to home screen page   console_list=console_1

TC5: [Home screen] User checks ellipsis on the Touch Console home screen
    [Tags]  314972  P1
    [Setup]  Testcase Setup for shared User     count=1
    Validate ellipsis options on homescreen     console=console_1
    [Teardown]  Run Keywords    Capture Failure  AND    Test Case Teardown    console=console_1

TC6: [Home screen] Multiple meetings are scheduled at the same time slot on Touch console
    [Tags]      314966     P2
    [Setup]  Testcase Setup for shared User     count=1
    Verify meeting display on home page     console=console_1
    Join a meeting   console=console_1      meeting=rooms_console_meeting
    Verify for call state     console_list=console_1      state=Connected
    End the meeting     console=console_1
    Verify for call state    console_list=console_1      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1

TC7:[Home screen] Home screen display
    [Tags]      322933      P2
    [Setup]  Testcase Setup for shared User     count=1
    Validate user details along with home screen options    console=console_1:meeting_user
    [Teardown]   Run Keywords    Capture Failure    AND       Come back to home screen page   console_list=console_1

TC8:[Home Screen] Verify the Aspects Ratio of the display
    [Tags]   322363     P2
    [Setup]  Testcase Setup for shared User     count=1
    Verify display aspect ratio     console=console_1       device=device_1
    [Teardown]   Run Keywords    Capture Failure    AND       Come back to home screen page   console_list=console_1

TC9:[Home UI] Verify the Home screen of the Touch console screen.
	[Tags]    452043    P0      bvt_sm      sanity_sm
	[Setup]  Testcase Setup for shared User     count=1
	Verify date and time with user details on home screen       console=console_1:meeting_user
	Verify user options on home screen       console=console_1
    [Teardown]   Run Keywords    Capture Failure    AND       Come back to home screen page   console_list=console_1

TC10:[Home UI] Verify the options once user taps on More option from Touch console Home screen
	[Tags]    452044    P0      bvt_sm      sanity_sm
	[Setup]  Testcase Setup for shared User     count=1
	Tap on more option  console=console_1
    Verify more options     console=console_1
	[Teardown]   Run Keywords    Capture Failure    AND     Test Case Teardown      console=console_1

*** Keywords ***
Test Case Teardown
    [Arguments]     ${console}
    Click on back layout btn   ${console}
    Come back to home screen page   console_list=${console}

Validate ellipsis options on homescreen
    [Arguments]     ${console}
    Verify available options in more    ${console}

End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

Verify display aspect ratio
     [Arguments]    ${console}    ${device}
     Check app supported UI     ${console}
     Check teams app supported UI   ${device}

