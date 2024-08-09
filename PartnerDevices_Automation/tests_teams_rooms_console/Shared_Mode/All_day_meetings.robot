*** Settings ***
Documentation   All day Meeting created as prerequisite before test execution
Force Tags    sm_meetings   sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Test Cases ***
TC1: [Landing Page] All-day meetings list should be display after tapping on the All-day title bar
    [Tags]      314944    bvt_sm        sanity_sm
    [Setup]  Testcase Setup for shared User     count=1
    Verify Home page options   console=console_1:meeting_user
    Tap on all day meetings title bar and validate   device=console_1
    Get meetings details present under all day title bar   device=console_1
    [Teardown]   Run Keywords    Capture Failure   AND   Navigate back to meetings   device=console_1   AND   Come back to home screen page   console_list=console_1

TC2: [Landing Page] All-day meetings should be displayed with highlighted background
    [Tags]      314946      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User     count=1
    Verify background display of all day meetings    device=console_1
    [Teardown]   Run Keywords    Capture Failure  AND   Navigate back to meetings   device=console_1   AND   Come back to home screen page   console_list=console_1

TC3: [Landing Page] DUT should navigate back to meetings when DUT user tap on All-day meeting title bar
    [Tags]      314948    P1        sanity_sm
    [Setup]  Testcase Setup for shared User     count=1
    Verify Home page options   console=console_1:meeting_user
    Tap on all day meetings title bar and validate   device=console_1
    Get meetings details present under all day title bar   device=console_1
    [Teardown]   Run Keywords    Capture Failure  AND   Navigate back to meetings   device=console_1    AND  Come back to home screen page   console_list=console_1

TC4: [Landing Page]All-day meeting tittle should be hide when there are no All-day meetings
    [Tags]      314942   P1
    [Setup]  Testcase Setup for shared User       count=1
    Verify Home page options   console=console_1:meeting_user
    Tap on all day meetings title bar and validate   device=console_1
   [Teardown]   Run Keywords   Capture Failure  AND  Navigate back to meetings   device=console_1    AND  Come back to home screen page   console_list=console_1

TC5: [Meetings]Verify that while connecting and after joined to meeting/all-day meeting, meeting name must be displayed
    [Tags]      315533   bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User    count=1
    ${before_toggle_show_meeting_names}=    Get meeting details    console=console_1
    Navigate to show meeting names page     console=console_1
    ${after_toggle_show_meeting_names}=     Get meeting details    console=console_1
    run keyword if   '${before_toggle_show_meeting_names}' != '${after_toggle_show_meeting_names}'   Log   Meeting name is showing as the meeting organizer name
    ...  ELSE  fail   Meeting is not showing the name of organizer.
    Join the meeting     console=console_1     organizer_name=console_1:meeting_user
    Verify for call state      console_list=console_1       state=Connected
    End the meeting   console=console_1
    Verify for call state   console_list=console_1      state=Disconnected
    Tap on all day meetings title bar and validate   device=console_1
    Join the meeting     console=console_1     organizer_name=console_1:meeting_user
    Verify for call state      console_list=console_1       state=Connected
    End the meeting   console=console_1
    Verify for call state   console_list=console_1      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND   Navigate back to meetings   device=console_1    AND     Come back to home screen page   console_list=console_1     AND     Enable show meeting names toggle btn    console=console_1


*** Keywords ***
Verify Home page options
    [Arguments]     ${console}
    validate user details along with home screen options        ${console}

Navigate to app settings screen
    [Arguments]   ${console}
    Tap on more option  ${console}
    Tap on settings page   ${console}

Navigate to show meeting names page
    [Arguments]       ${console}
    Navigate to app settings screen    ${console}
    Navigate to meeting and calling options from device settings page       ${console}  option=meeting
    Disable show meeting names toggle btn   ${console}
    come back from admin settings page      device_list=${console}

Enable show meeting names toggle btn
    [Arguments]    ${console}
    Navigate to app settings screen    ${console}
    Navigate to meeting and calling options from device settings page       ${console}  option=meeting
    Enable show meeting names toggle button    ${console}
    come back from admin settings page      device_list=${console}
