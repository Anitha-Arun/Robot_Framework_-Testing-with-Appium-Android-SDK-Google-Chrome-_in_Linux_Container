*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Resource    ../resources/keywords/common.robot


*** Test Cases ***
TC1 : [Meetings]Verify that no meeting name is shown for All day meeting when "Show meeting names" option is disabled
    [Tags]  303656  p2
    [Setup]    Testcase Setup for Meeting User   count=1
    tap on all day meetings title bar and validate  device=device_1
    ${meeting_name_before_disabling_show_meeting_names}=  Get meeting name   device=device_1
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    hide or unhide meeting names     device=device_1   state=off
    Come back from admin settings page      device_list=device_1
    ${meeting_name_after_disabling_show_meeting_names}=  Get meeting name    device=device_1
    Verify meeting name on homescreen after disabling   device_1    ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}
    [Teardown]  Run Keywords    Capture on Failure  AND     Modify show meeting names option     device=device_1   state=on

TC2 : [Meetings] Verify meeting name on meeting detail screen when user enable & disable "Show meeting names"
    [Tags]  303658      P1
    [Setup]    Testcase Setup for Meeting User   count=1
    ${meeting_name_before_disabling_show_meeting_names}=  Get meeting name   device=device_1
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    hide or unhide meeting names     device=device_1   state=off
    Come back from admin settings page      device_list=device_1
    ${meeting_name_after_disabling_show_meeting_names}=  Get meeting name    device=device_1
    Verify meeting name on homescreen after disabling   device_1    ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    hide or unhide meeting names     device=device_1   state=on
    Come back from admin settings page      device_list=device_1
    ${meeting_name_after_disabling_show_meeting_names}=  Get meeting name    device=device_1
    verify meeting name on homescreen enabled state   device_1    ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}
    [Teardown]  Run Keywords    Capture on Failure      AND   Come back to home screen    device_list=device_1  AND  Modify show meeting names option     device=device_1   state=on

TC3 : [Meetings]Verify the meeting name show in calendar or notification when the "show meeting names" option enabled
    [Tags]     260630   bvt   bvt_sm   sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=1
    ${meeting_name_before_disabling_show_meeting_names}=  Get meeting name   device=device_1
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    hide or unhide meeting names     device=device_1   state=on
    Come back from admin settings page      device_list=device_1
    ${meeting_name_after_disabling_show_meeting_names}=  Get meeting name    device=device_1
    verify meeting name on homescreen enabled state   device_1    ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}
   [Teardown]  Run Keywords    Capture on Failure  AND     Modify show meeting names option     device=device_1   state=on

TC4 : [Meetings] Verify when user enable & disable "Show meeting names" toggle multiple times, changes must reflect accordingly
     [Tags]  303655   p2
     [Setup]    Testcase Setup for Meeting User   count=1
     repeat keyword  2 times     Enable and disable toggle button       device=device_1
     [Teardown]  Run Keywords    Capture on Failure  AND     Modify show meeting names option     device=device_1    state=on

TC5: [Meetings]Verify that while connecting meeting ,meeting name must be displayed
    [Tags]  260632    P2
    [Setup]  Testcase Setup for Meeting User    count=1
    ${meeting_name_before_disabling_show_meeting_names}=  Get meeting name    device=device_1
    Modify show meeting names option     device=device_1   state=off
    ${meeting_name_after_disabling_show_meeting_names}=  Get meeting name    device=device_1
    Verify meeting name on homescreen after disabling   device_1    ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}
    join rooms meeting after hiding the title name   device=device_1    organizer_name=device_1:meeting_user
    Verify meeting state   device_list=device_1   state=Connected
    End meeting   device=device_1
    Verify meeting state   device_list=device_1   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure     AND  Come back to home screen    device_list=device_1   AND  Modify show meeting names option     device=device_1   state=on

TC6: [Meetings]Verify the no meeting name showin in calander or notification
    [Tags]  260626      P2
    [Setup]  Testcase Setup for Meeting User    count=1
    ${meeting_name_before_disabling_show_meeting_names}=  Get meeting name    device=device_1
    Modify show meeting names option     device=device_1   state=off
    ${meeting_name_after_disabling_show_meeting_names}=  Get meeting name    device=device_1
    Verify meeting name on homescreen after disabling   device_1    ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}
    [Teardown]   Run Keywords    Capture on Failure   AND  Modify show meeting names option     device=device_1   state=on  AND  Come back to home screen    device_list=device_1

TC7: [Meetings]Verify that while connecting and after joined to meeting/all day meeting, meeting name must be displayed
    [Tags]  260628    bvt_sm        sanity_sm
    [Setup]  Testcase Setup for Meeting User    count=1
    ${meeting_name_before_disabling_show_meeting_names}=  Get meeting name    device=device_1
    Modify show meeting names option     device=device_1   state=off
    ${meeting_name_after_disabling_show_meeting_names}=  Get meeting name    device=device_1
    Verify meeting name on homescreen after disabling   device_1    ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}
    join rooms meeting after hiding the title name   device=device_1    organizer_name=device_1:meeting_user
    Verify meeting state   device_list=device_1   state=Connected
    End meeting   device=device_1
    Verify meeting state   device_list=device_1   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure     AND  Come back to home screen    device_list=device_1   AND  Modify show meeting names option     device=device_1   state=on

TC8:[Meetings]Verify the meeting name show in calendar or notification for the new scheduled meeting
    [Tags]     260631        bvt_sm      sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=1
    ${meeting_name_before_disabling_show_meeting_names}=  Get meeting name   device=device_1
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    hide or unhide meeting names     device=device_1   state=off
    Come back from admin settings page      device_list=device_1
    ${meeting_name_after_disabling_show_meeting_names}=  Get meeting name    device=device_1
    Verify meeting name on homescreen after disabling   device_1    ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}
    [Teardown]  Run Keywords    Capture on Failure      AND   Come back to home screen    device_list=device_1  AND     Modify show meeting names option     device=device_1    state=on    AND   Come back to home screen    device_list=device_1


*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

Modify show meeting names option
    [Arguments]       ${device}   ${state}
    Navigate to app settings page  ${device}
    navigate to meetings option in device settings page   ${device}
    hide or unhide meeting names    ${device}    ${state}
    Come back from admin settings page      device_list=${device}

Enable and disable toggle button
     [Arguments]     ${device}
     ${meeting_name_before_disabling_show_meeting_names}=  Get meeting name    ${device}
     Modify show meeting names option     ${device}      state=off
     ${meeting_name_after_disabling_show_meeting_names}=  Get meeting name     ${device}
     Verify meeting name on homescreen after disabling     ${device}    ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}
     Modify show meeting names option     ${device}      state=on
     ${meeting_name_before_disabling_show_meeting_names}=  Get meeting name     ${device}
     Verify meeting name on homescreen after disabling  ${device}   ${meeting_name_before_disabling_show_meeting_names}    ${meeting_name_after_disabling_show_meeting_names}


