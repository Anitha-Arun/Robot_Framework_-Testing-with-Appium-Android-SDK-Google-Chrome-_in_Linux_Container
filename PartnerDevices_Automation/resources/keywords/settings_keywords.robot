*** Settings ***
Documentation    Suite description
Library     settings_keywords
Resource    ../resources/keywords/common.robot


*** Variables ***
${wait_time} =  15


*** Keywords ***
Set Call Forwarding
    [Arguments]     ${device}
    verify and enable call forwarding    ${device}

verify and enable call forwarding
    [Arguments]     ${device}
    Open settings page      ${device}
    Enable call forwarding      ${device}
    Come back to home screen    ${device}

verify and disable call forwarding
    [Arguments]     ${device}
    Open settings page      ${device}
    Disable call forwarding      ${device}
    Come back to home screen    ${device}

click back btn
    [Arguments]     ${device}
    click_back      ${device}

refresh the page
    [Arguments]     ${device}
    refresh_main_tab    ${device}

reboot the device
    [Arguments]     ${device}
    open_settings_page      ${device}
    click_device_settings     ${device}
    click_settings_debug    ${device}
    reboot_device    ${device}

verify and enable dark theme
    [Arguments]     ${device}
    open_settings_page      ${device}
    enable_dark_theme      ${device}
    verify_dark_theme_status     ${device}    status=ON
    #get_screenshot      ${device}   dark_theme_enabled
    get_screenshot     name=dark_theme_enabled    device_list=${device}
    Navigate back once    ${device}

verify and disable dark theme
    [Arguments]     ${device}
    open_settings_page      ${device}
    disable_dark_theme      ${device}
    verify_dark_theme_status     ${device}    status=OFF
    #get_screenshot      ${device}   dark_theme_disabled
    get_screenshot      name=dark_theme_disabled    device_list=${device}
    Navigate back once   ${device}


Enable call forwarding and add contact
    [Arguments]     ${from_device}     ${contact_device}
    open_settings_page      ${from_device}
    call_forward_setup      ${from_device}     contact_device=${contact_device}     call_forward_to=contacts

Enable unanswered call and add contact
    [Arguments]     ${from_device}     ${contact_device}
    open_settings_page      ${from_device}
    unanswered_call_setup      ${from_device}      contact_device=${contact_device}    select_option=contacts

Enable unanswered call to call group
    [Arguments]     ${from_device}     ${contact_device}
    open_settings_page      ${from_device}
    unanswered_call_setup      ${from_device}      contact_device=${contact_device}    select_option=call group

Enable unanswered call to delegates
    [Arguments]     ${from_device}     ${contact_device}
    open_settings_page      ${from_device}
    unanswered_call_setup      ${from_device}      contact_device=${contact_device}    select_option=delegate

Enable unanswered call to voicemail
    [Arguments]     ${from_device}      ${contact_device}
    open_settings_page      ${from_device}
    unanswered_call_setup      ${from_device}      contact_device=${contact_device}    select_option=voicemail

Disable unanswered call
    [Arguments]     ${device}       ${contact_device}
    open_settings_page      ${device}
    unanswered_call_setup      ${device}        contact_device=${contact_device}      select_option=off

Enable Also Ring Call group
    [Arguments]     ${device}
    open_settings_page      ${device}
    setup_also_ring     ${device}    select_option=call group

Enable Also Ring delegates
    [Arguments]     ${device}
    open_settings_page      ${device}
    setup_also_ring     ${device}    select_option=delegate

Enable Also Ring and add contact
    [Arguments]     ${device}   ${contact_device}
    open_settings_page      ${device}
    setup_also_ring     ${device}   contact_device=${contact_device}   select_option=contact

Enable Also Ring Voicemail
    [Arguments]     ${device}
    open_settings_page      ${device}
    setup_also_ring     ${device}    select_option=voicemail

Disable Also Ring
    [Arguments]     ${device}
    open_settings_page      ${device}
    setup_also_ring     ${device}      select_option=off

Enable call forwarding to call group
    [Arguments]     ${from_device}     ${contact_device}
    open_settings_page      ${from_device}
    call_forward_setup      ${from_device}     ${contact_device}     call_forward_to=call group
    Come back to home screen    ${from_device}

Enable call forwarding to delegates
    [Arguments]     ${from_device}     ${contact_device}
    open_settings_page      ${from_device}
    call_forward_setup      ${from_device}     ${contact_device}     call_forward_to=delegate
    Come back to home screen    ${from_device}

Enable call forwarding to voicemail
    [Arguments]     ${from_device}     ${contact_device}
    open_settings_page      ${from_device}
    call_forward_setup      ${from_device}     ${contact_device}     call_forward_to=voicemail
    Come back to home screen    ${from_device}

