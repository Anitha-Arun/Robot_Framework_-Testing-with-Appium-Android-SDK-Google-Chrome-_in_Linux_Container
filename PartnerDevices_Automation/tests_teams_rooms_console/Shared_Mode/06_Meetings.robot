*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Force Tags    sm_meetings     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1: [Meetings] Meeting should sync automatically on DUT
    [Tags]      315077   bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User     count=1
    Verify meeting display on home page   console=console_1
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1

TC2: [Meetings]Touch Console user can turn off/on the video while in a meeting
    [Tags]      315047   bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User    count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Turn off video call   console=console_1
    Turn on video call  console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3: [Meetings] Touch Console user can see the list of the participants in the meeting
    [Tags]      315051   bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant  console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC4: [Meetings] Touch Console user can exit meeting by using the hang-up icon
    [Tags]      315063   bvt_sm     sanity_sm
    [Setup]  Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    Come back to home screen page   console_list=console_1
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC5: [Meeting] While the meeting is being joined, a progress screen and list of participants is displayed
    [Tags]      315041      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Wait for Some Time    time=${wait_time}
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

#feature has been modified user not get the recording option
#TC6: [Meetings] Touch Console user gets meeting recording notification when any participants starts recording the session
#    [Tags]      315061   bvt_sm     sanity_sm
#    [Setup]   Testcase Setup for shared User    count=2
#    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
#    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
#    Start recording   device_list=device_2
#    Verify start recording notification display on screen  console=console_1
#    End a meeting     console=console_1       device=device_2
#    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
#    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC7: [Meetings] Touch Console user can Increase/decrease volume while in meeting
    [Tags]      315055      bvt_sm  sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify functionality of volume button    console=console_1   button=UP     state=In_meeting
    Verify functionality of volume button    console=console_1   button=Down   state=In_meeting
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC8: [Meetings] Verify 'Mute' & 'hang up' option while the Touch Console user joins the meeting
    [Tags]      315043      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User    count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant  console=console_1
    Validate call control bar options    console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC9: [Meetings]Touch Console user can mute/ unmute microphone while in a meeting
    [Tags]      315049   sanity_sm  P1
    [Setup]   Testcase Setup for shared User    count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant   console=console_1
    Mute the call      console=console_1
    Verify and check call mute state      console_list=console_1    state=Mute
    Unmute the call    console=console_1
    Verify and check call mute state     console_list=console_1    state=Unmute
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC10: [Meetings] Touch Console user can turn off incoming videos
    [Tags]      315059   sanity_sm  P1
    [Setup]   Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Turn off incoming video call   console=console_1
    Turn on incoming video call   console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC11: [Meetings] Touch Console user can mute the other participants in the meeting
    [Tags]      315069   sanity_sm      P1
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Mute all active participants    console=console_1
    Verify meeting Mute State    device_list=device_2,device_3    state=Mute
    Unmutes the phone call   device=device_2
    Unmutes the phone call   device=device_3
    Verify meeting Mute State       device_list=device_2,device_3   state=Unmute
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC12: [Meetings] User view the other participants (yet to join participants) on the Touch console screen
    [Tags]      315087   P2
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC13: [Meetings] User can see a preview of the video stream
    [Tags]      315045      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify video preview on screen    device=device_2
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC14: [Meetings] Verify Live captions on Touch Console
    [Documentation]  Validated only the option of live captions not the compelete functionality
    [Tags]      315095   bvt_sm     sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Turn on live captions option    console=console_1
    Turn off live captions option   console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC15: [Meetings]Touch Console user raise hand in the meeting
    [Tags]      315091   P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify and select raise hand option   console=console_1
    Verify raise hand notification   device_list=device_2
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC16: [Meetings] Touch Console user disabled raise hand in the meeting
    [Tags]      315093      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify and select raise hand option   console=console_1
    Verify raise hand notification   device_list=device_2
    Verify and select lower hand option   console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

