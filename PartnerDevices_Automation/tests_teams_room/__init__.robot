*** Settings ***
Resource    ../resources/keywords/common.robot
Suite Setup     Teams Room Setup
Suite Teardown     System Teardown


*** Variables ***


*** Keywords ***
Teams Room Setup
    ${config} =     Read Config
    set suite variable      ${config}   ${config}
    Capture config    ${config}
    Setup Devices