Enable call forwarding to contacts
    [Arguments]     ${from_device}     ${contact_device}
    open_settings_page      ${from_device}
    call_forward_setup      ${from_device}     ${contact_device}     call_forward_to=contacts
    Come back to home screen    ${from_device}

Add new delegates with both permission and validate
    [Arguments]     ${from_device}     ${to_device}
    open_settings_page      ${from_device}
    open_manage_delegate_page    ${from_device}
    Add new delegate      ${from_device}      ${to_device}
    validate added delegate user name      ${from_device}      ${to_device}
    Come back to home screen    ${from_device}
    navigate to calls favorites page  ${to_device}
    refresh calls main tab  ${to_device}

Add new delegates with Make call permission and validate
    [Arguments]     ${from_device}     ${to_device}
    open_settings_page      ${from_device}
    open_manage_delegate_page    ${from_device}
    Add new delegate      ${from_device}      ${to_device}  permission=Make Call
    validate added delegate user name      ${from_device}      ${to_device}
    Come back to home screen    ${from_device}

Add new delegates with Receive call permission and validate
    [Arguments]     ${from_device}     ${to_device}
    open_settings_page      ${from_device}
    open_manage_delegate_page    ${from_device}
    Add new delegate      ${from_device}      ${to_device}  permission=Receive Call
    validate added delegate user name      ${from_device}      ${to_device}
    Come back to home screen    ${from_device}

Edit added delegates with Receive call permission and validate
    [Arguments]     ${from_device}     ${to_device}
    open_settings_page      ${from_device}
    open_manage_delegate_page    ${from_device}
    Edit delegate      ${from_device}      ${to_device}  permission=Receive Call
    Come back to home screen    ${from_device}

Edit added delegates with Make call permission and validate
    [Arguments]     ${from_device}     ${to_device}
    open_settings_page      ${from_device}
    open_manage_delegate_page    ${from_device}
    Edit delegate      ${from_device}      ${to_device}  permission=Make Call
    Come back to home screen    ${from_device}

Edit added delegates with both permission and validate
    [Arguments]     ${from_device}     ${to_device}
    open_settings_page      ${from_device}
    open_manage_delegate_page    ${from_device}
    Edit delegate      ${from_device}      ${to_device}
    Come back to home screen    ${from_device}

Validate added delegate user visibility
    [Arguments]     ${from_device}     ${to_device}
    open_settings_page      ${from_device}
    validate added delegate user name      ${from_device}      ${to_device}
    Come back to home screen    ${from_device}

Refresh page for delegate user config changes visibility
    [Arguments]     ${device}
    open_settings_page      ${device}
    open_manage_delegate_page    ${device}
    Come back to home screen    ${device}
    navigate to calls favorites page  ${device}
    Refresh calls main tab   ${device}

check presence feature
    [Arguments]     ${device}    ${state}
    ${status}     verify_presence_feature       ${device}
    Pass Execution if    '${status}' == 'fail'    ${device}: Conference Portrait Devices doesn't supports Presence feature.

verify dark theme option
    [Arguments]     ${device}
    ${status}     verify_appearance_option       ${device}
    Pass Execution if    '${status}' == 'fail'    ${device}: Conference Portrait Devices doesn't supports Dark Theme enable/disable feature.

verify hotdesking enabled device
    [Arguments]     ${device}   ${status}
    ${status}     verify_presence_feature       ${device}
    Pass Execution if    '${status}' == 'fail'    ${device}: Conference Portrait Devices doesn't supports hot desk feature.

verify hamburger menu for conf devices
    [Arguments]     ${device}    ${status}
    ${status}     verify_presence_feature       ${device}
    Pass Execution if    '${status}' == 'fail'    ${device}: Conference Portrait Devices doesn't supports hamberg menu.

verify conference room UI feature
     [Arguments]     ${device}
     ${status}   verify_conf_room_UI_feature       ${device}
     Pass Execution if    '${status}' == 'fail'    ${device}: Conference Landscape Devices doesn't supports Conference room UI feature.

verify is portrait device
     [Arguments]     ${device}
     ${display_type}   verify_device_display_type       ${device}
     Pass Execution if    '${display_type}' == 'landscape'    ${device}:Landscape Devices doesn't supports Dail pad.

verify is landscape device
     [Arguments]     ${device}
     ${display_type}   verify_device_display_type     ${device}
     Pass Execution if    '${display_type}' == 'portrait'    ${device}:portrait Devices doesn't supports Extended Dail pad.

verify dial pad for conference
     [Arguments]     ${device}
     ${display_type}   verify_device_display_type       ${device}
     Pass Execution if    '${display_type}' == 'landscape'    ${device}:Landscape Devices doesn't supports Dial pad.

verify dial pad for cap
     [Arguments]     ${device}
     ${status}    is dial pad applicable for cap      ${device}
     Pass Execution if    '${status}' == 'pass'     ${device}:MP54 doesn't supports Dial pad.
