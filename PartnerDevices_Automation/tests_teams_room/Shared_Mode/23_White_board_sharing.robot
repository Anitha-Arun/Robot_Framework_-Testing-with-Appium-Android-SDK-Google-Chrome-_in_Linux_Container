*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  3
${action_time} =  5

*** Test Cases ***
TC1:[Whiteboard Sharing] DUT user should have an option to share whiteboard during meeting
    [Tags]  305644     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    verify whiteboard sharing option on call control bar   device=device_1
    Wait for Some Time    time=${action_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC2:[Whiteboard Sharing]DUT user to verify the whiteboard tools during meeting
    [Tags]      305646    bvt_sm     sanity_sm
    [Setup]  Testcase Setup for Meeting User   count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify and click on white board sharing in call control bar   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Verify whiteboard tools display on screen    device=device_1
    Stop presenting whiteboard share screen   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC3:[Whiteboard Sharing] "Stop presenting" button must be displayed on Docked Ubar on DUT user screen
     [Tags]  305665   P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    verify whiteboard sharing option under more option   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1,device_2
    verify Stop presenting whiteboard share screen in Docked Ubar and stop whiteboard share    device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC4:[MS Whiteboard] Verify mic status is same when whiteboard is shared as it is in meeting
    [Tags]      312852    P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2   meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    Mutes the phone call    device=device_2
    Verify meeting Mute State    device_list=device_2    state=mute
    verify whiteboard sharing option under more option   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1,device_2
    Verify meeting Mute State    device_list=device_2    state=mute
    Unmutes the phone call   device=device_1
    Verify meeting Mute State    device_list=device_1    state=unmute
    Stop presenting whiteboard share screen     device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC5:[Whiteboard] Observe Whiteboard when DUT user rejoins the meeting when removed by TDC
    [Tags]      313237   P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_1,device_2,device_3   meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3   state=Connected
    verify whiteboard sharing option under more option   device=device_2
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_2    connected_device_list=device_1,device_2,device_3
    Remove user from meeting call   from_device=device_2      to_device=device_1:meeting_user
    Verify someone removed you from the meeting call  device=device_1
    Close participants screen   device=device_2
    Verify meeting state    device_list=device_1   state=Disconnected
    Join meeting   device=device_1   meeting=lock_meeting
    Verify meeting state   device_list=device_1     state=Connected
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_2    connected_device_list=device_1,device_2,device_3
    Wait for Some Time    time=${wait_time}
    Stop presenting whiteboard share screen    device=device_2
    close white board popup     device=device_1
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC6:[Whiteboard] Verify DUT user screen when whiteboard is being shared and TDC user is spotlighted
    [Tags]      313359   P2
    [Setup]    Testcase Setup for Meeting User   count=3
    Join meeting   device=device_1,device_2,device_3   meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3   state=Connected
    verify whiteboard sharing option under more option   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_2    connected_device_list=device_1,device_2,device_3
    make a spotlight   from_device=device_2   to_device=device_1:meeting_user
    verify spotlight text on device   device=device_1   text=spotlight
    Close participants screen   device=device_2
    Stop presenting whiteboard share screen    device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC7:[Whiteboard Sharing]DUT user to share whiteboard during meeting
    [Tags]   305645     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    verify whiteboard sharing option on call control bar   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC8:[Whiteboard Sharing]DUT user to access whiteboard tools during meeting
    [Tags]      305647      P2
    [Setup]  Testcase Setup for Meeting User   count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify and click on white board sharing in call control bar   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Verify whiteboard tools display on screen    device=device_1
    Stop presenting whiteboard share screen   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC9:[Whiteboard Sharing] DUT user to mute the call from whiteboard screen
     [Tags]      305655    P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2   meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    verify whiteboard sharing option under more option   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1,device_2
    Mutes the phone call    device=device_2
    Verify meeting Mute State    device_list=device_2    state=mute
    Unmutes the phone call   device=device_1
    Verify meeting Mute State    device_list=device_1    state=unmute
    Stop presenting whiteboard share screen     device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC10:[Whiteboard Sharing] DUT user to verify settings option on whiteboard
    [Tags]  305657     P2
     [Setup]  Testcase Setup for Meeting User   count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify and click on white board sharing in call control bar   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Verify sliding menu option inside settings icon    device=device_1
    Stop presenting whiteboard share screen   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC11:[Whiteboard Sharing] Verify switching to separate layouts when DUT User is sharing whiteboard when in meeting
    [Tags]    316759        P2
    [Setup]  Testcase Setup for Meeting User   count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify and click on white board sharing in call control bar   device=device_1
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Verify whiteboard tools display on screen    device=device_1
    Stop presenting whiteboard share screen   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC12:[Whiteboard]Verify DUT user should be able to see MS Whiteboard option in home screen
    [Tags]   339392   P2
    [Setup]  Testcase Setup for Meeting User     count=1
    Validate that signin is successfully completed    device_list=device_1     state=Sign in
    verify white board is in home page screen     device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1

TC13:[Whiteboard]DUT user verifies the text displayed when Tapped on Whiteboard on Home screen
    [Tags]   339393      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=1
    verify whiteboard sharing option on home screen option  device=device_1
    Wait for Some Time    time=${action_time}
    verify the text of white board reflected on displayed   device=device_1
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1
    Wait for Some Time    time=${action_time}
    Stop presenting whiteboard share screen     device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1
    Verify meeting state    device_list=device_1  state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1


TC14:[Whiteboard Sharing] Incoming call during meeting when DUT shared whiteboard
    [Tags]      305663      P1
    [Setup]  Testcase Setup for Meeting User   count=3
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify and click on white board sharing in call control bar   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Make outgoing call with phonenumber    from_device=device_3     to_device=device_1
    verify user should not get second incoming call     device=device_1
    Stop presenting whiteboard share screen   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3


TC15:[Whiteboard]DUT user verifies "Add Participants UI" in the "Start Meeting" of Whiteboard.
    [Tags]      339399      P1
    [Setup]  Testcase Setup for Meeting User   count=3
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify and click on white board sharing in call control bar   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3    state=Connected
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2,device_3
    Stop presenting whiteboard share screen   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3


TC16:[Whiteboard Sharing]DUT user to stop presenting the whiteboard
    [Tags]       418905     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    Verify and click on white board sharing in call control bar   device=device_1
    Wait for Some Time    time=${action_time}
    Stop presenting whiteboard share screen   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC17:[Whiteboard]Verify DUT throws a Manual exit pop up when user select "Stop Whiteboard" with Whiteboard open.
    [Tags]        339402       P2
    [Setup]   Testcase Setup for Meeting User     count=1
    verify whiteboard sharing option on home screen option  device=device_1
    Wait for Some Time    time=${action_time}
    Verify Stop Whiteboard Button Behavior when Tapped on it    device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1


TC18:[Whiteboard]Verify DUT user can see "Start Meeting "and "Stop Whiteboard" options when the DUT user Launch whiteboard
    [Tags]        339394   P2
    [Setup]   Testcase Setup for Meeting User     count=1
    verify whiteboard sharing option on home screen option  device=device_1
    verify Start Meeting and Stop Whiteboard options when the dut user launch whiteboard    device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1

TC19:[Whiteboard]Verify whether DUT user is able to Start meeting after Whiteboard is launched
    [Tags]       339395     P2
    [Setup]   Testcase Setup for Meeting User     count=1
    verify Start meeting and verify Whiteboard launch  device=device_1
    Wait for Some Time    time=${action_time}
    Verify meeting state   device_list=device_1    state=Connected
    Stop presenting whiteboard share screen     device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1
    Verify meeting state    device_list=device_1  state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC20:[Whiteboard]Verifying the User able to select the Searched Participants while DUT start meeting in Whiteboard.
     [Tags]   339397     P2
    [Setup]   Testcase Setup for Meeting User     count=2
    verify Start Whiteboard sharing from home screen  device=device_1
    Wait for Some Time    time=${action_time}
    Add participant to conversation using display name   from_device=device_1      to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2    state=Connected
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Stop presenting whiteboard share screen   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC21:[Whiteboard]DUT user Verify Cancel Button Behavior when Tapped on Whiteboard Option.
    [Tags]        339400       P2
    [Setup]   Testcase Setup for Meeting User     count=1
    verify whiteboard sharing option on home screen option  device=device_1
    Wait for Some Time    time=${action_time}
    Verify Stop Whiteboard Button Behavior when Tapped on it    device=device_1
     [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1


TC22:[Whiteboard]Verifying the Whiteboard sharing screen visible to the added Participants.
    [Tags]      339407     P2
    [Setup]   Testcase Setup for Meeting User     count=2
    verify Start Whiteboard sharing from home screen  device=device_1
    Wait for Some Time    time=${action_time}
    Add participant to conversation using display name   from_device=device_1      to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2    state=Connected
    Check for whiteboard visibility of participants and validate  from_device=device_1    connected_device_list=device_1,device_2
    Stop presenting whiteboard share screen   device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC23:[Whiteboard]DUT user Enable the Whiteboard from the Teams admin settings.
    [Tags]     339417        P2
    [Setup]  Testcase Setup for Meeting User     count=1
    navigate to teams admin settings page   device=device_1
    Enable and disable white board sharing toggle     device=device_1     state=on
    come back from admin settings page     device_list=device_1
    verify white board is in home page screen  device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1

TC24:[Whiteboard]DUT user Disable the Whiteboard from the Teams admin settings.
    [Tags]     339424        P2
    [Setup]  Testcase Setup for Meeting User     count=1
    navigate to teams admin settings page   device=device_1
    Enable and disable white board sharing toggle     device=device_1     state=off
    come back from admin settings page     device_list=device_1
    verify whiteboard sharing option is not present in home screen  device=device_1
    [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1       AND     Enable the whiteboard sharing   device=device_1

TC25:[Whiteboard]Verifying the Reactions while in meeting on whiteboard screen.
    [Tags]      339428     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2   meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    verify whiteboard sharing option under more option   device=device_1
    Wait for Some Time    time=${action_time}
    Check for whiteboard visibility of participants and validate    from_device=device_1    connected_device_list=device_1,device_2
    tap on heart button     device=device_2
    verify reaction on screen    device=device_1
    tap on laugh button     device=device_2
    verify reaction on screen     device=device_1
    Stop presenting whiteboard share screen    device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC26:[Whiteboard]Verify when DUT user Stop white board " Continue or Exit whiteboard" pop up should be displayed
    [Tags]      418906    P2
    [Setup]   Testcase Setup for Meeting User     count=1
    verify whiteboard sharing option on home screen option  device=device_1
    Wait for Some Time    time=${action_time}
    Verify Stop Whiteboard Button Behavior when Tapped on it    device=device_1
     [Teardown]   Run Keywords   Capture on Failure   AND    Come back to home screen     device_list=device_1


*** Keywords ***
verify Stop presenting whiteboard share screen in Docked Ubar and stop whiteboard share
    [Arguments]    ${device}
    Stop presenting whiteboard share screen      ${device}

Verify and click on white board sharing in call control bar
        [Arguments]    ${device}
        Verify whiteboard sharing option under more option   ${device}

close white board popup
     [Arguments]    ${device}
     device right corner click   ${device}

verify white board is in home page screen
     [Arguments]    ${device}
     verify home page screen     ${device}

verify the text of white board reflected on displayed
    [Arguments]    ${device}
    start meeting from whiteboard sharing    ${device}

verify Start Whiteboard sharing from home screen
    [Arguments]    ${device}
    verify Start meeting and verify Whiteboard launch   ${device}

Verify Stop Whiteboard Button Behavior when Tapped on it
    [Arguments]    ${device}
    verify Start Meeting and Stop Whiteboard options when the dut user launch whiteboard    ${device}

navigate to teams admin settings page
    [Arguments]    ${device}
    Click on more option   ${device}
    Click on settings page   ${device}
    navigate to teams admin settings      ${device}

Enable the whiteboard sharing
    [Arguments]     ${device}
    navigate to teams admin settings page   ${device}
    Enable and disable white board sharing toggle     ${device}      state=on
    come back from admin settings page      device_list=${device}
    Come back to home screen    device_list=${device}


Verify Stop Whiteboard Button and verify cancle Whiteboard Button
    [Arguments]    ${device}
    verify Start Meeting and Stop Whiteboard options when the dut user launch whiteboard    ${device}
