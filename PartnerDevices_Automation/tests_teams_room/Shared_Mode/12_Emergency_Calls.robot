*** Settings ***
Documentation   Emergency Calls
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  10


*** Test Cases ***
TC1: [Emergency call] User must sign in to make an emergency call
    [Tags]  237789   P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User    count=1
    Sign out method    device=device_1
    Verify sign in to make an emergency call    device=device_1
    [Teardown]  Run Keywords    Capture on Failure  AND     Sign in method    device=device_1    user=meeting_user

# auto dial is not supported bug_3445550
#TC2 : [Emergency call] Check auto -dial for emergency number
#    # Dial 933 for Emergency Calling
#    [Tags]  237790   bvt    bvt_sm     sanity_sm
#    [Setup]  Testcase Setup for Meeting User   count=1
#    Navigate to dial pad on home screen   device=device_1
#    Auto dial emergency number and validate   device=device_1
#    Disconnect call   device=device_1
#    Verify Call State   device_list=device_1    state=Disconnected
#    [Teardown]   Run Keywords    Capture on Failure  AND   Come back to home screen    device_list=device_1
