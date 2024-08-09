*** Settings ***
Library     initiate_driver
Library     SignInOut
Library     DateTime
Library     OperatingSystem
Library     common
Library     device_settings_keywords
Library     settings_keywords
Library     hot_desking_keywords
Library     home_screen_keywords
Library     call_views_keywords
Library     meeting_reminder_keywords
Library     app_bar_keywords
Library     tr_signin_keywords
Library     tr_app_settings_keywords
Library     tr_device_settings_keywords
Library     tr_settings_keywords
Library     tr_home_screen_keywords
Library     tr_call_keywords
Library     tr_calendar_keywords
Library     call_hand_off
Library     transition_keywords
Library     panels_homescreen_keywords
Library     tr_background_change_keywords
Library     tr_console_signin_keywords
Library     tr_console_home_screen_keywords
Library     tr_console_settings_keywords
Library     tr_console_app_settings_keywords
Library     tr_console_call_keywords
Library     tr_console_calendar_keywords
Library     ztp_keywords
Library     walkie_talkie_keywords
Library     panels_app_settings_keywords
Library     panel_meetings_device_settings_keywords
Library     panel_and_room_keywords
Library     refresh_calendar_ux_keywords
Library     lcp_signinout
Library     lcp_homescreen_keywords
Library     lcp_calls
Library     qr_room_reservation_keywords
Library     intent_keywords
Library     search_keywords
Library     signin_keywords
Library     TAC_signin_keywords
Library     panel_maintenance_reboot_keywords
Resource    call_keywords.robot
Resource    calendar_keywords.robot
Resource    voicemail_keywords.robot
Resource    app_settings_keywords.robot
Resource    voicemail_keywords.robot
Resource    settings_keywords.robot
Resource    device_settings_keywords.robot
Resource    people_keywords.robot
Resource    hot_desking_keywords.robot
Resource    home_screen_keywords.robot
Resource    call_views_keywords.robot
Resource    app_bar_keywords.robot
Resource    tr_signin_keywords.robot
Resource    tr_device_settings.robot
Resource    tr_home_screen_keywords.robot
Resource    tr_call_keywords.robot
Resource    tr_calendar_keywords.robot
Resource    tr_settings_keywords.robot
Resource    transition_keywords.robot
Resource    panels_homescreen_keywords.robot
Resource    tr_background_change_keywords.robot
Resource    tr_console_call_keywords.robot
Resource    tr_console_calendar_keywords.robot
Resource    ztp_keywords.robot
Resource    walkie_talkie_keywords.robot
*** Variables ***

@{ALLDEVICES} =    device_1    device_2    device_3    device_4    device_5
@{PSTN_users}       user   pstn_user   user     user
@{2_PSTN_users}         user   pstn_user   pstn_user     user
@{GCP_PSTN_users}       user     gcp_user    pstn_user   user
@{Delegate_PSTN_users}      user    delegate_user   pstn_user   user
@{Delegate_users}       user     delegate_user   user     user
@{GCP_users}        user   gcp_user     user    user
@{CQ_users}         cq_user   user   cq_user   user
@{CQ_PSTN_users}        cq_user  pstn_user    cq_user    user
@{CAP_users}        cap_search_enabled   user   user   user
@{CAP_PSTN_users}       cap_search_enabled  pstn_user    user    user
@{Meeting_users}        meeting_user     user     user     user
@{Meeting_PSTN_users}       meeting_user    pstn_user   user     user
@{Meeting_2_PSTN_users}         meeting_user  pstn_user   pstn_user   user
@{Meeting_GCP_users}        meeting_user     gcp_user    user     user
@{CAP_2_PSTN_users}         cap_search_enabled    pstn_user   pstn_user   user
@{CAP_Delegate_users}       cap_search_enabled  delegate_user    user    user
@{CAP_Delegate_PSTN_users}      cap_search_enabled  delegate_user    pstn_user    user
@{CAP_2_Delegate_users}         cap_search_enabled    delegate_user   delegate_user   user
@{DUT_as_PSTN_users}        pstn_user   user     user     user
@{PSTN_users_Disabled}       meeting_user    pstn_disabled   user     user
@{CAP_and_GCP_users}        cap_search_enabled    gcp_user   user   user
@{auto_checkin_user}        auto_checkin_user       auto_checkin_user       user    auto_checkin_user

*** Keywords ***
System Setup
    Main Setup
    Log     System Setup

Main Setup
    ${config} =     Read Config
    set suite variable      ${config}   ${config}
    Capture config    ${config}
    Setup Devices
    Sign In

Cap User Setup
    Cap Main Setup
    Log     Cap User Setup

Cap Main Setup
    ${config} =     Read Config
    set suite variable      ${config}   ${config}
    Capture config    ${config}
    Setup Devices
    Sign In     user_list=cap_search_enabled,user,user,user

Conference System Setup
    Meeting Setup
    Log     Conference System Setup

