*** Settings ***
Library     calendar_keywords
Library     call_keywords

*** Variables ***


*** Keywords ***
Verify meeting state
    [Arguments]     ${device_list}      ${state}
    Verify Call State    ${device_list}     ${state}

End meeting
    [Arguments]     ${device}
    Disconnect call    ${device}

Verify meeting Mute State
    [Arguments]     ${device_list}      ${state}
    Verify Call mute State    ${device_list}     ${state}

Mutes the meeting
    [Arguments]     ${device}
    Mutes the phone call    ${device}

Unmutes the meeting
    [Arguments]     ${device}
    Unmutes the phone call    ${device}

Add participant to conversation using display name
    [Arguments]     ${from_device}      ${to_device}
    add participant to conversation      ${from_device}      ${to_device}    method=display_name

Add participant to conversation using phonenumber
    [Arguments]     ${from_device}     ${to_device}
    add participant to conversation      ${from_device}      ${to_device}    method=phone_number

Verify invited user list in Meeting Details
    [Arguments]     ${from_device}     ${participants}
    verify_invited_user_list_in_meeting     ${from_device}     ${participants}

Verify meeting object for new user
    [Arguments]     ${device}
    run keyword and ignore error  verify calendar empty   ${device}

Add participant to conversation using extension
    [Arguments]     ${from_device}     ${to_device}
    add participant to conversation      ${from_device}      ${to_device}    method=extension

Enable show meeting names
    [Arguments]     ${device}
    Come back to home screen    ${device}
    Verify meetings option under App settings page   ${device}
    Enable show meeting names option    ${device}
    Come back to home screen    ${device}

Disable show meeting names
    [Arguments]     ${device}
    Come back to home screen    ${device}
    Verify meetings option under App settings page   ${device}
    Disable show meeting names option    ${device}
    Come back to home screen    ${device}

Verify whiteboard sharing option under more option for ipphone
    [Arguments]     ${device}
    ${status}     verify_device_whiteboard_sharing_option_support    ${device}
    Pass Execution if    '${status}' == 'fail'    ${device}, device dosn't support WhiteBoard Sharing so aborting the test execution.

verify cancelled meetings on home screen for cnf device
     [Arguments]     ${device}
     ${status}     verify cancelled meetings appearance on home screen for cnf device    ${device}
     Pass Execution if    '${status}' == 'fail'    ${device}, Portrait Mode Conference devices don't show Cancelled Meetings on Home Screen

resume the meeting
    [Arguments]     ${device}
    resume the call     ${device}