*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  15

*** Test Cases ***
TC1: [Incoming Call] Audio call to DUT
    [Tags]  237702  444801    bvt   bvt_sm    sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC2: [Incoming Call] Video call to DUT
    [Tags]  237701   444800  bvt   bvt_sm     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call   device=device_1
    Close participants screen   device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC3: [Incoming Call] DUT does not answer the incoming call
     [Tags]  237704     444803    P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Disconnect call     device=device_2
    Come back to home screen  device_list=device_1,device_2
    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
    Verify incoming call    device=device_1     status=appear
    Close participants screen   device=device_2
    Wait for Some Time   ${wait_time}
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC4: [Incoming Call] DUT declines the incoming call
    [Tags]  237703      444802  P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Reject incoming call   device_list=device_1
    Come back to home screen  device_list=device_1,device_2
    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
    Close participants screen   device=device_2
    Reject incoming call   device_list=device_1
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC5: [Second incoming call] DUT should not get second incoming call
    [Tags]  237640   bvt   bvt_sm    sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=3
    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call   device=device_1
    Close participants screen   device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Make outgoing call with phonenumber    from_device=device_3     to_device=device_1:meeting_user
    Verify user should not get second incoming_call     device=device_1
    Wait for voicemail timeout disconnect    device=device_3
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC6: [Incoming Call] DUT user must be able to pick the incoming call on "Admin Only (Enter Password)"
     [Tags]  317032     444805   P2
    [Setup]  Testcase Setup for Meeting User     count=2
    navigate to device setting page  device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call    device=device_2
    Verify Call State    device_list=device_2    state=Disconnected
    Make Video call using display name   from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Close participants screen   device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call    device=device_1,device_2
    device setting back  device=device_1
    come back to home screen    device_list=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2


*** Keywords ***
Test Case Teardown
    [Arguments]     ${devices}
    Come back to home screen     ${devices}

Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

navigate to device setting page
    [Arguments]       ${device}
    Navigate to app settings page  ${device}
    navigate to meetings option in device settings page    ${device}
