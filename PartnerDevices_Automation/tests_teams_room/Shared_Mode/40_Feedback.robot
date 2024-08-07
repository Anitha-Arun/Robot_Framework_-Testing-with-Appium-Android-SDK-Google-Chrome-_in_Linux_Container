*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${action_time} =  5
*** Test Cases ***
TC1: [Feedback] Verify the [?] option present under more option of the DUT.
	[Tags]    452214    P0
	[Setup]    Testcase Setup for Meeting User   count=1
	Verify help option on home screen   device=device_1
	Click on more option      device=device_1
	Verify the Help button after Click on more option      device=device_1
	[Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1


TC2: [Feedback] Verify the functionality of [?] option present in the DUT screen..
	[Tags]    452216    P0
	[Setup]    Testcase Setup for Meeting User   count=1
	Verify help option on home screen      device=device_1
	Verify Give Feedback Page       device=device_1
	[Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

TC3: [Feedback] Verify the [?] option when Microsoft Whiteboard is initiated from Home screen.
	[Tags]    452217    P1
	[Setup]    Testcase Setup for Meeting User   count=1
	verify whiteboard sharing option on home screen option      device=device_1
    Wait for Some Time    time=${action_time}
    Verify the Help button after Microsoft Whiteboard is initiated from Home screen      device=device_1
    verify Start Meeting and Stop Whiteboard options when the dut user launch whiteboard        device=device_1
    [Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

TC4:[Feedback] Verify the [?] option present under the call option of the DUT.
    [Tags]    452220    P1
	[Setup]    Testcase Setup for Meeting User   count=1
	Verify help option present under the call option    device=device_1
	[Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

TC5:[Feedback]Verify the [?] (Report an issue) option in the Home screen.
    [Tags]    452213    P2
	[Setup]    Testcase Setup for Meeting User   count=1
	Verify help option on home screen    device=device_1
	verify feedback and report problem in help option       device=device_1
    [Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1


*** Keywords ***
Verify help option on home screen
    [Arguments]     ${device}
    verify home page screen   ${device}

verify feedback and report problem in help option
    [Arguments]     ${device}
    Verify the Help button functionality    ${device}

Verify the Help button after Microsoft Whiteboard is initiated from Home screen
    [Arguments]     ${device}
    Verify the Help button functionality    ${device}

Verify the Help button after Click on more option
    [Arguments]     ${device}
    Verify the Help button functionality    ${device}

