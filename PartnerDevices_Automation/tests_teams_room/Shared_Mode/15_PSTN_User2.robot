*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Home Screen] Dial pad should be available for PSTN enabled user
    [Tags]  237868   P1         sanity_sm     sm_home_screen
    [Setup]  Testcase Meeting PSTN Setup Main   count=2
    Verify dial pad present on landing page   device=device_1
    Dial number from dial pad     from_device=device_1      to_device=device_2:pstn_user
    Accept incoming call   device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure   AND    Come back to home screen   device_list=device_1,device_2

TC2: [Meetings] DUT user can add participants to the meeting
    [Tags]   237627    P1       sm_meetings
    [Setup]  Testcase Meeting PSTN Setup Main    count=3
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1    meeting=cnf_device_meeting
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Wait for Some Time    time=${wait_time}
    Close roaster button on participants screen   device=device_1
    Add participant to conversation using phonenumber    from_device=device_1      to_device=device_2:pstn_user
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Close roaster button on participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    End meeting      device=device_2
    Verify meeting state   device_list=device_1,device_3    state=Connected
    End meeting      device=device_1,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC3: [Incoming Call] DUT receives call from PSTN user
    [Tags]  237705      444804   P1   sm_Incoming_calls     sanity_sm
    [Setup]  Testcase Meeting PSTN Setup Main    count=2
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call   device=device_1
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC4: [Outgoing Call] DUT calls to PSTN user from home screen dialpad
    [Tags]  237606   bvt   bvt_sm    sanity_sm
    [Setup]  Testcase Meeting PSTN Setup Main   count=2
    Make outgoing call with phonenumber   from_device=device_1     to_device=device_2:pstn_user
    Accept incoming call     device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

