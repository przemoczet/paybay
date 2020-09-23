*** Settings ***
Library         RequestsLibrary
[Force Tags]    api_test

*** Variables ***
${base_url}    http://localhost:5000/


*** Test Cases ***
Check That Api Accepts Post Request
    Create Session    my_session    ${base_url}
    ${data}=    Create dictionary    order_id=400    payment_amount=3    currency=USD
    ${response}=    Post Request    my_session    process    data=${data}
    Should Be Equal As Strings    ${response}    <Response [200]>

Check That Api Does Not Accept Post Request With order_id Containing String
    Create Session    my_session    ${base_url}
    ${data}=    Create dictionary    order_id=aaa    payment_amount=3    currency=USD
    ${response}=    Post Request    my_session    process    data=${data}
    Should Be Equal As Strings    ${response}    <Response [400]>
    
Check That Api Does Not Accept Post Request With Not Existing Currency
    Create Session    my_session    ${base_url}
    ${data}=    Create dictionary    order_id=aaa    payment_amount=3    currency=AAA
    ${response}=    Post Request    my_session    process    data=${data}
    Should Be Equal As Strings    ${response}    <Response [400]>