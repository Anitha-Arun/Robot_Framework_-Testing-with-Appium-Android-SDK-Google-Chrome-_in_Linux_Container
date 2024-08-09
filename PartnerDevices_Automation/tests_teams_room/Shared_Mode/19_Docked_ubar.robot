*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***

*** Test Cases ***
TC1: [Docked UBar] Options available in Docked Ubar
    [Tags]  303205  p1      sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify docked ubar     device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1,device_2

TC2: [Docked Ubar]DUT user verify that Meeting title visible on Docked Ubar
    [Tags]  303206  p2
     [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify meeting name      device=device_1    meeting=cnf_device_meeting
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND         Come back to home screen    device_list=device_1,device_2


TC3 : [Docked Ubar] DUT user verify that Docked Ubar will be always available on DUT
    [Tags]    303207    bvt     bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User    count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify docked ubar      device=device_1
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen   device_list=device_1,device_2


*** Keywords ***
Verify docked ubar
     [Arguments]    ${device}
     verify_call_control_bar   ${device}
