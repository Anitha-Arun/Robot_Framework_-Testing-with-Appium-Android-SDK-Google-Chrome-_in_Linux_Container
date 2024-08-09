*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${5_minutes_wait_time} =  5 minutes
*** Test Cases ***
TC1:[Sign-in]User to sign-in from another device(web-sign-in)
    [Tags]    237611    P0      bvt_sm     sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=1
    Sign out method    device=device_1
    signin method with dcf code    device=device_1    user=meeting_user
    Verify home page screen   device=device_1
    Verify presence of Intents        device=device_1         feature=keycode         state=absent
   [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1

TC2:[ZTP][Sign-in] User to sign-in from another device (web sign-in) with DCF code
    [Tags]    263004    P0     bvt_sm     sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=1
    Sign out method    device=device_1
    ${old_dfc_code}=     fetch dfc code      device=device_1
    verify ztp signin ui    device=device_1
    Wait for Some Time    time=${5_minutes_wait_time}
    ${new_dfc_code}=     fetch dfc code      device=device_1
    Validate dfc code    ${old_dfc_code}    ${new_dfc_code}    device=device_1    status=different
    signin method with dcf code    device=device_1    user=meeting_user
    Validate that signin is successfully completed    device_list=device_1     state=Sign in
    Verify presence of Intents        device=device_1         feature=keycode         state=absent
    [Teardown]  Capture on Failure

*** Keywords ***
