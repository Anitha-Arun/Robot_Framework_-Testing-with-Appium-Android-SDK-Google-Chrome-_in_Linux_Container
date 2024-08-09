*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  5

*** Test Cases ***

TC1:[Modern Stage] Verify local video showing correctly on the screen
    [Tags]  317437     P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1   state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_2
    Accept incoming call    device=device_2
    Verify meeting state   device_list=device_1,device_2      state=Connected
    Close participants screen   device=device_1
    Verify video preview on screen  device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2



TC2:[Modern Stage] Verify the design of the meeting title
    [Tags]  317443        P2
    [Setup]   Testcase Setup for Meeting User    count=3
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Verify meeting state   device_list=device_1,device_2,device_3   state=Connected
    Close participants screen   device=device_1
    Verify docked ubar     device=device_1
    verify reactions buttons in call control     device=device_1
    Verify meeting info option in meeting   device=device_1
    End meeting      device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3


TC3:[Modern Stage] Verify the stage with multiple spotlight participants
    [Tags]      317542       P2
   [Setup]    Testcase Setup for Meeting User   count=3
    Join Meeting    device=device_1,device_2,device_3     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    make a spotlight   from_device=device_2   to_device=device_1:meeting_user
    verify spotlight text on device   device=device_1   text=spotlight
    Close participants screen   device=device_2
    verify spotlight icon    device=device_3
    make a spotlight   from_device=device_2   to_device=device_3
    verify spotlight text on device   device=device_3   text=spotlight
    Close participants screen   device=device_2
    verify spotlight icon    device=device_3
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2,device_3


TC4:[Modern Stage] Verify the stage with pinned participant
    [Tags]      317544      P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join Meeting    device=device_1,device_2,device_3     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    make a pin   from_device=device_1  to_device=device_3
    Close participants screen   device=device_1
    verify pin icon      device=device_1
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2,device_3


TC5:[Modern Stage] Verify the stage with pinned participant and multiple spotlight participants
     [Tags]      317545      P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join Meeting    device=device_1,device_2,device_3     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    make a pin       from_device=device_1  to_device=device_2
    Close participants screen   device=device_1
    verify pin icon      device=device_1
    make a spotlight   from_device=device_1   to_device=device_3
    verify spotlight text on device   device=device_3   text=spotlight
    Close participants screen   device=device_1
    verify spotlight icon    device=device_3
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2,device_3

TC6:[Modern Stage] Verify the layout switching is working as per the design in Together mode, Large Galley Mode, Galley Mode etc.
    [Tags]       317538     P1      sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    change meeting mode     device=device_1     mode=together
    verify changed mode   device=device_1       changed_mode=together_mode
    verify together mode participant list  from_device=device_1    connected_device_list=device_2
    change meeting mode     device=device_1     mode=large_gallery
    verify changed mode   device=device_1       changed_mode=large_gallery
    change meeting mode     device=device_1     mode=gallery
    verify gallery mode participant list  from_device=device_1    connected_device_list=device_2
    change meeting mode     device=device_1     mode=front_row
    verify front row participant  from_device=device_1    connected_device_list=device_2
    Verify front row mode   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2


TC7:[Modern Stage] Verify the display and functionality of the meeting actions on participant
    [Tags]      317536     p2
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user,device_3
    Verify you are an attendee now notification     device=device_1,device_3
    Mutes the phone call    device=device_1
    Verify meeting Mute State   device_list=device_1    state=mute
    Unmutes the phone call   device=device_1
    Verify meeting Mute State    device_list=device_1    state=unmute
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3



*** Keywords ***
Verify docked ubar
     [Arguments]    ${device}
     verify call control bar   ${device}

verify together mode participant list
    [Arguments]       ${from_device}   ${connected_device_list}
    verify front row participant   ${from_device}   ${connected_device_list}

verify gallery mode participant list
    [Arguments]       ${from_device}   ${connected_device_list}
    verify front row participant   ${from_device}   ${connected_device_list}
