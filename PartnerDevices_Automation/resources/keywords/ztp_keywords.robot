*** Settings ***
Library     ztp_keywords
Resource    ../resources/keywords/common.robot

*** Keywords ***
verify the signin ui for ztp
    [Arguments]     ${device}
    verify ztp signin ui    ${device}

verify settings option from signin page
    [Arguments]    ${device}
    verify settings from signin page    ${device}
    close settings window from signin page    ${device}

verify cloud option for provisioning device
    [Arguments]    ${device}
    verify cloud option    ${device}
    device setting back till signin btn visible    ${device}

Verify provision phone option
    [Arguments]    ${device}
    verify provision phone ui    ${device}
    Verify able to edit the code on provision phone ui      ${device}
    device setting back till signin btn visible    ${device}
