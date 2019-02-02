Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start


2.5.10 (2017-12-11)
-------------------

Bug fixes:

- Drop dependency on plone.app.form
  [MatthewWilkes]


2.5.9 (2017-03-09)
------------------

Bug fixes:

- Fix import location for Products.ATContentTypes.interfaces.
  [thet]


2.5.8 (2016-08-10)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


2.5.7 (2016-02-12)
------------------

Fixes:

- Fixed to work with Plone 5.  [vangheem]

- Updated to work with new plone.batching ``pagination`` selector as
  well as with old one.  [thet]


2.5.6 (2015-11-27)
------------------

Fixes:

- Do not fail if a level of the path we are adding the object using
  the ReferenceBrowser widget is not accessible by the current user.
  [gbastien]


2.5.5 (2015-10-27)
------------------

Fixes:

- Show elements that the reader has no access to as "Undisclosed" instead of
  throwing Unauthorized.
  [pbauer]


2.5.4 (2015-09-27)
------------------

- Follow README/CHANGES best practice.
  [tisto]

- saner check for isNotSelf(), which was throwing KeyError
  [alecpm, tkimnguyen]


2.5.3 (2015-04-15)
------------------

- #23 added parameter 'use_wildcard_search' to widget, True by default
  [gbastien]

- Replaced ``jq`` usage with ``$``
  [keul]

- Fixing reference sorting issue due to global function refactoring done
  on recent versions
  [keul]
- Add labels for images in the popup widget.
  [mitakas]

- #16 fix browsing for widgets in case field has set ``allowed_types``

  (Warning: changed return value of view/getResult from
  `[`brain1, brain2,..]``  to ``[dict(item=brain1,browsable=True,
  referenceable=False),...]`` in case you customized popup.pt)
  [fRiSi]


2.5.2 (2014-09-11)
------------------

- Fix the "Clear Reference" button, which was not working due to the
  refbrowser_removeReference function hidden in a anonymous function.
  [thet]

- fixed allowed_types
  [agitator]


2.5.1 (2014-07-10)
------------------

- Fix JavaScript for compatibility with jQuery 1.9 by using jQuery's ``on``,
  attached to document, instead of ``live``.
  [thet]

- Use foward compatable test for checked items with jQuery >=1.7
  fixes https://dev.plone.org/ticket/13853
  [arterrey]

- Fix non-multi reference selection when the referenced object
  no longer exists.
  [mattss]


2.5.0 (2014-02-23)
------------------

