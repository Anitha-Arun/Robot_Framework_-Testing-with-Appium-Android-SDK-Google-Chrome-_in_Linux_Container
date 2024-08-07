*** Settings ***
Documentation   Validating the functionality of Console Meet now feature
Force Tags    sm_meet_now      sm
Library     DateTime
Library     OperatingSystem
Resource  ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Meet now] Disconnecting the meet now call should redirect to home screen
    [Tags]      315366   bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User    count=3
    Start meeting using meet now   from_device=console_1    to_device=device_2
    Accept incoming call   device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Add participant to the conversation using display name  from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2,device_3    state=Connected
    Verify and view list of participant     console=console_1
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC2:[Meet now] TDC user invites Touch console user into meeting using DID number
    [Tags]  315354      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User    count=3
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
#    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Add participant to the conversation using phonenumber   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2,device_3    state=Connected
    Verify and view list of participant     console=console_1
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC3: [Meet now] Meet now icon should be present on Home Screen after Sign-in
    [Tags]      315344  bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User   count=1
    Verify signin is successful   console_list=console_1     state=Sign in
    Verify meet now present on home screen  console=console_1
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC4: [Meet now] Tapping on Meet now icon should initiate a conference call
    [Tags]      315346      sanity_sm   P1
    [Setup]   Testcase Setup for shared User   count=2
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    End up call     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

#Feature change: Meet now UI has changed to meeting UI, so, hold option is removed
#TC5: [Meet now] Touch console user adds TDC user as participant , holds and resumes during call
#    [Tags]      315358      bvt_sm      sanity_sm
#    [Setup]   Testcase Setup for shared User   count=2
#    Start meeting using meet now    from_device=console_1    to_device=device_2
#    Accept incoming call      device=device_2
#    Wait for Some Time    time=${wait_time}
#    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
#    Hold current call   console=console_1
#    Verify for call state     console_list=console_1    device_list=device_2    state=Hold
#    Resume current call  console=console_1
#    Verify for call state     console_list=console_1     state=Resume
#    End the meeting      console=console_1
#    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
#    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC6: [Meet now] Touch console user adds TDC user as participant , mute and unmutes during call
    [Tags]      315360   sanity_sm      P1
    [Setup]   Testcase Setup for shared User   count=2
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Mute the call      console=console_1
    Verify and check call mute state      console_list=console_1    state=Mute
    Unmute the call    console=console_1
    Verify and check call mute state     console_list=console_1    state=Unmute
    End up call     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC7 : [Meet now] Touch console user can check more options during meeting
    [Tags]      315372      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User   count=3
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Wait for Some Time    time=${wait_time}
    Verify for call state     console_list=console_1    device_list=device_2,device_3    state=Connected
    Verify and view list of participant     console=console_1
    Verify option present inside more option and validate  console=console_1
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC8: [Meet now] Start Meet now and Far mute Participants in Conference call
    [Tags]   315382   P1
    [Setup]   Testcase Setup for shared User   count=3
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Farmute the call and validate    from_device=console_1       to_device=device_2
    Verify meeting Mute State    device_list=device_2    state=mute
    Unmutes the meeting    device=device_2
    Verify meeting Mute State    device_list=device_2    state=Unmute
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC9: [Meet now] Start Meet now, Remove Participants from meeting
    [Tags]      315352      P2
    [Setup]   Testcase Setup for shared User   count=3
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1    device_list=device_2    state=Connected
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Remove user from meeting call   from_device=console_1     to_device=device_3        device_type=console
    Verify someone removed you from the meeting call  device=device_3
    Verify meeting state    device_list=device_3    state=Disconnected
    Verify for meeting state     console_list=console_1    device_list=device_2    state=Connected
    End up call      console=console_1      device=device_2
    Verify for meeting state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC10: [Meet now] Start Meet now and mute all Participants in Conference call
    [Tags]   315362   P2
    [Setup]   Testcase Setup for shared User   count=3
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Mute all active participants        console=console_1
    Verify meeting Mute State    device_list=device_2,device_3    state=mute
    End up call     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC11:[Meet now] Teams Desktop Client to reject the meeting invite call from Touch console user
    [Tags]   315368   P2
    [Setup]   Testcase Setup for shared User   count=2
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Reject incoming call   device_list=device_2
    Verify meeting state    device_list=device_2   state=Disconnected
    Disconnect the call     console=console_1
    Verify for call state     console_list=console_1      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC12:[Meet now] Verify Touch console user is able to on and off the Live caption during the meeting
    [Tags]   315370   P2
    [Setup]   Testcase Setup for shared User     count=2
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Check for live captions visibility   console=console_1
    Turn on live captions option    console=console_1
    Turn off live captions option   console=console_1
    End up call      console=console_1      device=device_2
    Verify for meeting state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC13:[Meet now]Touch console user able to raise /lower hand in the meeting
    [Tags]      315374  P2
    [Setup]   Testcase Setup for shared User     count=3
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Verify and select raise hand option  console=console_1
    Verify raise hand notification   device_list=device_2
    Verify and select lower hand option     console=console_1
    End up call      console=console_1      device=device_2,device_3
    Verify for meeting state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC14:[Meet now] Touch console invites TDC user into meeting using DID number
    [Tags]      315380  P2
    [Setup]   Testcase Setup for shared User     count=2
    Start meeting using DID    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    End up call      console=console_1      device=device_2
    Verify for meeting state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC15:[Meet now] Start Meet now and Add Participants to the call
    [Tags]   315348   P2
    [Setup]   Testcase Setup for shared User   count=3
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC16:[Meet now] Start Meet now, Increase and decrease volume after participants are added
    [Tags]   315350   P2
    [Setup]   Testcase Setup for shared User   count=3
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify video preview on screen  device=device_1,device_2,device_3
    Verify functionality of volume button    console=console_1   button=UP
    Verify functionality of volume button    console=console_1   button=Down
    End up call     console=console_1       device=device_2,device_3
    Verify for call state    console_list=console_1    device_list=device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC17:[Meeting] Touch console share the Whiteboard during meeting
    [Tags]      315384      P2
    [Setup]  Testcase Setup for shared User   count=3
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify whiteboard sharing option under more option        device=console_1
    Verify whiteboard visibility for all participants   device_list=device_1:meeting_user,device_2,device_3
    Click on stop whiteboard sharing    console=console_1       device=device_1
    End up call     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3


