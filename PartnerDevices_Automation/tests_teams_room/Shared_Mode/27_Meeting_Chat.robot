*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  5

*** Test Cases ***
TC1:[Chat] Verify the chat toggle button when user joined the meeting.
    [Tags]     379966       bvt_sm      sanity_sm       P0
    [Setup]   Testcase Setup for Meeting User    count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2    meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify that chat toggle button should be disabled by default    device=device_1
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC2:[Chat]Verify the chat option in P2P incoming call when show meeting chat is enabled in admin settings.
    [Tags]      379970       bvt_sm     sanity_sm
    [Setup]  Testcase Setup for Meeting User     count=2
    Enable the show meeting chat option     device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Verify that chat toggle button should be disabled by default    device=device_1
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC3:[Chat]Verify the chat option when DUT user initiates meet now with TDC user & Show meeting chat should be enabled.
    [Tags]   379976       bvt_sm      sanity_sm
    [Setup]   Testcase Setup for Meeting User     count=2
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify that chat toggle button should be disabled by default    device=device_1
    Enable and disable the chat toggle in meeting       device=device_1      state=on
    verify the chat options in meeting       device=device_1
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC4:[Chat]Verify the chat option in P2P incoming call when show meeting chat is disabled in admin settings.
    [Tags]   379972       P1         sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Disable the show meeting chat option    device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    verify that chat toggle button is not present    device=device_1
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure    AND    Come back to home screen    device_list=device_1,device_2  AND     Enable the show meeting chat option     device=device_1

TC5:[Chat]Verify the chat option when DUT user initiates meet now with TDC user & Show meeting chat should be disabled.
    [Tags]      379977      P1         sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Disable the show meeting chat option    device=device_1
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    verify that chat toggle button is not present    device=device_1
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure    AND    Come back to home screen    device_list=device_1,device_2      AND   Enable the show meeting chat option     device=device_1

TC6:[Chat]Verify the chat option in Together mode when DUT user disables "show meeting chat" option from Admin settings.
    [Tags]      379984      P1         sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Disable the show meeting chat option    device=device_1
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Change meeting mode     device=device_1     mode=together
    Wait for Some Time    time=${wait_time}
    Verify together mode participant list  from_device=device_1    connected_device_list=device_2
    verify that chat toggle button is not present    device=device_1
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure    AND    Come back to home screen    device_list=device_1,device_2  AND   Enable the show meeting chat option     device=device_1

TC7:[Chat] Verify the behavior of DUT, once chat toggle button is enabled in the meeting.
    [Tags]      379967      P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Enable the show meeting chat option     device=device_1
    Join meeting   device=device_1,device_2    meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Enable and disable the chat toggle in meeting   device=device_1   state=on
    Verify the chat options in meeting      device=device_1
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC8:[Chat]Verify "Show meeting chat" option under the admin settings.
    [Tags]      379968      P2
    [Setup]    Testcase Setup for Meeting User   count=1
    Navigate to app settings page    device=device_1
    navigate to meetings option in device settings page      device=device_1
    Verify chat toggle in admin setting     device=device_1
    come back from admin settings page  device_list=device_1
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1

TC9:[Chat]Verify the chat option in P2P incoming call when user enables chat option.
    [Tags]     379971       P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Verify that chat toggle button should be disabled by default    device=device_1
    Enable and disable the chat toggle in meeting   device=device_1   state=on
    Verify the chat options in meeting      device=device_1
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC10:[Chat]Verify the chat option in P2P outgoing call when show meeting chat is enabled in admin settings.
    [Tags]     379973       P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_1     to_device=device_2
    Accept incoming call  device=device_2
    Verify Call State    device_list=device_1,device_2    state=Connected
    Verify that chat toggle button should be disabled by default    device=device_1
    Disconnect call     device=device_1
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC11:[Chat]Verify the chat option in P2P outgoing call when user enables chat option.
    [Tags]    379974      P2
    [Setup]  Testcase Setup for Meeting User     count=2
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    Verify that chat toggle button should be disabled by default    device=device_1
    Enable and disable the chat toggle in meeting   device=device_1   state=on
    Verify the chat options in meeting      device=device_1
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC12:[Chat]Verify the chat option in P2P outgoing call when show meeting chat is disabled in admin settings.
    [Tags]    379975     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Disable the show meeting chat option    device=device_1
    Make outgoing call with phonenumber    from_device=device_2     to_device=device_1:meeting_user
    Accept incoming call  device=device_1
    Verify Call State    device_list=device_1,device_2    state=Connected
    verify that chat toggle button is not present    device=device_1
    Disconnect call     device=device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure    AND  Come back to home screen    device_list=device_1,device_2    AND     Enable the show meeting chat option     device=device_1

TC13:[Chat]Verify the chat option when DUT user enables chat option in Gallery mode.
    [Tags]     379978   P2
    [Setup]   Testcase Setup for Meeting User    count=2
    Verify meeting display on home screen     device=device_1
    Join meeting   device=device_1,device_2     meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    change meeting mode     device=device_1     mode=gallery
    verify together mode participant list  from_device=device_1    connected_device_list=device_2
    Enable and disable the chat toggle in meeting       device=device_1      state=on
    verify the chat options in meeting       device=device_1
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2