Meeting Setup
    ${config} =     Read Config
    set suite variable      ${config}   ${config}
    Capture config    ${config}
    Setup Devices
    Sign In     user_list=meeting_user,user,user,user

User Setup Main
    Set Global Variable     ${flag}     False
    User Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

User Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=user,user,user

User Teardown
    Run Keyword If      ${flag}==False      Capture on Suite Failure

PSTN Setup Main
    Set Global Variable     ${flag}     False
    PSTN Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

PSTN Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=user,pstn_user,user

Meeting PSTN Setup Main
    Set Global Variable     ${flag}     False
    Meeting PSTN Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

Meeting PSTN Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=meeting_user,pstn_user,user

PSTN Setup Main for 2 Users
    Set Global Variable     ${flag}     False
    PSTN Setup for 2 users
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

PSTN Setup for 2 users
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=user,pstn_user,pstn_user

CAP Setup Main
    Set Global Variable     ${flag}     False
    CAP Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

CAP Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=cap_search_enabled,user,user

Cap Setup for Search Disabled Main
    Set Global Variable     ${flag}     False
    CAP Setup for Search Disabled
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

CAP Setup for Search Disabled
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=cap_search_disabled,user,user

Meeting Policy Setup Main
    Set Global Variable     ${flag}     False
    Meeting Policy Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

Meeting Policy Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=meeting_user,user,user

Intents Setup Main
    Set Global Variable     ${flag}     False
    Intents Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

Intents Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=meeting_user,user,user

CAP and PSTN Setup Main
    Set Global Variable     ${flag}     False
    CAP and PSTN Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

CAP and PSTN Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=cap_search_enabled,pstn_user,user

Delegate User Setup Main
    Set Global Variable     ${flag}     False
    Delegate User Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

Delegate User Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=user,delegate_user,user

GCP User Setup Main
    Set Global Variable     ${flag}     False
    GCP User Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

GCP User Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=user,gcp_user,user

PSTN CQ User Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=cq_user,pstn_user,cq_user
    Reset Logcat Capture    device=device_1,device_2,device_3

GCP PSTN User Setup Main
    Set Global Variable     ${flag}     False
    GCP PSTN User Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

GCP PSTN User Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=user,gcp_user,pstn_user

Delegate PSTN User Setup Main
    Set Global Variable     ${flag}     False
    Delegate PSTN User Setup
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

Delegate PSTN User Setup
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=user,delegate_user,pstn_user

Teams CQ User Setup
    Set Global Variable     ${flag}     False
    Verify Device Users     device_list=device_1,device_2,device_3  user_list=cq_user,user,cq_user
    Reset Logcat Capture    device=device_1,device_2,device_3
    Set Global Variable     ${flag}     True

Wait for Some Time
    [Arguments]     ${time}
    Sleep       ${time}

Capture on Suite Failure
    get_screenshot      name=${SUITE NAME}

Capture on Failure
    Run Keyword If      ${tc_flag}==False    Fail    "Device criteria not met"
    run keyword if test failed   Screenshot and Logcat

Screenshot and Logcat
    run keyword and continue on failure  get_screenshot      name=${SUITE NAME}_${TEST NAME}
    run keyword and continue on failure  capture_logcat_logs     name=${SUITE NAME}_${TEST NAME}
    run keyword and continue on failure  get_bugreport_on_app_crash   name=${SUITE NAME}_${TEST NAME}

Capture screenshot logcats and app crash
    [Arguments]  ${name}
    run keyword and continue on failure  get_screenshot      name=${name}
    run keyword and continue on failure  capture_logcat_logs     name=${name}
    run keyword and continue on failure  get_bugreport_on_app_crash   name=${name}

Suite Failure Capture
    run keyword if any tests failed    Screenshot and Logcat for suite

Screenshot and Logcat for suite
    run keyword and continue on failure  get_screenshot      name=${SUITE NAME}
    run keyword and continue on failure  capture_logcat_logs     name=${SUITE NAME}

System Teardown
#    Sign Out
    Capture bugreport post run
    Kill Servers

System Teardown for CAP Premium
    Disable advance calling option     device=device_1
    Capture bugreport post run
    Kill Servers

Kill Servers
    log     Killing Appium Servers
    teardown devices

get device displayname
    [Arguments]     ${device}
    ${displayname_name}    device_displayname      ${device}
    [Return]    ${displayname_name}

Testcase Setup
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     device_list=${ALLDEVICES}[:${count}]

Testcase Setup for PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${PSTN_users}[:${count}]

Testcase Setup for 2 PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${2_PSTN_users}[:${count}]

Testcase Setup for GCP PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${GCP_PSTN_users}[:${count}]

Testcase Setup for Delegate PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${Delegate_PSTN_users}[:${count}]

Testcase Setup for Delegate User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${Delegate_users}[:${count}]

Testcase Setup for GCP User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${GCP_users}[:${count}]

Testcase Setup for CQ User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CQ_users}[:${count}]

Testcase Setup for CQ PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CQ_PSTN_users}[:${count}]

Testcase Setup for CAP User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_users}[:${count}]

