*** Settings ***
Documentation   Validating the functionality of Lock meeting Feature.
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

Suite Setup      Meeting setup
Suite Teardown   Suite Failure Capture


*** Test Cases ***
TC1: [Lock Meeting] Verify that lock the meeting option must not be available at DUT user's end (DUT user is presenter)
     [Tags]  260592   P2
     [Setup]  Testcase Setup for Meeting User     count=2
     Join meeting   device=device_1,device_2     meeting=lock_meeting
     Verify meeting state   device_list=device_1,device_2    state=Connected
     Verify participants list in meeting    device=device_1
     verify lock meeting is not present         device=device_1
     End meeting      device=device_1,device_2
     Verify meeting state    device_list=device_1,device_2    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC2: [Lock Meeting] Verify lock icon must be displayed along with "Lock the meeting"
     [Tags]  260593   P2
     [Setup]  Testcase Setup for Meeting User     count=2
     Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
     Verify meeting state   device_list=device_1,device_2    state=Connected
     Check meeting lock state   device_list=device_1
     Tap on lock meeting   device=device_1
     Tap on unlock meeting     device=device_1
     End meeting      device=device_1,device_2
     Verify meeting state    device_list=device_1,device_2    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC3: [Lock Meeting] Verify that user can lock/unlock the meeting/All day meeting
     [Tags]  260594     bvt_sm      sanity_sm
     [Setup]  Testcase Setup for Meeting User     count=2
     Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
     Verify meeting state   device_list=device_1,device_2    state=Connected
     Verify participants list in meeting    device=device_1
     Check meeting lock state   device_list=device_1
     Tap on lock meeting   device=device_1
     Check meeting unlock state   device_list=device_1
     Tap on unlock meeting    device=device_1
     End meeting      device=device_1,device_2
     Verify meeting state    device_list=device_1,device_2    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC4: [Lock Meeting] Verify that DUT user should not able to join the meeting when the meeting is locked by TDC user
     [Tags]  260597   P1        sanity_sm
     [Setup]  Testcase Setup for Meeting User     count=3
     Join meeting   device=device_2,device_3    meeting=lock_meeting
     Verify meeting state   device_list=device_2,device_3    state=Connected
     Tap on lock meeting   device=device_2
     Verify user cannot join the locked meeting    device=device_1     meeting=lock_meeting
     End meeting      device=device_2,device_3
     Verify meeting state    device_list=device_2,device_3    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC5: [Lock Meeting] Verify that DUT user cannot join the locked meeting
     [Tags]  260601   bvt_sm        sanity_sm
     [Setup]  Testcase Setup for Meeting User     count=2
     Join meeting    device=device_2    meeting=lock_meeting
     Verify meeting state   device_list=device_2    state=Connected
     Tap on lock meeting   device=device_2
     Verify user cannot join the locked meeting    device=device_1    meeting=lock_meeting
     Come back to home screen    device_list=device_1
     Tap on unlock meeting     device=device_2
     Join meeting   device=device_1    meeting=lock_meeting
     Verify meeting state   device_list=device_1,device_2    state=Connected
     End meeting      device=device_1,device_2
     Verify meeting state    device_list=device_1,device_2    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC6: [Lock Meeting] Verify that Organizer(DUT) should have lock meeting option at meeting screen
     [Tags]  260600   P1
     [Setup]  Testcase Setup for Meeting User     count=2
     Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
     Verify meeting state   device_list=device_1,device_2    state=Connected
     Verify participants list in meeting    device=device_1
     Check meeting lock state   device_list=device_1
     End meeting      device=device_1,device_2
     Verify meeting state    device_list=device_1,device_2    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC7: [Lock Meeting] Verify that DUT user can add other participants in a locked meeting
     [Tags]     260598    bvt_sm      sanity_sm
     [Setup]  Testcase Setup for Meeting User     count=3
     Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
     Verify meeting state   device_list=device_1,device_2    state=Connected
     Check meeting lock state  device_list=device_1
     Tap on lock meeting   device=device_1
     Add participant to conversation using display name     from_device=device_1      to_device=device_3
     Accept incoming call    device=device_3
     Close participants screen   device=device_1
     Verify list of participants   from_device=device_1      connected_device_list=device_1:meeting_user,device_2,device_3
     Verify meeting state   device_list=device_1,device_2,device_3   state=Connected
     Tap on unlock meeting     device=device_1
     End meeting      device=device_1,device_2,device_3
     Verify meeting state    device_list=device_1,device_2,device_3    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2,device_3