# auto dial is not supported for u3 feature bug_3445550
#TC5: [Outgoing Call] DUT auto dials to PSTN user from home screen dialpad
#    [Tags]  237607    bvt   bvt_sm      sanity_sm       sm_outgoing_calls
#    [Setup]  Testcase Meeting PSTN Setup Main   count=2
#    Make outgoing call using auto dial      from_device=device_1     to_device=device_2:pstn_user
#    Accept incoming call      device=device_2
#    Wait for Some Time    time=${wait_time}
#    Verify Call State    device_list=device_1,device_2    state=Connected
#    Disconnect call     device=device_2
#    Verify Call State    device_list=device_1,device_2     state=Disconnected
#    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC6: [Escalate to Conference] DUT can add PSTN user while in call with TDC user
   [Tags]  237772       444788    bvt   bvt_sm   sanity_sm
   [Setup]  Testcase Meeting PSTN Setup Main   count=3
   Make Video call using display name   from_device=device_3     to_device=device_1:meeting_user
   Accept incoming call      device=device_1
   Close participants screen   device=device_3
   Wait for Some Time    time=${wait_time}
   Verify Call State    device_list=device_1,device_3    state=Connected
   Add participant to conversation using phonenumber   from_device=device_1      to_device=device_2:pstn_user
   Accept incoming call      device=device_2
   Close participants screen   device=device_1
   Verify list of participants     from_device=device_1      connected_device_list=device_1:meeting_user,device_2:pstn_user,device_3
   Verify Call State    device_list=device_1,device_2,device_3    state=Connected
   Disconnect call     device=device_2
   Verify Call State    device_list=device_1,device_3    state=Connected
   Disconnect call     device=device_1,device_3
   Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
   [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC7: [Escalate to conference]DUT user can add another DUT user while in call with PSTN user
    [Tags]   237778   P1    sm_esc_to_conf_pstn    sanity_sm
    [Setup]  Testcase Meeting PSTN Setup Main     count=3
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2:pstn_user
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen       device=device_1
    Verify list of participants    from_device=device_1      connected_device_list=device_1:meeting_user,device_2:pstn_user,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Verify video call state and validate   from_device=device_1     to_device=device_3
    Disconnect call     device=device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC8: [Escalate to conference] DUT user can add PSTN user while in call with another DUT user
    [Tags]   237777     444796   P1   sm_esc_to_conf_pstn     sanity_sm
    [Setup]  Testcase Meeting PSTN Setup Main     count=3
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_3
    Accept incoming call      device=device_3
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_3    state=Connected
    Add participant to conversation using phonenumber    from_device=device_1      to_device=device_2:pstn_user
    Accept incoming call      device=device_2
    Close participants screen       device=device_1
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2:pstn_user,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Verify video call state and validate   from_device=device_1     to_device=device_3
    Disconnect call     device=device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC9: [Meet Now] Start new meeting from Home screen
    [Tags]   305573     237871    P2    sm_meet_now
    [Setup]  Testcase Meeting PSTN Setup Main     count=3
    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_3    state=Connected
    Add participant to conversation using phonenumber   from_device=device_1      to_device=device_2:pstn_user
    Accept incoming call      device=device_2
    Close participants screen       device=device_1
    Verify list of participants     from_device=device_1      connected_device_list=device_1:meeting_user,device_2:pstn_user,device_3
    Check video call On state    device_list=device_1,device_2,device_3
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Disconnect call     device=device_1,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC10: [Escalate to conference] DUT user can add TDC user while in call with PSTN user
    [Tags]      237773         444790       sanity_sm
    [Setup]  Testcase Meeting PSTN Setup Main     count=3
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2:pstn_user
    Accept incoming call      device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen       device=device_1
    Verify list of participants    from_device=device_1      connected_device_list=device_1:meeting_user,device_2:pstn_user,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Verify video call state and validate   from_device=device_1     to_device=device_3
    Disconnect call     device=device_1,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC11: [Call control] DUT user hold the muted call with PSTN user
    [Tags]  304796     P2
    [Setup]  Testcase Meeting PSTN Setup Main     count=2
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call      device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Mutes the phone call    device=device_1
    verify call mute state    device_list=device_1    state=mute
    Hold the call   device=device_1
    Verify Call State    device_list=device_1     state=Hold
    Resume the call   device=device_1
    Verify Call State    device_list=device_1,device_2     state=Resume
    unmutes the phone call      device=device_1
    verify call mute state    device_list=device_1    state=Unmute
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2

TC12: [Meet now] Tapping on Meet now icon should initiate a conference call
    [Tags]   259696   P1        sanity_sm
    [Setup]   Testcase Meeting PSTN Setup Main     count=3
    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify Call State    device_list=device_1,device_3    state=Connected
    Add participant to conversation using phonenumber   from_device=device_1      to_device=device_2:pstn_user
    Accept incoming call      device=device_2
    Close participants screen   device=device_1
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Disconnect call     device=device_1,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC13: [Escalate to conference] DUT user can add another PSTN user while in call with a PSTN user
    [Tags]   237779  P1     sanity_sm
    [Setup]  Testcase Meeting 2 PSTN Setup Main  count=3
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2:pstn_user
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using phonenumber    from_device=device_1      to_device=device_3:pstn_user
    Accept incoming call    device=device_3
    Close participants screen       device=device_1
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2:pstn_user,device_3:pstn_user
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Disconnect call     device=device_3
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3


#TC15:[Auto accept] Auto accept should be disabled for PSTN and P2P calls
#    [Tags]   237842     P1
#    [Setup]  Testcase Meeting PSTN Setup Main     count=2
#    Navigate to app settings page  device=device_1
#    navigate calling option  device=device_1
#    accept meeting invites automatically    device=device_1      state=on
#    start my video automatically        device=device_1      state=on
#    Click close btn    device_list=device_1
#    device setting back  device=device_1
#    device setting back  device=device_1
#    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
#    verify auto accept timer is not present    device=device_1
#    Wait for Some Time    time=${wait_time}
#    Wait for Some Time    time=${wait_time}
#    Verify Call State    device_list=device_1,device_2    state=disconnected
#    [Teardown]  Run Keywords    Capture on Failure    AND   Come back to home screen    device_list=device_1,device_2   AND    disabling auto accept meeting invite and start my video automatically    device=device_1      state=off


TC16:[Layout][Call] Verify layout option when DUT makes call to PSTN User
    [Tags]       317129     bvt_sm      sanity_sm
    [Setup]  Testcase Meeting PSTN Setup Main     count=2
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2:pstn_user
    Accept incoming call      device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Verify layout option is not present     device=device_2
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2


TC17: [Outgoing Call] DUT calls to PSTN user from home screen dialpad
    [Tags]       444779     P1
    [Setup]  Testcase Meeting PSTN Setup Main   count=2
    Make outgoing call with phonenumber   from_device=device_1     to_device=device_2:pstn_user
    Accept incoming call     device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2


TC18:[Call-App] Verify mic is enabled and video is disabled by default, when user makes P2P call.
     [Tags]       444772    P2
    [Setup]  Testcase Meeting PSTN Setup Main   count=2
    Make outgoing call with phonenumber   from_device=device_1     to_device=device_2:pstn_user
    Accept incoming call     device=device_2
    Wait for Some Time    time=${wait_time}
    Check video call Off state      device_list=device_1
    Verify meeting Mute State    device_list=device_1    state=Unmute
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC19:[Call] Start new Call from Home screen
    [Tags]       444806   P2
    [Setup]  Testcase Meeting PSTN Setup Main   count=2
    verify dial pad present on landing page          device=device_1
    Make outgoing call with phonenumber   from_device=device_1     to_device=device_2:pstn_user
    Accept incoming call     device=device_2
    Wait for Some Time    time=${wait_time}
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC20:[Call-App] Verify user can enter mail id/ DID for PSTN or cross tenants call/meeting.
    [Tags]        444775     P0     bvt_sm      sanity_sm
    [Setup]  Testcase Meeting PSTN Setup Main   count=2
    Make outgoing call with username          from_device=device_1     to_device=device_2:pstn_user
    Reject incoming call   device_list=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure   AND   Come back to home screen    device_list=device_1,device_2

TC21:[Initiate spotlight] User to check the initiate spotlight for the PSTN user.
    [Tags]     381980        P2    sanity_sm
    [Setup]  Testcase Meeting PSTN Setup as Main device   count=2
    Join Meeting    device=device_1,device_2     meeting=lock_meeting
    make admit and deny in the meeting      from_device=device_2   to_device=device_1     lobby=admit_lobby
    Close participants screen   device=device_2
    Verify meeting state   device_list=device_1,device_2   state=Connected
    make a spotlight   from_device=device_1      to_device=device_1:meeting_user
    verify spotlight text on device   device=device_1   text=spotlight
    Close participants screen   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2  state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2

TC22:[Call-App] Verify user can enter mail id/user name and search For External Participants.
    [Tags]        444777      P0     bvt_sm      sanity_sm
    [Setup]  Testcase Setup for PSTN Disabled    count=2
    Verify user can enter mail id/user name and search For External Participants  from_device=device_1     to_device=device_2:pstn_disabled
    Reject incoming call   device_list=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]    Run Keywords    Capture on Failure   AND   Come back to home screen    device_list=device_1,device_2

*** Keywords ***
Test Case Teardown
    [Arguments]     ${devices}
    Come back to home screen     ${devices}

Wait untill call completes
    [Arguments]        ${time}
    Wait for Some Time    time=${wait_time}


Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page    ${device}

navigate calling option
    [Arguments]       ${device}
    navigate to teams admin settings   ${device}
    verify calling option in device settings page     ${device}

disabling auto accept meeting invite and start my video automatically
    [Arguments]     ${device}   ${state}
    Navigate to app settings page   ${device}
    navigate calling option      ${device}
    accept meeting invites automatically   ${device}    ${state}
    start my video automatically       ${device}     ${state}
    device setting back    ${device}
    device setting back    ${device}

Verify user can enter mail id/user name and search For External Participants
    [Arguments]     ${from_device}     ${to_device}
    Make outgoing call with username     ${from_device}     ${to_device}
