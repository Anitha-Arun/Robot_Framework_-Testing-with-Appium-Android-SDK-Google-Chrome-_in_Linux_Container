*** Settings ***
Force Tags      feedback    32
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***

*** Test Cases ***
TC1:[Feedback]Verify the [?] (Report an issue) option in the Home screen.
    [Tags]    452143    bvt_sm  sanity_sm
	[Setup]  Testcase Setup for shared User     count=1
	Verify help option on home screen       console=console_1:meeting_user
    [Teardown]   Run Keywords    Capture Failure    AND     Come back to home screen page   console_list=console_1

TC2:[Feedback] Verify the [?] option present under the more option of the Touch console.
	[Tags]    452148    P1      sanity_sm
	[Setup]  Testcase Setup for shared User     count=1
	Verify help option on home screen       console=console_1:meeting_user
	Tap on more option  console=console_1
	Verify help option present under the more option        console=console_1
	Click on back layout btn        console=console_1
	[Teardown]   Run Keywords    Capture Failure    AND     Come back to home screen page   console_list=console_1

TC3:[Feedback] Verify the functionality of [?] option in the Touch console.
	[Tags]      452194      bvt_sm  sanity_sm
	[Setup]  Testcase Setup for shared User     count=1
	Verify give feedback page   device=console_1
	[Teardown]   Run Keywords    Capture Failure    AND     Come back to home screen page   console_list=console_1

TC4: [Feedback] Verify the [?] option when Microsoft Whiteboard is initiated from Home screen.
	[Tags]    452201    P1      sanity_sm
	[Setup]  Testcase Setup for shared User     count=1
	Verify help option when whiteboard initiated from home screen       console=console_1
    [Teardown]   Run Keywords    Capture Failure    AND     Come back to home screen page   console_list=console_1

TC5:[Feedback] Verify the [?] option present under the call option of the Touch console.
    [Tags]    452218    P1      sanity_sm
	[Setup]  Testcase Setup for shared User     count=1
	Verify help option present under the call option    device=console_1
	[Teardown]   Run Keywords    Capture Failure    AND     Come back to home screen page   console_list=console_1

*** Keywords ***
Verify help option on home screen
    [Arguments]     ${console}
    Verify date and time with user details on home screen   ${console}

Verify help option present under the more option
    [Arguments]     ${console}
    Verify more options     ${console}
