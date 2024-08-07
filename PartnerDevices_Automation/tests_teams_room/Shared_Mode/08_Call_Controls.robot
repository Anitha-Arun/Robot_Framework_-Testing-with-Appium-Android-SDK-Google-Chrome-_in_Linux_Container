*** Settings ***
Documentation   Call Controls
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Audio - Call Hold] DUT puts call on hold with TDC
    [Tags]  237619   P1
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_2      to_device=device_1:meeting_user
    Accept incoming call    device=device_1
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Hold the call   device=device_1
    Verify Call State    device_list=device_1,device_2     state=Hold
    Resume the call   device=device_1
    Verify Call State    device_list=device_1,device_2     state=Resume
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC2: [Audio - Mute Call] DUT puts the call on Mute with TDC
    [Tags]  237621   bvt    bvt_sm      sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_2      to_device=device_1:meeting_user
    Accept incoming call    device=device_1
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2    state=Connected
    Mutes the phone call    device=device_1
    Verify meeting Mute State    device_list=device_1    state=mute
    Unmutes the phone call  device=device_1
    Verify meeting Mute State    device_list=device_1    state=Unmute
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

#Feature change: Video call UI has changed to meeting UI, so, hold option is removed
#TC3: [Video - Call Hold] DUT puts call on hold with TDC
#    [Tags]  237620   bvt   bvt_sm     sanity_sm
#    [Setup]  Testcase Setup for Meeting User    count=2
#    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
#    Accept incoming call    device=device_1
#    Wait for Some Time    time=${wait_time}
#    Verify Call State    device_list=device_1,device_2    state=Connected
#    Hold the call   device=device_1
#    Verify Call State    device_list=device_1,device_2     state=Hold
#    Resume the call   device=device_1
#    Verify Call State    device_list=device_1,device_2     state=Resume
#    Disconnect call     device=device_1
#    Verify Call State    device_list=device_1,device_2    state=Disconnected
#    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC4: [Video - Mute Call] DUT puts the call on Mute with TDC
    [Tags]  237622   P1  sanity_sm
    [Setup]  Testcase Setup for Meeting User    count=2
    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call    device=device_1
    Close participants screen   device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Mutes the phone call    device=device_1
    Verify meeting Mute State    device_list=device_1    state=mute
    Unmutes the phone call  device=device_1
    Verify meeting Mute State    device_list=device_1    state=Unmute
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC5: [Dialpad][Mic]Soft mute icon is disabled when user try to use dial pad in call
     [Tags]   317565   P2
    [Setup]   Testcase Setup for Meeting User   count=2
    Make outgoing call with phonenumber    from_device=device_1    to_device=device_2
    Accept incoming call    device=device_2
    verify dailpad on call controlbar   device=device_1
    verify mic on calling screen is not clickable    device=device_1
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC6: [Mixed - Mute Call] DUT puts the call on mute with Video enabled TDC
     [Tags]  237624   P1  sanity_sm
    [Setup]  Testcase Setup for Meeting User    count=2
    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call    device=device_1
    Close participants screen   device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Mutes the phone call    device=device_1
    Verify meeting Mute State    device_list=device_1    state=mute
    Unmutes the phone call  device=device_1
    Verify meeting Mute State    device_list=device_1    state=Unmute
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC7:[Call-App] Verify Call button on the home screen and Icon is updated to “Phone”.
    [Tags]        444757      P0
    [Setup]  Testcase Setup for Meeting User    count=1
    Verify Call button on the home screen and icon is updated to Phone      device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1

TC8:[Call-App] Verify the UI after selecting Call button on the home screen
     [Tags]        444758      P0
    [Setup]  Testcase Setup for Meeting User    count=1
    tap on dialpad and validate       device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1

TC9:[Call-App] Verify the Back button when user enters text in search field.
    [Tags]        444763      P2
    [Setup]  Testcase Setup for Meeting User    count=1
    verify back button when user enters text in search field    device=device_1
    [Teardown]    Run Keywords    Capture on Failure   AND   Come back to home screen    device_list=device_1

TC10:[Call] Call icon should be present on Home screen after Sign-in
     [Tags]        444807     P2
    [Setup]  Testcase Setup for Meeting User    count=1
    verify dial pad present on landing page          device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1

