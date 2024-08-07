*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_for_time} =   5
${wait_time} =  10

*** Test Cases ***
TC1: [Auto Dismiss] DUT user to rate the rating in rating screen
    [Tags]  237952  P1
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call      device=device_1
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC2: [Auto Dismiss] DUT user to get rating screen after meeting
    [Tags]  237954   P2
    [Setup]  Testcase Setup for Meeting User     count=3
    Verify meeting display on home screen     device=device_1
    Join meeting    device=device_1,device_2,device_3    meeting=cnf_device_meeting
    Wait for Some Time    time=${wait_time}
    Verify meeting state   device_list=device_1,device_2,device_3   state=Connected
    End meeting   device=device_1,device_2,device_3
    Verify meeting state   device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure   AND   Come back to home screen    device_list=device_1,device_2,device_3

TC3:[Auto Dismiss] DUT user to get rating screen after incoming call
    [Tags]  237955    bvt    bvt_sm     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber   from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call      device=device_1
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure   AND   Come back to home screen    device_list=device_1,device_2

TC4: [Auto Dismiss] DUT user to get rating screen after outgoing call
    [Tags]  237956   P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber   from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure   AND   Come back to home screen    device_list=device_1,device_2

TC5: [Auto Dismiss] Verify the Dismiss button in rating screen
    [Tags]  237951   bvt    bvt_sm     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber   from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure   AND   Come back to home screen    device_list=device_1,device_2

TC6: [Auto Dismiss] Verify call ended screen will disappear within 3 seconds
    [Tags]  303929   P1
    [Setup]  Testcase Setup for Meeting User      count=2
    Verify meeting display on home screen     device=device_1
    Join meeting    device=device_1   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1   state=Connected
    Verify video preview on screen      device=device_1
    Disconnect call and verify ended screen   device=device_1
    Verify meeting state   device_list=device_1   state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure   AND    Come back to home screen    device_list=device_1

TC7: [Auto Dismiss] Verify call decline screen auto dismissed within 5 seconds
    [Tags]  303930   P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User      count=2
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    Reject incoming call   device_list=device_2
    Verify call decline screen  device=device_1
    [Teardown]    Run Keywords    Capture on Failure   AND   Come back to home screen    device_list=device_1,device_2

TC8:[Auto Dismiss] Verify call cancelled screen auto dismissed within 5 seconds
    [Tags]      303934       P2
    [Setup]  Testcase Setup for Meeting User      count=2
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    cancelled incoming call   device_list=device_2
    Verify call decline screen  device=device_1
    [Teardown]    Run Keywords    Capture on Failure   AND   Come back to home screen    device_list=device_1,device_2


*** Keywords ***
cancelled incoming call
    [Arguments]     ${device_list}
    Reject incoming call   ${device_list}
