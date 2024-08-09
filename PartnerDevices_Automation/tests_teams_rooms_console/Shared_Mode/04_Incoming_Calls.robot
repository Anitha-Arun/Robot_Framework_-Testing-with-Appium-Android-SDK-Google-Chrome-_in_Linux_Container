*** Settings ***
Documentation  Validating the functionality of Console Incoming Calls
Force Tags   sm_Incoming_calls     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Incoming Call] Audio call to DUT
    [Tags]      314984   bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User   count=2
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2 : [Incoming Call] Video call to DUT
    [Tags]      314982   bvt_sm     sanity_sm
    [Setup]    Testcase Setup for shared User   count=2
    Place a video call using display name   from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Close participants screen   device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    End a meeting      console=console_1    device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3 : [Incoming Call] Touch Console does not answer the incoming call
    [Tags]  314988   P1     sanity_sm
    [Setup]    Testcase Setup for shared User   count=2
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Disconnect the call      console=console_1
    Come back to home screen page   console_list=console_1   device_list=device_2
    Place a video call using display name   from_device=device_2     to_device=console_1:meeting_user
    Disconnect the call      console=console_1
    Close participants screen   device=device_2
    Disconnect call     device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC4 : [Second incoming call] DUT should not get second incoming call
    [Tags]  315019      bvt_sm     sanity_sm
    [Setup]    Testcase Setup for shared User   count=3
    Place a video call using display name   from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Close participants screen   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Place an outgoing call using dial pad    from_device=device_3     to_device=console_1:meeting_user
    Verify user not to get second incoming call     console=console_1
    Disconnect call     device=device_3
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    End a meeting      console=console_1    device=device_2
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC5: [Incoming Call] Touch console user must be able to pick the incoming call on "Admin Only (Enter Password)"
    [Tags]  322308      P2
    [Setup]    Testcase Setup for shared User   count=3
    Navigate to more button and settings page    console=console_1
    Navigate to admin only enter password page      console=console_1
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect the call      console=console_1
    Navigate to admin only enter password page      console=console_1
    Place a video call using display name   from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect the call      console=console_1
    Come back to landing page   console=console_1
    [Teardown]   Run Keywords    Capture Failure  AND    Verify for call state     console_list=console_1    device_list=device_2    state=Disconnected    AND  Come back to home screen page   console_list=console_1   device_list=device_2

TC6: [Incoming Call] Touch Console declines the incoming call
    [Tags]  314986      P2
    [Setup]    Testcase Setup for shared User   count=2
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    Place a video call using display name   from_device=device_2     to_device=console_1:meeting_user
    Disconnect the call      console=console_1
    Close participants screen   device=device_2
    Disconnect call     device=device_2
    Verify for call state      console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2


*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    Disconnect the call  ${console}
    Disconnect call     ${device}

Navigate to more button and settings page
    [Arguments]     ${console}
    Tap on more option  ${console}
    Tap on settings page   ${console}

Come back to landing page
    [Arguments]     ${console}
    Click on close button    console_list=${console}
    Click on back layout btn   ${console}
