*** Settings ***
Library     tr_app_settings_keywords
Library     tr_settings_keywords
Library     tr_device_settings_keywords
Library     tr_call_keywords
Library     call_keywords
Library     tr_calendar_keywords
Resource    ../resources/keywords/common.robot


*** Keywords ***
Verify call state for video call
    [Arguments]     ${device_list}      ${state}
    Verify call mute state   ${device_list}     ${state}

Verify list of participants
    [Arguments]    ${from_device}    ${connected_device_list}
    Verify participant list     ${from_device}    ${connected_device_list}

Check video call On state
    [Arguments]     ${device_list}
    Verify video call state   ${device_list}     state=ON

Check video call Off state
    [Arguments]     ${device_list}
    Verify video call state    ${device_list}     state=OFF

Verify call state for audio call
    [Arguments]     ${device_list}      ${state}
    Verify call mute state   ${device_list}     ${state}

Make outgoing call with phonenumber
    [Arguments]     ${from_device}     ${to_device}
    Place a call    ${from_device}     ${to_device}    method=phone_number

Navigate to More menu option
     [Arguments]     ${device}
     Click on more option   ${device}

Verify participants list during call
    [Arguments]    ${device}
    Verify participants list in meeting   ${device}

Make outgoing call using auto dial
    [Arguments]     ${from_device}     ${to_device}
    Place a call    ${from_device}     ${to_device}    method=phone_number    dial_mode=auto_dial

Verify incoming call notification
    [Arguments]    ${device}
    Verify second incoming call      ${device}

Stop presenting whiteboard share screen
    [Arguments]    ${device}
    Click stop presenting whiteboard     ${device}

Verify video call state and validate
    [Arguments]     ${from_device}      ${to_device}
    ${status}     verify_device_video_call_support    ${to_device}
    Pass Execution if    '${status}' == 'fail'    ${to_device},  device doesn't support Video call
    Enable video call    device=${from_device}
    Verify video call state   device_list=device_1,device_3    state=ON

Auto dial incorrect number from dial pad
    [Arguments]     ${device}
    Dial incorrect number     ${device}    method=phone_number   dial_mode=auto_dial

Dial incorrect number from dial pad
    [Arguments]     ${device}
    Dial incorrect number     ${device}    method=phone_number

Close add participants roaster button
    [Arguments]      ${device}
    ${status}     verify_device_type    ${device}
    run keyword if  "${status}" == "norden"   run keyword   Close roaster button on participants screen   ${device}
    ...  ELSE   Log   Close roaster button on participants screen is not visible as device type is not norden

Make outgoing call with username
    [Arguments]     ${from_device}     ${to_device}
    Place a call    ${from_device}     ${to_device}    method=username

Make outgoing call with displayname
    [Arguments]     ${from_device}     ${to_device}
    Place a call    ${from_device}     ${to_device}    method=displayname
