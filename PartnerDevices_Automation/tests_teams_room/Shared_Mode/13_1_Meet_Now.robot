*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Test Cases ***
TC1: [Meet now] Meet now icon should be present on Home screen after Sign-in
    [Tags]   259695     bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User    count=1
    Validate that signin is successfully completed    device_list=device_1     state=Sign in
    Verify Meet now icon present on home screen  device=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC2: [Meet now] Start Meet now, Add Participants to Conference call
    [Tags]   259697   bvt   bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=2
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC3: [Meet now] DUT user invites TDC user into meeting using DID number
     [Tags]   259700   bvt   bvt_sm  sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=2
    Initiates meeting using Meet now option using DID    from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Disconnect call   device=device_2
    End meeting   device=device_1
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

#Feature change: Meet now UI has changed to meeting UI, so, hold option is removed
#TC4: [Meet now] DUT user adds TDC user as participant , holds and resumes during call
#    [Tags]   259701     bvt_sm    sanity_sm
#    [Setup]   Testcase Setup for Meeting User     count=2
#    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_2
#    Accept incoming call    device=device_2
#    Verify meeting state   device_list=device_1,device_2    state=Connected
#    Hold the call   device=device_1
#    Verify Call State    device_list=device_1,device_2     state=Hold
#    Resume the call   device=device_1
#    Verify Call State    device_list=device_1,device_2     state=Resume
#    Check video call On state   device_list=device_1,device_2
#    End meeting   device=device_2
#    Verify meeting state    device_list=device_1,device_2   state=Disconnected
#    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC5: [Meet now] DUT user adds TDC user as participant , mute and unmutes during call
    [Tags]   259702   P1    sanity_sm
    [Setup]   Testcase Setup for Meeting User    count=2
    Initiates conference meeting using Meet now option   from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    Mutes the phone call    device=device_1
    Verify meeting Mute State    device_list=device_1    state=mute
    Unmutes the phone call  device=device_1
    Verify meeting Mute State    device_list=device_1    state=Unmute
    End meeting    device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC6: [Meet now] Verify DUT user is able to view the Live caption during meeting
    [Tags]   259711   sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=3
    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3    state=Connected
    Check video call On state    device_list=device_1,device_2,device_3
    Verify live captions visibility   device=device_1
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC7: [Meet now] Start Meet now, Increase and decrease volume after participants are added
    [Tags]   259698   P3
    [Setup]   Testcase Setup for Meeting User      count=2
    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    Adjust volume button   device=device_1   state=UP     functionality=In_meeting
    Adjust volume button   device=device_1   state=Down   functionality=In_meeting
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2

TC8: [Meet now] Start Meet now, Remove Participants from call
    [Tags]   259699   P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3    state=Connected
    Remove user from meeting call   from_device=device_1      to_device=device_3
    Verify someone removed you from the meeting call  device=device_3
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2    state=Connected
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC9: [Meet now] Verify DUT user is able to on and off the Live caption during the meeting
    [Tags]   259707   P2
    [Setup]   Testcase Setup for Meeting User    count=3
    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3    state=Connected
    Check video call On state   device_list=device_1,device_2,device_3
    Turn on live captions and validate   device=device_1
    Turn off live captions and validate  device=device_1
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC10: [Meet now] Start Meet now and Far mute Participants in call
    [Tags]   259713   P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Initiates conference meeting using Meet now option   from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3    state=Connected
    Check video call On state   device_list=device_1,device_2,device_3
    Farmute the call and validate   from_device=device_1     to_device=device_2
    Verify meeting Mute State    device_list=device_2    state=mute
    Unmutes the meeting    device=device_2
    Verify meeting Mute State    device_list=device_2    state=Unmute
    Close participants screen   device=device_1
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC11: [Meet now]DUT user able to raise /lower hand in the meeting
    [Tags]   259709   P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Initiates conference meeting using Meet now option   from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state    device_list=device_1,device_2,device_3    state=Connected
    Check video call On state   device_list=device_1,device_2,device_3
    Select raise hand option  device=device_1
    Verify raise hand notification   device_list=device_2,device_3
    Select Lower hand option  device=device_1
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC12: [Meet now] Teams Desktop Client to reject the meeting invite call from DUT user
    [Tags]   259706   P2
    [Setup]   Testcase Setup for Meeting User      count=3
    Initiates conference meeting using Meet now option   from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Reject incoming call   device_list=device_3
    Close participants screen   device=device_1
    Verify participants list in meeting     device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC13: [Meet now] Start Meet now and mute all Participants in call
    [Tags]   259703   P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Initiates conference meeting using Meet now option   from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check video call On state   device_list=device_1,device_2
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Mute all participants   device=device_1
    Verify meeting Mute State    device_list=device_2,device_3    state=Mute
    End meeting      device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC14: [Meet now] DUT user can check more options during meeting
    [Tags]  259708  bvt     bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=3
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Check video call On state   device_list=device_1,device_2,device_3
    verify more options in call control bar     device=device_1
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC15: [Meet now] Start Meet now, Verify mute UI on DUT in meeting
     [Tags]    259694       P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Farmute the call and validate   from_device=device_1     to_device=device_2
    verify farmute text on device   device=device_2     text=you have been muted
    verify mute off icon      device=device_2
    Close participants screen  device=device_1
    Farmute the call and validate   from_device=device_1     to_device=device_3
    verify farmute text on device     device=device_3     text=you have been muted
    verify mute off icon      device=device_3
    Close participants screen   device=device_1
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3

TC16: [Meet now] DUT user invites TDC user into meeting using DID number
    [Tags]   259712    P2
    [Setup]   Testcase Setup for Meeting User     count=3
    Initiates conference meeting using Meet now option    from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using phonenumber   from_device=device_1      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    End meeting   device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3    state=Disconnected
    [Teardown]   Run Keywords    Capture on Failure  AND    Test Case Teardown    devices=device_1,device_2,device_3


*** Keywords ***
Test Case Teardown
    [Arguments]     ${devices}
    Come back to home screen     ${devices}

Verify Meet now icon present on home screen
    [Arguments]     ${device}
    Verify home page screen     ${device}

Naviagte back to home screen page and validate
    [Arguments]     ${device}
    Come back to home screen     ${device}