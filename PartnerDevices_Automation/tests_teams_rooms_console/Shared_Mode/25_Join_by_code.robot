*** Settings ***
Force Tags    join_by_code  25  sm
Library     DateTime
Library     OperatingSystem
Resource    ../resources/keywords/common.robot

*** Variables ***
${wait_time} =  10

*** Test Cases ***
TC1:[Join by Code] Verify meeting info option when user join a meeting from "Join with an ID"
    [Tags]      345115      bvt_sm      sanity_sm
    [Setup]  Testcase Setup for shared User     count=2
    Join meeting    device=device_2    meeting=console_lock_meeting
    Verify join with an meeting id options   device=console_1
    Click on close button    console_list=console_1
    join with an meeting id   device=console_1
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    Verify meeting info options when user join a meeting    device=console_1
    Click on close button    console_list=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC2: [Join by Code] Verify "Join with an id" button on console
    [Tags]  345055    P1    sanity_sm
    [Setup]  Testcase Setup for shared User     count=1
    Verify join with an id button in more option     console=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC3:[Join by Code] Verify "Join with an id" should be able to access from more button
    [Tags]      345058      P1      sanity_sm
    [Setup]  Testcase Setup for shared User     count=1
    Verify join with an meeting id options   device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC4:[Join by Code] Verify user cannot join a meeting without passcode
    [Tags]  345088   P1     sanity_sm
    [Setup]  Testcase Setup for shared User     count=1
    Verify join with an meeting id options   device=console_1
    Click on close button    console_list=console_1
    Verify user cannot join a meeting without passcode       device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC5:[Join by Code] Verify meeting ID and passcode fields strings when user tap on "Join with an ID" button
    [Tags]   345091   P1    sanity_sm
    [Setup]    Testcase Setup for shared User     count=1
    Verify meeting ID and passcode fields   device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC6:[Join by Code] Verify Join meeting via Join by ID
    [Tags]   345092       P1    sanity_sm
    [Setup]  Testcase Setup for shared User     count=2
    Join meeting    device=device_2    meeting=console_lock_meeting
    Verify meeting state   device_list=device_2    state=Connected
    Verify join with an meeting id options   device=console_1
    Click on close button    console_list=console_1
    join with an meeting id   device=console_1
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC7:[Join by Code] Verify retry button when a user enters an invalid meeting ID or invalid passcode
    [Tags]   345097       P1     sanity_sm
    [Setup]    Testcase Setup for shared User   count=1
    Checking retry button after enters an invalid meeting ID and invalid passcode      device=console_1
    Click on close button    console_list=console_1
    join with an meeting id   device=console_1
    Verify for call state  console_list=console_1   state=Connected
    End the meeting     console=console_1
    Verify for call state    console_list=console_1   state=Disconnected
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC8:[Join by Code]Verify meeting ID field
    [Tags]   345064     P2
    [Setup]    Testcase Setup for shared User   count=1
    Verify join with an meeting id options   device=console_1
    Click on close button    console_list=console_1
    join with an meeting id   device=console_1
    Verify for call state  console_list=console_1   state=Connected
    End the meeting     console=console_1
    Verify for call state    console_list=console_1   state=Disconnected
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC9:[Join by Code]Verify that when the length of the Meeting ID is less than seven digits the "Join a Meeting button" should be disabled.
    [Tags]     345082  P1      sanity_sm
    [Setup]    Testcase Setup for shared User      count=1
    verify join meeting ID with less than and greater than 7 digit number    device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC10:[Join by Code] Verify user should accept only numeric for meeting ID in meeting field
    [Tags]   345067  P2
    [Setup]  Testcase Setup for shared User  count=1
    Accepting numeric values for meeting id in meeting field      device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC11:[Join by Code]Verify user should not accept Alphabet for meeting ID in meeting field
    [Tags]      345073   P2
    [Setup]    Testcase Setup for shared User   count=1
    Verify meeting field should not accept alphabets for meeting id     device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC12:[Join by Code]Verify meet now from ambient screen
    [Tags]     345121    P1     sanity_sm
    [Setup]    Testcase Setup for shared User   count=2
    Verify precall screen after clicking on meetnow     device=device_1     console=console_1
    End the meeting     console=console_1
    Start meeting using meet now   from_device=console_1    to_device=device_2
    Accept incoming call   device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Connected
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC13:[Join by Code]Verify meeting id should be formatted with a white space every 3 characters
    [Tags]   345074     P2
    [Setup]    Testcase Setup for shared User      count=1
    meeting details containes space for every 3 characters    device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC14:[Join by Code]Verify "Join with an id"button must be added to one of the buttons in the ambient screen of the device
    [Tags]     418772    P1     sanity_sm
    [Setup]    Testcase Setup for shared User   count=1
    verify join with an meeting id options  device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC15:[Join by Code] Verify user should not accept alphanumeric for meeting ID in meeting field
    [Tags]  345079   P2
    [Setup]    Testcase Setup for shared User   count=1
    Verify meeting field should not accept alphanumeric     device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC16:[Join by Code] Verify that when the user enter only meeting passcode "Join a Meeting button" should be disabled.
    [Tags]   345086   P2
    [Setup]    Testcase Setup for shared User   count=1
    verify that user enter only meeting passcode     device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC17:[Join by Code] Verify Error handling when meeting not found.
    [Tags]   345093       P2
    [Setup]    Testcase Setup for shared User   count=1
    invalid meeting id and passcode for join with meeting id    device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC18:[Join by Code] Verify user must be able to edit the meeting ID and passcode previously entered
    [Tags]   345096       P2
    [Setup]    Testcase Setup for shared User   count=1
    verify invalid number and edit the meeting id and passcode  device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC19:[Join by Code] Verify cancel button when a user enters an invalid meeting ID or invalid passcode
    [Tags]   345101     P2
    [Setup]    Testcase Setup for shared User   count=1
    verify invalid number and edit the meeting id and passcode  device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC20:[Join by Code] Verify when a user Join with a wrong meeting code/meeting passcode it should throw a error message
    [Tags]   345107     P2
    [Setup]    Testcase Setup for shared User   count=1
    Verify error message when a user enters an wrong meeting ID   device=console_1
    Click on close button    console_list=console_1
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1

