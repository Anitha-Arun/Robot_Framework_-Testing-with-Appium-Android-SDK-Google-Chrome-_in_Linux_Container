*** Settings ***
Library     cap_policy_keywords
Library     IPPhone_policies_keywords.py
Library     calendar_keywords
Library     call_keywords
Library     app_settings_keywords.py
Resource    ../resources/keywords/common.robot

*** Variables ***


*** Keywords ***
Verify settings calling option
    [Arguments]     ${device}
    Open settings page    ${device}
    open and verify calling option    ${device}

Verify settings company portal page
    [Arguments]     ${device}
    Open settings page    ${device}
    Swipe till end    ${device}
    Verify company portal option    ${device}

verify and block calls with no caller id
    [Arguments]     ${device}   ${block_user}
    Block calls with no caller id      ${device}    ${block_user}
    go back to previous page    ${device}

verify and unblock calls with no caller id
    [Arguments]     ${device}
    Unblock calls with no caller id      ${device}
    go back to previous page    ${device}

verify privacy and cookies view
    [Arguments]     ${device}
    verify privacy and cookies     ${device}

verify terms of use view
    [Arguments]     ${device}
    verify terms of use     ${device}

verify user profile view
    [Arguments]     ${device}
    View user profile     ${device}
