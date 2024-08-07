*** Settings ***
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot
*** Variables ***

*** Test Cases ***
TC1: [Hard Mute] Verify "Disable mic for attendees", "Disable camera for attendees" option should be available in "manage audio or video."
    [Tags]      303247      bvt     bvt_sm  sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify participants list in meeting    device=device_1
    Verify manage audio and video options in participants       device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2

TC2 :[Hard Mute] Verify "your camera has been disabled" message display on main stage to attendee
    [Tags]      303253   P2
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_1       to_device=device_3
    Verify you are an attendee now notification     device=device_3
    Disable and enable camera for attendees   from_device=device_1      to_device=device_3      state=on
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC3 :[Add participant] [Group call] Verify 'Add participant' option on roster when role set as attendee
     [Tags]   303989     P2
    [Setup]  Testcase Setup for Meeting User   count=3
    Make Video call using display name  from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call    device=device_1
    Close participants screen   device=device_2
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Add participant to conversation using display name   from_device=device_2      to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_2
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user
    Verify you are an attendee now notification     device=device_1
    Add participants button not present     device=device_1
    Close participants screen   device=device_1
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC4 :[Hard Mute] Verify One attendee can view hand raised by another attendee
    [Tags]      303255   P2
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user
    Verify you are an attendee now notification     device=device_1
    Make an attendee    from_device=device_2       to_device=device_3
    Verify you are an attendee now notification     device=device_3
    Raise hand  device=device_3
    Verify raised hand notification on another user     device=device_3     from_device=device_1
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC5 :[Hard Mute] Verify that attendee get a proper message when hand is lowered by organizer.
    [Tags]      303256    p2
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user
    Verify you are an attendee now notification     device=device_1
    Make an attendee    from_device=device_2       to_device=device_3
    Verify you are an attendee now notification     device=device_3
    raise hand   device=device_1
    lower the raised hand from another user      from_device=device_2       to_device=device_1:meeting_user
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC6 :[Hard Mute] Presenter/organizer can provide individual restrictions to users
    [Tags]      303257    P2
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user,device_3
    Verify you are an attendee now notification     device=device_1,device_3
    Check user options after making an attendee    from_device=device_2       to_device=device_1:meeting_user
    Close participants screen   device=device_2
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC7 :[Hard Mute] Verify the participants mic and camera status in the meeting
     [Tags]      303260    P2
    [Setup]  Testcase Setup for Meeting User    count=2
    Join meeting   device=device_1,device_2   meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify participants list in meeting  device=device_1
    verify mic camera in participants list     device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2

TC8 :[Add participant] Verify whether user able to nudge other users into Meeting when presenter [Meeting]
    [Tags]      313241   P2
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    verify participants list in meeting  device=device_1
    Add participant to conversation using display name  from_device=device_1       to_device=device_3
    Accept incoming call      device=device_3
    Close participants screen   device=device_1
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC9 :[Hard Mute] Presenter/organizer can provide individual restrictions to users >>Disable camera/ Allow camera
     [Tags]      303259   P1
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user,device_3
    Verify you are an attendee now notification     device=device_1,device_3
    Disable camera options for attendees   from_device=device_2      to_device=device_1:meeting_user
    Allow camera options for attendees   from_device=device_2      to_device=device_1:meeting_user
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3


TC10 :[Hard Mute] Presenter/organizer can provide individual restrictions to users >> Disable Mic/ Allow mic
     [Tags]      303258   P1
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user,device_3
    Verify you are an attendee now notification     device=device_1,device_3
    Disable mic options for attendees   from_device=device_2      to_device=device_1:meeting_user
    Allow mic options for attendees   from_device=device_2      to_device=device_1:meeting_user
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC11: [Add participant]Verify user behavior when role changed to attendee [Meeting]
    [Tags]      303990    P2
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user
    Verify you are an attendee now notification     device=device_1
    add participants Button not present     device=device_1
    Close participants screen   device=device_1
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC12: [Hard Mute] Verify Organizer/presenter disables mic for attendees
     [Tags]     303248    P2
    [Setup]  Testcase Setup for Meeting User    count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user
    Verify you are an attendee now notification     device=device_1
    Disable camera and mic for attendees   from_device=device_2   to_device=device_1    mic=off   camera=on
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2

