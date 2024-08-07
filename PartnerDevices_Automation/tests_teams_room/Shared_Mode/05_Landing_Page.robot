*** Settings ***
Documentation   Validating the test cases realted to Landing Page feature
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot



*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Landing Page] DUT user view the time, User name of the account , DID on the Landing screen
    [Tags]   238008   P2
    [Setup]  Testcase Setup for Meeting User     count=1
    Validate that signin is successfully completed    device_list=device_1     state=Sign in
    Verify user details present on landing page   device=device_1:meeting_user
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1

TC2: [Landing Page] DUT user rejects the incoming call from Teams Desktop Client
    [Tags]   238026   P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Verify home page screen     device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Reject incoming call     device_list=device_1
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC3: [Landing Page] Verify Highlighted background , Teams Icon , Join button for current meeting
    [Tags]   238032   P1
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify home page screen     device=device_1
    View current meeting display on screen    device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1

TC4: [Landing Page] DUT user to verify incoming video call
    [Tags]   238025   P1
    [Setup]  Testcase Setup for Meeting User     count=2
    Make Video call using display name   from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call      device=device_1
    Close participants screen   device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Verify participants list during call      device=device_1
    Disconnect call      device=device_1,device_2
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1,device_2

TC5: [Landing Page] DUT user to view and able start meeting using Meet now
    [Tags]   238010   P1
    [Setup]  Testcase Setup for Meeting User     count=2
    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_2
    Reject incoming call      device_list=device_2
    Close participants screen   device=device_1
    Verify Call State    device_list=device_2     state=Disconnected
    Disconnect call      device=device_1
    Verify Call State    device_list=device_1    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1,device_2

TC6: [Landing Page] Verify No meeting schedule for the day
    [Tags]   238030     sanity_sm       P1
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify no meeting schedule on landing page    device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1

TC7: [Landing Page]DUT user able to view dial-pad on Landing screen
    [Tags]   238009   P1
    [Setup]  Testcase Setup for Meeting User      count=2
    Verify dial pad present on landing page   device=device_1
    Dial number from dial pad     from_device=device_1      to_device=device_2
    Accept incoming call   device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND   Come back to home screen   device_list=device_1,device_2

TC8: [Landing Page] DUT user able to navigate settings via Landing Page
    [Tags]  238012   P1
    [Setup]  Testcase Setup for Meeting User    count=1
    Navigate to more button and validate options   device=device_1
    Navigate to settings page   device=device_1
    Verify settings page options and validate   device=device_1:meeting_user
    [Teardown]   Run Keywords    Capture on Failure  AND    Landing Page Teardown   device=device_1

TC9: [Landing Page] DUT user able to increase and decrease the volume via Landing Page using More button
    [Tags]  238011    bvt   bvt_sm  sanity_sm
    [Setup]  Testcase Setup for Meeting User      count=1
    Navigate to more option  device=device_1
    Adjust volume button  device=device_1   state=UP
    Adjust volume button  device=device_1   state=Down
    [Teardown]   Run Keywords    Capture on Failure  AND    Navigate back to home screen page  device=device_1

TC10: [Landing Page] DUT user able navigate "Sign out" via Landing page
    [Tags]  238022    P2
    [Setup]  Testcase Setup for Meeting User      count=1
    Verify home page screen    device=device_1
    Navigate to app settings page   device=device_1
    Verify settings page options and validate   device=device_1:meeting_user
    Navigate back to home screen from settings page     device=device_1
    Sign out method    device=device_1
    [Teardown]  Run Keywords   Capture on Failure  AND   Sign in method     device=device_1     user=meeting_user

# Test obsolete, new cases for new report and isssue will be added
#TC11: [Landing Page] DUT user able navigate "Report an issue " via Landing Screen
#    [Tags]  238018    P2
#    [Setup]  Testcase Setup for Meeting User      count=1
#    Navigate to more button and validate options   device=device_1
#    Navigate to settings page   device=device_1
#    Verify settings page options and validate   device=device_1:meeting_user
#    Report an issue    device=device_1
#    [Teardown]   Run Keywords    Capture on Failure  AND    Landing Page Teardown   device=device_1

#TC12: [Landing Page] Further meeting should not be having Teams Icon
#    [Tags]  238034    P1   sanity_sm
#    [Setup]  Testcase Setup for Meeting User    count=1
#    Verify meeting display on home screen     device=device_1
#    Verify default option present on landing page and validate   device=device_1
#    Teams icon visibility for future meetings   device=device_1
#    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


TC13: [Landing Page] DUT user able navigate "Device Settings" via Landing Page
     [Tags]  238020   P2
    [Setup]  Testcase Setup for Meeting User      count=1
    Verify home page screen    device=device_1
    Navigate to app settings page    device=device_1
    verify option inside settings page   device=device_1:meeting_user
    verify options in device settings   device=device_1
    [Teardown]   Run Keywords   Capture on Failure  AND  Come back to home screen     device_list=device_1

# reference: Feature Test Request 451143: [FTR][MTRA] Remove calling admin settings
#TC14: [Landing Page] DUT user able navigate "calling" via Landing Page
#    [Tags]   238015     P2
#    [Setup]    Testcase Setup for Meeting User   count=1
#    Navigate to app settings page  device=device_1
#    navigate calling option  device=device_1
#    verify options in device settings calling    device=device_1
#    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1

TC19:[Landing Page] DUT user able navigate "about" via Landing page
    [Tags]     238019        bvt_sm      sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=1
    Navigate to about page  device=device_1
    Verify about page  device=device_1
    click close btn     device_list=device_1
    [Teardown]   Run Keywords   Capture on Failure  AND    Come back to home screen    device_list=device_1


*** Keywords ***
Landing Page Teardown
    [Arguments]     ${device}
    Click close btn    device_list=${device}
    Come back to home screen    device_list=${device}

Verify settings page options and validate
    [Arguments]     ${device}
    Verify option inside settings page  ${device}

Test Case Teardown
    [Arguments]     ${device}
    Click back btn   ${device}
    Click back btn   ${device}
    Come back to home screen    device_list=${device}

Navigate to settings page
    [Arguments]     ${device}
    Click on settings page    ${device}

Verify default option present on landing page and validate
    [Arguments]     ${device}
    Verify home page screen    ${device}

Navigate to more option
    [Arguments]     ${device}
    Click on more option   ${device}

Navigate back to home screen page
     [Arguments]     ${device}
     Click on settings page    ${device}
     Click close btn    device_list=${device}
     Come back to home screen    device_list=${device}

Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page    ${device}

Navigate back to home screen from settings page
    [Arguments]      ${device}
    Click close btn    device_list=${device}
    Come back to home screen    device_list=${device}

verify options in device settings
    [Arguments]      ${device}
    navigate to meetings option in device settings page    ${device}
    come back from admin settings page      device_list=${device}

navigate calling option
    [Arguments]       ${device}
    navigate to teams admin settings   ${device}
    verify calling option in device settings page     ${device}

Navigate to about page
     [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}
    click on about page  ${device}
