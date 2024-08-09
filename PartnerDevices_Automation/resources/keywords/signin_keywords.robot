*** Settings ***
Library     cap_policy_keywords
Library     signin_keywords.py
Library     IPPhone_policies_keywords.py
Library     calendar_keywords
Library     call_keywords
Library  tr_signin_keywords

*** Variables ***


*** Keywords ***
Verify that sign in is successfully completed
    [Arguments]     ${device_list}      ${state}
    Verify that sign in is successful   ${device_list}     ${state}

Verify that sign out is successfully completed
    [Arguments]     ${device_list}      ${state}
    Verify that sign in is successful   ${device_list}     ${state}
