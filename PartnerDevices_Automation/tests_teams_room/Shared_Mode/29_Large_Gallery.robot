*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  2
${action_time} =  5

*** Test Cases ***
TC1:[Large Gallery] Verify Gallery, Together mode and Large Gallery Layouts when participant is pinned
     [Tags]     304443      bvt_sm          sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_1,device_2,device_3    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    make a pin   from_device=device_1  to_device=device_3
    Close participants screen   device=device_1
    verify pin icon      device=device_1
    change meeting mode     device=device_1     mode=together
    verify changed mode    device=device_1      changed_mode=together_mode
    verify pin icon      device=device_1
    verify together mode participant list  from_device=device_1    connected_device_list=device_2
    change meeting mode     device=device_1     mode=large_gallery
    verify changed mode  device=device_1      changed_mode=large_gallery
    verify pin icon      device=device_1
    change meeting mode     device=device_1     mode=gallery
    verify pin icon      device=device_1
    verify together mode participant list  from_device=device_1    connected_device_list=device_2
    change meeting mode     device=device_1     mode=front_row
    verify front row participant  from_device=device_1    connected_device_list=device_2
    verify pin icon      device=device_1
    Verify front row mode   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2,device_3


TC2:[Large Gallery] Verify Layout options in Group video call
     [Tags]     316700      P1             sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=3
    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3    state=Connected
    verify layout options   device=device_2
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2,device_3


TC3:[Large Gallery] Verify Gallery, Together mode and Large Gallery Layouts when participant is spotlighted
    [Tags]     304444     P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_1,device_2,device_3    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    make a spotlight   from_device=device_2   to_device=device_3
    verify spotlight text on device   device=device_3   text=spotlight
    Close participants screen   device=device_2
    verify spotlight icon    device=device_1
    change meeting mode     device=device_1     mode=together
    verify changed mode    device=device_1             changed_mode=together_mode
    verify spotlight icon    device=device_1
    verify together mode participant list  from_device=device_1    connected_device_list=device_2
    change meeting mode     device=device_1     mode=large_gallery
    verify changed mode    device=device_1             changed_mode=large_gallery
    verify spotlight icon    device=device_1
    change meeting mode     device=device_1     mode=gallery
    verify spotlight icon    device=device_1
    verify together mode participant list  from_device=device_1    connected_device_list=device_2
    change meeting mode     device=device_1     mode=front_row
    verify front row participant  from_device=device_1    connected_device_list=device_2
    Verify front row mode   device=device_1
    verify spotlight icon    device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2,device_3


TC4:[Large Gallery] Verify Layout icon in Meeting with 2 participants
    [Tags]     313229        P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2        meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2     state=Connected
    verify layout should present   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2

TC5:[Large Gallery] Verify 'Together mode' is displaying with 2 participants with and without video
    [Tags]     316625        P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2        meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2     state=Connected
    disable video call  device=device_1
    verify layout options after disable video call      device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2


TC6:[Large Gallery] Verify Layout options when TDC adds DUT
    [Tags]     316689     P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_2,device_3   meeting=lock_meeting
    Verify meeting state   device_list=device_2,device_3    state=Connected
    Add participant to conversation using display name   from_device=device_2      to_device=device_1:meeting_user
    Accept incoming call    device=device_1
    Close participants screen   device=device_2
    verify layout options   device=device_1
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3  state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2,device_3

TC7:[Large Gallery] Verify Layout options in Group audio call
    [Tags]        316698   P2
    [Setup]  Testcase Setup for Meeting User   count=3
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using phonenumber    from_device=device_2      to_device=device_3
    Pick incoming call    device=device_3
    Close participants screen   device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Layout options in Group audio call   device=device_2
    Disconnect call     device=device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen     device_list=device_1,device_2,device_3


TC8:[Large Meeting]Verify the meeting UI when 3 participants joined
    [Tags]       316773        P2
    [Setup]   Testcase Setup for Meeting User    count=2
    Verify meeting display on home screen     device=device_1
    Join meeting    device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2  state=Connected
    Verify participants list in meeting    device=device_1
    Verify docked ubar  device=device_1
    End meeting   device=device_1,device_2
    Verify meeting state   device_list=device_1,device_2  state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC9:[Large Meeting]Verify that user can remove other users from the meeting
    [Tags]   316800        P2
    [Setup]   Testcase Setup for Meeting User    count=2
    Verify meeting display on home screen     device=device_1
    Join meeting    device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    Verify participants list in meeting    device=device_1
    Verify docked ubar  device=device_1
    Remove user from meeting call   from_device=device_1      to_device=device_2
    Verify someone removed you from the meeting call  device=device_2
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1   state=Connected
    End meeting   device=device_1
    Verify meeting state   device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC10:[Large Meeting]DUT User should be able to PIN a user
    [Tags]       316901        P2
    [Setup]   Testcase Setup for Meeting User    count=2
    Verify meeting display on home screen     device=device_1
    Join meeting    device=device_1,device_2  meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2  state=Connected
    Verify participants list in meeting    device=device_1
    Verify docked ubar  device=device_1
    make a pin       from_device=device_1       to_device=device_2
    Close participants screen   device=device_1
    verify pin icon      device=device_1
    End meeting   device=device_1,device_2
    Verify meeting state   device_list=device_1,device_2  state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC11:[Large Gallery] Verify Layout option when no one else has joined the meeting
     [Tags]   316643        P2
    [Setup]   Testcase Setup for Meeting User    count=1
    Verify meeting display on home screen     device=device_1
    Join meeting    device=device_1     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1       state=Connected
    Verify participants list in meeting    device=device_1
    Verify docked ubar  device=device_1
    End meeting   device=device_1
    Verify meeting state   device_list=device_1        state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure   AND    Come back to home screen    device_list=device_1


*** Keywords ***
Verify docked ubar
     [Arguments]    ${device}
     verify call control bar   ${device}

verify together mode participant list
    [Arguments]       ${from_device}   ${connected_device_list}
    verify front row participant   ${from_device}   ${connected_device_list}

verify layout should present
    [Arguments]       ${device}
    verify layout options   ${device}

Layout options in Group audio call
    [Arguments]       ${device}
    verify layout options after disable video call  ${device}

