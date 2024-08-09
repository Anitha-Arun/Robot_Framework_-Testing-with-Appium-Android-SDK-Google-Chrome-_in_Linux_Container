*** Settings ***
Documentation    Suite description
Library     call_keywords
Library     settings_keywords
Library     device_settings_keywords
Resource    ../resources/keywords/common.robot

*** Keywords ***
Get device current TimeZone
    [Arguments]     ${device}
    ${tz_value}  Get device TimeZone    ${device}
    log     ${tz_value}
    [Return]  ${tz_value}

Get device TimeZone
    [Arguments]     ${device}
    ${tz_value}    get current timezone    ${device}
    Device Setting Back     ${device}
    Come back to home screen    ${device}
    [Return]  ${tz_value}

Change device TimeZone
    [Arguments]     ${device}   ${required_timezone}
    change timezone     ${device}    ${required_timezone}
    Device Setting Back     ${device}
    Come back to home screen    ${device}

Change device TimeFormat
    [Arguments]     ${device}   ${required_timeformat}
    change timeformat   ${device}    ${required_timeformat}
    Device Setting Back     ${device}
    Come back to home screen    ${device}

Enable device lock and set password
    [Arguments]     ${device}
    Enable lock device    ${device}     pin=123456
    Device Setting Back     ${device}
    Come back to home screen    ${device}

Disable device lock
    [Arguments]     ${device}
    disable lock device     ${device}   pin=123456
    Device Setting Back     ${device}
    Come back to home screen    ${device}

Navigate to device setting page
    [Arguments]     ${device}
    Open settings page   device=${device}
    Click device settings   device=${device}