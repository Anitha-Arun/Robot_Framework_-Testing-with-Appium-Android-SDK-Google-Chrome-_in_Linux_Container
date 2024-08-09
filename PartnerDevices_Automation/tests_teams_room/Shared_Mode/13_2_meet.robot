*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  3
${action_time} =  5

*** Test Cases ***
TC1: [Meet]DUT to add the participants to the meeting
    [Tags]       344897       bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=2
    Initiates conference meeting using Meet option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC2: [Meet] Verify Meet Now button on the home screen. Title must be updated to [Meet] from current implementation. Icon must remain the same.
    [Tags]   344887   P1     sanity_sm
    [Setup]   Testcase Setup for Meeting User    count=1
    Validate that signin is successfully completed    device_list=device_1     state=Sign in
    Verify Meet icon present on home screen  device=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC3:[Meet]Verify the educational message when user arrives is ad-hoc meeting
    [Tags]       344892      P1     sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=2
    Verify Meet icon present on home screen      device=device_1
    verify educational message when user arrives is ad-hoc meeting     device=device_1
    verify that after clicking the meetnow it will join the meeting directly        device=device_1
    Initiates conference meeting using Meet option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC4:[Meet] Verify that DUT user's video is seen while inviting the participants
    [Tags]      344910      P1   sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=2
    Initiates conference meeting using Meet option     from_device=device_1     to_device=device_2
    Wait for Some Time    time=${action_time}
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1    state=Connected
    Check video call On state   device_list=device_1
    End meeting   device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2


TC5:[Meet] Verify the UI after Selecting Meet button on the home screen
    [Tags]      344888     P2
    [Setup]   Testcase Setup for Meeting User     count=2
    Initiates conference meeting using Meet option     from_device=device_1     to_device=device_2
    Wait for Some Time    time=${action_time}
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1    state=Connected
    Check video call On state   device_list=device_1
    End meeting   device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2


TC6:[Meet] Verify the DUT can share whiteboard during 1:1 meet now
    [Tags]   344895     P2
    [Setup]   Testcase Setup for Meeting User     count=2
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    verify whiteboard sharing option under more option   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1,device_2
    Stop presenting whiteboard share screen     device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC7:[Meet] Verify the ad-hoc meeting is started by escalating a whiteboard from home screen, the education prompt (dialog) must not be applied on the DUT.
    [Tags]      344908   P2
    [Setup]   Testcase Setup for Meeting User     count=2
    verify whiteboard sharing option on home screen option  device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1
    start meeting from whiteboard sharing   device=device_1
    Wait for Some Time    time=${action_time}
    Add participant to conversation using display name   from_device=device_1      to_device=device_2
    Accept incoming call    device=device_2
    Verify meeting state   device_list=device_1,device_2   state=Connected
    Close participants screen   device=device_1
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1,device_2
    verify educational message is not present in meeting        device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND         Test Case Teardown    devices=device_1,device_2

TC8:[Meet] DUT User to start Meet from Home screen with policy assigned account
    [Tags]   424477        P1       sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=2
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    Verify docked ubar      device=device_1
    verify reactions buttons in call control     device=device_1
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen   device_list=device_1,device_2

TC9:[Meet] After joining the meeting verify All organizer options must be available for ad-hoc meeting Lock meeting Manage permissions Mute all Dont allow attendees to unmute
    [Tags]       344890      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=1
    Verify Meet icon present on home screen      device=device_1
    verify meet now parameters in meeting joining ui        device=device_1
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    verify educational message when user arrives is ad-hoc meeting     device=device_1
    Verify manage audio and video options in participants       device=device_1
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1

TC10:[Meet] Verify that the meeting starts with all default parameters Meeting title format Meeting with Room Name Camera ON
    [Tags]       344889      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=1
    Verify Meet icon present on home screen      device=device_1
    verify meet now parameters in meeting joining ui        device=device_1
    End meeting   device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    Verify educational message when user arrives is ad-hoc meeting     device=device_1
    Verify meeting state     device_list=device_1   state=Connected
    Check video call On state     device_list=device_1
    Verify call control bar   device_list=device_1
    End meeting     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1

TC11:[Meet] Verify the User is able to share whiteboard in meeting
    [Tags]      422405   P2
    [Setup]   Testcase Setup for Meeting User     count=2
    verify whiteboard sharing option on home screen option  device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1
    start meeting from whiteboard sharing   device=device_1
    Wait for Some Time    time=${action_time}
    Add participant to conversation using display name   from_device=device_1      to_device=device_2
    Accept incoming call    device=device_2
    Verify meeting state   device_list=device_1,device_2   state=Connected
    Close participants screen   device=device_1
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1,device_2
    verify educational message is not present in meeting        device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND         Test Case Teardown    devices=device_1,device_2


*** Keywords ***
Test Case Teardown
    [Arguments]     ${devices}
    Come back to home screen     ${devices}

Verify Meet icon present on home screen
    [Arguments]     ${device}
    Verify home page screen     ${device}

Initiates conference meeting using Meet option
     [Arguments]     ${from_device}     ${to_device}
    Initiates conference meeting using Meet now option   ${from_device}     ${to_device}


verify educational message when user arrives is ad-hoc meeting
    [Arguments]     ${device}
    verify meet info         ${device}

verify educational message is not present in meeting
    [Arguments]     ${device}
    verify meet dail info is not present in meeting     ${device}

Verify docked ubar
     [Arguments]    ${device}
     verify call control bar   ${device}

verify that after clicking the meetnow it will join the meeting directly
    [Arguments]     ${device}
    Verify meeting state     device_list=${device}   state=Connected
    Check video call On state     device_list=${device}
    End meeting     ${device}