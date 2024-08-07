*** Settings ***
Library     transition_keywords
Resource    ../resources/keywords/common.robot


*** Variables ***


*** Keywords ***

Speed Dial Transition
    [Arguments]     ${device}
    speed dial pretransition       ${device}
    speed dial performtransition       ${device}

dial pad Transition
    [Arguments]     ${device}
    dialpad pretransition       ${device}
    dialpad performtransition       ${device}

Pre-Call To In-Call Transition
    Make outgoing call using from call icon    from_device=device_1      to_device=device_2
    Pick incoming call    device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
Resume Transition
    Make outgoing call using display name    from_device=device_1     to_device=device_2
    Pick incoming call    device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Hold the call   device=device_1
    Verify Call State    device_list=device_1,device_2     state=Hold
    Resume the call   device=device_1
    Verify Call State    device_list=device_1,device_2     state=Resume
Hold Transition
    Make outgoing call using display name    from_device=device_1     to_device=device_2
    Pick incoming call    device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Hold the call   device=device_1
    Verify Call State    device_list=device_1,device_2     state=Hold