*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  3
${action_time} =  5

*** Test Cases ***
TC1:[Layout][Call] Verify DUT user have Switch Gallery orientation option when participant tray is visible with Outgoing Audio Call
    [Tags]      418907     P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=2
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    Accept incoming call  device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Change meeting mode     device=device_1     mode=gallery
    verify together mode participant list  from_device=device_1    connected_device_list=device_2
    change meeting mode     device=device_1     mode=front_row
    verify front row participant  from_device=device_1    connected_device_list=device_2
    Verify front row mode   device=device_1
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure  AND    Come back to home screen     device_list=device_1,device_2


TC2:[Layout] Verify Horizontal participant tray looks exactly the same way as the vertical participant tray in P2P call
    [Tags]       317043     P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=3
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using phonenumber    from_device=device_2      to_device=device_3
    Pick incoming call    device=device_3
    Close participants screen   device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    change meeting mode     device=device_1     mode=together
    verify changed mode    device=device_1      changed_mode=together_mode
    verify together mode participant list  from_device=device_1    connected_device_list=device_2
    change meeting mode     device=device_1     mode=gallery
    verify together mode participant list  from_device=device_1    connected_device_list=device_2
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2,device_3     state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure  AND    Come back to home screen     device_list=device_1,device_2,device_3


*** Keywords ***
verify the large gallarey, together mode and switch orientation toggle
    [Arguments]     ${device}
    Verify switch orientation toggle hidden after taping on frontrow         ${device}

verify together mode participant list
    [Arguments]       ${from_device}   ${connected_device_list}
    verify front row participant   ${from_device}   ${connected_device_list}
