# v1.20.0

## what's new

This is a major feature release.

> [!TIP]
> Maybe it is necessary to clean your browser cache after the update, to be sure that everything works well!

### Time-based position control

Roller shutters can now be moved to a specific position (0–100 %) directly via the WebUI slider or via MQTT.
Position tracking is purely time-based: after a one-time calibration the firmware calculates how long the motor has to run to reach the desired position and then sends an RF STOP at the right moment.

**Calibration** is done in two phases (DOWN then UP) from the service page.  
Both travel times (DOWN and UP) are stored independently so that asymmetric motors are handled correctly.

### Extended timer system

The timer has been completely redesigned:

- **Per-channel timers** – each of the 16 channels can have its own independent UP/DOWN schedule
- **Per-group timers** – each of the 6 groups can also have an independent UP/DOWN schedule
- **Weekend override** – Saturday/Sunday can use a different time or astro event than the weekday schedule
- **Astro modes** – choose between Real, Civil, Nautical, Astronomical twilight or a custom Horizon angle for sunrise/sunset events
- **Min/Max time constraints** – limit astro-based events so they never fire before a minimum or after a maximum clock time

### ESP32-S3 16 MB support

A new build target `esp32s3_16mb` with a matching 16 MB partition table has been added.

## changelog

- [FEATURE] Time-based position control via WebUI slider and MQTT numeric payload (0–100 %)
- [FEATURE] Two-phase calibration (DOWN + UP) with independent travel times per channel
- [FEATURE] Per-channel timer with individual UP/DOWN events and weekday selection
- [FEATURE] Per-group timer with individual UP/DOWN events and weekday selection
- [FEATURE] Weekend override for timer events (Sa+So use separate time/astro settings)
- [FEATURE] Astro modes: Real, Civil, Nautical, Astronomical, Horizon for sunrise/sunset timers
- [FEATURE] Min/Max time constraints for astro-based timer events
- [FEATURE] New build target esp32s3_16mb (16 MB flash with matching partition table)
- [FIX] Timer overview: `astroKeys` renamed to `astroKeyNames` – fixes ReferenceError for astro-mode timers
- [FIX] Timer overview: `buildTimerOverview()` now called after server data load instead of fixed timeout
- [FIX] Timer weekend override: corrected element ID lookup in `toggleWeekend()` (`_we_block` instead of `_we_we_block`)
- [FIX] Browser refresh: timer fields `horizon_value`, `use_min_time`, `use_max_time`, `min_time` and `max_time` now correctly restored after page reload
- [FIX] Service log: channel number in learn/unlearn/endpoint commands now correct
- [FIX] Config load: duplicate `eth.ipaddress` read removed
