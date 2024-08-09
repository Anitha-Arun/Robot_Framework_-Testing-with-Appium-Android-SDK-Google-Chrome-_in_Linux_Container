*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot



*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Escalate to conference] DUT user can add another DUT user while in call with TDC user
    [Tags]   237775     444793   bvt   bvt_sm    sanity_sm
    [Setup]   Testcase Setup for Meeting User  count=3
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name     from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Disconnect call     device=device_3
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC2: [Escalate to conference] DUT user can add another TDC user while in call with TDC user
    [Tags]   237776     444795    P1
    [Setup]   Testcase Setup for Meeting User  count=3
    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call      device=device_1
    Close participants screen   device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Disconnect call     device=device_3
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

#Feature change: we are unable to check participant profile while in call
#TC3: [Esc to conference] Check participant's profile while adding to the call
#    [Documentation]  Tested for DUT only
#    [Tags]   237874   P2
#    [Setup]  Testcase Setup for Meeting User     count=3
#    Make Video call using display name   from_device=device_3     to_device=device_1:meeting_user
#    Accept incoming call      device=device_1
#    Wait for Some Time    time=${wait_time}
#    Verify Call State    device_list=device_1,device_3    state=Connected
#    Add participant to conversation using display name   from_device=device_1      to_device=device_2
#    Accept incoming call      device=device_2
#    Close participants screen   device=device_1
#    Verify participant list    from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
#    Check participants profile view   device=device_1
#    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
#    Disconnect call     device=device_2
#    Verify Call State    device_list=device_1,device_3    state=Connected
#    Disconnect call     device=device_3
#    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
#    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3


TC4: [Escalate to conference] DUT user can add TDC user while in call with another DUT user
    [Tags]   237774     444791   P1    sanity_sm
    [Setup]   Testcase Setup for Meeting User  count=3
    Make Video call using display name  from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Close participants screen   device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Disconnect call     device=device_1,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3


TC5:[Escalate to conference]Check participant's profile while adding to the call.
    [Tags]      444799      P1       sanity_sm
    [Setup]   Testcase Setup for Meeting User        count=3
    Make outgoing call with displayname         from_device=device_1     to_device=device_2
    Accept incoming call           device=device_2
    Verify Call State            device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name           from_device=device_1      to_device=device_3
    Accept incoming call          device=device_3
    Close participants screen         device=device_1
    Verify list of participants          from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State          device_list=device_1,device_2,device_3    state=Connected
    Disconnect call           device=device_1,device_2
    Verify Call State            device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords        Capture on Failure      AND        Test Case Teardown    devices=device_1,device_2,device_3

TC6:[Call] Start Call, Add Participants to Conference call.
    [Tags]      444809      P3
    [Setup]   Testcase Setup for Meeting User        count=3
    Make outgoing call with displayname         from_device=device_1     to_device=device_2
    Accept incoming call           device=device_2
    Verify Call State            device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name           from_device=device_1      to_device=device_3
    Accept incoming call          device=device_3
    Close participants screen         device=device_1
    Verify list of participants          from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State          device_list=device_1,device_2,device_3    state=Connected
    Disconnect call           device=device_1,device_2
    Verify Call State            device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords        Capture on Failure      AND        Come back to home screen     device_list=device_1,device_2,device_3

TC7:[Call] DUT user adds TDC user as participant, holds and resumes during call.
     [Tags]      444813      P1     sanity_sm
    [Setup]   Testcase Setup for Meeting User        count=3
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    Accept incoming call           device=device_2
    Verify Call State            device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name           from_device=device_1      to_device=device_3
    Accept incoming call          device=device_3
    Close participants screen         device=device_1
    Hold the call   device=device_1
    Verify Call State    device_list=device_1    state=Hold
    Resume the call   device=device_1
    Verify Call State    device_list=device_1     state=Resume
    Verify Call State            device_list=device_1,device_2,device_3    state=Connected
    Disconnect call           device=device_1,device_2
    Verify Call State            device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords        Capture on Failure      AND        Come back to home screen     device_list=device_1,device_2,device_3


*** Keywords ***
Test Case Teardown
    [Arguments]     ${devices}
    Come back to home screen     ${devices}