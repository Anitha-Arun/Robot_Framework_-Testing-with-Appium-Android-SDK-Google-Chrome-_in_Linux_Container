*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_for_time}=  3

*** Test Cases ***
# Test obsolete, new cases for new report and isssue will be added
#TC1: [App settings] User checks 'Report an issue' option in app settings
#    [Tags]  237729  bvt_sm    sanity_sm     bvt_sm_app_settings
#    [Setup]  Testcase Setup for Meeting User   count=1
#    Navigate to app settings page    device=device_1
#    Report an issue  device=device_1
#    [Teardown]   Run Keywords    Capture on Failure   AND    App Setting Teardown     device=device_1

TC2: [App settings] DUT user checks the about option in app settings
    [Tags]  237727  P1    sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=1
    Navigate to app settings page    device=device_1
    Verify about page  device=device_1
    Click back btn    device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    App Setting Teardown   device=device_1

TC3: [App settings] User should have the option to navigate to device settings
    [Tags]  237730   P1
    [Setup]  Testcase Setup for Meeting User   count=1
    Navigate to device settings page   device=device_1
    Come back from admin settings page   device_list=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1

TC4: [App settings] User checks there is no help option in Sign in screen and app settings
    [Tags]      313034  P1
    [Setup]  Testcase Setup for Meeting User   count=1
    Sign out method    device=device_1
    Verify no help option on sign in screen     device=device_1
    Sign in method     device=device_1     user=meeting_user
    verify no help option on app settings   device=device_1
    [Teardown]   Run Keywords    Capture on Failure   AND    Come back to home screen   device_list=device_1

TC5:[App Settings] Teams App User to see the terms of use
    [Tags]  312850  P2
    [Setup]  Testcase Setup for Meeting User   count=1
    Navigate to about page   device=device_1
    verify microsoft software license terms  device=device_1
    Click back btn    device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    App Setting Teardown   device=device_1

TC6: [App Settings] Teams App User to view the third-party Notices of use
    [Tags]  312849  P2
    [Setup]  Testcase Setup for Meeting User   count=1
    Navigate to about page   device=device_1
    verify third party software and information     device=device_1
    Click close btn    device_list=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1

TC7: [App Settings] Teams app user to see and define Privacy and cookies
    [Tags]    312855    P2
    [Setup]  Testcase Setup for Meeting User   count=1
    Navigate to about page     device=device_1
    verify privacy cookies     device=device_1
    Click close btn    device_list=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND   Come back to home screen    device_list=device_1




*** Keywords ***
App Setting Teardown
    [Arguments]     ${device}
    Click close btn    device_list=${device}
    Come back to home screen    device_list=${device}

Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

Navigate to device settings page
    [Arguments]     ${device}
    Click on more option   device=${device}
    Click on settings page  device=${device}
    click on device settings page    device=${device}
    Wait for Some Time    time=${wait_for_time}

Navigate to about page
     [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}
    click on about page  ${device}
