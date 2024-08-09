*** Settings ***
Library     people_keywords
Library     call_keywords

*** Variables ***


*** Keywords ***
Click plus icon and Verify its two options
    [Arguments]     ${device}
    click_on_plus_icon_on_people_tab    ${device}
    verify_plus_icon_two_options   ${device}

Navigate to Create group screen
    [Arguments]     ${device}
    Navigate to people tab    ${device}
    Verify plus icon on people tab    ${device}
    click_on_plus_icon_on_people_tab    ${device}
    verify_plus_icon_two_options   ${device}
    Select people app option and verify     ${device}    option=Create new group

Navigate to Add from directory screen
    [Arguments]     ${device}
    Navigate to people tab    ${device}
    Verify plus icon on people tab    ${device}
    click_on_plus_icon_on_people_tab    ${device}
    verify_plus_icon_two_options   ${device}
    Select people app option and verify     ${device}    option=Add from directory

Select created group from drop down
    [Arguments]     ${device}    ${group_name}
    Click drop down menu and verify list of groups    ${device}
    Select group from drop down     ${device}     ${group_name}

Verify Speed dial contacts from people tab should reflect under calls favorites tab
    [Arguments]     ${from_device}    ${to_device}
    Verify added favorite user in favorites page    ${from_device}     ${to_device}


