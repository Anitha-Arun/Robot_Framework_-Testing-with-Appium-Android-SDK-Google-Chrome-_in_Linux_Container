*** Settings ***
Documentation   Validating the functionality of Console Outgoing Calls
Force Tags    sm_outgoing_calls     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Outgoing Call] User calls to TDC from home screen dial pad
    [Tags]      315004   P1     sanity_sm
    [Setup]   Testcase Setup for shared User  count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect call     device=device_2
    Verify for call state     console_list=console_1     device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2: [Outgoing Call] Touch Console user calls TDC call number from more menu dialpad
    [Tags]      314998   P2
    [Setup]   Testcase Setup for shared User  count=2
    Make outgoing call from more menu dialpad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect the call      console=console_1
    Verify for call state     console_list=console_1     device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3:[Outgoing Call] DUT calls incorrect number.
    [Tags]      444713      P2
    [Setup]  Testcase Setup for shared User  count=1
    Dial incorrect number from dial pad    device=console_1
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

T4: [Outgoing Calls] DUT is pre-selected as a default calling
    [Tags]      315007  P2
    [Setup]    Testcase Setup for shared User  count=2
    Make outgoing call using dial pad    from_device=console_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Disconnect the call      console=console_1
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2


*** Keywords ***
Make outgoing call from more menu dialpad
    [Arguments]     ${from_device}      ${to_device}
    verify dialpad in more options      ${from_device}
    Make outgoing call using dial pad    ${from_device}     ${to_device}
