*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Test Cases ***
TC1: [Meet now] Ending the call should redirect Teams App user to homescreen
    [Tags]   259705   P2        exclude_ftp_sm
    [Setup]   Testcase Setup for Meeting User    count=4
    Initiates conference meeting using Meet now option   from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_4
    Accept incoming call      device=device_4
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3,device_4    state=Connected
    Check video call On state   device_list=device_1,device_2,device_3,device_4
    End meeting   device=device_1
    Naviagte back to home screen page and validate    device=device_1
    End meeting   device=device_2,device_3,device_4
    Verify meeting state    device_list=device_1,device_2,device_3,device_4   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3,device_4

TC2: [Meet now] Participant count updates, when organizer adds the participant after meeting is started.
     [Tags]     322386        P2        exclude_ftp_sm
    [Setup]   Testcase Setup for Meeting User     count=4
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_4
    Accept incoming call      device=device_4
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2,device_3,device_4    state=Connected
    Check video call On state   device_list=device_1,device_2,device_3,device_4
    Verify list of participants     from_device=device_1      connected_device_list=device_1,device_2,device_3,device_4
    End meeting   device=device_1,device_2,device_3,device_4
    Verify meeting state    device_list=device_1,device_2,device_3,device_4   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3,device_4

TC3: [Report an Issue] Verify that user should be able to get report an issue option on Group call
    [Tags]   316583  P2     exclude_ftp_sm
    [Setup]   Testcase Setup for Meeting User    count=4
    Initiates conference meeting using Meet now option   from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen       device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_4
    Accept incoming call      device=device_4
    Close participants screen       device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3,device_4    state=Connected
    Check video call On state   device_list=device_1,device_2,device_3,device_4
    Verify Call State    device_list=device_1,device_2    state=Connected
    report an issue     device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2,device_3,device_4    state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC4: [Spotlight] Spotlight overrides the Pin in the meeting
    [Tags]  237965   p2     exclude_ftp_sm
    [Setup]    Testcase Setup for Meeting User   count=4
    Join Meeting        device=device_1,device_2,device_3,device_4     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3,device_4   state=Connected
    make a pin   from_device=device_1  to_device=device_3
    verify pin icon      device=device_1
    Close participants screen   device=device_1
    make a spotlight   from_device=device_2   to_device=device_4
    verify spotlight text on device   device=device_4   text=spotlight
    Close participants screen   device=device_2
    verify spotlight icon    device=device_3
    End meeting     device=device_1,device_2,device_3,device_4
    Verify meeting state    device_list=device_1,device_2,device_3,device_4    state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2,device_3,device_4


*** Keywords ***
Naviagte back to home screen page and validate
    [Arguments]     ${device}
    Come back to home screen     ${device}

Test Case Teardown
    [Arguments]     ${devices}
    Come back to home screen     ${devices}
