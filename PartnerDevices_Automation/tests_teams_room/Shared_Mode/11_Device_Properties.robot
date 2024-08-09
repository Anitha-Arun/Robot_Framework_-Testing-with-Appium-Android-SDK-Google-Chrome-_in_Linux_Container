*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Test Cases ***
TC1: [Device Properties] Check firmware version
    [Tags]  237875   bvt    bvt_sm  sanity_sm
    [Setup]  Testcase Setup for Meeting User    count=1
    Check device firmware version    device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen   device_list=device_1

TC2: [Device Properties] Check device type
    [Tags]  237876   P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=1
    Check device type and validate    device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen   device_list=device_1

#Need to modify the test case
#TC3: [Device Properties] Check device capabilities
#    [Tags]  237877   P2
#    [Setup]  Testcase Setup for Meeting User    count=1
#    Check device capabilities   device=device_1
#    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen   device_list=device_1