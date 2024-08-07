*** Settings ***
Resource    ../resources/keywords/common.robot

*** Keywords ***
Verify Default view relaunches after changing the value
    [Arguments]     ${device}    ${option}
    Verify call views option under callings settings    ${device}
    Select default view     ${device}    option=${option}

Select and cancel default value
    [Arguments]     ${device}    ${option}
    Verify call views option under callings settings    ${device}
    Cancel selected default view    ${device}    option=${option}
    Click back btn     ${device}

Select default view value
    [Arguments]     ${device}    ${option}
    Verify call views option under callings settings    ${device}
    Select default view     ${device}    option=${option}