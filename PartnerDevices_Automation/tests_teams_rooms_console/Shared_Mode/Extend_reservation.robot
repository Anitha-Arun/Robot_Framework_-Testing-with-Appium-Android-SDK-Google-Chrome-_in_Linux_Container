*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Force Tags    sm_extend_meeting_reservation     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

Suite Setup         Enable extend room reservation toggle btn
Suite Teardown    Run Keywords   Suite Failure Capture    AND   Disable extend room reservation toggle btn     console=console_1

*** Test Cases ***
TC1:[Checkout and Extend Reservation] Verify extend reservation option is seen in More option when user joins the meeting .
    [Tags]   333005     bvt_sm      sanity_sm
    [Setup]    Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify extend reservation in call more options  device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC2: [Checkout and extend reservation] Verify On Tapping the Extend reservation option, user should see a dialog with appropriate suggestions so that user can extend the reservation
     [Tags]   333007    P1      sanity_sm
    [Setup]    Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify extend reservation options   device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC3:[Checkout and Extend Reservation] Verify On clicking confirm, successful notification is seen at the bottom of the screen
    [Tags]   333011    P1       sanity_sm
    [Setup]    Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and extend reservation   device=console_1     time_in_minutes=30
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC4:[Checkout and Extend Reservation] Verify the meeting can be extended more than twice if the meeting room is the organizer
    [Tags]   333012     P1         sanity_sm
    [Setup]    Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2:norden    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and extend reservation   device=console_1    time_in_minutes=15
    Verify and extend reservation   device=console_1     time_in_minutes=30
    Verify and extend reservation   device=console_1     time_in_minutes=45
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC5:[Checkout and Extend Reservation] Verify the first suggestion should always be selected by default.
    [Tags]   333009     P2
    [Setup]    Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify tick symbol at right side along with the confirm button      device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC6:[Checkout and Extend Reservation] Verify the meeting can be extended more than twice if the meeting room is not the organizer.
    [Tags]   333013     P2
    [Setup]    Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    verify and extend reservation   device=console_1     time_in_minutes=15
    verify and extend reservation   device=console_1     time_in_minutes=30
    verify and extend reservation   device=console_1     time_in_minutes=45
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC7:[Extend Reservation] Verify when user extends a meeting using meet now, it should show an error banner to the user.
    [Tags]     379923    P2
    [Setup]    Testcase Setup for shared User   count=1
    Verify precall screen after clicking on meetnow     device=device_1     console=console_1
    Verify error banner for extend meeting while using meetnow     device=console_1
    End the meeting     console=console_1
    Verify for call state    console_list=console_1      state=Disconnected
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC8:[Extend Reservation] Verify checkout and extend reservation options are available under Meeting settings.
    [Tags]     379921    P2
    [Setup]    Testcase Setup for shared User   count=1
    Navigate to app settings screen     console=console_1
    Navigate to meeting and calling options from device settings page       console=console_1  option=meeting
    Verify extend room reservation option inside meeting settings       device=console_1
    Navigate back from metting settings page        console=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC9: [Checkout and extend reservation] Verify the suggestions shown should be 15 minutes apart
    [Tags]   333010   P2
    [Setup]    Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Extend meeting suggestions should show 15min apart of time       device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

*** Keywords ***
Enable extend room reservation toggle btn
    Navigate to app settings screen     console=console_1
    Navigate to meeting and calling options from device settings page       console=console_1  option=meeting
    extend room reservation toggle    device=console_1    state=on
    come back from admin settings page      device_list=console_1

Disable extend room reservation toggle btn
    [Arguments]       ${console}
    Navigate to app settings screen    ${console}
    Navigate to meeting and calling options from device settings page       ${console}  option=meeting
    extend room reservation toggle      device=${console}       state=off
    come back from admin settings page      device_list=${console}

Navigate to app settings screen
    [Arguments]   ${console}
    Tap on more option  ${console}
    Tap on settings page   ${console}

End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

Navigate back from metting settings page
    [Arguments]    ${console}
    device setting back btn     ${console}
    Click on back layout btn   ${console}
    Come back to home screen page   console_list=${console}

Navigating back to home page
    [Arguments]     ${console}
    Click on close button    console_list=${console}
    Click on back layout btn   ${console}
