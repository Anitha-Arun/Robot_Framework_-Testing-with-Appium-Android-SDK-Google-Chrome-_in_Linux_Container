*** Settings ***
Resource    ../resources/keywords/common.robot
Suite Setup     Teams Rooms Console Setup
Suite Teardown     console System Teardown

*** Variables ***


*** Keywords ***
Teams Rooms Console Setup
    ${config} =     Read Config
    set suite variable      ${config}   ${config}
    Capture config    ${config}
    Setup Devices

console System Teardown
    sign out from the users
    Capture bugreport post run
    Kill Servers

sign out from the users
    run keyword and ignore error       Sign Out Console
    run keyword and ignore error       Sign Out
