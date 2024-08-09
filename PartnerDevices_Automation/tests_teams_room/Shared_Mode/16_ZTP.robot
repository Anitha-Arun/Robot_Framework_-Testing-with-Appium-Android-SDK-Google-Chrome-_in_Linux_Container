*** Settings ***
Resource    ../resources/keywords/common.robot
Suite Setup   ZTP Setup
Suite Teardown   Suite Failure Capture

*** Test Cases ***
TC1: [ZTP][Sign-in] DCF code fetching for sign-in from other device either with PC or Phone
    [Tags]  263002  P1  sanity_sm
    [Setup]  Testcase Setup for ZTP    count=1
    verify the signin ui for ztp    device=device_1
    [Teardown]  Capture on Failure

TC2: [CP Enrollment] No blocking GUI
    [Tags]  263013  P1
    [Setup]  Testcase Setup for Meeting User  count=1
    verify home page screen  device=device_1
    sign out method  device=device_1
    verify teams app signin page    device=device_1
    [Teardown]  Capture on Failure

TC3: [ZTP][Sign-in] Settings must provide options to provision phone
    [Tags]  263028   bvt    bvt_sm   sanity_sm
    [Setup]  Testcase Setup for ZTP    count=1
    verify teams app signin page    device=device_1
    verify settings option from signin page    device_1
    [Teardown]  Run Keywords    Capture on Failure    AND    Device setting back till signin btn visible    device=device_1

TC4: [ZTP][Sign-in] Selecting cloud option to provisioning the phone
    [Tags]  263032      P1
    [Setup]  Testcase Setup for ZTP    count=1
    verify teams app signin page    device=device_1
    verify settings from signin page    device_1
    verify cloud option for provisioning device    device_1
    verify teams app signin page    device_1
    [Teardown]  Run Keywords    Capture on Failure    AND    Device setting back till signin btn visible    device=device_1

TC5: [ZTP][Sign-in] DUT User should able go back to sign-in page from cloud
    [Tags]  263039      P1
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=device_1
    verify settings from signin page    device_1
    verify cloud option   device_1
    navigate back to signin page form cloud    device_1
    verify teams app signin page    device_1
    [Teardown]  Run Keywords    Capture on Failure    AND    Device setting back till signin btn visible    device=device_1

TC6: [ZTP][Sign-in] For provisioning the phone, DUT needs to show UI to enter verification code and able to edit the verification code on provision phone screen
    [Tags]  263042   bvt    bvt_sm  sanity_sm
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=device_1
    verify settings from signin page    device_1
    verify provision phone option    device_1
    [Teardown]  Run Keywords    Capture on Failure    AND    Device setting back till signin btn visible    device=device_1

TC7: [ZTP]Device login url on Landing page
    [Tags]  263071      P1
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=device_1
    verify settings from signin page    device_1
    verify cloud option    device_1
    verify login url with cloud settings as public    device_1
    verify settings from signin page    device_1
    verify cloud option    device_1
    verify login url with cloud setting as gcc    device_1
    verify settings from signin page    device_1
    verify cloud option    device_1
    verify login url with cloud setting as gcc high    device_1
    verify settings from signin page    device_1
    verify cloud option    device_1
    verify login url with cloud setting as gcc dod    device_1
    verify settings from signin page    device_1
    verify cloud option    device_1
    verify login url with cloud settings as public    device_1
    [Teardown]  Run Keywords    Capture on Failure    AND    Device setting back till signin btn visible    device=device_1

TC8: [CP Enrollment] Re-enrollment with same user
    [Tags]  263008    P1    sanity_sm
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=device_1
    sign in method  device=device_1   user=meeting_user
    verify home page screen  device=device_1
    sign out method  device=device_1
    verify signin button on signin page  count=1
    sign in method  device=device_1   user=meeting_user
    verify home page screen  device=device_1
    [Teardown]  Run Keywords    Capture on Failure    AND    sign out method    device=device_1

TC9: [CP Enrollment] Sending failure cases with invalid password in signin
    [Tags]  263010      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=device_1
    Verify signin with wrong password     device=device_1
    [Teardown]  Run Keywords    Capture on Failure    AND    Device setting back till signin btn visible    device=device_1

TC10: [CP Enrollment] Unenrollment
    [Tags]  263017      P2
    [Setup]  Testcase Setup for Meeting User  count=1
    verify home page screen  device=device_1
    sign out method  device=device_1
    verify teams app signin page    device=device_1
    [Teardown]  Capture on Failure

TC11: [CP Enrollment] Re-enrollment with different user
    [Tags]      263007  P1
    [Setup]  Testcase Setup for ZTP  count=1
    verify teams app signin page    device=device_1
    sign in method  device_1
    verify home page screen  device=device_1
    sign out method  device_1
    verify teams app signin page    device=device_1
    sign in method  device_1    user=meeting_user
    verify home page screen  device=device_1
    [Teardown]  Run Keywords    Capture on Failure    AND    sign out method  device=device_1


TC12: [ZTP][Sign-in] Emergency call banner should always be available in signed out state
    [Tags]      263020   P1     sanity_sm
    [Setup]  Testcase Setup for ZTP    count=1
    verify teams app signin page    device=device_1
    Verify emergency call label in sign in page     device=device_1
    [Teardown]  Capture on Failure

TC13:[ZTP] Welcome message should display at sign in page and able to dismiss setting pop up from DCF screen
    [Tags]      316905   P2
    [Setup]  Testcase Setup for ZTP    count=1
    verify welcome message on dfc screen    device=device_1
    verify settings pop up in DFC screen    device=device_1
    verify dfc settings popup closed successfully     device=device_1
    [Teardown]  Run Keywords   Capture on Failure  AND   Sign in method     device=device_1     user=meeting_user


*** Keywords ***
ZTP Setup
    sign out method  device_1

verify settings pop up in DFC screen
    [Arguments]     ${device}
    verify settings from signin page    ${device}