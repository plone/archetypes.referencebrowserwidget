*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Test cases ***

Move reference down while adding (before saving)
    Add three pages
    Add two related items
    Click element  css=#ref-relatedItems-0 .atrb_move_down
    Click element  name=form.button.save
    ${first-related}=  Get text  css=#relatedItemBox dd:nth-child(2) a
    Should be equal  ${first-related}  Second Page
    ${second-related}=  Get text  css=#relatedItemBox dd:nth-child(3) a
    Should be equal  ${second-related}  First Page

Move reference down after saving
    Add three pages
    Add two related items
    Click element  name=form.button.save
    Click link  Edit
    Click link  Categorization
    Click element  css=#ref-relatedItems-0 .atrb_move_down
    Click element  name=form.button.save
    ${first-related}=  Get text  css=#relatedItemBox dd:nth-child(2) a
    Should be equal  ${first-related}  Second Page
    ${second-related}=  Get text  css=#relatedItemBox dd:nth-child(3) a
    Should be equal  ${second-related}  First Page

Move reference up while adding (before saving)
    Add three pages
    Add two related items
    Click element  css=#ref-relatedItems-1 .atrb_move_up
    Click element  name=form.button.save
    ${first-related}=  Get text  css=#relatedItemBox dd:nth-child(2) a
    Should be equal  ${first-related}  Second Page
    ${second-related}=  Get text  css=#relatedItemBox dd:nth-child(3) a
    Should be equal  ${second-related}  First Page

Move reference up after saving
    Add three pages
    Add two related items
    Click element  name=form.button.save
    Click link  Edit
    Click link  Categorization
    Click element  css=#ref-relatedItems-1 .atrb_move_up
    Click element  name=form.button.save
    ${first-related}=  Get text  css=#relatedItemBox dd:nth-child(2) a
    Should be equal  ${first-related}  Second Page
    ${second-related}=  Get text  css=#relatedItemBox dd:nth-child(3) a
    Should be equal  ${second-related}  First Page

*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Manager

Add three pages
    Add document  First Page
    Add document  Second Page
    Add document  Third Page

Add two related items
    Click link  Edit
    Click link  Categorization
    Click element  css=input.searchButton.addreference
    Click element  css=tr:nth-child(1) input.insertreference
    Click element  css=tr:nth-child(2) input.insertreference
    Close overlay

Close overlay
    Click element  css=.overlay-ajax .close
