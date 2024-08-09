*** Settings ***
Documentation   Emergency Calls
Force Tags    sm_emergency_calls    14     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***


*** Test Cases ***
TC1 : [Emergency call] Check auto -dial for emergency number
    # Dial 933 for Emergency Calling
    [Tags]  315449   bvt    bvt_sm     sanity_sm
    [Setup]  Testcase Setup for shared User      count=1
    Verify should not autodial the emergency number  console=console_1
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC2: [Emergency call] User must sign in to make an emergency call
    [Tags]      315447   P1     sanity_sm
    [Setup]  Testcase Setup for shared User      count=1
    Console sign out method   console=console_1
    Verify signin is successful    console_list=console_1     state=Sign out
    Verify sign in to make an emergency call    device=console_1
    Sign out method    device=device_1
    Verify sign in to make an emergency call    device=device_1
    Sign in method    device=device_1    user=meeting_user
    [Teardown]   Run Keywords    Capture Failure  AND  console sign in method    console=console_1       user=meeting_user   AND   Get device pairing code    device_list=device_1    console_list=console_1   user_list=meeting_user