Testcase Setup for CAP Premium User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_users}[:${count}]
    verify and enable cap premium          device=device_1

Testcase Setup for CAP User for panel
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=cap_user,user,user

Testcase Setup for CAP User for panel and norden
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=cap_user,cap_user,user

Testcase Setup for AC User for panel and norden
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${auto_checkin_user}[:${count}]

Testcase Setup for longname User for panel
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=longname_user

Testcase Setup for CAP PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_PSTN_users}[:${count}]

Testcase Setup for CAP Premium PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_PSTN_users}[:${count}]
    verify and enable cap premium          device=device_1

Testcase Setup for CAP Search Disable User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=cap_search_disabled,user,user

Testcase Setup for Meeting User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${Meeting_users}[:${count}]

Testcase Meeting PSTN Setup Main
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${Meeting_PSTN_users}[:${count}]

Testcase Meeting 2 PSTN Setup Main
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${Meeting_2_PSTN_users}[:${count}]

Testcase Meeting Setup for GCP User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${Meeting_GCP_users}[:${count}]

Testcase Setup for CQ 2PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CQ_PSTN_users}[:${count}]
    signin with other user   device=device_4    other_user_account=device_3:pstn_user

Testcase Setup for HD disabled user
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=hotdesk_disabled_user,user,user

Testcase Setup for Call hand off
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}

Testcase Setup for ZTP
    [Arguments]  ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify signin button on signin page    ${count}

Home Screen Enable
    [Arguments]     ${device}
    verify_and_enable_home_app    ${device}

Home Screen Disable
    [Arguments]     ${device}
    check_version_disable_home_app    ${device}

Capture Failure
    Run Keyword If      ${tc_flag}==False    Fail    "Device criteria not met"
    run keyword if test failed   Screenshot and Logcat
    run keyword if test failed   Capture screenshot and logcat logs

Capture screenshot and logcat logs
    run keyword and continue on failure   capture_screenshot      name=${SUITE NAME}_${TEST NAME}
    run keyword and continue on failure   logcat_logs_capture     name=${SUITE NAME}_${TEST NAME}

Testcase Setup for Shared User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    Check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=meeting_user,user,user
    Verify Console Users    device_list=device_1   console_list=console_1  user_list=meeting_user

Testcase Shared Mode PSTN Setup Main
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=meeting_user,pstn_user,user
    Verify Console Users    device_list=device_1   console_list=console_1  user_list=meeting_user

Testcase Setup for User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users
    Verify Console Users

Testcase Setup for CAP 2 PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_2_PSTN_users}[:${count}]

Testcase Setup for CAP Premium 2 PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_2_PSTN_users}[:${count}]
    verify and enable cap premium          device=device_1

Testcase Shared Mode For 2 PSTN Setup
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=meeting_user,pstn_user,pstn_user
    Verify Console Users    device_list=device_1   console_list=console_1  user_list=meeting_user

Testcase Setup for CAP Delegate User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_Delegate_users}[:${count}]

Testcase Setup for CAP Premium Delegate User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_Delegate_users}[:${count}]
    verify and enable cap premium          device=device_1

Testcase Setup for CAP Delegate PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_Delegate_PSTN_users}[:${count}]

Testcase Setup for CAP Premium Delegate PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_Delegate_PSTN_users}[:${count}]
    verify and enable cap premium          device=device_1

Testcase Setup for CAP 2 Delegate User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_2_Delegate_users}[:${count}]

Panels Suite Setup
    verify devices configured in panels setup
    verify device users in panels setup

Capture config
    [Arguments]     ${config}
    ${status}   capture config details
    Run keyword if  '${status}' == 'True'    Log    ${config}
    ...  ELSE   Log   Partner Devices doesn't capture config details

Testcase Setup for idle mode recovery optimization and presence resilience
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}


Testcase Setup for premium license User for panel
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=premium_user,user,user

Testcase Setup for standard license User for panel
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=standard_user,user,user

Testcase Setup for LCP ZTP
    [Arguments]  ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}

Testcase Setup for LCP PSTN User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=user,pstn_user,user

Testcase Meeting PSTN Setup as Main device
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${DUT_as_PSTN_users}[:${count}]

Testcase Setup for PSTN Disabled
     [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${PSTN_users_Disabled}[:${count}]

Testcase Setup for CAP and GCP User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_and_GCP_users}[:${count}]

Testcase Setup for CAP Premium and GCP User
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${CAP_and_GCP_users}[:${count}]
    verify and enable cap premium          device=device_1

Testcase setup for shared mode PSTN Setup as Main device
    [Arguments]     ${count}
    Set Global Variable     ${tc_flag}     False
    check for device count      count=${count}
    Set Global Variable     ${tc_flag}     True
    Reset Logcat Capture    ${count}
    Verify Device Users     user_list=${DUT_as_PSTN_users}[:${count}]
    Verify Console Users    device_list=device_1   console_list=console_1   user_list=pstn_user

