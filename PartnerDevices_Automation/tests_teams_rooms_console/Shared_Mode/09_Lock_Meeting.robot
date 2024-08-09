*** Settings ***
Documentation   Validating the functionality of Lock meeting Feature on console device.
Force Tags    sm_lock_meeting     sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1:[Lock Meeting] Verify that lock the meeting option should not be available at DUT user's end (DUT user is presenter)
    [Tags]      315405  P1
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify lock meeting state    console_list=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC2: [Lock Meeting] Verify lock icon must be displayed along with "Lock the meeting"
    [Tags]      315407      P1
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify lock meeting state    console_list=console_1
    Tap on lock meeting option  console=console_1
    Tap on unlock meeting option   console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC3: [Lock Meeting] Verify That user can unlock the locked meeting
    [Tags]      315409      bvt_sm      sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Verify lock meeting state    console_list=console_1
    Tap on lock meeting option  console=console_1
    Tap on unlock meeting option   console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC4: [Lock Meeting] Verify that DUT user should not able to join the meeting when the meeting is locked by TDC user
     [Tags]     315415   sanity_sm      P1
     [Setup]  Testcase Setup for shared User      count=3
     Join meeting       device=device_2,device_3     meeting=console_lock_meeting
     Verify meeting state   device_list=device_2,device_3    state=Connected
     Tap on lock meeting   device=device_2
     Verify that user cannot join the locked meeting     console=console_1      meeting=console_lock_meeting
     End meeting      device=device_2,device_3
     Verify meeting state    device_list=device_2,device_3    state=Disconnected
     [Teardown]   Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC5: [Lock Meeting] Verify that DUT user cannot join the locked meeting
     [Tags]     315423      bvt_sm      sanity_sm
     [Setup]  Testcase Setup for shared User     count=3
     Join meeting   device=device_2,device_3   meeting=console_lock_meeting
     Wait for Some Time    time=${wait_time}
     Verify meeting state   device_list=device_2,device_3    state=Connected
     Tap on lock meeting   device=device_2
     Verify that user cannot join the locked meeting     console=console_1      meeting=console_lock_meeting
     Come back to home screen page   console_list=console_1
     Tap on unlock meeting     device=device_2
     Join a meeting   console=console_1        meeting=console_lock_meeting
     Wait for Some Time    time=${wait_time}
     Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
     End a meeting     console=console_1       device=device_2,device_3
     Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
     [Teardown]   Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC6: [Lock Meeting] Verify that user should be able turn ON/OFF the live caption option when meeting is locked
     [Tags]     315429   P2
     [Setup]  Testcase Setup for shared User     count=2
     Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
     Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
     Verify lock meeting state    console_list=console_1
     Tap on lock meeting option  console=console_1
     Turn on live captions option    console=console_1
     Turn off live captions option   console=console_1
     End a meeting     console=console_1       device=device_2
     Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
     [Teardown]   Run Keywords    Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC7: [Lock Meeting]Verify that DUT user can add other participants in a locked meeting
     [Tags]     315417      bvt_sm      sanity_sm
     [Setup]  Testcase Setup for shared User     count=3
     Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
     Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
     Verify lock meeting state    console_list=console_1
     Tap on lock meeting option  console=console_1
     Add participant to the conversation using display name   from_device=console_1    to_device=device_3
     Accept incoming call      device=device_3
     Wait for Some Time    time=${wait_time}
     Verify for call state     console_list=console_1    device_list=device_2,device_3    state=Connected
     Verify and view list of participant     console=console_1
     End a meeting     console=console_1       device=device_2,device_3
     Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
     [Teardown]   Run Keywords    Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC8: [Lock Meeting]Verify that Organizer should always join in locked meeting.
     [Tags]     315419   P2
     [Setup]  Testcase Setup for shared User     count=2
     Join a meeting    console=console_1     device=device_2      meeting=rooms_console_meeting
     Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
     Verify lock meeting state    console_list=console_1
     Tap on lock meeting option  console=console_1
     End the meeting  console=console_1
     Join a meeting   console=console_1     meeting=rooms_console_meeting
     Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
     End a meeting     console=console_1       device=device_2
     Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
     [Teardown]   Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC9: [Lock Meeting]Verify that Organizer(DUT) should have lock meeting option at meeting screen
     [Tags]  315421   P1
     [Setup]  Testcase Setup for shared User     count=2
     Join a meeting   console=console_1     device=device_2    meeting=rooms_console_meeting
     Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
     Verify lock meeting state    console_list=console_1
     End a meeting     console=console_1       device=device_2
     Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
     [Teardown]   Run Keywords   Capture Failure   AND    Come back to home screen page    console_list=console_1   device_list=device_2

TC10: [Lock Meeting] Verify that Attendees should not see lock the meeting option
    [Tags]      315411  P1      sanity_sm
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify and view list of participant    console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification   device=console_1
    Verify user should not have lock meeting option     console=console_1
    Make an presenter   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an presenter now notification   device=console_1
    Verify user should not have lock meeting option     console=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2

TC11: [Lock Meeting] Verify Lock meeting option must not be present in menu(...) when Touch console is an Attendee
    [Tags]      322779  P2
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Make an attendee   from_device=device_2     to_device=console_1:meeting_user    device_type=console
    Verify you are an attendee now notification   device=console_1
    Verify user should not have lock meeting option     console=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC12: [Lock Meeting] Verify Lock meeting option must be present in menu(...) to Organizer
    [Tags]      322778  P2
    [Setup]   Testcase Setup for shared User     count=3
    Join a meeting   console=console_1     device=device_2,device_3    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify and view list of participant    console=console_1
    Verify lock meeting state    console_list=console_1
    End a meeting     console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]   Run Keywords    Capture Failure  AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC13 :[Lock Meeting] Verify that DUT user can see reactions on screen when meeting is locked
    [Tags]      315431  P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2,device_3    meeting=console_lock_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Tap on lock meeting   device=device_2
    Click like button     device=device_3
    Verify reaction button on screen after tap on it   device=device_1
    End a meeting   console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC14 :[Lock Meeting] Verify that user should able to open dial pad option when meeting is locked
    [Tags]      315433  P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2,device_3    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify lock meeting state    console_list=console_1
    Tap on lock meeting option   console=console_1
    Open dial pad from call control bar  device=console_1
    Tap on unlock meeting option   console=console_1
    End a meeting   console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

TC15 :[Lock Meeting] Verify that DUT user should able to mute/unmute when meeting is locked
    [Tags]      315427  P2
    [Setup]   Testcase Setup for shared User     count=2
    Join a meeting   console=console_1     device=device_2,device_3    meeting=rooms_console_meeting
    Verify for meeting state     console_list=console_1      device_list=device_2,device_3     state=Connected
    Verify lock meeting state    console_list=console_1
    Tap on lock meeting option   console=console_1
    Mute the call      console=console_1
    Verify and check call mute state      console_list=console_1    state=Mute
    Unmute the call    console=console_1
    Verify and check call mute state     console_list=console_1    state=Unmute
    Disable video call     device=console_1
    Enable video call    device=console_1
    Tap on unlock meeting option   console=console_1
    End a meeting   console=console_1       device=device_2,device_3
    Verify for meeting state    console_list=console_1      device_list=device_2,device_3      state=Disconnected
    [Teardown]  Run Keywords   Capture Failure   AND    Come back to home screen page   console_list=console_1   device_list=device_2,device_3

*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}
