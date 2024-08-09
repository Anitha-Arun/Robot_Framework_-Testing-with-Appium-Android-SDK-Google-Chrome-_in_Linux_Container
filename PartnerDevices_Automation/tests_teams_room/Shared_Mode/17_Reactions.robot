*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***

*** Test Cases ***
TC1 : [Reactions] Verify that reaction is visible on main stage when DUT user video ON
    [Tags]  303239      P1
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify video preview on screen      device=device_1,device_2
    Verify reactions buttons in call control     device=device_2
    Tap on like button     device=device_2
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC2 : [Reactions]Verify a reaction window should be shown
    [Tags]  303238      P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify docked ubar  device_list=device_1
    verify reactions buttons in call control     device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC3 : [Reactions] DUT user to verify the reaction of TDC user when TDC user is displayed on the main stage
    [Tags]      303630      P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify reactions buttons in call control     device=device_2
    tap on heart button      device=device_2
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC4 :[Reactions]Extra call control must not be displayed in meeting
    [Tags]     313235     P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_1,device_2,device_3   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Verify docked ubar  device_list=device_1
    verify reactions buttons in call control     device=device_2
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC5 :[Reactions]Observe reactions when DUT rejoins the meeting
     [Tags]     316631     P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_1,device_2,device_3   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    End meeting     device=device_1
    Join meeting   device=device_1      meeting=cnf_device_meeting
    tap on heart button     device=device_1
    verify reaction on screen    device=device_2
    tap on laugh button     device=device_2
    verify reaction on screen     device=device_3
    tap on clap button      device=device_3
    verify reaction on screen     device=device_2
    click like button    device=device_1
    verify reaction on screen    device=device_3
    End meeting     device=device_1,device_2,device_3
    Verify meeting state   device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC6 :[Reactions]DUT should be able to lower hand itself
    [Tags]  316634    P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_1,device_2,device_3   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    select raise hand option    device=device_1
    verify raise hand reaction  device=device_1
    lower hand  device=device_1
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC7 :[Reactions]TDC should be able to lower hand of DUT
     [Tags]  316636    P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_1,device_2,device_3   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    select raise hand option    device=device_3
    verify raise hand reaction  device=device_3
    lower the raised hand from another user     from_device=device_1   to_device=device_3
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC8 : [Reactions] Verify that reaction is visible at Avtar when video is not ON
    [Tags]      303240      bvt_sm  sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify video preview on screen      device=device_1,device_2
    Disable video call      device=device_2
    Check video call Off state      device_list=device_2
    Verify reactions buttons in call control     device=device_1
    Verify reactions visible on screen after taping     from_device=device_1       to_device=device_2
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC9: [Reactions]In all flavors, When the user pressed any reaction, the reaction window shown should be dismissed
     [Tags]  303960     P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_1,device_2,device_3   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    tap on heart button     device=device_1
    verify reaction on screen    device=device_2
    verify reaction window will dissmiss    device=device_1
    End meeting     device=device_1,device_2,device_3
    Verify meeting state     device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC10: [Reactions] Raise hand should not be displayed separately when reactions button is available in docked ubar
    [Tags]   303624     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2   meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify reactions buttons in call control     device=device_1
    tap on heart button     device=device_1
    verify reaction on screen    device=device_2
    verify raise hand should not be displayed on dockedubar  device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state     device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC11 :[Reactions] DUT user to verify the raise hand feature from reactions window
     [Tags]  303626    P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2   meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify reactions buttons in call control     device=device_1
    select raise hand option    device=device_1
    verify raise hand reaction  device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC12 :[Reactions] Reactions invoked by the user should be shown in the local preview
     [Tags]     303627     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2   meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    tap on heart button     device=device_1
    verify reaction on screen    device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state   device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC13:[Reaction] User to verify the show/hide behavior of call control bar
    [Tags]      303632     P1       sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify docked ubar  device_list=device_1
    verify reactions buttons in call control     device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC14:[Reactions] User to verify the reactions when the user is displayed on the main stage of TDC user
    [Tags]      303628     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    make a spotlight   from_device=device_2   to_device=device_1:meeting_user
    verify spotlight text on device   device=device_1   text=spotlight
    Close participants screen   device=device_2
    Verify docked ubar  device_list=device_1
    verify reactions buttons in call control     device=device_1
    tap on heart button     device=device_1
    verify reaction on screen    device=device_2
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


*** Keywords ***
Verify docked ubar
     [Arguments]    ${device_list}
     verify call control bar   ${device_list}

Verify reactions visible on screen after taping
    [Arguments]       ${from_device}        ${to_device}
    Click like button     ${from_device}
    Verify reaction button on screen after tap on it   ${to_device}
    Tap on laugh button     ${from_device}
    Verify reaction button on screen after tap on it        ${to_device}
    Tap on clap button     ${from_device}
    Verify reaction button on screen after tap on it       ${to_device}
    Tap on heart button     ${from_device}
    Verify reaction button on screen after tap on it   ${to_device}
    Verify and select raise hand option  ${from_device}
    Verify raise hand notification   ${to_device}
    Verify and select lower hand option  ${from_device}
