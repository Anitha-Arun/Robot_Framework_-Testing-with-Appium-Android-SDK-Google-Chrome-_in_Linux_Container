*** Settings ***
Force Tags   sm_ztp   13   sm
Resource    ../resources/keywords/common.robot

Suite Setup   ZTP Setup
Suite Teardown   Suite Failure Capture

*** Test Cases ***
TC1: [ZTP][Sign-in] Settings must provide options to provision phone
    [Tags]      314809      bvt   bvt_sm   sanity_sm
    [Setup]  Testcase Setup for ZTP    count=1
    verify teams app signin page    device=console_1
    verify settings option from signin page    device=console_1
    [Teardown]  Run Keywords    Capture Failure    AND    Device setting back till signin btn visible    device=console_1

TC2: [ZTP][Sign-in] DCF code fetching for sign-in from other device either with PC or Phone.
    [Tags]  314760  P1  sanity_sm
    [Setup]  Testcase Setup for ZTP    count=1
    verify the signin ui for ztp    device=console_1
    [Teardown]  Capture Failure

TC3: [ZTP][Sign-in] Sign-in on this device should support username/password flow
    [Tags]      314766      P1
    [Setup]  Testcase Setup for ZTP    count=1
    verify teams app signin page    device=console_1
    Console sign in method     console=console_1    user=meeting_user
    Get device pairing code    device_list=device_1    console_list=console_1     user_list=meeting_user
    Verify signin is successful    console_list=console_1     state=Sign in
    [Teardown]  Capture Failure

TC4: [CP Enrollment] No blocking GUI
    [Tags]  314780  P1
    [Setup]  Testcase Setup for shared User       count=1
    Validate user details along with home screen options    console=console_1:meeting_user
    Console sign out method   console=console_1
    verify teams app signin page    device=console_1
    [Teardown]  Capture Failure

TC5: [ZTP][Sign-in] User should able go back to sign-in page from cloud
    [Tags]      314831      P1
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=console_1
    verify settings from signin page    device=console_1
    verify cloud option   device=console_1
    navigate back to signin page form cloud    device=console_1
    verify teams app signin page    device=console_1
    [Teardown]  Capture Failure

TC6: [ZTP][Sign-in] Emergency call banner should always be available in signed out state
    [Tags]      314794   P1     sanity_sm
    [Setup]  Testcase Setup for ZTP    count=1
    verify teams app signin page    device=console_1
    Verify emergency call label in sign in page     device=console_1
    [Teardown]  Capture Failure

TC7: [ZTP][Sign-in] For provisioning the phone, DUT needs to show UI to enter verification code and able to edit the verification code on provision phone screen
    [Tags]      314836      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=console_1
    verify settings from signin page    device=console_1
    Verify provision phone ui    device=console_1
    Verify able to edit the code on provision phone ui      device=console_1
    navigate back to signin page form cloud    device=console_1
    [Teardown]  Capture Failure

TC8: [CP Enrollment] Sending failure cases with invalid password in signin
    [Tags]      314774      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=console_1
    Verify signin with wrong password     device=console_1
    Navigate back to signin page form cloud     device=console_1
    [Teardown]  Run Keywords    Capture Failure    AND    Device setting back btn     console=console_1

TC9: [CP Enrollment] Re-enrollment with different user
    [Tags]      314768  P1
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=console_1
    sign out method  device=device_1
    sign in method  device=device_1
    Console sign in method     console=console_1
    Get device pairing code    device_list=device_1    console_list=console_1     user_list=user
    Verify signin is successful    console_list=console_1     state=Sign in
    Console sign out method   console=console_1
    sign out method  device=device_1
    verify teams app signin page    device=device_1
    sign in method  device=device_1    user=meeting_user
    Console sign in method     console=console_1    user=meeting_user
    Get device pairing code    device_list=device_1    console_list=console_1     user_list=meeting_user
    Verify signin is successful    console_list=console_1     state=Sign in
    [Teardown]  Run Keywords    Capture Failure    AND   Console sign out method   console=console_1     AND     sign out method  device=device_1

TC10: [CP Enrollment] Re-enrollment with same user
    [Tags]      314770    P1
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=console_1
    sign out method  device=device_1
    sign in method  device=device_1   user=meeting_user
    Console sign in method     console=console_1    user=meeting_user
    Get device pairing code    device_list=device_1    console_list=console_1     user_list=meeting_user
    Verify signin is successful    console_list=console_1     state=Sign in
    Console sign out method   console=console_1
    sign out method  device=device_1
    verify signin button on signin page  count=1
    sign in method  device=device_1   user=meeting_user
    Console sign in method     console=console_1    user=meeting_user
    Get device pairing code    device_list=device_1    console_list=console_1     user_list=meeting_user
    Verify signin is successful    console_list=console_1     state=Sign in
    [Teardown]  Run Keywords    Capture Failure    AND   Console sign out method   console=console_1     AND     sign out method  device=device_1

TC11: [ZTP][Sign-in] Selecting cloud option to provisioning the phone
    [Tags]      314817      P1
    [Setup]  Testcase Setup for ZTP    count=1
    verify teams app signin page    device=console_1
    verify settings from signin page    device=console_1
    Verify cloud option to provisioning the Phone    device=console_1
    verify teams app signin page    device=console_1
    [Teardown]  Run Keywords    Capture Failure    AND     Device setting back btn     console=console_1

TC12: [CP Enrollment] Unenrollment
    [Tags]      314788      P2
    [Setup]  Testcase Setup for shared User       count=1
    Validate user details along with home screen options    console=console_1:meeting_user
    Console sign out method   console=console_1
    verify teams app signin page    device=console_1
    [Teardown]  Capture Failure


*** Keywords ***
ZTP Setup
    Console sign out method   console=console_1

Verify cloud option to provisioning the Phone
    [Arguments]    ${device}
    verify cloud option    ${device}
