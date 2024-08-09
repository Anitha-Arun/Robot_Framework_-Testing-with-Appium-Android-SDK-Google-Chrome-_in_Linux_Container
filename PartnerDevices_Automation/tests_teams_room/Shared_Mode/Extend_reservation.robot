*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

Suite Setup         Enable extend room reservation
Suite Teardown    Run Keywords   Suite Failure Capture    AND   Disable extend room reservation     device=device_1

*** Variables ***
${wait_time} =  3
${action_time} =  5

*** Test Cases ***
TC1: [Checkout and extend reservation] Verify extend reservation option is seen in More option when user joins the meeting
    [Tags]  332988     bvt_sm         sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2    meeting=extend_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify extend reservation in call more options  device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC2: [Checkout and extend reservation] Verify On Tapping the Extend reservation option, user should see a dialog with appropriate suggestions so that user can extend the reservation
    [Tags]   332990    bvt_sm      sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2   meeting=extend_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify extend reservation options   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC3: [Checkout and extend reservation] Verify the first suggestion should always be selected by default.
    [Tags]   332992     P1       sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2    meeting=extend_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify tick symbol at right side along with the confirm button      device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC4: [Checkout and extend reservation] Verify On clicking confirm, successful notification is seen at the bottom of the screen
    [Tags]   332993    P1       sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting        device=device_1,device_2    meeting=extend_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify tick symbol at right side along with the confirm button      device=device_1
    verify and extend reservation   device=device_1     time_in_minutes=30
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC5: [Checkout and extend reservation] Verify the meeting can be extended more than twice if the meeting room is the organizer
    [Tags]   332994  P1     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting        device=device_1,device_2    meeting=extend_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify and extend reservation   device=device_1     time_in_minutes=15
    verify and extend reservation   device=device_1     time_in_minutes=30
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC6: [Checkout and extend reservation] Verify the suggestions shown should be 15 minutes apart
    [Tags]   332999   P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting        device=device_1,device_2    meeting=extend_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Extend meeting suggestions should show 15min apart of time       device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC7:[Extend Reservation] Verify Extend reservation options are available under Meeting settings.
    [Tags]     379818    P2
    [Setup]    Testcase Setup for Meeting User   count=1
    Navigate to app settings page     device=device_1
    Navigate to meetings option in device settings page      device=device_1
    Verify extend room reservation option inside meeting settings       device=device_1
     Come back from admin settings page       device_list=device_1
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen    device_list=device_1

TC8:[Checkout and extend reservation] Verify the meeting can be extended more than twice if the meeting room is not the organizer.
    [Tags]   332995     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2       meeting=extend_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify and extend reservation   device=device_1     time_in_minutes=15
    verify and extend reservation   device=device_1     time_in_minutes=30
    verify and extend reservation   device=device_1     time_in_minutes=45
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC9:[Extend Reservation] Verify when user extends a meeting using meet now, it should show an error banner to the user.
    [Tags]   379820        P2
    [Setup]   Testcase Setup for Meeting User     count=2
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify error banner for extend meeting while using meetnow       device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen   device_list=device_1,device_2

TC10:[Checkout and Extend room reservation] User to check for the extend room reservation when user joined by using code.
    [Tags]    381969       P2
    [Setup]    Testcase Setup for Meeting User   count=1
    Join with an meeting id with extend meeting details   device=device_1
    Verify meeting state   device_list=device_1    state=Connected
    verify error banner for extend meeting while using meetnow       device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1
    Verify meeting state    device_list=device_1    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1



*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

Enable extend room reservation
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    extend room reservation toggle   device=device_1    state=on
    Come back from admin settings page    device_list=device_1

Disable extend room reservation
    [Arguments]     ${device}
    Navigate to app settings page     ${device}
    navigate to meetings option in device settings page      ${device}
    extend room reservation toggle   ${device}    state=off
    Come back from admin settings page    device_list=${device}