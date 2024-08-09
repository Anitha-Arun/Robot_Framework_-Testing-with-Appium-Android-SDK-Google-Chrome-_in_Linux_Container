*** Settings ***
Library     tr_call_keywords
Library     call_keywords
Library     tr_console_call_keywords
Library     tr_console_calendar_keywords
Resource    ../resources/keywords/common.robot

*** Keywords ***
Verify for meeting state
    [Arguments]     ${console_list}     ${device_list}      ${state}
    Verify for call state    ${console_list}   ${device_list}    ${state}

End the meeting
    [Arguments]      ${console}
    Disconnect the call   ${console}

Start meeting using meet now
    [Arguments]    ${from_device}     ${to_device}
    Start meet now meeting   ${from_device}     ${to_device}    method=display_name

Add participant to the conversation using display name
    [Arguments]   ${from_device}     ${to_device}
    Add participant to the conversation   ${from_device}     ${to_device}   method=display_name

Add participant to the conversation using phonenumber
    [Arguments]   ${from_device}     ${to_device}
    Add participant to the conversation   ${from_device}     ${to_device}   method=phone_number

Verify and view list of participant in meeting
    [Arguments]     ${console}
    Verify and view list of participant     ${console}

Disable show meeting names toggle btn
    [Arguments]     ${console}
    Validate the functionality of meeting names toggle btn   ${console}   state=OFF

Enable show meeting names toggle button
    [Arguments]     ${console}
    Validate the functionality of meeting names toggle btn   ${console}   state=ON

Verify lock meeting state
    [Arguments]    ${console_list}
    Verify for lock meeting visibility    ${console_list}   state=lock_meeting

Verify unlock meeting state
    [Arguments]    ${console_list}
    Verify for lock meeting visibility   ${console_list}   state=unlock_meeting

Start meeting using DID
    [Arguments]    ${from_device}     ${to_device}
    Start meet now meeting   ${from_device}     ${to_device}    method=phone_number
