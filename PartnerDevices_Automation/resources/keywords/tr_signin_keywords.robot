*** Settings ***
Library     call_keywords
Library     tr_signin_keywords
Library     tr_home_screen_keywords

*** Variables ***

*** Keywords ***
Validate that signin is successfully completed
    [Arguments]     ${device_list}      ${state}
    Validate that signin successful  ${device_list}     ${state}

Validate rooms ui after signin
    [Arguments]  ${device}
    verify home page screen   ${device}
    tap on meet now and validate    ${device}
    tap on dialpad and validate    ${device}
    tap on more and validate    ${device}


















