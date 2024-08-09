*** Settings ***
Documentation    Validating the functionality of console sigin/signout feature.
Force Tags    sm_signin    sm
Resource    ../resources/keywords/common.robot

*** Variables ***

*** Test Cases ***
TC1 : [Sign-in] User to sign-in with username and password
    [Tags]     314720    bvt_sm     sanity_sm
    [Setup]  Testcase Setup for shared User       count=1
    Verify signin is successful    console_list=console_1     state=Sign in
    [Teardown]   Capture Failure

TC2: [Sign-out] Account sign out option should be under Admin Section for Room/meeting account
     [Tags]   314748   bvt_sm       sanity_sm
     [Setup]  Testcase Setup for shared User      count=1
     Verify signin is successful   console_list=console_1     state=Sign in
     Console sign out method   console=console_1
     [Teardown]  Run Keywords  Capture Failure    AND   Console sign in method     console=console_1    user=meeting_user  AND  Get device pairing code    device_list=device_1    console_list=console_1     user_list=meeting_user

TC3: [Sign-in] Sign-out from the TC and check for the intents
     [Tags]     314728   bvt    bvt_sm  sanity_sm
     [Setup]  Testcase Setup for shared User      count=1
     Verify signin is successful   console_list=console_1     state=Sign in
     Console sign out method   console=console_1
     [Teardown]  Run Keywords   Capture Failure    AND   console sign in method    console=console_1    user=meeting_user  AND  Get device pairing code    device_list=device_1    console_list=console_1   user_list=meeting_user

TC4: [Sign-in] User to sign-out from existing account and sign-in with a different account
     [Tags]     314732  bvt     bvt_sm      sanity_sm
     [Setup]  Testcase Setup for shared User      count=1
     Verify signin is successful   console_list=console_1     state=Sign in
     Console sign out method   console=console_1
     Verify signin is successful    console_list=console_1     state=Sign out
     Verify home page screen   device=device_1
     Sign out method    device=device_1
     Sign in method     device=device_1
     Console sign in method     console=console_1
     Get device pairing code    device_list=device_1    console_list=console_1     user_list=user
     Verify signin is successful    console_list=console_1     state=Sign in
     Console sign out method   console=console_1
     Sign out method    device=device_1
     Sign in method     device=device_1     user=meeting_user
     [Teardown]  Run Keywords   Capture Failure  AND  console sign in method    console=console_1       user=meeting_user   AND   Get device pairing code    device_list=device_1    console_list=console_1   user_list=meeting_user

#Removed the testcase due to Bug 2130229: [Tracking][Norden][Blocked][CP Bug] Teams app stuck after entering username in "Connecting" page
#TC5: [Sign-in] User to re-sign-in multiple times to with same user
#     [Tags]   314746    bvt_sm      sanity_sm
#     [Setup]  Testcase Setup for shared User      count=1
#     Console sign out method   console=console_1
#     Sign out method    device=device_1
#     Sign in method     device=device_1     user=meeting_user
#     Console sign in method    console=console_1        user=meeting_user
#     Get device pairing code    device_list=device_1    console_list=console_1   user_list=meeting_user
#     Verify signin is successful   console_list=console_1     state=Sign in
#     Console sign out method   console=console_1
#     Sign out method    device=device_1
#     Sign in method     device=device_1     user=meeting_user
#     Console sign in method     console=console_1       user=meeting_user
#     Get device pairing code    device_list=device_1    console_list=console_1   user_list=meeting_user
#     Verify signin is successful   console_list=console_1     state=Sign in
#     Console sign out method   console=console_1
#     Sign out method    device=device_1
#     Sign in method     device=device_1     user=meeting_user
#     Console sign in method     console=console_1       user=meeting_user
#     Get device pairing code    device_list=device_1    console_list=console_1   user_list=meeting_user
#     Verify signin is successful   console_list=console_1     state=Sign in
#     [Teardown]  Run Keywords   Capture Failure     AND     Come back to home screen page   console_list=console_1

TC6: [Sign in] DID of the user should be displayed on the Home screen and dial pad
    [Tags]      322300      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User      count=1
    Verify did user displayed on homescreen and on dialpad      console=console_1:meeting_user
    [Teardown]  Run Keywords   Capture Failure    AND     Come back to home screen page   console_list=console_1

TC7:[Sign-in] User to be signed in to Teams App within a specified time limit
     [Tags]     314734      P2
     [Setup]  Testcase Setup for shared User      count=1
     Verify signin is successful   console_list=console_1     state=Sign in
     Verify Home page options   console=console_1:meeting_user
     [Teardown]  Run Keywords   Capture Failure  AND     Come back to home screen page   console_list=console_1

TC8: [Sign-in] User to Sign-in Touch console and TDC simultaneously with same valid user
    [Tags]      323361   P2
    [Setup]  run keywords   Testcase Setup for shared User    count=2   AND    Signin with other user    device=device_2   other_user_account=device_1:meeting_user
    Validate that signin is successfully completed    device_list=device_2     state=Sign in
    Validate user details along with home screen options    console=console_1:meeting_user
    Console sign out method   console=console_1
    Console sign in method     console=console_1        user=meeting_user
    Get device pairing code    device_list=device_1    console_list=console_1     user_list=meeting_user
    [Teardown]  Run Keywords   Capture Failure  AND     Come back to home screen page   console_list=console_1      device_list=device_2

TC9:[Sign-in] Sign into DUT with invalid user
    [Tags]   343759      P2
    [Setup]   Run Keywords     Testcase Setup for shared User    count=1    AND   Console sign out method   console=console_1
    Verify signin with invalid user     device=console_1
    [Teardown]  Run Keywords   Capture Failure   AND    Sign in Teardown    device_list=device_1    console=console_1

TC10:[Sign-in] Sign-in to DUT with wrong Password
    [Tags]   343760      P1
    [Setup]   Run Keywords     Testcase Setup for shared User    count=1    AND   Console sign out method   console=console_1
    Verify signin with wrong password     device=console_1
    Navigate back to signin page     console=console_1
    [Teardown]  Run Keywords   Capture Failure    AND       Sign in Teardown    device_list=device_1    console=console_1

TC11:[Sign-in] Sign-in attempt in DUT with invalid domain name
    [Tags]   343762   P2
    [Setup]   Run Keywords     Testcase Setup for shared User    count=1    AND   Console sign out method   console=console_1
    Verify signin with invalid domain     device=console_1
    [Teardown]  Run Keywords   Capture Failure   AND    Sign in Teardown    device_list=device_1    console=console_1

*** Keywords ***
Sign in Teardown
    [Arguments]     ${device_list}      ${console}
    Device setting back btn    ${console}
    Console sign in method    ${console}      user=meeting_user
    Get device pairing code    ${device_list}    console_list=${console}     user_list=meeting_user

Verify Home page options
    [Arguments]     ${console}
    validate user details along with home screen options        ${console}

Navigate back to signin page
    [Arguments]     ${console}
    Navigate back to signin page form cloud     device=${console}
