*** Settings ***
Library     tr_background_change_keywords
Library     tr_call_keywords
Library     call_keywords
Library     tr_calendar_keywords
Library     calendar_keywords
Library     settings_keywords
Resource    ../resources/keywords/common.robot

*** Variables ***
${five_seconds} =   5

*** Keywords ***
Select background change
     [Arguments]     ${device}
     Choose background change     ${device}     option=teams_beach_background

Change to default no background option
    [Arguments]     ${device}
    Choose background change     ${device}     option=no_background

Select other background change from options
     [Arguments]     ${device}
     Choose background change     ${device}     option=teams_home_background

Choose blur background option
     [Arguments]     ${device}
     Choose background change      ${device}          option=blur_background
     Get background effect    ${device}
     Wait for Some Time    time=${five_seconds}
     get_screenshot     name=verify_blur_background    device_list=${device}

Verify selected background
    [Arguments]     ${device}
    get_screenshot     name=verify_background_change    device_list=${device}

Verify background change under more option
    [Arguments]     ${device}
    ${status}     verify_background_change_support_device    ${device}
    Pass Execution if    '${status}' == 'fail'    ${device}, Device doesn't supports background change option, so aborting the test execution.

Change to default No background screen
     [Arguments]    ${device}
     Select no background option    ${device}
     Get background effect    ${device}