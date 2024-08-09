*** Settings ***
Library     tr_app_settings_keywords
Library     tr_settings_keywords
Library     tr_call_keywords
Library     call_keywords
Library     tr_console_call_keywords
Library     tr_console_home_screen_keywords
Resource    ../resources/keywords/common.robot

*** Keywords ***
Make outgoing call using dial pad
    [Arguments]     ${from_device}     ${to_device}
    Make a call     ${from_device}     ${to_device}    method=phone_number

Make outgoing call using auto dial from dial pad
    [Arguments]     ${from_device}     ${to_device}
    Make a call     ${from_device}     ${to_device}    method=phone_number    dial_mode=auto_dial

Place an outgoing call using dial pad
    [Arguments]     ${from_device}     ${to_device}
    Make a call     ${from_device}     ${to_device}    method=phone_number   device_type=console

Place a video call using display name
    [Arguments]       ${from_device}     ${to_device}
    ${status}     Verify device video call support    ${from_device}
    Pass Execution if    '${status}' == 'fail'    ${from_device}, This device doesn't support Video call so aborting the execution.
    Make video call   ${from_device}    ${to_device}    method=display_name    device_type=console

Verify should not autodial the emergency number
    [Arguments]     ${console}
    Auto dial emergency num      ${console}

Make outgoing call with username using dial pad
    [Arguments]     ${from_device}     ${to_device}
    Make a call     ${from_device}     ${to_device}    method=username
