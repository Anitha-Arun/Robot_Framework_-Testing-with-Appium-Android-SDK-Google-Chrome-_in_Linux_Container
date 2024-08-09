*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${action_time} =  5

*** Test Cases ***
TC1:[Lobby] Verify when User joins the Meeting after Meeting started "We've, let people in the meeting know you're waiting." Message should be displayed.
    [Tags]       380733    bvt_sm   sanity_sm
    [Setup]  Testcase Meeting PSTN Setup as Main device   count=1
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1    meeting=lock_meeting
    verify waiting in the lobby message     device=device_1
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC2: [Lobby]Verify when User joins the Meeting before Meeting started When the meeting starts,we’ll let people know you’re waiting in the lobby
    [Tags]       380734     P1   sanity_sm
    [Setup]  Testcase Meeting PSTN Setup as Main device   count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1         meeting=lock_meeting
    Wait for Some Time    time=${action_time}
    verify waiting in the lobby message     device=device_1
    Join meeting   device=device_2         meeting=lock_meeting
    Verify meeting state   device_list=device_1    state=Connected
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC3:[Lobby] Verify "Meeting name and preview video are displayed in waiting lobby.
    [Tags]       380735    P1  sanity_sm
    [Setup]  Testcase Meeting PSTN Setup as Main device   count=1
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1       meeting=lock_meeting
    verify meeting name and preview video are displayed in waiting lobby     device=device_1    meeting=lock_meeting
    End meeting      device=device_1
    Verify meeting state    device_list=device_1    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC4:[Lobby] Verify DUT user is getting all Call controls on DUT, when admitted by TDC.
    [Tags]      380737   P2
    [Setup]  Testcase Meeting PSTN Setup as Main device   count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    verify waiting in the lobby message     device=device_1
    make admit and deny in the meeting      from_device=device_2   to_device=device_1:pstn_user     lobby=admit_lobby
    Close participants screen   device=device_2
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify docked ubar     device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC5:[Lobby] Verify DUT is displaying error message when TDC "Deny" Join Request.
    [Tags]      380739   P2
    [Setup]  Testcase Meeting PSTN Setup as Main device   count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2   meeting=lock_meeting
    verify waiting in the lobby message     device=device_1
    make admit and deny in the meeting      from_device=device_2   to_device=device_1:pstn_user      lobby=decline_lobby
    Close participants screen   device=device_2
    End meeting     device=device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC6:[Lobby] DUT user joins cross tenant meetings using the join with an id.
    [Tags]      381855     P2
    [Setup]  Testcase Meeting PSTN Setup as Main device   count=2
    Join meeting   device=device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_2    state=Connected
    join with an meeting id   device=device_1
    make admit and deny in the meeting      from_device=device_2   to_device=device_1:pstn_user     lobby=admit_lobby
    Close participants screen   device=device_2
    Verify meeting state   device_list=device_1   state=Connected
    Wait for Some Time    time=${action_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC7:[Lobby] Verify DUT is not receiving Meeting invites when DUT is waiting in Lobby.
    [Tags]      380740       P2
    [Setup]  Testcase Meeting PSTN Setup as Main device   count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1   meeting=lock_meeting
    verify waiting in the lobby message     device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:pstn_user
    verify user should not get second incoming call     device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

*** Keywords ***
Verify docked ubar
     [Arguments]    ${device}
     verify call control bar   ${device}
