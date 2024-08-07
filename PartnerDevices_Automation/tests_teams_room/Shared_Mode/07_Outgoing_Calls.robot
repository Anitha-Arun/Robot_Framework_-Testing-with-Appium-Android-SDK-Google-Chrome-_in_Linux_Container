*** Settings ***
Documentation   Outgoing Calls
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Outgoing Call] DUT dials to TDC call number from home screen dialpad
     [Tags]  237617      313018   P1        sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=2
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC2: [Outgoing Call] DUT calls incorrect number
    [Tags]  237614      444783    P2
    [Setup]  Testcase Setup for Meeting User   count=1
    Dial incorrect number from dial pad    device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1

TC3:[Call] Start Call, Increase and decrease volume after participants are added
    [Tags]      444810    P3
    [Setup]   Testcase Setup for Meeting User      count=2
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    Adjust volume button   device=device_1   state=UP     functionality=In_meeting
    Adjust volume button   device=device_1   state=Down   functionality=In_meeting
    End meeting   device=device_1
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen     device_list=device_1,device_2

TC4:[Call] TDC user to reject the Call invite call from DUT user.
    [Tags]     444818   P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    Reject incoming call   device_list=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen     device_list=device_1,device_2

# auto dial is not supported bug_3445550
#TC2: [Outgoing Call] DUT auto-dial to TDC call number from home screen dialpad
#    [Tags]  237618   P2
#    [Setup]  Testcase Setup for Meeting User   count=2
#    Make outgoing call using auto dial      from_device=device_1     to_device=device_2
#    Accept incoming call      device=device_2
#    Wait for Some Time    time=${wait_time}
#    Verify Call State    device_list=device_1,device_2    state=Connected
#    Disconnect call     device=device_2
#    Verify Call State    device_list=device_1,device_2     state=Disconnected
#    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

# auto dial is not supported bug_3445550
#TC3: [Outgoing Call] DUT not to auto dial incorrect number
#    [Tags]  237615   P1     sanity_sm
#    [Setup]  Testcase Setup for Meeting User   count=1
#    Verify not going call in auto dail incorrect number  device=device_1
#    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1

*** Keywords ***
Test Case Teardown
    [Arguments]     ${devices}
    Come back to home screen     ${devices}

Verify not going call in auto dail incorrect number
        [Arguments]     ${device}
         Auto dial incorrect number from dial pad       ${device}