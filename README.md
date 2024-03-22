# Phase Switcher
Easily manage the test phases!
![screenshot1](https://github.com/kakoytochelik/PhaseSwitcher/assets/48015759/e3a18d42-a7d5-4401-a8ab-9f0b26ef99b0)


## Features

### Switch any phase on or off before building test scenarios

Simply check or uncheck the desired tests at each build phase. Or you can switch all scenarios at once!
<br>
When you are ready, simply click Run and the tests will switch according to the checkboxes you have selected.
<br>
<br>
If you are confused and don't remember which tests should be on or off - just click:
- the Refresh button: it will reset checkboxes to their current state (before clicking the Run button)
- or the Default values button: it will reset checkboxes to their default values, as they should be in the build.


### Switch between projects
In the additional menu you can specify the paths to the various projects and then select the desired project from the drop-down list. All checkbox states are saved separately for each project.
<br>
Project-specific checkboxes are automatically activated or deactivated depending on whether a particular test is available.


### UUID Generator
Each test requires a unique UUID, so if you create a new test, you can generate a new UUID directly from the Phase Switcher user interface. It will be automatically copied to the clipboard, but if you want, you can copy it again manually or generate a new one.

### Easy to maintain!
If there will be a new region or a new test, all you need to do is:
- For regions:
  - Just add the new country to the `regionComboBox` in the `setupWidgets` method of MainWindow
  - and in the `createLabels` method of the `PathsWindow` class
- For new phases:
  - add a new phase to `tab_info` in the `createTabs` method
  - create a new `tab{N}UI` method that will define what is inside this phase
- For tests:
  - add a new path to `data.json`
  - then simply add a new `"label"` element with the name of the test to any `tab{N}UI` method