#feature has been modified user not get the recording option
#TC17: [Meetings] Touch console to start recording the meeting
#    [Tags]  251327      bvt_sm
#    [Setup]  Testcase Setup for shared User   count=2
#    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
#    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
#    Select start recording option   console=console_1
#    Verify recording notification display on screen  device=device_2
#    Select stop recording option     console=console_1
#    Verify saved chat history notification display on screen    device_list=device_2
#    End a meeting     console=console_1       device=device_2
#    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
#    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC18: [Meeting] TDC user share the Whiteboard during meeting with DUT
    [Tags]      315168      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and click on white board sharing in call control bar   device=device_2
    Verify whiteboard visibility for all participants   device_list=device_1:meeting_user,device_2
    Verify user should not have stop presenting button     device=console_1
    Stop presenting whiteboard share screen    device=device_2
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC19: [Meeting] Verify user behavior when role transition to presenter from attendee
    [Tags]      322519    bvt_sm   sanity_sm
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification   device=console_1
    verify attendee participant not able to add user in meeting  from_device=console_1      to_device=device_3
    Make an presenter     from_device=device_2     to_device=console_1:meeting_user     device_type=console
    Verify you are an presenter now notification   device=console_1
    verify add user option_is visible for presenter  console=console_1
    Add participant to the conversation using display name   from_device=console_1    to_device=device_3
    Accept incoming call      device=device_3
    Verify for meeting state     console_list=console_1    device_list=device_2,device_3    state=Connected
    Verify and view list of participant     console=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3


TC20: [Meeting] Verify user behaviour when role changed to presenter from attendee
    [Tags]      315443      P1
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification   device=console_1
    Verify user not have manage audio and video option       console=console_1
    Make an presenter   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an presenter now notification   device=console_1
    verify add user option is visible for presenter  console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC21: [Meeting] verify attendee can raise hand in meeting
    [Tags]      322518   P1     sanity_sm
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification   device=console_1
    Verify user not have manage audio and video option       console=console_1
    Verify and select raise hand option     console=console_1
    Verify raise hand notification   device_list=device_2
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC22: [Meeting] Verify attendee cannot add participants in the meeting
    [Tags]      322517   sanity_sm      P1
    [Setup]  Testcase Setup for shared User   count=3
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification   device=console_1
    verify attendee participant not able to add user in meeting  from_device=console_1      to_device=device_3
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC23: [Meeting] Verify "Manage audio and video" option in meeting
    [Tags]      322515    P1    sanity_sm
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting    console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC24: [Meeting] Verify "Manage audio and video" option not available for attendee.
    [Tags]      322516    P1        sanity_sm
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify manage audio and video option in meeting     console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification   device=console_1
    Verify not to have ellipse manage audio and video option        console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC25: [Meeting] Touch console share the Whiteboard during meeting
    [Tags]      315166      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User   count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify whiteboard sharing option under more option        device=console_1
    Verify whiteboard visibility for all participants   device_list=device_1:meeting_user,device_2
    Click on stop whiteboard sharing    console=console_1       device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC26: [Meetings] The menu bar can be dismissed, if the user clicks somewhere outside of the bar area
    [Tags]      315067      P2
    [Setup]  Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Clicking on more option and taping on outside the menu bar    console=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC27:[Meeting] Teams is pre-selected as a default meeting provider
    [Tags]      315101  P2
    [Setup]   Testcase Setup for shared User   count=2
    Start meeting using meet now    from_device=console_1    to_device=device_2
    Accept incoming call      device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Verify and view list of participant     console=console_1
    Validate call control bar options   console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for call state    console_list=console_1    device_list=device_2     state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

Navigate to show meeting names page
    [Arguments]       ${console}
    Navigate to app settings screen    ${console}
    Navigate to meeting and calling options from device settings page       ${console}  option=meeting
    Verify show meeting names toggle btn status    ${console}
    Disable show meeting names toggle btn   ${console}
    Click back btn   ${console}
    device setting back btn     ${console}
    device setting back btn     ${console}
    Click on back layout btn   ${console}
    Come back to home screen page   console_list=${console}

Navigate to app settings screen
    [Arguments]   ${console}
    Tap on more option  ${console}
    Tap on settings page   ${console}

Enable show meeting names toggle btn
    [Arguments]    ${console}
    Navigate to app settings screen    ${console}
    Navigate to meeting and calling options from device settings page       ${console}  option=meeting
    Enable show meeting names toggle button    ${console}
    Click back btn   ${console}
    device setting back btn     ${console}
    device setting back btn     ${console}
    Click on back layout btn   ${console}
    Come back to home screen page   console_list=${console}

verify attendee participant not able to add user in meeting
    [Arguments]    ${from_device}   ${to_device}
    Verify not able to add user in meeting      ${from_device}   ${to_device}
    Verify notification not able to add new user        ${from_device}

Verify not to have ellipse manage audio and video option
    [Arguments]    ${console}
    Verify user not have manage audio and video option     ${console}

Verify and click on white board sharing in call control bar
    [Arguments]    ${device}
    Verify whiteboard sharing option under more option   ${device}

Clicking on more option and taping on outside the menu bar
    [Arguments]    ${console}
    verify menu bar more options    ${console}
    tapping outside more option     ${console}
