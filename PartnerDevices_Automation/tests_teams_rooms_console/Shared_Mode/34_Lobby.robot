*** Settings ***
Force Tags  34
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

Suite Setup     Lobby Setup
Suite Teardown      Run Keywords   Suite Failure Capture    AND     Lobby teardown

*** Variables ***
${action_time} =  5

*** Test Cases ***
TC1:[Lobby] Verify when User joins the Meeting before Meeting started "We've, let people in the meeting know you're waiting." Message should be displayed.
    [Tags]      380758    bvt_sm   sanity_sm
    [Setup]   Testcase setup for shared mode PSTN Setup as Main device     count=1
    Verify meeting display on home page   console=console_1
    Join a meeting   console=console_1     meeting=console_lock_meeting
    verify waiting in the lobby message     device=console_1
    End the meeting     console=console_1
    Verify for call state    console_list=console_1     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC2:[Lobby]Verify "Meeting name and preview video is displayed in waiting lobby.
    [Tags]       380759    bvt_sm   sanity_sm
    [Setup]   Testcase setup for shared mode PSTN Setup as Main device     count=1
    Verify meeting display on home page   console=console_1
    Join a meeting   console=console_1     meeting=console_lock_meeting
    Verify waiting in the lobby message     device=console_1
    Verify meeting name and preview video are displayed in waiting lobby     device=console_1       meeting=console_lock_meeting
    End the meeting     console=console_1
    Verify for call state    console_list=console_1     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC3:[Lobby]Verify Console User is displaying error message when TDC "Deny" Join Request.
    [Tags]      380761   P2
    [Setup]   Testcase setup for shared mode PSTN Setup as Main device     count=2
    Verify meeting display on home page   console=console_1
    Join a meeting   console=console_1     device=device_2     meeting=console_lock_meeting
    verify waiting in the lobby message     device=console_1
    make admit and deny in the meeting      from_device=device_2   to_device=console_1:pstn_user     lobby=decline_lobby
    Close participants screen   device=device_2
    End meeting     device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2       state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC4: [Lobby] Verify when Console user joins Cross cloud Meeting only Hang up button is displayed on Call control bar.
    [Tags]       380745    P1   sanity_sm
    [Setup]   Testcase setup for shared mode PSTN Setup as Main device     count=1
    Verify meeting display on home page   console=console_1
    Join a meeting   console=console_1     meeting=console_lock_meeting
    verify hang up button displayed in call control bar while in lobby     console=console_1
    End the meeting     console=console_1
    Verify for call state    console_list=console_1     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC5:[Lobby] Verify Console user is getting all Call controls once on console, when admitted by TDC.
    [Tags]      380760   P2
    [Setup]   Testcase setup for shared mode PSTN Setup as Main device     count=2
    Verify meeting display on home page   console=console_1
    Join a meeting   console=console_1     device=device_2     meeting=console_lock_meeting
    verify waiting in the lobby message     device=console_1
    make admit and deny in the meeting      from_device=device_2   to_device=console_1:pstn_user     lobby=admit_lobby
    Close participants screen   device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify call control bar options     console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC6:[Lobby]Verify DUT[Console] is not receiving Meeting invites when DUT[Console] is waiting in Lobby.
    [Tags]      380762      P2
    [Setup]   Testcase setup for shared mode PSTN Setup as Main device     count=1
    Verify meeting display on home page   console=console_1
    Join a meeting   console=console_1     meeting=console_lock_meeting
    verify waiting in the lobby message     device=console_1
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:pstn_user
    verify user should not get second incoming call     device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC7:[Lobby] DUT user joins cross tenant meetings using the join with an id.
    [Tags]      382107     P2
    [Setup]   Testcase setup for shared mode PSTN Setup as Main device     count=1
    Verify meeting display on home page   console=console_1
    Verify lobby message when user joining in meeting with join by code     console=console_1
    Verify meeting name and preview video are displayed in waiting lobby     device=console_1       meeting=console_lock_meeting
    End the meeting     console=console_1
    Verify for call state    console_list=console_1     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

*** Keywords ***
verify hang up button displayed in call control bar while in lobby
    [Arguments]    ${console}
    Verify waiting in the lobby message     device=${console}

Verify call control bar options
    [Arguments]    ${console}
    Validate call control bar options       ${console}

End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}


Lobby Setup
    Console sign out method   console=console_1
    Sign out method    device=device_1
    Sign in method     device=device_1     user=pstn_user
    console sign in method    console=console_1       user=pstn_user
    Get device pairing code    device_list=device_1    console_list=console_1     user_list=pstn_user

Lobby teardown
    Console sign out method   console=console_1
    Sign out method    device=device_1
    Sign in method     device=device_1     user=meeting_user
    console sign in method    console=console_1       user=meeting_user
    Get device pairing code    device_list=device_1    console_list=console_1     user_list=meeting_user
