*** Settings ***
Force Tags    15    reactions_sm     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***


*** Test Cases ***
TC1 : [Reactions] Verify that reaction is visible at Avtar when video is not ON
    [Tags]      322874      bvt     bvt_sm  sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Disable video call      device=device_2
    Check video call Off state      device_list=device_2
    Verify reactions options in call control bar     console=console_1
    Verify reactions visible on screen after taping     from_device=console_1       to_device=device_2
    End a meeting   console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2 : [Reactions] Verify that reaction is visible on main stage when Touch console user video ON
    [Tags]      322873  P1      sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify video preview on screen    device=device_1,device_2
    Verify reactions visible on screen after taping     from_device=device_2        to_device=device_1
    End a meeting   console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3 :[Reaction] User to verify the show/hide behavior of call control bar
    [Tags]     322883     P1
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant  console=console_1
    Verify docked ubar       console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC4 :[Reactions] Raise hand should not be displayed separately when reactions button is available in docked ubar
    [Tags]     322875     P1    sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant  console=console_1
    Verify reaction buttons in docked ubar       console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC5 :[Reactions]Verify a reaction window should be shown
    [Tags]  322872      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify docked ubar       console=console_1
    Verify reaction buttons in docked ubar       console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC6 :[Reactions] Touch console user to verify the raise hand feature from reactions window
    [Tags]  322877      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify docked ubar       console=console_1
    Verify reaction buttons in docked ubar       console=console_1
    Verify and select raise hand option  console=console_1
    Verify raise hand notification      device_list=device_2
    verify raise hand reaction  device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC7 :[Reactions]TDC should be able to lower hand of Touch console
    [Tags]  322890      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify docked ubar       console=console_1
    Verify reaction buttons in docked ubar       console=console_1
    Verify and select raise hand option  console=console_1
    Verify raise hand notification      device_list=device_2
    lower the raised hand from another user     from_device=device_2   to_device=console_1      device_type=console
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC8 :[Reactions] Touch console should be able to lower hand itself
    [Tags]  322889      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify docked ubar       console=console_1
    Verify reaction buttons in docked ubar       console=console_1
    Verify and select raise hand option  console=console_1
    Verify raise hand notification      device_list=device_2
    lower hand  device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC9 :[Reactions]Extra call control must not be displayed in meeting
    [Tags]  322886      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify docked ubar       console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1

TC10:[Reactions]In all flavors, When the user pressed any reaction, the reaction window shown should be dismissed
    [Tags]  322884      P2
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify docked ubar       console=console_1
    Verify reaction buttons in docked ubar       console=console_1
    Verify and select raise hand option  console=console_1
    Verify raise hand notification      device_list=device_2,device_3
    verify reaction window will dissmiss    device=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1      device_list=device_2,device_3

TC11:[Reactions] Reactions invoked by the user should be shown in the local preview
    [Tags]  322878      P2
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify docked ubar       console=console_1
    Verify reaction buttons in docked ubar       console=console_1
    Verify and select raise hand option  console=console_1
    Verify raise hand notification      device_list=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1      device_list=device_2,device_3

TC12:[Reactions] Touch console user to verify the reaction of TDC user when TDC user is displayed on the main stage
    [Tags]  322881      P2
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    verify device docked ubar  device_list=device_2
    verify reactions buttons in call control     device=device_2
    select raise hand option    device=device_2
    Verify raise hand notification      device_list=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1          device_list=device_2,device_3

TC13:[Reactions]Observe reactions when Touch console rejoins the meeting
    [Tags]  322888      P2
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    End the meeting         console=console_1
    Verify for call state    console_list=console_1     state=Disconnected
    Join a meeting   console=console_1          meeting=console_lock_meeting
    Verify for call state     console_list=console_1       state=Connected
    select raise hand option    device=device_2
    Verify raise hand notification      device_list=console_1
    select raise hand option    device=device_3
    Verify raise hand notification      device_list=console_1
    Verify docked ubar       console=console_1
    Verify reaction buttons in docked ubar       console=console_1
    Verify and select raise hand option  console=console_1
    Verify raise hand notification      device_list=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1      device_list=device_2,device_3

TC14:[Reactions] User to verify the reactions when the user is displayed on the main stage of TDC user
    [Tags]  322879      P2
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify docked ubar       console=console_1
    Make a spotlight   from_device=device_2   to_device=console_1:meeting_user      device_type=console
    verify spotlight text on device   device=console_1     text=spotlight
    Close participants screen   device=device_2
    Verify reaction buttons in docked ubar       console=console_1
    Verify and select raise hand option  console=console_1
    Verify raise hand notification      device_list=console_1
    select raise hand option    device=device_3
    Verify raise hand notification      device_list=device_3
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1      device_list=device_2,device_3


*** Keywords ***
Verify reactions visible on screen after taping
    [Arguments]       ${from_device}        ${to_device}
    Click like button     ${from_device}
    Verify reaction button on screen after tap on it   ${to_device}
    Click on laugh button     ${from_device}
    Verify reaction button on screen after tap on it        ${to_device}
    click on clap button     ${from_device}
    Verify reaction button on screen after tap on it       ${to_device}
    click on heart button     ${from_device}
    Verify reaction button on screen after tap on it   ${to_device}
    Verify and select raise hand option  ${from_device}
    Verify raise hand notification   ${to_device}
    Verify and select lower hand option  ${from_device}

End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

Verify docked ubar
    [Arguments]    ${console}
    Validate call control bar options       ${console}

Verify reaction buttons in docked ubar
    [Arguments]    ${console}
    Verify reactions options in call control bar     ${console}

verify device docked ubar
    [Arguments]    ${device_list}
     verify call control bar   ${device_list}

