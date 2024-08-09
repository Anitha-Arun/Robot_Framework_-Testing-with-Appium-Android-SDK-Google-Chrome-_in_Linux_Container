*** Settings ***
Documentation  Here we are validating the stress scenerio's of teams rooms on shared mode
...  The goal is ensure that all the feature related to teams app should work properly with mutiple iteration run.
Force Tags    sm_stress     alt_blocked
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =      10s
${iteration}=   30

*** Test Cases ***
TC1: Verify DUT user and other participants can joins the same meeting multiple times without any failure
    [Tags]    stress_sm
    [Setup]  Testcase Setup for Meeting User    count=3
    Verify DUT user join teams room meeting with participants      device=device_1      meeting=cnf_device_meeting
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC2: Verify DUT user can turn off/on the video icon mutiple times during the meeeting.
    [Tags]    stress_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Wait for Some Time    time=${wait_time}
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Get screenshot     name=verify_particpants_preview   device_list=device_1,device_2
    DUT user turn off/on video icon mutiple times   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen     device_list=device_1,device_2

TC3: Verify DUT user can mute/unmute itself multiple times while in a meeting.
    [Tags]    stress_sm
    [Setup]  Testcase Setup for Meeting User      count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Wait for Some Time    time=${wait_time}
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify DUT user mute and unmute in a meeting   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen   device_list=device_1,device_2

#Feature change: Video call UI has changed to meeting UI, so, hold option is removed
#TC4: Verify DUT user can hold/resume and mute/unmute the TDC user video call multiple times.
#    [Tags]    stress_sm
#    [Setup]  Testcase Setup for Meeting User     count=2
#    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
#    Accept incoming call    device=device_1
#    Wait for Some Time    time=${wait_time}
#    Verify meeting state   device_list=device_1,device_2    state=Connected
#    Verify DUT user hold and resume & mute and unmute the call multiple times  device=device_1
#    Disconnect call     device=device_2
#    Verify Call State    device_list=device_1,device_2    state=Disconnected
#    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1,device_2

TC5: Verify DUT user can mute/unmute participants multiple times during a meeting.
    [Tags]    stress_sm
    [Setup]  Testcase Setup for Meeting User      count=3
    Join meeting    device=device_1,device_2,device_3    meeting=cnf_device_meeting
    Wait for Some Time    time=${wait_time}
    Verify meeting state   device_list=device_1,device_2,device_3   state=Connected
    Verify participants list in meeting    device=device_1
    Verify DUT user mute other participants while in a meeting     device=device_1
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1,device_2,device_3

TC6: Verify DUT user can make video call to TDC and turn off/on the video icon mutiple times.
    [Tags]    stress_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Make Video call using display name  from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Get screenshot     name=verify_particpants_preview   device_list=device_1,device_2
    DUT user turn off/on video icon mutiple times     device=device_1
    End meeting   device=device_1,device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1,device_2

TC7: Verify DUT user can hold/resume and mute/unmute outgoing voice call to TDC multiple times without any failure.
    [Tags]    stress_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Verify DUT user make an outgoing voice call to TDC user multiple times     from_device=device_1     to_device=device_2
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1,device_2

TC8: Verify DUT user can increase/decrease the volume in a meeting.
    [Tags]    stress_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting    device=device_1,device_2   meeting=cnf_device_meeting
    Wait for Some Time    time=${wait_time}
    Verify meeting state   device_list=device_1,device_2   state=Connected
    Verify participants list in meeting    device=device_1
    Verify Increase/decrease volume button    device=device_1
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1,device_2

TC9: Verify DUT user can dial the number from 0_to_9 without any failure.
    [Tags]    stress_sm     0_9
    [Setup]  Testcase Setup for Meeting User     count=1
    Verify DUT user can dial the number from 0_to_9    device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1

TC10: Verify the DUT user can turn off/on incoming video mutiple times and check for the self preview display properly on the screen.
    [Tags]    stress_sm
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting    device=device_1,device_2,device_3    meeting=cnf_device_meeting
    Wait for Some Time    time=${wait_time}
    Verify meeting state   device_list=device_1,device_2,device_3   state=Connected
    Verify participants list in meeting    device=device_1
    Verify DUT user can turn off and on incoming video    device=device_1
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Come back to home screen   device_list=device_1,device_2,device_3

TC11: Verify DUT user can enable/disabled raise hand in the meeting.
    [Tags]    stress_sm
    [Setup]  Testcase Setup for Meeting User    count=2
    DUT user can enable and disable raise hand in a meeting    device=device_1      meeting=cnf_device_meeting
    [Teardown]   Run Keywords    Capture on Failure  AND     Come back to home screen    device_list=device_1,device_2




*** Keywords ***
Verify DUT user join teams room meeting with participants
    [Arguments]       ${device}     ${meeting}
    FOR   ${INDEX}   IN RANGE    0   ${iteration}
        Log   ${INDEX}
        Join meeting    device=device_1,device_2,device_3    meeting=${meeting}
        Wait for Some Time    time=${wait_time}
        Verify meeting state   device_list=device_1,device_2,device_3   state=Connected
        Verify participants list in meeting    device=${device}
        End meeting   device=device_1,device_2,device_3
        Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
        Come back to home screen   device_list=device_1,device_2,device_3
    END

