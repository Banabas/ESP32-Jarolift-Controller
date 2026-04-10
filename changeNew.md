# v1.10.3-beta

## what's new

This is a bugfix release for the Timer WebUI.

### Timer – Overview table now always populated correctly

The timer overview table (bottom of the Timer tab) was not filled after page load.
Two issues were fixed:

1. A JavaScript `ReferenceError` (`astroKeys` was used instead of the correct global `astroKeyNames`) caused the overview to silently fail whenever a timer using sunrise/sunset mode was active.
2. `buildTimerOverview()` is now called at the end of `initTimerUI()`, which runs after the server data has been received via WebSocket. Previously it ran on a fixed 3-second timeout which was independent of data availability.

### Timer – Weekend override input now opens correctly

The "Weekend override" section (Sa+So) inside each timer event block did not expand when the checkbox was ticked.
The toggle function was looking for an element ID with a double `_we` suffix (`_we_we_block`) instead of the correct ID (`_we_block`).

## changelog

- [FIX] Timer overview: `astroKeys` renamed to `astroKeyNames` – fixes ReferenceError for astro-mode timers #timer
- [FIX] Timer overview: `buildTimerOverview()` now called after server data load instead of fixed timeout
- [FIX] Timer weekend override: corrected element ID lookup in `toggleWeekend()` (`_we_block` instead of `_we_we_block`)
