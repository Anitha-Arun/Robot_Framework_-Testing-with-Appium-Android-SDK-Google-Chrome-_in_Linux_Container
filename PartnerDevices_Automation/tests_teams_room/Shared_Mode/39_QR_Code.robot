*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../../resources/keywords/common.robot


*** Variables ***

*** Test Cases ***
TC1:[QR Code]Verify When DUT user disables parent toggle "Show room QR Code" child toggle "Automatically accept proximity based meeting invitations should also be disabled
    [Tags]     452449        P2
    [Setup]    Testcase Setup for Meeting User   count=1
	Navigate to QR settings    device=device_1
	enable and disable qrcode toggle    device=device_1     activity_state=off
	verify proximity based meeting invitations disabled     device=device_1
	Enable QR code   device=device_1    state=on
	Navigate to home screen    device=device_1
    [Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

TC2:[QR Code] Verify user is able to Enable/Disable Show room QR Code
    [Tags]     452431   452435  452439  452444  452452  452486        P2
    [Setup]    Testcase Setup for Meeting User   count=1
	Navigate to QR settings    device=device_1
	Verify option under Wireless connection       device=device_1
	Enable QR code   device=device_1    state=on
	Navigate to home screen    device=device_1
    Verify qr code visible    device=device_1   state=visible
    Navigate to QR settings     device=device_1
    Enable QR code   device=device_1    state=off
	Navigate to home screen    device=device_1
    Verify qr code visible    device=device_1   state=invisible
    [Teardown]   Run Keywords    Capture on Failure   AND   Come back to home screen     device_list=device_1

*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

Navigate to General option and verify Wireless connection
	[Arguments]     ${device}
	verify and click General option in device settings page   ${device}

Navigate to QR settings
    [Arguments]     ${device}
    Navigate to app settings page      ${device}
	navigate to teams admin settings        ${device}
	Navigate to General option and verify Wireless connection       ${device}

Navigate to home screen
    [Arguments]     ${device}
    device setting back     ${device}
    device setting back     ${device}
    come back to home screen  ${device}

Enable QR code
    [Arguments]     ${device}   ${state}
	Verify option under Wireless connection       ${device}
	enable and disable qrcode toggle    ${device}      activity_state=${state}
	enable and disable proximity based toggle   ${device}    activity_state=${state}

