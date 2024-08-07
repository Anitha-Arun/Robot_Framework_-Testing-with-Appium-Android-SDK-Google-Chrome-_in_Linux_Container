*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Test Cases ***
# Test obsolete, new cases for new report and isssue will be added
#TC1: [Report an Issue] Verify that video camera should not disable when user report feedback in a meeting
#    [Tags]   305605     P1
#    [Setup]  Testcase Setup for Meeting User     count=2
#    Verify meeting display on home screen     device=device_1
#    Join meeting   device=device_1     meeting=lock_meeting
#    Add participant to conversation using display name    from_device=device_1  to_device=device_2
#    report an issue     device=device_1
#    verify send feedback text   device=device_1
#    End meeting     device=device_1,device_2
#    Verify meeting state    device_list=device_1,device_2   state=Disconnected
#    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1,device_2
#
#TC2: [Report an Issue] Verify that "feedback has been sent" notification appearing after immediate disconnect of meeting.
#    [Tags]   305618     P1
#    [Setup]  Testcase Setup for Meeting User     count=2
#    Verify meeting display on home screen     device=device_1
#    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
#    report an issue     device=device_1
#    verify send feedback text   device=device_1
#    End meeting     device=device_1,device_2
#    Verify meeting state    device_list=device_1,device_2   state=Disconnected
#    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1,device_2
#
#
#TC3: [Report an Issue] Verify that user should be able to get report an issue option in Video call
#    [Tags]  305619      P2
#    [Setup]  Testcase Setup for Meeting User     count=2
#    Make outgoing call with phonenumber    from_device=device_1      to_device=device_2
#    Accept incoming call    device=device_2
#    Verify Call State    device_list=device_1,device_2    state=Connected
#    report an issue     device=device_1
#    verify send feedback text   device=device_1
#    End meeting     device=device_1,device_2
#    Verify meeting state    device_list=device_1,device_2   state=Disconnected
#    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1,device_2
#
#
#TC4: [Report an Issue] Verify DUT should get Report an Issue option with Incoming/Outgoing Audio Call
#    [Tags]   316575     P2
#    [Setup]  Testcase Setup for Meeting User     count=2
#    Make outgoing call with phonenumber    from_device=device_2      to_device=device_1:meeting_user
#    Accept incoming call    device=device_1
#    Wait for Some Time    time=${wait_time}
#    Verify Call State    device_list=device_1,device_2    state=Connected
#    report an issue     device=device_1
#    verify send feedback text   device=device_1
#    End meeting     device=device_1,device_2
#    Verify meeting state    device_list=device_1,device_2   state=Disconnected
#    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1,device_2

