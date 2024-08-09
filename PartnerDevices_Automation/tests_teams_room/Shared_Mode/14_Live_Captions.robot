*** Settings ***
Documentation   Validating the functionality of live captions Feature.
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  10


*** Test Cases ***
TC1 : [Live Caption 1:1 call]Verify that user is getting "Turn On Live Captions" option in the more(...) option of 1:1 call
    [Tags]  260615   bvt   bvt_sm   sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Verify live captions option visibility    device=device_1
    Disconnect call     device=device_2
    Verify Call State     device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC2: [Live Caption ] Verify that user is getting "Turn On Live Captions" option in the more(...) option of group call
    [Tags]  260622   P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=3
    Make outgoing call with phonenumber    from_device=device_3     to_device=device_2
    Accept incoming call  device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_2,device_3   state=Connected
    Add participant to conversation using display name   from_device=device_3      to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Wait for Some Time    time=${wait_time}
    Close add participants roaster button   device=device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Verify live captions option visibility    device=device_1
    Turn on live captions and validate   device=device_1
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3




