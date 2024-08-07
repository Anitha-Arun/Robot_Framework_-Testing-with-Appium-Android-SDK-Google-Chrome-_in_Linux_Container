*** Settings ***
Library     call_keywords
Library     settings_keywords
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  15
${30wait_time} =  30

*** Keywords ***
Make outgoing call using display name
    [Arguments]     ${from_device}      ${to_device}
    Place call      ${from_device}      ${to_device}    method=display_name

Make outgoing call using phonenumber
    [Arguments]     ${from_device}     ${to_device}
    Place call      ${from_device}      ${to_device}    method=phone_number

Make outgoing call using extension number
    [Arguments]     ${from_device}     ${to_device}
    Place call      ${from_device}      ${to_device}    method=extension_number

Make outgoing call using username
    [Arguments]     ${from_device}      ${to_device}
    Place call      ${from_device}      ${to_device}    method=username

Blindtransfers the call using display name
    [Arguments]     ${from_device}      ${to_device}
    Blindtransfers the call      ${from_device}      ${to_device}    method=display_name

Blindtransfers the call using phonenumber
    [Arguments]     ${from_device}      ${to_device}
    Blindtransfers the call      ${from_device}      ${to_device}    method=phone_number

Make outgoing call using privateline number
    [Arguments]     ${from_device}     ${to_device}
    Place call      ${from_device}      ${to_device}    method=privateline_number

Consult first to transfer the call using display name
    [Arguments]     ${from_device}      ${to_device}
    Consult first to transfer the call      ${from_device}      ${to_device}    method=display_name

Consult first to transfer the call using phonenumber
    [Arguments]     ${from_device}      ${to_device}
    Consult first to transfer the call      ${from_device}      ${to_device}    method=phone_number

Escalating to conference call by using display name
    [Arguments]     ${from_device}      ${to_device}
    Escalating to conference call      ${from_device}      ${to_device}    method=display_name

Escalating to conference call by using phonenumber
    [Arguments]     ${from_device}      ${to_device}
    Escalating to conference call      ${from_device}      ${to_device}    method=phone_number

get first call participant name
    [Arguments]     ${device}
    ${participant_name}    get_call_participant_name      ${device}
    log   ${participant_name}
    [Return]    ${participant_name}

get first call duration
    [Arguments]     ${device}
    ${call_duration}    get_call_duration      ${device}
    log   ${call_duration}
    [Return]    ${call_duration}

call park and get the code
    [Arguments]     ${device}
    click_call_park      ${device}
    ${call_park_code}=    get_call_park_code      ${device}
    [Return]    ${call_park_code}

validate call duration or missed call
    [Arguments]     ${device}
    navigate_to_calls_tab   ${device}
    ${device_call_duration}=    get first call duration    ${device}
    ${sec_check_status}=    check_sec_in_call_duration    ${device_call_duration}
    run keyword if  '${device_call_duration}' == 'Missed call'    Should match    '${sec_check_status}'    'False'
    ...   ELSE   Should match    '${sec_check_status}'    'True'

Dial emergency num and validate
    [Arguments]     ${device}
    Dial emergency num      ${device}
    Wait for Some Time    time=${wait_time}
    Verify emergency call state     ${device}    state=Connected

Make Video call using display name
    [Arguments]     ${from_device}      ${to_device}
    ${status}     verify_device_video_call_support    ${from_device}
    Pass Execution if    '${status}' == 'fail'    ${from_device}, device dosn't support Video call
    Place video call      ${from_device}      ${to_device}    method=display_name

Make Video call using phonenumber
    [Arguments]     ${from_device}      ${to_device}
    ${status}     verify_device_video_call_support    ${from_device}
    Pass Execution if    '${status}' == 'fail'    ${from_device}, device dosn't support Video call
    Place video call      ${from_device}      ${to_device}    method=phone_number

Verify calls object for new user
    [Arguments]     ${device}
    run keyword and ignore error  Verify no calls object display for new user   ${device}

Verify floating Dialpad
    [Arguments]     ${device}
    verify_dialpad_in_call_control  ${device}

Validate Transfer for Emergency Calling
    [Arguments]     ${device}
    verify_call_more_option_for_emergency_call  ${device}

Validate Call Park for Emergency Calling  
    [Arguments]     ${device}
    verify_call_more_option_for_emergency_call  ${device}

Verify UI return to home screen
    [Arguments]         ${device}
    Come back to home screen    device_list=${device}

Dialing incorrect number
    [Arguments]     ${device}
    Dial an incorrect number     ${device}    method=phonenumber

Wait time to receive the bad_number announcement
    [Arguments]     ${time}
    Sleep       ${time}

Verify call decline message on UI
    [Arguments]     ${device}
    verify_call_decline_screen  ${device}

verify notification call
    [Arguments]     ${device}
    Verify call notification    ${device}   status=appear

verify outgoing call from PSTN to CQ
    [Arguments]     ${device}
    verify call state   ${device}     state=connected

Tap to return to call
    [Arguments]     ${device}
    tap to return to meeting  ${device}

Initiate OBO call using display name
    [Arguments]     ${from_device}      ${to_device}    ${obo_option}
    Place call      ${from_device}      ${to_device}    method=display_name   obo_option=${obo_option}

Consult transfer OBO call using display name
    [Arguments]     ${from_device}      ${to_device}    ${obo_option}
    Consult first to transfer the call      ${from_device}      ${to_device}    method=display_name    obo_option=${obo_option}

Initiate OBO call and verify boss list
    [Arguments]     ${from_device}      ${to_device}    ${obo_option}    ${boss_list}
    Place call      ${from_device}      ${to_device}    method=display_name   obo_option=${obo_option}     boss_list=${boss_list}