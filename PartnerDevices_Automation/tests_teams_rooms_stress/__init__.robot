*** Settings ***
Resource    ../resources/keywords/common.robot
Suite Setup     Teams Room Setup


*** Variables ***


*** Keywords ***
Teams Room Setup
    ${config} =     Read Config
    set suite variable      ${config}   ${config}
    Log     ${config}
    Setup Devices