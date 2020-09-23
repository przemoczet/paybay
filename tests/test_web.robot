*** Settings ***
Library SeleniumLibrary
[Force Tags]   web_test 
[Teardown]     Close Browser

*** Variables ***
${web_url}    http://localhost:5000/
${browser}    Chrome

*** Test Cases ***
Check That Passing Form Is Possible With Correct Data
    Open Web Page
    Fill Field    order_id    1
    Fill Field    payment_amount    200
    Fill Field    currency    USD
    Register Transaction
    Page Should Contain    Pay!
        
*** Keywords ***
Open Web Page
   Open browser    ${web_url}   ${browser}
   
Fill Field
    [Arguments]    input_id    value
    Click Element    id=input_id
    Input Text    id=input_id     value

Register Transaction
    Click Element    id=pay
