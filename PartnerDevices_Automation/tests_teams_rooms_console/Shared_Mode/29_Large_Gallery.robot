*** Settings ***
Force Tags    large_gallery    29     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***

*** Test Cases ***
TC1:[Large Gallery] Verify Layout options in Group video call
    [Tags]     322597      P1      sanity_sm
    [Setup]   Testcase Setup for shared User     count=3
    Initiates conference meeting using Meet now option    from_device=device_2     to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_2
    Verify meeting state   device_list=device_2,device_3    state=Connected
    Add participant to the conversation using display name   from_device=device_2   to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Close participants screen   device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify layout options   device=console_1
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC2:[Large Gallery] Verify Layout icon in Meeting with 2 participants
    [Tags]     322589   P2
    [Setup]  Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    verify layout should present   device=console_1
    End up call     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3:[Large Gallery] Verify 'Together mode' is displaying with 2 participants with and without video
    [Tags]     322590   P2
    [Setup]  Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify layout options   device=console_1
    disable video call  device=console_1
    Verify layout options after disable video call      device=console_1
    End up call     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC4:[Large Gallery] Verify Gallery, Together mode and Large Gallery Layouts when participant is pinned
    [Tags]     322587      P1      sanity_sm
    [Setup]  Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Make a pin   from_device=console_1      to_device=device_3      device_type=console
    Change meeting mode     device=console_1    mode=together
    verify changed mode    device=device_1      changed_mode=together_mode
    verify together mode participant list  from_device=device_1    connected_device_list=device_2,device_3
    Verify pin icon     device=console_1
    change meeting mode     device=console_1    mode=large_gallery
    verify changed mode  device=device_1      changed_mode=large_gallery
    Verify pin icon     device=console_1
    change meeting mode     device=console_1     mode=gallery
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC5:[Large Gallery] Verify Gallery, Together mode and Large Gallery Layouts when participant is spotlighted
    [Tags]      322588      P2
    [Setup]  Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    make a spotlight   from_device=device_2   to_device=device_3
    verify spotlight text on device   device=device_3   text=spotlight
    Close participants screen   device=device_2
    Change meeting mode     device=console_1    mode=together
    verify changed mode    device=device_1      changed_mode=together_mode
    verify spotlight icon  device=console_1
    Verify spotlight icon on top left in the meeting  device=device_3
    change meeting mode     device=console_1    mode=large_gallery
    verify changed mode  device=device_1      changed_mode=large_gallery
    change meeting mode     device=console_1     mode=gallery
    Verify spotlight icon on top left in the meeting  device=device_3
    verify spotlight icon  device=console_1
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC6:[Large Gallery] Verify Layout option when no one else has joined the meeting
    [Tags]      322591      P2
    [Setup]  Testcase Setup for shared User     count=1
    Join a meeting   console=console_1      meeting=console_lock_meeting
    Verify for call state       console_list=console_1       state=Connected
    Verify layout icon on call control bar      console=console_1
    Disconnect the call     console=console_1
    Verify for call state       console_list=console_1       state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC7:[Large Gallery] Verify Layout options when TDC adds DUT
    [Tags]      322595      P2
    [Setup]  Testcase Setup for shared User     count=3
    Join meeting   device=device_2,device_3   meeting=console_lock_meeting
    Verify Call State    device_list=device_2,device_3    state=Connected
    Add participant to the conversation using display name   from_device=device_2    to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Close add participants roaster button   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2,device_3    state=Connected
    Verify layout options   device=console_1
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC8:[Large Gallery] Verify Layout options in Group audio call
    [Tags]        322596   P2
    [Setup]  Testcase Setup for shared User   count=3
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_3
    Accept incoming call    device=device_3
    Verify Call State    device_list=device_2,device_3    state=Connected
    Add participant to the conversation using phonenumber   from_device=device_2    to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Close add participants roaster button   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2,device_3    state=Connected
    Layout options in group audio call   console=console_1
    End up call     console=console_1       device=device_2
    Verify for call state     console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen     device_list=device_1,device_2,device_3

TC9:[Large Meeting]Verify the meeting UI when 3 participants joined
    [Tags]     322603      P2
    [Setup]  Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify docked ubar options      console=console_1
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3


*** Keywords ***
End up call
    [Arguments]    ${console}    ${device}
    Disconnect the call  ${console}
    Disconnect call     ${device}

verify layout should present
    [Arguments]       ${device}
    verify layout options   ${device}

verify together mode participant list
    [Arguments]       ${from_device}   ${connected_device_list}
    verify front row participant   ${from_device}   ${connected_device_list}

Verify layout icon on call control bar
    [Arguments]    ${console}
    verify_docked_ubar_options      ${console}

Layout options in group audio call
    [Arguments]       ${console}
    Verify layout options   device=${console}