TC19:[Meet] [MTRA + Console] Verify the DUT is able to initiate a meeting using a meet option in Console home screen.
    [Tags]      344901   bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User    count=2
    Verify ad-hoc meeting page     device=device_1     console=console_1
    End the meeting     console=console_1
    Verify for call state    console_list=console_1    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC20:[Meet] [MTRA + Console] Verify the console is able to add participants in meeting.
    [Tags]      344902   P1     sanity_sm
    [Setup]   Testcase Setup for shared User    count=2
    Verify ad-hoc meeting page     device=device_1     console=console_1
    End the meeting     console=console_1
    Verify for call state    console_list=console_1    state=Disconnected
    Start meeting using meet now   from_device=console_1    to_device=device_2
    Accept incoming call   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    End up call     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC21:[Meet] Touch console User to start Meet from Home screen with policy assigned account
    [Tags]      424480  P1      sanity_sm
    [Setup]   Testcase Setup for shared User    count=2
    Start meeting using meet now   from_device=console_1    to_device=device_2
    Accept incoming call   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Verify call control bar options     console=console_1
    End up call     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC22:[Meet] [MTRA + Console] Verify the User is able to share whiteboard in meeting using console.
    [Tags]      344904      P2
    [Setup]  Testcase Setup for shared User   count=2
    Verify ad-hoc meeting page     device=device_1     console=console_1
    End the meeting     console=console_1
    Verify for call state    console_list=console_1    state=Disconnected
    Start meeting using meet now   from_device=console_1    to_device=device_2
    Accept incoming call   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Verify and click on white board sharing in call control bar   device=console_1
    Wait for Some Time    time=${wait_time}
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    End up call     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC22:[Meet] Verify that the meeting starts with all default parameters:Meeting title format – “Meeting with [Room Name]" Camera ON ,Audio ON
    [Tags]      438411      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User   count=1
    Verify meet now parameters in meeting joining ui      device=console_1
    Disconnect the call     console=console_1
    Verify for call state    console_list=console_1     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC23:[Meet] After joining the meeting verify All organizer options must be available for ad-hoc meeting Lock meeting Manage permissions Mute all Don’t allow attendees to unmute
    [Tags]      438412      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User   count=3
    Verify meet now parameters in meeting joining ui      device=console_1
    Disconnect the call     console=console_1
    Verify for call state    console_list=console_1     state=Disconnected
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify the organizer options on ad hoc meeting      console=console_1
    End up call     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3


*** Keywords ***
End up call
    [Arguments]    ${console}    ${device}
    Disconnect the call  ${console}
    Disconnect call     ${device}

Verify ad-hoc meeting page
    [Arguments]     ${device}       ${console}
    Verify precall screen after clicking on meetnow     ${device}       ${console}

Verify call control bar options
    [Arguments]    ${console}
    Verify docked ubar options      ${console}

Verify and click on white board sharing in call control bar
        [Arguments]    ${device}
        Verify whiteboard sharing option under more option   ${device}
