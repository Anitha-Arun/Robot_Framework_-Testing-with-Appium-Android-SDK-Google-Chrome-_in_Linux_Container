*** Settings ***
Documentation   Validating the functionality of live captions Feature.
Force Tags    sm_live_captions     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1 : [Live Caption 1:1 call]Verify that user is getting "Turn On Live Captions" option in the more(...) option of 1:1 call
    [Tags]      315386   bvt_sm     sanity_sm
    [Setup]  Testcase Setup for shared User     count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Check for live captions visibility   console=console_1
    Disconnect the call      console=console_1
    Verify for call state     console_list=console_1     device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2: [Live Caption ] Verify that user is getting "Turn On Live Captions" option in the more(...) option of group call
    [Tags]      315399      sanity_sm   P1
    [Setup]  Testcase Setup for shared User    count=3
    Make outgoing call with phonenumber    from_device=device_3     to_device=device_2
    Accept incoming call  device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_2,device_3    state=Connected
    Add participant to the conversation using display name   from_device=device_3    to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Wait for Some Time    time=${wait_time}
    Close add participants roaster button   device=device_3
    Verify for call state     console_list=console_1    device_list=device_2,device_3    state=Connected
    Check for live captions visibility   console=console_1
    Turn on live captions option    console=console_1
    Disconnect call     device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3  state=Disconnected
    [Teardown]  Run Keywords   Capture Failure    AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3