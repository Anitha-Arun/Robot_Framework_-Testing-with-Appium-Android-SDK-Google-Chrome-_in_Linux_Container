*** Settings ***
Library     panels_homescreen_keywords


*** Variables ***


*** Keywords ***
Verify homescreen on panel
    [Arguments]  ${device}
    verify room parameters    ${device}
    verify scrollable agenda view  ${device}
    verify room availability to reserve  ${device}
    verify extensibility apps on homescreen  ${device}


Verify and reserve room
    [Arguments]  ${device}
    verify room availability to reserve  ${device}  action="reserve"