TC8: [Lock Meeting] Verify that user should be able turn ON/OFF the live caption option when meeting is locked
     [Tags]  260604   P2
     [Setup]  Testcase Setup for Meeting User     count=2
     Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
     Verify meeting state   device_list=device_1,device_2    state=Connected
     Check meeting lock state  device_list=device_1
     Tap on lock meeting   device=device_1
     Turn on live captions and validate   device=device_1
     Turn off live captions and validate  device=device_1
     Tap on unlock meeting     device=device_1
     End meeting      device=device_1,device_2
     Verify meeting state    device_list=device_1,device_2    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC9: [Lock Meeting] Verify that user should able to open dial pad option when meeting is locked
     [Tags]  260606   P2
     [Setup]  Testcase Setup for Meeting User     count=2
     Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
     Verify meeting state   device_list=device_1,device_2    state=Connected
     Check meeting lock state  device_list=device_1
     Tap on lock meeting   device=device_1
     Open dial pad from call control bar  device=device_1
     Tap on unlock meeting     device=device_1
     End meeting      device=device_1,device_2
     Verify meeting state    device_list=device_1,device_2    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC10 : [Lock Meeting] Verify that DUT user should able to mute/unmute when meeting is locked
     [Tags]  260603   P2
     [Setup]  Testcase Setup for Meeting User     count=2
     Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
     Verify meeting state   device_list=device_1,device_2    state=Connected
     Check meeting lock state  device_list=device_1
     Tap on lock meeting   device=device_1
     Mutes the phone call    device=device_1
     Verify meeting Mute State    device_list=device_1    state=mute
     Unmutes the phone call  device=device_1
     Verify meeting Mute State    device_list=device_1    state=Unmute
     Disable video call     device=device_1
     Enable video call    device=device_1
     Tap on unlock meeting     device=device_1
     End meeting      device=device_1,device_2
     Verify meeting state    device_list=device_1,device_2    state=Disconnected
     [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC11: [Lock Meeting] Verify that Attendees should not see lock the meeting option
    [Tags]  260595   P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check meeting lock state  device_list=device_2
    Make an attendee   from_device=device_2     to_device=device_1:meeting_user
    Verify you are an attendee now notification    device=device_1
    Verify lock meeting option should not visible for attendee   device=device_1
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC12: [Lock Meeting]Verify that Organizer should always join in locked meeting.
    [Tags]  260599   P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify participants list in meeting    device=device_1
    Check meeting lock state  device_list=device_1
    Tap on lock meeting   device=device_1
    End meeting      device=device_1
    Come back to home screen    device_list=device_1
    Join meeting   device=device_1   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC13: [Lock Meeting] Verify that DUT user can see reactions on screen when meeting is locked
     [Tags]    260605   P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify participants list in meeting    device=device_1
    Check meeting lock state  device_list=device_2
    Tap on lock meeting   device=device_2
    tap on clap button      device=device_1
    verify reaction on screen     device=device_2
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC14: [Lock Meeting] Verify Lock meeting option must be present in menu(...) to Organizer/Co-organizer
     [Tags]  303891  P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify participants list in meeting    device=device_1
    Check meeting lock state  device_list=device_2
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


TC15:[Lock Meeting] Verify Lock meeting option must not be present in menu(...) when DUT is an Attendee
     [Tags]  303892   P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Check meeting lock state  device_list=device_2
    Make an attendee   from_device=device_2     to_device=device_1:meeting_user
    Verify you are an attendee now notification    device=device_1
    Verify lock meeting option should not visible for attendee   device=device_1
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

*** Keywords ***
Meeting setup
    Verify meeting display on home screen   device=device_1
