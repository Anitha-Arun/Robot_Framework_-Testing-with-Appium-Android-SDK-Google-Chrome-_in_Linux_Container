*** Settings ***
Library     tr_app_settings_keywords
Library     tr_settings_keywords
Library     tr_device_settings_keywords
Library     tr_call_keywords
Library     call_keywords
Library     tr_calendar_keywords
Library     calendar_keywords
Resource    ../resources/keywords/common.robot

*** Keywords ***
Verify meeting unmute state
    [Arguments]     ${device_list}      ${state}
    Verify call mute state   device_list=device_1    state=unmute

Meeting call on hold
    [Arguments]    ${device}
    Hold the call   device=device_1

Verify list of inivited participant on screen
    [Arguments]   ${device}    ${connected_device_list}
    Verify participant list from meeting roster     ${device}    ${connected_device_list}

Turn off incoming call
    [Arguments]     ${device_list}
    Choose incoming video call   ${device_list}   state=OFF

Turn on incoming call
    [Arguments]     ${device_list}
    Choose incoming video call   ${device_list}   state=ON

Initiates conference meeting using Meet now option
    [Arguments]     ${from_device}     ${to_device}
    Meet now meeting   ${from_device}     ${to_device}    method=displayname

View current meeting display on screen
    [Arguments]    ${device}
    Verify meeting display on home screen   ${device}

Refresh Meeting visibility
    [Arguments]    ${device}
     Refresh meeting visibility for conf device  ${device}

Verify sliding menu option inside settings icon
   [Arguments]    ${device}
   Tap on whiteboard share screen settings icon   ${device}

Verify call screen state after tapping on stop presenting button
    [Arguments]     ${device_list}      ${state}
    Verify Call State    ${device_list}     ${state}

Verify list of inivited participants display on screen
    [Arguments]    ${device}
    Verify participants list in meeting   ${device}

Close participants screen
    [Arguments]    ${device}
    Close roaster button on participants screen   ${device}

Check for whiteboard visibility of participants and validate
    [Arguments]    ${from_device}      ${connected_device_list}
    Verify whiteboard visibility for participants   ${from_device}      ${connected_device_list}

Verify device supports whiteboard sharing under more option
    [Arguments]     ${device}
    ${status}     verify_whiteboard_sharing_support_device    ${device}
    Pass Execution if    '${status}' == 'fail'    ${device}, device doesn't support whiteBoard Sharing so aborting the test execution.

Validate edit box options on whiteboard share screen
    [Arguments]     ${device}     ${text}
    Navigate back to call screen after tapping on back button   ${device}
    Verify text box options and validate    ${device}     ${text}

Disable meeting name toggle button
    [Arguments]       ${device}
    Validate functionality of meeting name toggle button   ${device}    state=OFF

Check meeting lock state
    [Arguments]    ${device_list}
    Verify lock meeting visiblity   ${device_list}   state=lock_meeting

Check meeting unlock state
    [Arguments]    ${device_list}
    Verify lock meeting visiblity   ${device_list}   state=unlock_meeting

Validate Drag and Drop functinality of sticky notes
    [Arguments]     ${device}    ${text}
    Verify drag and drop of sticky notes    ${device}    ${text}   source=sticky_notes   destination=moving_down

Switch to together mode
    [Arguments]    ${device}
    Verify together mode and validate   ${device}

Switch to gallery mode
    [Arguments]    ${device}
    Verify gallery mode and validate  ${device}

Switch to large gallery mode
    [Arguments]      ${device}
    Verify large gallery mode and validate    ${device}

Initiates meeting using Meet now option using DID
    [Arguments]     ${from_device}     ${to_device}
    Meet now meeting   ${from_device}     ${to_device}    method=phone_number