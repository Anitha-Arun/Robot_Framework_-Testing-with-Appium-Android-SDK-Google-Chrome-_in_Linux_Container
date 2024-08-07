*** Settings ***
Force Tags    sm_spotlight  19_1    19    sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Test Cases ***
TC1 : [Spotlight] TDC user enable spotlight on the DUT user
    [Tags]  315212      bvt_sm  sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify video preview on screen  device=device_1
    Make a spotlight   from_device=device_2   to_device=console_1:meeting_user      device_type=console
    verify spotlight text on device   device=console_1     text=spotlight
    Close participants screen   device=device_2
    Verify spotlight icon on top left in the meeting  device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2 : [Spotlight] Spotlighted should end once the spotlighted user leave the meeting
    [Tags]  315216      bvt_sm  sanity_sm
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Make a spotlight   from_device=device_2   to_device=device_3
    verify spotlight text on device   device=device_3   text=spotlight
    Close participants screen   device=device_2
    verify spotlight icon on main screen in the meeting    device=device_1
    End meeting     device=device_3
    Join Meeting    device=device_3        meeting=console_lock_meeting
    spotlight icon should not present    device=device_3
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC3 : [Spotlight] Remove spotlight option should be displayed for spotlighted participant
    [Tags]      315214    P1        sanity_sm
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Make a spotlight   from_device=device_2   to_device=console_1:meeting_user      device_type=console
    verify spotlight text on device   device=console_1   text=spotlight
    Close participants screen   device=device_2
    Verifying and removing spotlight    device=console_1:meeting_user
    Verify spotlight icon disable       device=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC4 :[Spotlight] Avatar should be displayed on the screen if the video turned off during the spotlight
    [Tags]      315218      P1      sanity_sm
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3    state=Connected
    Verify and view list of participant    console=console_1
    Verify video preview on screen  device=device_1
    make a spotlight   from_device=device_2   to_device=device_3
    verify spotlight text on device   device=device_3   text=spotlight
    verify spotlight icon on main screen in the meeting    device=device_1
    Close participants screen   device=device_2
    disable video call   device=device_3
    verify spotlight icon    device=device_3
    Verify spotlight icon on top left in the meeting  device=device_3
    enable video call    device=device_3
    verify spotlight icon    device=device_3
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3


TC5 :[Spotlight] User clicking on spotlight icon there should be an option displayed to remove spotlight
    [Tags]      315226      P1
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify video preview on screen  device=device_1
    make a spotlight   from_device=device_2   to_device=console_1:meeting_user       device_type=console
    verify spotlight text on device   device=console_1   text=spotlight
    Close participants screen   device=device_2
    Verifying and removing spotlight    device=console_1:meeting_user
    Verify spotlight icon disable       device=console_1
    make a spotlight   from_device=device_2   to_device=device_3
    verify spotlight text on device   device=device_3   text=spotlight
    Close participants screen   device=device_2
    verify spotlight icon    device=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC6 :[Spotlight] TDC user spotlight the remote participant during meeting
    [Tags]      315220      P2
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify video preview on screen  device=device_1
    make a spotlight   from_device=device_2   to_device=console_1:meeting_user       device_type=console
    verify spotlight text on device   device=console_1   text=spotlight
    Close participants screen   device=device_2
    Verify spotlight icon on top left in the meeting  device=device_1
    remove spotlight from other user  from_device=device_2   to_device=console_1:meeting_user      device_type=console
    verify spotlight text on device   device=console_1   text=no_spotlight
    Close participants screen   device=device_2
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