TC21:[Join by code] check the Layout option when joined a meeting through meeting id.
    [Tags]      382122      P2
    [Setup]  Testcase Setup for shared User     count=2
    Join meeting    device=device_2    meeting=console_lock_meeting
    join with an meeting id   device=console_1
    Verify for meeting state     console_list=console_1      device_list=device_2     state=Connected
    change meeting mode     device=console_1    mode=front_row
    Verify front row mode   device=device_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

TC22:[Join by Code] Verify meeting info option & details when DUT user joins a meeting from "Meet now"
    [Tags]      345123      P2
    [Setup]  Testcase Setup for shared User     count=2
    Verify precall screen after clicking on meetnow     device=device_1     console=console_1
    End the meeting     console=console_1
    Verify for call state    console_list=console_1    state=Disconnected
    Start meeting using meet now   from_device=console_1    to_device=device_2
    Accept incoming call   device=device_2
    Verify for call state     console_list=console_1    device_list=device_2    state=Connected
    Verify meeting info details when user join a meeting from Meet      device=console_1
    Click on close button    console_list=console_1
    End a meeting     console=console_1       device=device_2
    Verify for meeting state    console_list=console_1      device_list=device_2      state=Disconnected
    [Teardown]  Run Keywords    Capture Failure  AND   Come back to home screen page   console_list=console_1   device_list=device_2

*** Keywords ***
End a meeting
    [Arguments]    ${console}    ${device}
    End the meeting  ${console}
    End meeting      ${device}

verify meeting ID and passcode fields
    [Arguments]    ${device}
    verify join with an meeting id options   ${device}

Checking retry button after enters an invalid meeting ID and invalid passcode
    [Arguments]     ${device}
    verify invalid number and edit the meeting id and passcode    ${device}

Accepting numeric values for meeting id in meeting field
    [Arguments]    ${device}
    meeting details containes space for every 3 characters      ${device}

invalid meeting id and passcode for join with meeting id
    [Arguments]    ${device}
    verify invalid number and edit the meeting id and passcode    ${device}

Verify error message when a user enters an wrong meeting ID
    [Arguments]   ${device}
    Verify user cannot join a meeting without passcode    ${device}

Verify and change the layouts option after joining the meeting
    [Arguments]   ${device}     ${mode}
    change meeting mode     ${device}       ${mode}
    Verify together mode after switching       ${device}

Verify meeting info details when user join a meeting from Meet
    [Arguments]    ${device}
    Verify meeting info options when user join a meeting      ${device}
