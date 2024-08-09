*** Settings ***
Resource    ../resources/keywords/common.robot
Library      tr_app_settings_keywords
Library      tr_home_screen_keywords
Library      tr_settings_keywords
Library     tr_call_keywords

*** Keywords ***
Navigate to app settings
    [Arguments]     ${device}
    Click on more option   ${device}

Verify provide option to access when click on ellipsis
    [Arguments]     ${device}
    Click on more option   ${device}
    Verify available option to access when clicked on ellipsis  ${device}

Verify home page screen after reboot
    [Arguments]     ${device}
    Verify home page screen   ${device}

Navigate to setting page and verify options present inside
    [Arguments]     ${device}
    View app settings options   ${device}
    Verify option inside settings page   ${device}

Verify About page option
    [Arguments]     ${device}
    Verify about page  ${device}
    Click back btn    ${device}

Verify more option reflected on landing page
    [Arguments]     ${device}
    Verify home page screen  ${device}

Dial number from dial pad
    [Arguments]     ${from_device}     ${to_device}
    Place a call    ${from_device}     ${to_device}    method=phone_number

End Call
    [Arguments]     ${device_list}
    Reject incoming call   ${device_list}

Verify more option present on home screen
    [Arguments]     ${device}
    Verify home page screen   ${device}

Get meetings details present under all day title bar
    [Arguments]     ${device}
    Verify meeting display on home screen   ${device}

Navigate to dial pad on home screen
    [Arguments]     ${device}
    click on dial pad   ${device}

Auto dial emergency number and validate
    [Arguments]     ${device}
    Dial emergency num      ${device}
    Wait for Some Time    time=${wait_time}
    Verify emergency call state     ${device}    state=Connected

Navigate to more button and validate options
    [Arguments]     ${device}
    Click on more option   ${device}
    Verify app settings options   ${device}

Navigate to settings page and verify options
    [Arguments]     ${device}
    Click on settings page    ${device}
    Verify option inside settings page  ${device}

