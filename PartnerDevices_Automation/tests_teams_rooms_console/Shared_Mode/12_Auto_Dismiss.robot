*** Settings ***
Documentation   Validating the functionality of Auto dismiss Feature.
Force Tags    sm_auto_dismiss      sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Auto Dismiss] Verify call ended screen will disappear within 3 seconds
    [Tags]  315489   sanity_sm          P1
    [Setup]  Testcase Setup for shared User      count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect call     device=device_2
    Verify for call state     console_list=console_1     device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure   AND    Come back to home screen page   console_list=console_1     device_list=device_2

TC2: [Auto Dismiss] Touch console user to get rating screen after meeting
    [Tags]      315503   P2
    [Setup]   Testcase Setup for shared User      count=3
    Join a meeting   console=console_1     device=device_2,device_3     meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3    state=Connected
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state     console_list=console_1     device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1     device_list=device_2,device_3

TC3: [Auto Dismiss] Touch console user to get rating screen after incoming call
    [Tags]      315505    bvt_sm        sanity_sm
    [Setup]  Testcase Setup for shared User      count=2
    Place an outgoing call using dial pad    from_device=device_2     to_device=console_1:meeting_user
    Pick up incoming call    console=console_1
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect call     device=device_2
    Verify for call state     console_list=console_1     device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure   AND    Come back to home screen page   console_list=console_1     device_list=device_2

TC4: [Auto Dismiss] Touch console user to get rating screen after outgoing call
    [Tags]      315507   P2
    [Setup]  Testcase Setup for shared User      count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect the call      console=console_1
    Verify for call state     console_list=console_1     device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure   AND    Come back to home screen page   console_list=console_1     device_list=device_2

TC5: [Auto Dismiss] Verify the Dismiss button in rating screen
    [Tags]      315497      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User     count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect the call      console=console_1
    Verify for call state     console_list=console_1     device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure   AND    Come back to home screen page   console_list=console_1     device_list=device_2

TC6: [Auto Dismiss] Verify call decline screen auto dismissed within seconds
    [Tags]  315491   P1     sanity_sm
    [Setup]  Testcase Setup for shared User     count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Reject incoming call   device_list=device_2
    Verify call decline screen  device=console_1
    [Teardown]    Run Keywords    Capture Failure   AND   Come back to home screen page   console_list=console_1     device_list=device_2

*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}
