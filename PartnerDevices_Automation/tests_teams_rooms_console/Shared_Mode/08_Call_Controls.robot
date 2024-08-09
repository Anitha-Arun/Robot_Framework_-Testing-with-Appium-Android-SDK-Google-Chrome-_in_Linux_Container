*** Settings ***
Documentation  Validating the functionality of Console Call Controls feature
Force Tags    sm_call_controls   sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  10

*** Test Cases ***
#Feature change: Video call UI has changed to meeting UI, so, hold option is removed
#TC1: [Video - Call Hold] DUT puts call on hold with TDC
#    [Tags]   315011   bvt_sm        sanity_sm
#    [Setup]   Testcase Setup for shared User    count=2
#    Place a video call using display name   from_device=device_2     to_device=console_1:meeting_user
#    Pick up incoming call    console=console_1
#    Wait for Some Time    time=${wait_time}
#    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
#    Hold current call   console=console_1
#    Verify for call state     console_list=console_1    device_list=device_2    state=Hold
#    Resume current call  console=console_1
#    Verify for call state     console_list=console_1     state=Resume
#    Disconnect call     device=device_2
#    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
#    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2: [Audio - Mute Call] DUT puts the call on Mute with TDC
    [Tags]      315013      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User   count=2
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Mute the call      console=console_1
    Verify and check call mute state      console_list=console_1    state=Mute
    Unmute the call    console=console_1
    Verify and check call mute state     console_list=console_1    state=Unmute
    Disconnect call     device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3: [Video - Mute Call] DUT puts the call on Mute with TDC
    [Tags]      315015   Sanity_sm      P1
    [Setup]   Testcase Setup for shared User   count=2
    Place a video call using display name   from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Close participants screen   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Mute the call      console=console_1
    Verify and check call mute state      console_list=console_1    state=Mute
    Unmute the call    console=console_1
    Verify and check call mute state     console_list=console_1    state=Unmute
    End a meeting     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC4: [Audio - Call Hold] DUT puts call on hold with TDC
    [Tags]      315009   P1
    [Setup]   Testcase Setup for shared User    count=2
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Hold current call   console=console_1
    Verify for call state     console_list=console_1    device_list=device_2    state=Hold
    Resume current call  console=console_1
    Verify for call state     console_list=console_1     state=Resume
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC5: [Mixed - Mute Call] DUT puts the call on mute with Video enabled TDC
    [Tags]   315017   P1        sanity_sm
    [Setup]   Testcase Setup for shared User   count=2
    Place a video call using display name   from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Close participants screen   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Mute the call      console=console_1
    Verify and check call mute state      console_list=console_1    state=Mute
    Unmute the call    console=console_1
    Verify and check call mute state     console_list=console_1    state=Unmute
    End a meeting     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC6: [Dialpad][Mic]Soft mute icon is disabled when user try to use dial pad in call
    [Tags]   322319   P2
    [Setup]   Testcase Setup for shared User   count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    verify dailpad on call controlbar   device=console_1
    verify mic on calling screen is not clickable    device=console_1
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC7:[Call-App] Verify Call button on the home screen and Icon is updated to “Phone”.
    [Tags]        444606    bvt_sm    sanity_sm
    [Setup]   Testcase Setup for shared User    count=1
    check dial pad on landing page   console=console_1
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC8:[Call-App] Verify the UI after selecting Call button on the home screen
    [Tags]        444607    bvt_sm    sanity_sm
    [Setup]   Testcase Setup for shared User    count=1
    verify dial pad on homescreen       console=console_1
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC10:[Call-App] Verify mic is enabled and video is disabled by default, when user makes P2P call.
    [Tags]       444617    P1    sanity_sm
    [Setup]   Testcase Setup for shared User    count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Check video call Off state      device_list=console_1
    Verify meeting Mute State    device_list=console_1    state=Unmute
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}
