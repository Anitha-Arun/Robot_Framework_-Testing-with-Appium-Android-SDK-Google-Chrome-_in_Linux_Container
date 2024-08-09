*** Settings ***
Library     voicemail_keywords
Library     settings_keywords
Resource    ../resources/keywords/common.robot


*** Variables ***


*** Keywords ***
Click on voicemail play button and validate
    [Arguments]     ${device}
    play_voicemail_from_left    ${device}

Play multiple voicemail from list
    [Arguments]     ${on_device}    ${from_device}
    play_multiple_voicemail      ${on_device}    ${from_device}

Get unread voicemail count
    [Arguments]     ${device}
    ${voicemail_count}=    get_missed_voicemail_count    ${device}
    log    ${voicemail_count}
    [Return]    ${voicemail_count}

Validate voicemail count
    [Arguments]     ${before_new_vm_count}     ${after_new_vm_count}    ${new_vm_num}
    ${total_vm_num}=   Evaluate    ${before_new_vm_count}+${new_vm_num}

    run keyword if  ${total_vm_num} == ${after_new_vm_count}    Log   voicemail count got increased
    ...   ELSE   fail   Voicemail count didn't increase.
    [Return]    ${total_vm_num}

Verify voicemail object for new user
    [Arguments]     ${device}
    run keyword and ignore error  Verify no voicemail object display for new user   ${device}

Get unread voicemail count lcp
    [Arguments]     ${device}
    navigate to calls tab    device=device_1
    come back to home screen  device_list=device_1
    ${voicemail_count}=    get_missed_voicemail_count    ${device}
    log    ${voicemail_count}
    [Return]    ${voicemail_count}