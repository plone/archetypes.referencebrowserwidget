*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

Test Setup  Test Setup

*** Test cases ***

Test monovalued field
    Add single reference
    Textfield Value Should Be  css=#ref_browser_singleRef_label  First Page
    Click element  name=form.button.save
    Click link  Edit
    Textfield Value Should Be  css=#ref_browser_singleRef_label  First Page

Test monovalued field delete
    Add single reference
    Textfield Value Should Be  css=#ref_browser_singleRef_label  First Page
    Click element  css=#archetypes-fieldname-singleRef .atrb_remove
    Textfield Value Should Be  css=#ref_browser_singleRef_label  ${EMPTY}
    Click element  name=form.button.save
    Click link  Edit
    Textfield Value Should Be  css=#ref_browser_singleRef_label  No reference set. Click the add button to select.

Move reference down while adding (before saving)
    Add two related items
    Click element  css=#ref-relatedItems-0 .atrb_move_down
    Click element  name=form.button.save
    ${first-related}=  Get text  css=#relatedItemBox dd:nth-child(2) a
    Should be equal  ${first-related}  Second Page
    ${second-related}=  Get text  css=#relatedItemBox dd:nth-child(3) a
    Should be equal  ${second-related}  First Page

Move reference down after saving
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
    Add two related items
    Click element  css=#ref-relatedItems-1 .atrb_move_up
    Click element  name=form.button.save
    ${first-related}=  Get text  css=#relatedItemBox dd:nth-child(2) a
    Should be equal  ${first-related}  Second Page
    ${second-related}=  Get text  css=#relatedItemBox dd:nth-child(3) a
    Should be equal  ${second-related}  First Page

Move reference up after saving
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

Test Setup
    Create content  type=Document  id=first  title=First Page
    Create content  type=Document  id=second  title=Second Page
    Create content  type=Document  id=third  title=Third Page
    Create content  type=RefBrowserDemo  id=atrb  title=ATRB Demo

Add two related items
    Go to  ${PLONE_URL}/third
    Click link  Edit
    Click link  Categorization
    Click element  css=input.searchButton.addreference
    Click element  css=tr:nth-child(1) input.insertreference
    Click element  css=tr:nth-child(2) input.insertreference
    Close overlay

Add single reference
    Go to  ${PLONE_URL}/atrb
    Click link  Edit
    Click element  css=input.searchButton.addreference
    Click element  css=tr:nth-child(1) input.insertreference
    Close overlay

Close overlay
    Click element  css=.overlay-ajax .close
