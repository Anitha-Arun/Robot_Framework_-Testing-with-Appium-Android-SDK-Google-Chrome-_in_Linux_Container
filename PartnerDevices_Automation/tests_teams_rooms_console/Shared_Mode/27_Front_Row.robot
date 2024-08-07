*** Settings ***
Force Tags    front_row    27     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***


*** Test Cases ***
TC1:[Front Row] Verify Front row option is present under Layout option on call control bar.
    [Tags]  380541    bvt_sm  sanity_sm
    [Setup]    Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify front row option     console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

#TC2:[Front Row] Verify Switch orientation toggle must be hidden when Front row is selected layout in a meeting.
#    [Tags]  380543  bvt_sm      sanity_sm
#    [Setup]   Testcase Setup for shared User   count=2
#    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
#    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
#    Verify switch orientation toggle hidden after taping on frontrow   device=console_1
#    End a meeting     console=console_1       device=device_2
#    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
#    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3: [Front Row] Verify Raise hands on the front row UI.
    [Tags]    380545    P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Change meeting mode     device=console_1    mode=front_row
    Verify front row mode      device=device_1
    Verify and select raise hand option  console=console_1
    Verify raise hand notification      device_list=device_2
    Verify highlighted raised hand in meeting        device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC4:[Front Row] Check for the Front row behavior at the Teams admin settings page
    [Tags]      382113        P2
    [Setup]   Testcase Setup for shared User     count=2
    Navigate to app settings screen     console=console_1
    Navigate to meeting and calling options from device settings page       console=console_1     option=meeting
    Enable front row toggle from device setting     device=console_1         default_state_layout=front_row
    Join meeting   device=device_2    meeting=console_lock_meeting
    Verify meeting state   device_list=device_2    state=Connected
    Add participant to the conversation using display name   from_device=device_2    to_device=console_1:meeting_user
    Accept incoming call      device=device_1
    Close participants screen   device=device_2
    Verify front row mode      device=device_1
    End a meeting       console=console_1       device=device_2
    Verify meeting state    device_list=device_2       state=Disconnected
    Enable front row toggle from device setting     device=console_1        default_state_layout=content_gallery
    come back from admin settings page      device_list=console_1
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC5:[Front Row] Verify Participant tray on the front row Layout.
    [Tags]    380546    P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Change meeting mode     device=console_1    mode=front_row
    Verify participant tray on front row layout     device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC6:[Front Row] Verify U-bar in the Meeting when user selects Front Row
    [Tags]    380549    P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Change meeting mode     device=console_1    mode=front_row
    Verify front row mode   device=device_1
    Verify docked ubar options      console=console_1
    Verify meeting info details in the meeting      console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC7:[Front row] Verify the Content when whiteboard is shared.
    [Tags]   380561     P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Change meeting mode     device=console_1    mode=front_row
    Verify front row mode   device=device_1
    Verify and click on white board sharing in call control bar   device=console_1
    Wait for Some Time    time=${wait_time}
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Stop presenting whiteboard share screen   device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC8:[Front Row] Verify Top bar in the meeting when DUT user selects Front Row Layout
    [Tags]   380548     P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Change meeting mode     device=console_1    mode=front_row
    Verify front row mode   device=device_1
    Verify the chat options in meeting      device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC9:[Front Row] Check for White board sharing in Front Row.
    [Tags]   382111     P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Change meeting mode     device=console_1    mode=front_row
    Verify front row mode   device=device_1
    Verify and click on white board sharing in call control bar   device=console_1
    Wait for Some Time    time=${wait_time}
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Verify front row mode   device=device_1
    Stop presenting whiteboard share screen   device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

Navigate to app settings screen
    [Arguments]   ${console}
    Tap on more option  ${console}
    Tap on settings page   ${console}

Verify participant tray on front row layout
    [Arguments]    ${device}
    Verify front row mode   ${device}

Verify and click on white board sharing in call control bar
        [Arguments]    ${device}
        Verify whiteboard sharing option under more option   ${device}
