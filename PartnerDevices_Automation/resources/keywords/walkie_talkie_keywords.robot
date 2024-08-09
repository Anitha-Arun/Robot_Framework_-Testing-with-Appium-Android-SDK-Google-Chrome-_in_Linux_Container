*** Settings ***
Library     walkie_talkie_keywords
Resource    ../resources/keywords/common.robot

*** Keywords ***
Select and switch between channels
    [Arguments]     ${device}     ${channel}
    select the channel  ${device}     channel=${channel}
    click on connect and verify mic    ${device}
    verify connected paricipant list   device=device_1      connected_device_list=${device}
    press and hold the mic button     from_device=device_1    to_device=device_2