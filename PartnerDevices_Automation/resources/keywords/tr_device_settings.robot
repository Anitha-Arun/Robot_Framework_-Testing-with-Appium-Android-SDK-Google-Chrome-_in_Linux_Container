*** Settings ***
Library     tr_app_settings_keywords
Library     tr_settings_keywords
Library     tr_device_settings_keywords
Resource    ../resources/keywords/common.robot


*** Keywords ***
Navigate to device settings
    [Arguments]     ${device}
    Click on more option   device=${device}
    Click on settings page  device=${device}
    Click on device settings page  device=${device}

Verify user have option to navigate back to app settings
    [Arguments]     ${device}
    Verify back button   device=${device}

Click on reboot the device
    [Arguments]     ${device}
    restart the device  ${device}

Check device type and validate
    [Arguments]     ${device}
    ${status}     verify_device_type    ${device}
    Pass Execution if    '${status}' == 'null'    ${device}, device type is not norden
    Check device type   ${device}

Check device encryption state and validate
    [Arguments]     ${device}
    ${status}     verify_encryption_supported_device    ${device}
    Pass Execution if    '${status}' == 'unsupported'    ${device}, This device doesn't supports encryption
    Check device encryption state   ${device}