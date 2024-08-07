*** Settings ***
Force Tags    meeting_chat  26  sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Chat] Verify the chat toggle button when user joined the meeting.
    [Tags]      380040      bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    verify meeting chat     console=console_1       action_type=verify
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2: [Chat] Verify the behavior of DUT, once chat toggle button is enabled in the meeting.
    [Tags]      380041      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    verify meeting chat     console=console_1        action_type=modify
    verify meeting chat toggle on behaviour      device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3: [Chat]Verify "Show meeting chat" option under the admin settings.
    [Tags]      380042      P2
    [Setup]   Testcase Setup for shared User     count=1
    Navigate to app settings screen     console=console_1
    Navigate to meeting and calling options from device settings page       console=console_1   option=meeting
    verify meeting chat under admin settings    console=console_1
    come back from admin settings page      device_list=console_1
    [Teardown]  Run Keywords   Capture Failure  AND    Come back to home screen page   console_list=console_1

TC4:[Chat]Verify the chat option in P2P incoming call when show meeting chat is enabled in admin settings.
    [Tags]      380044      bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    verify meeting chat     console=console_1       action_type=verify
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC5: [Chat]Verify the chat option in P2P incoming call when user enables chat option.
    [Tags]      380045      P2
    [Setup]   Testcase Setup for shared User     count=2
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    verify meeting chat     console=console_1       action_type=modify
    verify meeting chat toggle on behaviour      device=device_1
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC6: [Chat]Verify the chat option in P2P outgoing call when show meeting chat is enabled in admin settings.
    [Tags]      380047      P2
    [Setup]   Testcase Setup for shared User     count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    verify meeting chat     console=console_1       action_type=verify
    Disconnect call     device=device_2
    Verify for call state     console_list=console_1     device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC7: [Chat]Verify the chat option in P2P outgoing call when user enables chat option.
    [Tags]      380048      P2
    [Setup]   Testcase Setup for shared User     count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    verify meeting chat     console=console_1       action_type=modify
    verify meeting chat toggle on behaviour      device=device_1
    Disconnect call     device=device_2
    Verify for call state     console_list=console_1     device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC8: [Chat]Verify the chat option when DUT user initiates meet now with TDC user & Show meeting chat should be enabled.
    [Tags]      380050      sanity_sm   P1
    [Setup]   Testcase Setup for shared User   count=2
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    verify meeting chat     console=console_1       action_type=modify
    verify meeting chat toggle on behaviour      device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC9: [Chat]Verify the chat option when DUT user enables chat option in Large Gallery mode.
    [Tags]      380054      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    change meeting mode     device=console_1    mode=large_gallery
    Verify large gallery mode after switching      device=console_1
    verify changed mode  device=device_1      changed_mode=large_gallery
    verify meeting chat     console=console_1        action_type=modify
    verify meeting chat toggle on behaviour      device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC10: [Chat]Verify the chat option when DUT user enables chat option in Together mode.
    [Tags]      380056      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    change meeting mode     device=console_1    mode=together
    Verify together mode after switching       device=console_1
    verify changed mode  device=device_1      changed_mode=together_mode
    verify meeting chat     console=console_1        action_type=modify
    verify meeting chat toggle on behaviour      device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC11: [Chat]Verify the chat option when DUT user enables chat option in Front Row mode.
    [Tags]      380058      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    verify and validate front row mode      device=console_1
    verify meeting chat toggle on behaviour      device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC12: [Chat]Verify the chat option when TDC user initiates meet now with DUT user & Show meeting chat should be enabled.
    [Tags]      380075      P2
    [Setup]   Testcase Setup for shared User   count=2
    Start meeting using meet now    from_device=device_2    to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Close participants screen   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    verify meeting chat     console=console_1       action_type=modify
    verify meeting chat toggle on behaviour      device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

Disable the show meeting chat option
    [Arguments]       ${console}
    Navigate to app settings screen    ${console}
    Navigate to meeting and calling options from device settings page       ${console}  option=meeting
    Enable and disable the chat toggle in admin setting     device=${console}       state=off
    come back from admin settings page      device_list=${console}

Navigate to app settings screen
    [Arguments]   ${console}
    Tap on more option  ${console}
    Tap on settings page   ${console}

Enable the show meeting chat option
    [Arguments]    ${console}
    Navigate to app settings screen    ${console}
    Navigate to meeting and calling options from device settings page       ${console}  option=meeting
    Enable and disable the chat toggle in admin setting     device=${console}       state=on
    come back from admin settings page      device_list=${console}