TC11:[Call] DUT user adds TDC user as participant, mute and unmutes during call.
    [Tags]      444814    P1       sanity_sm
    [Setup]   Testcase Setup for Meeting User  count=3
    Make outgoing call with displayname   from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Mutes the phone call    device=device_1
    Verify meeting Mute State    device_list=device_1    state=mute
    Unmutes the phone call  device=device_1
    Verify meeting Mute State    device_list=device_1    state=Unmute
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3


TC12:[Call]DUT user able to raise /lower hand in the Call.
     [Tags]     444821    P1       sanity_sm
    [Setup]   Testcase Setup for Meeting User  count=3
    Make outgoing call with displayname   from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    select raise hand option    device=device_3
    verify raise hand reaction  device=device_3
    lower the raised hand from another user     from_device=device_1   to_device=device_3
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC13:[Call] Start Call, Remove Participants from call
    [Tags]          444811       P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Make outgoing call with displayname    from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Remove user from meeting call   from_device=device_1      to_device=device_3
    Verify someone removed you from the meeting call  device=device_3
    Close participants screen   device=device_1
    End meeting   device=device_1
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC14:[Call] Start Call and mute all Participants in call.
    [Tags]         444815       P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Make outgoing call with displayname  from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    mute all participants       device=device_1
    Verify meeting Mute State    device_list=device_2,device_3    state=Mute
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3


TC15:[Call] Ending the call should redirect DUT user to home screen.
     [Tags]        444817      P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Make outgoing call with displayname  from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Wait for Some Time    time=${wait_time}
    Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    End meeting   device=device_1,device_2
    Ending the call should redirect DUT user to home screen  device=device_1
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC16:[Call-App] Verify the search field after dialing on the dial pad.
    [Tags]         444761      P2
    [Setup]   Testcase Setup for Meeting User     count=1
    verify functionality of dialing on the dial pad     device=device_1
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1

TC17:[Call] Verify DUT user is able to on and off the Live caption during the Call.
    [Tags]         444819      P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Make outgoing call with phonenumber    from_device=device_1      to_device=device_2
    Accept incoming call    device=device_2
    Wait for Some Time    time=${wait_time}
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Turn on live captions and validate   device=device_1
    Turn off live captions and validate  device=device_1
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC18:[Call] DUT user can check more options during Call.
    [Tags]         444820    P2
    [Setup]   Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_1      to_device=device_2
    Accept incoming call    device=device_2
    verify more options in call control bar     device=device_1
    End meeting   device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC19:[Call] DUT user invites TDC user into Call using DID number.
    [Tags]         444823    P2
    [Setup]   Testcase Setup for Meeting User     count=2
    call with DID number        from_device=device_1      to_device=device_2
    Accept incoming call    device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_1
    Verify meeting state    device_list=device_1   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC20:[Call] Start call and Far mute Participants in call.
    [Tags]      444824    P2
    [Setup]   Testcase Setup for Meeting User  count=3
    Make outgoing call with displayname   from_device=device_1     to_device=device_2
    Accept incoming call      device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call    device=device_3
    Close participants screen   device=device_1
    Wait for Some Time    time=${wait_time}
    Verify Call State    device_list=device_1,device_2,device_3    state=Connected
    Farmute the call and validate    from_device=device_1      to_device=device_2
    Verify meeting Mute State    device_list=device_2    state=mute
    End meeting   device=device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3



TC21:[Call] Verify that Auto dial functionality after entering the Valid/Non valid DID
     [Tags]      451147        P2
    [Setup]   Testcase Setup for Meeting User  count=2
    Make outgoing call with displayname   from_device=device_1     to_device=device_2
    verify auto accept timer is not present     device=device_1
    Accept incoming call      device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2


*** Keywords ***
Test Case Teardown
    [Arguments]     ${devices}
    Come back to home screen     ${devices}

Verify Call button on the home screen and icon is updated to Phone
    [Arguments]     ${device}
    verify dial pad present on landing page     ${device}

Ending the call should redirect DUT user to home screen
    [Arguments]     ${device}
    Verify home page screen    ${device}

call with DID number
    [Arguments]     ${from_device}      ${to_device}
    Make outgoing call with phonenumber     ${from_device}      ${to_device}

verify functionality of dialing on the dial pad
    [Arguments]     ${device}
    Dial and verify the numbers from 0 to 9    device_list=${device}