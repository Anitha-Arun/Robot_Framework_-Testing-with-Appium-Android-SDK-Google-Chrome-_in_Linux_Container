*** Settings ***
Documentation   Meeting created as prerequisite before test execution
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot


*** Test Cases ***
TC1:[Stage Layout Switcher] Verify the layout switcher UI is shown.
     [Tags]    444527    P0
     [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2      meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    verify layout options   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2

TC2:[Stage Layout Switcher] Verify that Gallery Layout with chat.
    [Tags]    444530   P0
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2      meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    verify the gallery layout selected default and with chat    device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2

TC3:[Stage Layout Switcher] Verify the Large Gallery Layout switch.
    [Tags]    444533     P1     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    verify layout switcher ui       device=device_1
    Dismiss the popup screen        device=device_1
    Change meeting mode    device=device_1      mode=large_gallery
    verify large gallery mode after switching       device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2


TC4:[Stage Layout Switcher] Verify the Gallery Layout switch.
    [Tags]    444528     P1     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    verify the gallery layout selected default and with chat    device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2

TC5: [Stage Layout Switcher] Verify the Together Mode layout.
    [Tags]    444535     P1     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    verify layout switcher ui       device=device_1
    Dismiss the popup screen        device=device_1
    Change meeting mode    device=device_1      mode=together
    verify together mode after switching       device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2

TC6:[Stage Layout Switcher] Verify the Front Row layout.
    [Tags]    444537     P1     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2      meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    verify layout switcher ui       device=device_1
    Dismiss the popup screen        device=device_1
    change meeting mode     device=device_1    mode=front_row
    Verify front row mode   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2

TC7:[Stage Layout Switcher] Verify the Large Gallery Layout with chat.
	[Tags]    444534     P1     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Enable and Disable the show meeting chat option    device=device_1    state=on
    Join Meeting    device=device_1,device_2      meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    verify layout switcher ui       device=device_1
    Dismiss the popup screen        device=device_1
    verify Content Gallery should be selected   device=device_1     mode=gallery
    Change meeting mode     device=device_1     mode=large_gallery
    verify large gallery mode after switching       device=device_1
    Enable and disable the chat toggle in meeting       device=device_1      state=on
    verify the chat options in meeting       device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2

TC8:[Stage Layout Switcher] Verify the Together Mode layout with chat panel.
	[Tags]    444536     P2     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Enable and Disable the show meeting chat option    device=device_1    state=on
    Join Meeting    device=device_1,device_2      meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    verify layout switcher ui       device=device_1
    Dismiss the popup screen        device=device_1
    verify Content Gallery should be selected   device=device_1     mode=gallery
    Change meeting mode     device=device_1     mode=together
    verify together mode after switching       device=device_1
    Enable and disable the chat toggle in meeting       device=device_1      state=on
    verify the chat options in meeting       device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2

TC9:[Stage Layout Switcher] Verify the Gallery layout when show meeting chat is disabled under the teams admin settings.
	[Tags]    444541     P2     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Enable and Disable the show meeting chat option    device=device_1    state=off
    Join Meeting    device=device_1,device_2      meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    Verify layout options       device=device_1
    verify Content Gallery should be selected   device=device_1     mode=gallery
    verify that chat toggle button is not present   device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2    AND     Enable and Disable the show meeting chat option     device=device_1    state=on

TC10:[Stage Layout Switcher]Verify that Large Gallery respect Chat settings
	[Tags]    444582     P2     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Enable and Disable the show meeting chat option    device=device_1    state=off
    Join Meeting    device=device_1,device_2      meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    Verify layout options       device=device_1
    verify Content Gallery should be selected   device=device_1     mode=gallery
    Change meeting mode     device=device_1     mode=large_gallery
    verify large gallery mode after switching       device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2    AND     Enable and Disable the show meeting chat option     device=device_1    state=on

TC11:[Stage Layout Switcher] Verify that Together Mode Layout with Chat panel.
	[Tags]    444584     P2     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Enable and Disable the show meeting chat option    device=device_1    state=off
    Join Meeting    device=device_1,device_2     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    Verify layout options       device=device_1
    verify Content Gallery should be selected   device=device_1     mode=gallery
    Change meeting mode     device=device_1     mode=together
    verify together mode after switching       device=device_1
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2    AND     Enable and Disable the show meeting chat option     device=device_1    state=on

TC12:[Stage Layout Switcher] Verify that Front Row layout when show meeting Chat is disabled under the teams admin settings.
	[Tags]    444585     P2     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Enable and Disable the show meeting chat option    device=device_1    state=off
    Join Meeting    device=device_1,device_2     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    Verify layout options       device=device_1
    verify Content Gallery should be selected   device=device_1     mode=gallery
    Change meeting mode     device=device_1     mode=front_row
    verify front row mode     device=device_1   chat_toggle=off
    select the drop down under show on left and show on right     device=device_1     show_on_left=hide    show_on_right=raised_hands
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2    AND     Enable and Disable the show meeting chat option     device=device_1    state=on

TC13:[Stage Layout Switcher] Verify default Front Row settings
	[Tags]    444588     P1     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Enable and Disable the show meeting chat option    device=device_1    state=on
    Join Meeting    device=device_1,device_2      meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    verify layout switcher ui       device=device_1
    Dismiss the popup screen        device=device_1
    verify Content Gallery should be selected   device=device_1     mode=gallery
    Change meeting mode     device=device_1     mode=front_row
    Verify front row mode   device=device_1
    select the drop down under show on left and show on right     device=device_1     show_on_left=hide     show_on_right=chat
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2

TC14:[Stage Layout Switcher] Verify default Front Row layout when show meeting chat is disabled under the teams admin settings.
	[Tags]    444590     P1     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Enable and Disable the show meeting chat option    device=device_1    state=off
    select front row left default panel option    device=device_1    show_on_left=chat
    Join Meeting    device=device_1,device_2      meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    Verify layout options       device=device_1
    verify Content Gallery should be selected   device=device_1     mode=gallery
    Change meeting mode     device=device_1     mode=front_row
    Verify front row mode   device=device_1     chat_toggle=off
    select the drop down under show on left and show on right     device=device_1     show_on_left=raised_hands     show_on_right=hide
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2    AND     Enable and Disable the show meeting chat option     device=device_1    state=on

TC15:[Stage Layout Switcher] Verify the Front Row with Left and Right Panels.
	[Tags]    444538     P1     sanity_sm
    [Setup]    Testcase Setup for Meeting User   count=2
    Join Meeting    device=device_1,device_2     meeting=cnf_device_meeting
    Verify meeting state   device_list=device_1,device_2       state=Connected
    Verify layout options       device=device_1
    verify Content Gallery should be selected   device=device_1     mode=gallery
    Change meeting mode     device=device_1     mode=front_row
    Verify front row mode   device=device_1
    select the drop down under show on left and show on right     device=device_1     show_on_left=raised_hands     show_on_right=chat
    Verify the right and left after switching the dropdown options in front row     device=device_1     mode=raised_hands
    End meeting     device=device_1,device_2
    Verify meeting state    device_list=device_1,device_2     state=Disconnected
    [Teardown]  Run Keywords    Capture on Failure  AND   Come back to home screen     device_list=device_1,device_2


*** Keywords ***
Navigate to app settings page
    [Arguments]     ${device}
    Click on more option   ${device}
    Click on settings page   ${device}

Enable and Disable the show meeting chat option
    [Arguments]       ${device}    ${state}
    Navigate to app settings page    ${device}
    navigate to meetings option in device settings page      ${device}
    Enable and disable the chat toggle in admin setting     ${device}   state=${state}
    Come back from admin settings page      device_list=${device}

select front row left default panel option
    [Arguments]       ${device}    ${show_on_left}
    Navigate to app settings page    ${device}
    navigate to meetings option in device settings page      ${device}
    select front row left default panel option in admin setting     ${device}   show_on_left=${show_on_left}
    Come back from admin settings page      device_list=${device}