DUT user turn off/on video icon mutiple times
    [Arguments]      ${device}
    FOR  ${INDEX}   IN RANGE   0    ${iteration}
        Log   ${INDEX}
        Disable video call   device=${device}
        Get screenshot       name=verify_self_preview_after_disable_video   device_list=${device}
        Enable video call    device=${device}
        Get screenshot       name=verify_self_preview_after_enable_video   device_list=${device}
    END

Verify DUT user mute and unmute in a meeting
    [Arguments]      ${device}
    FOR  ${INDEX}   IN RANGE   0   ${iteration}
        Log   ${INDEX}
        Mutes the phone call    device=${device}
        Verify meeting Mute State   device_list=${device}    state=mute
        Unmutes the phone call   device=${device}
        Verify meeting Mute State    device_list=${device}    state=unmute
    END

Verify DUT user hold and resume & mute and unmute the call multiple times
    [Arguments]      ${device}
    FOR  ${INDEX}   IN RANGE   0   ${iteration}
         Log   ${INDEX}
         Hold the call   device=${device}
         Verify Call State    device_list=device_1,device_2     state=Hold
         Resume the call   device=${device}
         Verify Call State    device_list=device_1,device_2     state=Resume
         Mutes the phone call    device=${device}
         Verify meeting Mute State   device_list=${device}    state=mute
         Unmutes the phone call   device=${device}
         Verify meeting Mute State    device_list=${device}    state=unmute
    END

Verify DUT user mute other participants while in a meeting
    [Arguments]      ${device}
    FOR  ${INDEX}   IN RANGE   0    ${iteration}
        Log   ${INDEX}
        Mute all participants    device=${device}
        Unmutes the phone call   device=device_2
    END

Verify DUT user make an outgoing voice call to TDC user multiple times
    [Arguments]     ${from_device}      ${to_device}
    FOR  ${INDEX}   IN RANGE   0    ${iteration}
        Log   ${INDEX}
        Make outgoing call with phonenumber    from_device=${from_device}     to_device=${to_device}
        Accept incoming call      device=${to_device}
        Wait for Some Time    time=${wait_time}
        Verify Call State    device_list=${from_device}   state=Connected
        Hold the call   device=${from_device}
        Verify Call State    device_list=device_1,device_2     state=Hold
        Resume the call   device=${from_device}
        Verify Call State    device_list=device_1,device_2     state=Resume
        Mutes the phone call    device=${from_device}
        Verify meeting Mute State   device_list=${from_device}   state=mute
        Unmutes the phone call   device=${from_device}
        Verify meeting Mute State    device_list=${from_device}    state=unmute
        Disconnect call     device=${to_device}
        Verify Call State    device_list=${from_device}      state=Disconnected
    END

Verify Increase/decrease volume button
     [Arguments]       ${device}
     FOR  ${INDEX}   IN RANGE   0    ${iteration}
        Adjust volume button   ${device}    state=UP     functionality=In_meeting
        Adjust volume button   ${device}    state=Down   functionality=In_meeting
     END


Verify DUT user make outgoing call using auto dial
    [Arguments]     ${from_device}     ${to_device}
    FOR  ${INDEX}   IN RANGE   0    ${iteration}
        Log   ${INDEX}
        Place a call    ${from_device}     ${to_device}    method=phone_number    dial_mode=auto_dial
        Accept incoming call      device=${to_device}
        Wait for Some Time    time=${wait_time}
        Verify Call State    device_list=${from_device}   state=Connected
        Disconnect call     device=${to_device}
        Verify Call State    device_list=${from_device}      state=Disconnected
    END

Verify DUT user can dial the number from 0_to_9
     [Arguments]        ${device}
     FOR  ${INDEX}   IN RANGE   0    ${iteration}
        Log   ${INDEX}
        Dial and verify the numbers from 0 to 9    device_list=${device}
#        Close dial pad screen       ${device}
     END


DUT user can enable and disable raise hand in a meeting
    [Arguments]       ${device}     ${meeting}
    FOR   ${INDEX}   IN RANGE    0   ${iteration}
        Log   ${INDEX}
        Join meeting    device=device_1,device_2    meeting=${meeting}
        Wait for Some Time    time=${wait_time}
        Verify meeting state   device_list=device_1,device_2   state=Connected
        Check video call On state   device_list=device_1,device_2
        Select raise hand option   ${device}
        Verify raise hand notification   device_list=device_2
        Select Lower hand option    ${device}
        End meeting   device=device_1,device_2
        Verify meeting state    device_list=device_1,device_2   state=Disconnected
    END

Verify DUT user can turn off and on incoming video
    [Arguments]       ${device}
    FOR   ${INDEX}   IN RANGE    0   ${iteration}
        Log   ${INDEX}
        Turn off incoming call   device_list=${device}
        Get screenshot    name=verify_self_preview_after_turn_off_incoming_video   device_list=device_1,device_2,device_3
        Turn on incoming call    device_list=${device}
        Get screenshot   name=verify_self_preview_after_turn_on_incoming_video   device_list=device_1,device_2,device_3
    END
