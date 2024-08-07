*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Test Cases ***
TC1 : Verify that DUT user able to access "What's new" page under the settings.
    [Tags]  344932      bvt     bvt_sm      sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=1
    Navigate to about page   device=device_1
    verify whats new in privacy cookies    device=device_1
    navigate back to more option page        device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1

TC2 : Verify that DUT user able to access "Privacy & Cookies" page under About in settings.
    [Tags]  345017  p1    sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=1
    Navigate to about page     device=device_1
    verify whats new in privacy cookies     device=device_1
    verify that unable to open external links privacy cookies     device=device_1
    navigate back to more option page     device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1

TC3: Verify that DUT user able to access "Terms of Use" page under About in settings.
    [Tags]  345018   p0     bvt     bvt_sm      sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=1
     Navigate to about page     device=device_1
     verify terms of use option   device=device_1
     verify that unable to open external links in terms of use  device=device_1
     navigate back to more option page      device=device_1
     [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1

TC4: Verify that DUT should not have "Connected Experiences" option under About in settings.
     [Tags]  345019   p1          sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=1
     Navigate to about page     device=device_1
     verify about page and connected experiences is not present in about page     device=device_1
     navigate back to more option page       device=device_1
     [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1

TC5: Verify that DUT user should be able to accept the call/meeting in "What's new" page under the settings.
     [Tags]  345020   p2
    [Setup]  Testcase Setup for Meeting User   count=2
    Navigate to about page     device=device_1
    whats new in privacy and cookies page    device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    navigate back to more option page       device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1

TC6:Verify that DUT user should be able to answer the call/meeting from "Privacy & Cookies" page under About in settings.
    [Tags]  345021   p2
    [Setup]  Testcase Setup for Meeting User   count=2
    Navigate to about page     device=device_1
    whats new in privacy and cookies page   device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    navigate back to more option page       device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1

TC7: Verify that DUT user should be able to answer the call/meetng from "Terms of Use" page under About in settings.
     [Tags]  345022   p2
    [Setup]  Testcase Setup for Meeting User   count=2
    Navigate to about page     device=device_1
    verify terms of use option   device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    navigate back to more option page       device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_2

TC8: Verify that DUT user should be able to access "Third party software notices and information" page under About in settings.
    [Tags]  345023   p1     sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=1
    Navigate to about page   device=device_1
    verify third party software and information     device=device_1
    navigate back to more option page       device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1

TC9: Verify that DUT user should be able answer a call/meeting from "Third party software notices and information" page under About in settings.
     [Tags]  345024   p1     sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=2
    Navigate to about page   device=device_1
    third party software and information in about page     device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    navigate back to more option page       device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1

*** Keywords ***
Come back to main page
    [Arguments]     ${device}
    Click close btn    device_list=${device}
    device right corner click   ${device}
    Come back to home screen    device_list=${device}
    device right corner click   ${device}

Navigate to about page
     [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}
    click on about page  ${device}

whats new in privacy and cookies page
    [Arguments]     ${device}
    verify whats new in privacy cookies  ${device}