TC14:[Chat]Verify the chat option in Gallery mode when DUT user disables "show meeting chat" option from Admin settings.
    [Tags]       379979      P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Disable the show meeting chat option    device=device_1
    Join meeting   device=device_1,device_2     meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify that chat toggle button is not present   device=device_1
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure    AND  Come back to home screen    device_list=device_1,device_2    AND      Enable the show meeting chat option     device=device_1

TC15:[Chat]Verify the chat option in Large Gallery mode when DUT user disables "show meeting chat" option from Admin settings.
    [Tags]      379982     P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Disable the show meeting chat option    device=device_1
    Join meeting   device=device_1,device_2     meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Change meeting mode     device=device_1     mode=large_gallery
    Wait for Some Time    time=${wait_time}
    Verify that chat toggle button is not present   device=device_1
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure    AND  Come back to home screen    device_list=device_1,device_2    AND  Enable the show meeting chat option     device=device_1

TC16:[Chat]Verify the chat option when DUT user enables chat option in Together mode.
    [Tags]      379983    P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Join meeting   device=device_1,device_2     meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Change meeting mode     device=device_1     mode=together
    Wait for Some Time    time=${wait_time}
    Enable and disable the chat toggle in meeting       device=device_1      state=on
    Verify the chat options in meeting       device=device_1
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure    AND  Come back to home screen    device_list=device_1,device_2

# This feature is not supported in the new apk(2024031401). Reference: Feature Test Request 419702: [MTRA][W parity H1] Stage Layout switcher
#TC17:[Chat]Verify the chat option when DUT user enables chat option in Front Row mode.
#    [Tags]      379985      P2
#    [Setup]    Testcase Setup for Meeting User   count=2
#    Join meeting   device=device_1,device_2     meeting=lock_meeting
#    Verify meeting state   device_list=device_1,device_2    state=Connected
#    Verify switch orientation toggle hidden after taping on frontrow        device=device_1
#    Disconnect call     device=device_1,device_2
#    Verify Call State    device_list=device_1,device_2    state=Disconnected
#    [Teardown]  Run Keywords    Capture on Failure    AND  Come back to home screen    device_list=device_1,device_2

TC18:[Chat]Verify the chat option in Front Row mode when DUT user disables "show meeting chat" option from Admin settings.
    [Tags]     379986       P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Disable the show meeting chat option    device=device_1
    Join meeting   device=device_1,device_2     meeting=lock_meeting
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Change meeting mode     device=device_1     mode=front_row
    Wait for Some Time    time=${wait_time}
    Verify front row mode   device=device_1
    verify that chat toggle button is not present   device=device_1
    Disconnect call     device=device_1,device_2
    Verify Call State    device_list=device_1,device_2    state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure    AND  Come back to home screen    device_list=device_1,device_2        AND  Enable the show meeting chat option     device=device_1

TC19:[Chat]Verify the chat option when TDC user initiates meet now with DUT user & Show meeting chat should be enabled.
    [Tags]     380004       P2
    [Setup]    Testcase Setup for Meeting User   count=2
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Verify that chat toggle button should be disabled by default    device=device_1
    Enable and disable the chat toggle in meeting       device=device_1      state=on
    verify the chat options in meeting       device=device_1
    Wait for Some Time    time=${wait_time}
    End meeting   device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2   state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure    AND  Come back to home screen    device_list=device_1,device_2

TC20:[Chat] Start meet and check the chat window behavior in different layout.
    [Tags]       381894      P2
    [Setup]    Testcase Setup for Meeting User      count=2
    Initiates conference meeting using Meet now option     from_device=device_1     to_device=device_2
    Accept incoming call    device=device_2
    Close participants screen   device=device_1
    Verify meeting state   device_list=device_1,device_2    state=Connected
    Enable and disable the chat toggle in meeting       device=device_1      state=on
    change meeting mode     device=device_1    mode=front_row
    verify front row mode      device=device_1
    verify the chat options in meeting       device=device_1
    change meeting mode     device=device_1    mode=gallery
    verify the chat options in meeting       device=device_1
    change meeting mode     device=device_1    mode=large_gallery
    verify the chat options in meeting       device=device_1
    End meeting      device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2        state=Disconnected
    [Teardown]  Run Keywords   Capture on Failure   AND    Come back to home screen    device_list=device_1,device_2


*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

verify together mode participant list
    [Arguments]       ${from_device}   ${connected_device_list}
    verify front row participant   ${from_device}   ${connected_device_list}

verify Front Row chat toggle is Disables in front row
    [Arguments]     ${device}
    verify that chat toggle button is not present    ${device}

Enable the show meeting chat option
    [Arguments]    ${device}
    Navigate to app settings page    ${device}
    navigate to meetings option in device settings page      ${device}
    Enable and disable the chat toggle in admin setting     ${device}   state=on
    come back from admin settings page  device_list=${device}

Disable the show meeting chat option
    [Arguments]       ${device}
    Navigate to app settings page    ${device}
    navigate to meetings option in device settings page      ${device}
    Enable and disable the chat toggle in admin setting     ${device}   state=off
    come back from admin settings page  device_list=${device}
