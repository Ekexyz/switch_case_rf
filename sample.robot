*** Settings ***
Library                 SwitchCaseLibrary.py
Library                 QForce
Suite Setup             OpenBrowser  about:blank  chrome
Suite Teardown          CloseAllBrowsers


*** Test Cases ***
Example Test With Switch Case

    ${apple_case}=    Create List    Log    Found an apple!    console=${TRUE}
    ${banana_case}=   Create List    Log    Found a banana!    console=${TRUE}
    ${default_case}=  Create List    Log    Unknown fruit      console=${TRUE}
    
    ${cases}=    Create Dictionary
    ...    apple=${apple_case}
    ...    banana=${banana_case}
    ...    default=${default_case}

    ${result}=    Run Keyword Switch    banana  ${cases}
