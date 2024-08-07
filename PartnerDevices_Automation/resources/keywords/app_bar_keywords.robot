*** Settings ***
Resource    ../resources/keywords/common.robot
Resource    ../resources/keywords/call_views_keywords.robot
Library     call_views_keywords
Library     app_bar_keywords

*** Keywords ***
Select default view value option
    [Arguments]     ${device}    ${option}
    Verify call views option under callings settings    ${device}
    Select default view option    ${device}    option=${option}


Navigate away from meeting roaster and tap on more option
    [Arguments]     ${device}
    #Click back btn  ${device}
    Come back to home screen    device_list=${device}    disconnect=False
    Navigate to more option   ${device}
    Navigate to hidden app inside more option  ${device}
    Click on call action bar  ${device}

Check app bar feature
    [Arguments]  ${device}    ${status}
    ${status}   app_bar_feature  ${device}
    pass execution if  'status==fail'       ${device}:Portrait devices does not support app bar feature