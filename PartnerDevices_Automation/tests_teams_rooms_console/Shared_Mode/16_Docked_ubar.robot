*** Settings ***
Force Tags    16    docked_uBar_sm    sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***

*** Test Cases ***
TC1 : [Docked Ubar] Touch console user verify that Docked Ubar will be always available on Touch console
    [Tags]    322783    bvt     bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User    count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant  console=console_1
    Verify docked ubar       console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2 : [Docked UBar] Options available in Docked Ubar
    [Tags]    322781        P1      sanity_sm
    [Setup]   Testcase Setup for shared User    count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify docked ubar options      console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3 : [Docked Bar][Touch console] DUT user verify Docked Ubar when FoR connected with Touch console
    [Tags]    322785        P1
    [Setup]   Testcase Setup for shared User    count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify video preview on screen    device=device_2
    Verify not having video preview on screen       console=console_1
    Verify docked ubar options      console=console_1
    Verify not to have docked ubar options      device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC4 :[Docked Ubar]Touch console user verify that Meeting title visible on Docked Ubar
    [Tags]    322782        P2
    [Setup]   Testcase Setup for shared User    count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify meeting title with meeting time     console=console_1    meeting=rooms_console_meeting
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2


*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

Verify docked ubar
    [Arguments]    ${console}
    Validate call control bar options       ${console}
