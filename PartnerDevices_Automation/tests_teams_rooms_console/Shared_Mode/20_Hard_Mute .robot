*** Settings ***
Force Tags    sm_hard_mute      20  sm
Library     DateTime
Library     OperatingSystem
Resource  ../resources/keywords/common.robot

*** Variables ***


*** Test Cases ***
TC1:[Hard Mute] Verify "Disable mic for attendees", "Disable camera for attendees" option should be available in "manage audio or video."
    [Tags]      322521      bvt_sm  sanity_sm
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting       console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2 :[Hard Mute] Verify Organizer/presenter-can turn on hard mute, it disables camera for attendees with toggle and update UI
     [Tags]      322523   P1    sanity_sm
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting     console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification     device=console_1
    Verify user not have manage audio and video option      console=console_1
    Disable and enable camera for attendees     from_device=device_2    to_device=console_1     state=on
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3:[Hard Mute] Verify "your mic has been disabled" message display on main stage to participant/attendee
    [Tags]      322528      P1      sanity_sm
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting       console=console_1
    Make an attendee   from_device=console_1     to_device=device_3    device_type=console
    Verify you are an attendee now notification     device=device_3
    Disable and enable mic for attendees        from_device=console_1    to_device=device_3     state=on
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC4 :[Hard Mute] Presenter/organizer can provide individual restrictions to users. Allow to Unmute
    [Tags]      322532   P1    sanity_sm
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification     device=console_1
    Disable mic options for attendees    from_device=device_2       to_device=console_1:meeting_user
    Allow mic options for attendees    from_device=device_2       to_device=console_1:meeting_user
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC5 :[Hard Mute] Presenter/organizer can provide individual restrictions to users. Allow to share video
    [Tags]      322533   P1    sanity_sm
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification     device=console_1
    Disable camera options for attendees    from_device=device_2       to_device=console_1:meeting_user
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC6 :[Hard Mute] Verify Organizer/presenter-can turn on hard mute, it disables mic for attendees with toggle
     [Tags]      322522     P2
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting     console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification     device=console_1
    Verify user not have manage audio and video option      console=console_1
    Disable and enable mic for attendees    from_device=device_2       to_device=console_1    state=on
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC7 :[Hard Mute] Verify "your camera has been disabled" message display on main stage to participant/attendee
     [Tags]      322527     P2
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting     console=console_1
    Make an attendee   from_device=console_1     to_device=device_3    device_type=console
    Verify you are an attendee now notification     device=device_3
    Verify not to have manage audio and video option      device=device_3
    Disable and enable camera for attendees   from_device=console_1      to_device=device_3      state=on
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC8 :[Hard Mute] Verify One attendee can view hand raised by another attendee
    [Tags]      322529   P2
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting     console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification     device=console_1
    Make an attendee    from_device=device_2       to_device=device_3
    Verify you are an attendee now notification     device=device_3
    Raise hand  device=device_3
    Verify raised hand notification on another user     device=device_3     from_device=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC9 :[Hard Mute] Verify that attendee get a proper message when hand is lowered by organizer.
    [Tags]      322530    P2
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting     console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification     device=console_1
    Make an attendee    from_device=device_2       to_device=device_3
    Verify you are an attendee now notification     device=device_3
    Raise hand   device=console_1
    Lower the raised hand from another user      from_device=device_2       to_device=console_1:meeting_user        device_type=console
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC10 :[Hard Mute] Verify the participants mic and camera status in the meeting
    [Tags]      322534    P2
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2    state=Connected
    Verify and view list of participant    console=console_1
    Verify mic camera in participants list     device=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC11:[Hard Mute]Verify Organizer/presenter-can manage request to speak in a hard-muted meeting to allow selected attendees to speak, after attendees raise hands and ask for permission to speak.
    [Tags]      322524     bvt_sm   sanity_sm
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3    state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting     console=console_1
    Make an attendee   from_device=console_1     to_device=device_3    device_type=console
    Verify you are an attendee now notification     device=device_3
    Disable and enable mic for attendees        from_device=console_1    to_device=device_3     state=on
    Raise hand  device=device_3
    Verify raised hand notification on another user     device=device_3     from_device=console_1
    Disable and enable mic for attendees        from_device=console_1    to_device=device_3     state=off
    Make an presenter     from_device=console_1    to_device=device_3     device_type=console
    Verify you are an presenter now notification   device=device_3
    Unmutes the phone call  device=device_3
    Verify meeting Mute State    device_list=device_3    state=Unmute
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC12:[Hard Mute] Presenter/organizer can provide individual restrictions to users
    [Tags]      322531  P2
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3    state=Connected
    Verify and view list of participant    console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification     device=console_1
    Make an attendee    from_device=device_2       to_device=device_3
    Verify you are an attendee now notification     device=device_3
    Tap on attendee participant and check individual options    from_device=device_2       to_device=console_1:meeting_user
    Close the add participant and attendee options page     device=device_2
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3


*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

Disable mic options for attendees
     [Arguments]    ${from_device}    ${to_device}
    Verify options visible after making an attendee     ${from_device}    ${to_device}     device_type=console
    Disable and allow mic options for attendees     ${from_device}    ${to_device}      mic=disable

Allow mic options for attendees
    [Arguments]    ${from_device}    ${to_device}
    Verify options visible after making an attendee     ${from_device}    ${to_device}     device_type=console
    Disable and allow mic options for attendees     ${from_device}    ${to_device}      mic=allow

Disable camera options for attendees
    [Arguments]    ${from_device}    ${to_device}
    Verify options visible after making an attendee     ${from_device}    ${to_device}     device_type=console
    Disable and allow camera options for attendees     ${from_device}    ${to_device}      camera=disable

Close the add participant and attendee options page
    [Arguments]    ${device}
    Dismiss the popup screen        ${device}
    Close participants screen   ${device}

Tap on attendee participant and check individual options
    [Arguments]    ${from_device}    ${to_device}
    Verify options visible after making an attendee     ${from_device}    ${to_device}     device_type=console
