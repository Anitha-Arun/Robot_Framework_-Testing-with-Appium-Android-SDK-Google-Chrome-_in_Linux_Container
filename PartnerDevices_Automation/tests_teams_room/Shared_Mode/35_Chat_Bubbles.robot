*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Test Cases ***
TC1:[Chat Bubbles] Verify during a call or meeting click on more options than by default "Show chat bubble" is enabled.
    [Tags]      317660     P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=2
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    Accept incoming call  device=device_2
    verify show chat bubble is enabled default      device=device_1
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure  AND    Come back to home screen     device_list=device_1,device_2