- Do not use portal_interface tool but @@plone_interface_info (PLIP #13770).
  [ale-rt]

- Filter out references that are None.  This may happen when the
  reference_catalog has links from a source to a no longer existing
  target.
  [maurits]


2.4.19 (2013-08-13)
-------------------

- Modified pagination links selector to use only ".listingBar" instead of
  "div.listingBar". The batchnavigation.pt template can be customized in a
  theme and use a different structure, "ul.listingBar" for example.
  [vincentfretin]

- If we have a sort_on parameter in base_query,
  use it instead of getObjPositionInParent to display folder content.
  [thomasdesvenain]


2.4.18 (2013-05-23)
-------------------

- Added two widget properties that allow to add help messages on popup,
  in two slots (top and bottom).
  [thomasdesvenain]

- Added css ids in popup.
  [thomasdesvenain]

- Wrap jQuery functions for better compatibility.
  [esteele]


2.4.17 (2013-03-05)
-------------------

- 2.4.15 broke non-multi reference selection. Added code to discriminate
  between multi and single widget id. Fixes http://dev.plone.org/ticket/13402
  [smcmahon]


2.4.16 (2013-01-13)
-------------------

- Add an option of searching for related items by path.
  [plamut]


2.4.15 (2012-12-14)
-------------------

- Make new added references sortable with already existing ones
  while editing a content.  Fixes http://dev.plone.org/plone/ticket/13271
  [gbastien]

- Use HTML5 placeholder attribute on search box. Replaces deprecated
  inputLabel class.
  [danjacka]


2.4.14.1 (2012-11-07)
---------------------

- Fixed typo
  [tomgross]


2.4.14 (2012-10-18)
-------------------

- Use normalizeString to create class names for an item's portal type
  and review state. Fixes http://dev.plone.org/plone/ticket/11400.
  [danjacka]

- don't let search fail on broken catalog
  [tomgross]


2.4.13 (2012-10-11)
-------------------

- Restored a "*view*" link on linkable items (as with Plone 3):
  It will open a preview of the element in a popup window.
  [keul]

- Fixed referenced elements sort order on widget view.
  [gbastien]

- Take search_index into account while used in popup search form.
  [gbastien]


2.4.12 (2012-08-11)
-------------------

- Show item icons in popup.
  [thomasdesvenain]

- Limit the width of checkboxes column in popup.
  [thomasdesvenain]

2.4.11 (2012-04-09)
-------------------

- Fixed breadcrumbs internationalization in popup.
  [thomasdesvenain]


2.4.10 (2012-02-09)
-------------------

- We can restrict browsable types, with browsable_types parameter on widget.
  [thomasdesvenain]


2.4.9 (2011-12-08)
------------------

- updated query to take allowed_types into account
  [hpeteragitator]
- fixed form submission issue in ie #11984
  [tom_gross]

2.4.8 (2011-11-23)
------------------

- Completed MANIFEST.in
  [tom_gross]

2.4.7 (2011-11-23)
------------------

- Added MANIFEST.in
  [tom_gross]

2.4.6 (2011-11-23)
------------------

- Fixed release
  [tom_gross]


2.4.5 (2011-11-23)
------------------

- Fixed tests for plone.uuid >= 1.0.2
  [tom_gross]


2.4.4 (2011-08-19)
------------------

- Fix: text searches should search outside navigation root
  [gotcha]

2.4.3 (2011-07-04)
------------------

- Use label tags for selectable items.
  [esteele]

- Fix: text search searches from navigation root.
  [thomasdesvenain]

- moved checkPermission from widget template to helper
  [tom_gross]

- Fix referencebrowser.js error when using allow_sorting = 1
  [toutpt]

2.4.2 (2011-06-02)
------------------

- Fix: overlay is not closed at item selection when field is multivalued.
  [thomasdesvenain]

- Fix undefined variable checkPermission
  [kiorky]

- Fix error in refbrowser_moveReferenceDown and refbrowser_moveReferenceUp
  which caused page reloads when a referenced item was moved twice.
  Refs http://dev.plone.org/plone/ticket/11859
  [cewing]

- Fix errors in sorting scripts which caused failure to detect items at head
  or tail of list of referenced items. Refs
  http://dev.plone.org/plone/ticket/11859
  [cewing]


2.4.1 (2011-05-12)
------------------

- Add js hack to move overlay div to be a direct child of body to avoid
  IE7 z-index bug. Fixes http://dev.plone.org/plone/ticket/11465.
  [smcmahon]

2.4 (2011-04-11)
----------------

- Fix regression in UID lookup in cases where plone.uuid is present, but not
  used for Archetypes content (such as with plone.app.discussion 1.0 on Plone
  4.0)
  [davisagli]

2.3 (2011-04-01)
----------------

- Fixed: widget did not work when search was disallowed.
  [thomasdesvenain]

2.2 (2011-02-25)
----------------

- Fixed `getStartupDirectory` method if a `startup_directory_method` was
  defined, which cannot be traversed to.
  [hannosch]

- check the references in the overlay that are checked in the widget
  when the overlay is constructed or refreshed.
  [csenger]

- Don't disable checkboxes in overlay when an item is selected.
  Remove the item from the value list when it is unchecked in
  the value list. fixes http://dev.plone.org/plone/ticket/10786
  [csenger]

2.1 (2011-01-03)
----------------

- Don't issue deprecation-warnings on Zope 2.13
  [tom_gross]

- Fixed title display for images with preview
  http://dev.plone.org/plone/ticket/11290
  [tom_gross]

- Fixed: do not return results that are outside of startup directory
  if browse is restricted to it.
  [thomasdesvenain]

- Qualify input tag id to avoid name-clashing. Fixes
  http://dev.plone.org/plone/ticket/11325.
  [malthe]

- Made sure to always quote ``at_url`` when forwarding it in the templates.
  [deo]

- Use URL quoting of ``at_url`` everywhere and quote in Python code not in
  templates. Fixes http://dev.plone.org/plone/ticket/11297
  [tom_gross]

- Cleaned breadcrumb code Fixes http://dev.plone.org/plone/ticket/11289
  [tom_gross]

2.0 (2010-09-06)
----------------

- Fixed i18n of "You are here:".
  [vincentfretin]

- Set a minimum version for jquerytools, to avoid this problem #10939
  [do3cc]

- Encode search-URL. Fixes http://dev.plone.org/plone/ticket/10942
  [tom_gross]

2.0rc2 (2010-07-29)
-------------------

- Make sure the popup can be closed by the same ways as other popups in Plone
  4. Fixes http://dev.plone.org/plone/ticket/10773
  [davisagli]

- Fixed bug: pop-up didn't render id of file with empty title because of
  improper use of TALES Path expression. Now uses browser method instead.
  [kleist]

2.0rc1 (2010-07-12)
-------------------

- Fixed link rebinding of pagination links (thanks Mustapha Benali!)
  [tom_gross]

2.0b4 (2010-06-02)
------------------

- Fixed display of title (introduced in 2.0b3)

2.0b3 (2010-06-02)
------------------

- Use getOverlay() instead of the deprecated getContent()
  Closes http://dev.plone.org/plone/ticket/10548
  [esteele]

- Use content icons from sprite
  Closes http://dev.plone.org/plone/ticket/10543
  [tom_gross]

2.0b2 (2010-04-23)
------------------

- Adding missing return falses to prevent page reloads on reordering
  [cah190,esteele]

- Mark already related objects visually in referencebrowser
  [tom_gross]

- Only show sorting arrows on adding, if field is really sortable
  [tom_gross]

- use Python doctest instead of zope.testing.doctest
  [tom_gross]

2.0b1 (2010-04-08)
------------------

- Updated package description
  [tom_gross]

- Merged javascript files to one, which is included only with the widget
  [tom_gross]
