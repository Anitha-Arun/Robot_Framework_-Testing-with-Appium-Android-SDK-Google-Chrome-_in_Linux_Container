*** Settings ***
Force Tags    meeting_chat  26_1  sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

Suite Setup     Disable the show meeting chat option     console=console_1
Suite Teardown    Run Keywords   Suite Failure Capture    AND   Enable the show meeting chat option   console=console_1

*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1:[Chat]Verify the chat option in P2P incoming call when show meeting chat is disabled in admin settings.
    [Tags]  380046   P1     sanity_sm
    [Setup]   Testcase Setup for shared User    count=2
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Verify that chat toggle button is not present   device=console_1
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
   [Teardown]   Run Keywords    Capture Failure  AND     Come back to home screen page   console_list=console_1      device_list=device_2

TC2:[Chat]Verify the chat option in P2P outgoing call when show meeting chat is disabled in admin settings.
    [Tags]      380049      P2
    [Setup]   Testcase Setup for shared User    count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Verify that chat toggle button is not present   device=console_1
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
   [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1      device_list=device_2

TC3:[Chat]Verify the chat option in Gallery mode when DUT user disables "show meeting chat" option from Admin settings.
    [Tags]      380053      P2
    [Setup]   Testcase Setup for shared User    count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify that chat toggle button is not present   device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
   [Teardown]   Run Keywords    Capture Failure  AND     Come back to home screen page   console_list=console_1      device_list=device_2

TC4:[Chat]Verify the chat option in Together mode when DUT user disables "show meeting chat" option from Admin settings.
    [Tags]      380057      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    change meeting mode     device=console_1    mode=together
    Verify together mode after switching       device=console_1
    verify changed mode  device=device_1      changed_mode=together_mode
    Verify that chat toggle button is not present   device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC5:[Chat]Verify the chat option in Front Row mode when DUT user disables "show meeting chat" option from Admin settings.
    [Tags]      380059      P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Change meeting mode     device=console_1    mode=front_row
    Verify that chat toggle button is not present   device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC6:[Chat]Verify the chat option when DUT user initiates meet now with TDC user & Show meeting chat should be disabled.
    [Tags]      380051      P2
    [Setup]   Testcase Setup for shared User     count=2
    Start meeting using meet now   from_device=console_1    to_device=device_2
    Accept incoming call   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Verify that chat toggle button is not present    device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC7:[Chat]Verify the chat option in Large Gallery mode when DUT user disables "show meeting chat" option from Admin settings.
    [Tags]      380055     P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    change meeting mode     device=console_1    mode=large_gallery
    Verify large gallery mode after switching      device=console_1
    verify changed mode  device=device_1      changed_mode=large_gallery
    Verify that chat toggle button is not present   device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC8:[Chat]Verify Chat UI is disappearing from Front Row Layout when User Disables Chat
    [Tags]      380077     P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Change meeting mode     device=console_1    mode=front_row
    Verify front row mode after disabeling the chat option      device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

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
