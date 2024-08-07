*** Settings ***
Documentation   All day Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Test Cases ***
TC1: [Landing Page] All-day meetings should be displayed with highlighted background
    [Tags]  238038    bvt   bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=1
    Verify background display of all day meetings    device=device_1
    [Teardown]  Run Keywords   Capture on Failure  AND   Navigate back to meetings   device=device_1  AND   Come back to home screen    device_list=device_1

TC2: [Landing Page] DUT should navigate back to meetings when DUT user tap on All-day meeting title bar
    [Tags]  238039    P1    sanity_sm
    [Setup]  Testcase Setup for Meeting User      count=1
    Verify default option present on landing page and validate   device=device_1
    Tap on all day meetings title bar and validate   device=device_1
    Get meetings details present under all day title bar   device=device_1
    [Teardown]   Run Keywords   Capture on Failure  AND     Navigate back to meetings   device=device_1     AND  Come back to home screen     device_list=device_1

TC3: [Landing Page] All-day meeting should be display in landing page
    [Tags]  238035    P2
    [Setup]  Testcase Setup for Meeting User   count=1
    Verify default option present on landing page and validate   device=device_1
    Tap on all day meetings title bar and validate  device=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND   Navigate back to meetings   device=device_1  AND   Come back to home screen    device_list=device_1

TC4: [Landing Page] All-day meetings list should be display after tapping on the All-day title bar
    [Tags]  238037    bvt   bvt_sm      sanity_sm
    [Setup]  Testcase Setup for Meeting User      count=1
    Verify default option present on landing page and validate   device=device_1
    Tap on all day meetings title bar and validate   device=device_1
    Get meetings details present under all day title bar   device=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND   Navigate back to meetings   device=device_1   AND   Come back to home screen    device_list=device_1

TC5: [Landing Page]All-day meeting tittle should be hide when there are no All-day meetings
    [Tags]  238036   P2
    [Setup]  Testcase Setup for Meeting User      count=1
    Verify home page screen    device=device_1
    tap on all day meetings title bar and validate    device=device_1
   [Teardown]   Run Keywords   Capture on Failure  AND  Navigate back to meetings   device=device_1     AND  Come back to home screen     device_list=device_1

TC6:[MTRA] Verify All day meetings
     [Tags]     444935   P1
    [Setup]  Testcase Setup for Meeting User      count=1
    Verify default option present on landing page and validate   device=device_1
    Tap on all day meetings title bar and validate   device=device_1
    Get meetings details present under all day title bar   device=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND   Navigate back to meetings   device=device_1   AND   Come back to home screen    device_list=device_1

TC7:[MTRA] Verify that new calendar UI visible.
    [Tags]     444850     bvt_sm  sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify that new calendar UI visible     device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1

TC8:[MTRA] Verify All day meetings, count and banner.
    [Tags]     444935   P1
    [Setup]  Testcase Setup for Meeting User      count=1
    Verify default option present on landing page and validate   device=device_1
    Verify all day meetings count and banner   device=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND   Navigate back to meetings   device=device_1   AND   Come back to home screen    device_list=device_1

*** Keywords ***
Verify default option present on landing page and validate
    [Arguments]     ${device}
    Verify home page screen    ${device}

Verify and click on white board sharing in call control bar
        [Arguments]    ${device}
        Verify whiteboard sharing option under more option   ${device}

Verify all day meetings count and banner
    [Arguments]    ${device}
    Tap on all day meetings title bar and validate   ${device}

Verify that new calendar UI visible
    [Arguments]    ${device}
    Verify current time display on home screen    ${device}
    verify start and end time display on calendar tab    ${device}
    Verify background display of all day meetings       ${device}