TC13: [Hard Mute] Verify Organizer/presenter-can disables camera for attendees
     [Tags]    303249    P1     sanity_sm
    [Setup]  Testcase Setup for Meeting User    count=2
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2   state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user
    Verify you are an attendee now notification     device=device_1
    Disable camera and mic for attendees   from_device=device_2   to_device=device_1    mic=on   camera=off
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2

TC14:[Hard Mute] Verify Organizer/presenter-can manage request to speak for attendees, after attendees raise hands and ask for permission to speak.
    [Tags]   303250     bvt_sm   sanity_sm
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_1       to_device=device_3
    Verify you are an attendee now notification     device=device_3
    Disable and enable mic for attendees   from_device=device_1      to_device=device_3      state=on
    raise hand      device=device_3
    Verify raised hand notification on another user     device=device_3     from_device=device_1
    Allow mic options for attendees   from_device=device_1      to_device=device_3
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC15: [Hard Mute] Verify that prejoin screen is correct for attendee if the video is disabled
     [Tags]    316807    P2
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_1       to_device=device_2
    Verify you are an attendee now notification     device=device_2
    Disable camera and mic for attendees   from_device=device_1   to_device=device_2    mic=on   camera=off
    disconnect call     device=device_2
    Verify meeting state    device_list=device_2   state=Disconnected
    Join meeting   device=device_2    meeting=cnf_device_meeting
    disable camera for attendees avatar     device=device_2
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3

TC16: [Meeting] Verify that new icons on roster do not interact badly with existing icons
     [Tags]  316813    P2
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user,device_3
    Verify you are an attendee now notification     device=device_1,device_3
    Disable and enable mic for attendees   from_device=device_2      to_device=device_1      state=on
    raise hand      device=device_2
    Verify raised hand notification on another user    device=device_2      from_device=device_1
    make a spotlight   from_device=device_2   to_device=device_3
    Close participants screen   device=device_2
    verify spotlight icon user is attendee    device=device_3
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3


TC17:[Hard Mute] Verify "your mic has been disabled" message display on main stage to attendee
    [Tags]       303254    P1   sanity_sm
    [Setup]  Testcase Setup for Meeting User    count=3
    Join meeting   device=device_1,device_2,device_3    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2,device_3    state=Connected
    Make an attendee    from_device=device_2       to_device=device_1:meeting_user,device_3
    Verify you are an attendee now notification     device=device_1,device_3
    Disable camera and mic for attendees   from_device=device_2   to_device=device_1    mic=off   camera=on
    End meeting     device=device_1,device_2,device_3
    Verify meeting state    device_list=device_1,device_2,device_3   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND    Come back to home screen    device_list=device_1,device_2,device_3


*** Keywords ***
verify options visibel after disabeling camera/ mic
        [Arguments]    ${from_device}       ${to_device}
        verify_options_visible_after_making_an_attendee     ${from_device}       ${to_device}

Disable camera options for attendees
    [Arguments]    ${from_device}    ${to_device}
    Verify options visible after making an attendee     ${from_device}    ${to_device}
    Disable and allow camera options for attendees     ${from_device}    ${to_device}      camera=disable

Allow camera options for attendees
    [Arguments]    ${from_device}    ${to_device}
    Verify options visible after making an attendee     ${from_device}    ${to_device}
    Disable and allow camera options for attendees     ${from_device}    ${to_device}      camera=allow

Disable mic options for attendees
    [Arguments]    ${from_device}    ${to_device}
    Verify options visible after making an attendee     ${from_device}    ${to_device}
    Disable and allow mic options for attendees     ${from_device}    ${to_device}      mic=disable

Allow mic options for attendees
    [Arguments]    ${from_device}    ${to_device}
    Verify options visible after making an attendee     ${from_device}    ${to_device}
    Disable and allow mic options for attendees     ${from_device}    ${to_device}      mic=allow

