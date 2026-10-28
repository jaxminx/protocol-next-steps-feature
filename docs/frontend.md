# Frontend sketch

Clickable prototype (built on Figma):
<https://www.figma.com/proto/av8xtSKE8pQNb8KMB3bam3/Frontend-Tests-from-your-results?node-id=12-22&starting-point-node-id=12%3A22&scaling=scale-down>

Board with notes on design decision:
<https://www.figma.com/design/av8xtSKE8pQNb8KMB3bam3/Frontend-Tests-from-your-results>

---

## How I'd build the app

**React Native with Expo.** One TypeScript codebase for iOS and Android, so a small in-house team can own both and ship ideas quickly. Fully native would mean two codebases and two sets of skills, and Flutter adds a second language.

It also covers what's next on my list. Smart reminders need notifications that reliably arrive, and wearables need Apple Health. A web app installed from the browser can't read Apple Health, and on iPhone it [only gets notifications once it's been added to the home screen](https://pushpad.xyz/blog/ios-special-requirements-for-web-push-notifications), which most people never do.

It's a common choice for health apps like [Superpower](https://jobs.ashbyhq.com/superpower/6ecd0142-eb4e-404d-be5b-31c7cf10cf4d), [Function Health](https://www.builtinnyc.com/job/sr-mobile-engineer/8873662) and [Doctolib](https://jobs.accel.com/companies/doctolib-2/jobs/61652111-staff-mobile-engineer-react-native-x-f-m), and Expo is what the [React Native team recommends](https://reactnative.dev/blog/2024/06/25/use-a-framework-to-build-react-native-apps) for new apps. It handles builds and releases, supports Face ID and secure storage for health data, and lets small fixes go out the same day without waiting for App Store review.

---

## What the sketch needs that the API doesn't give yet

I didn't add these to keep to the time limit, but the screens need them:

1. **Each marker's range.** The charts and "Optimal is 2.6 or below" need the thresholds, which only live in `config/bands.yaml` right now. I'd send a `range` with each flag, plus a `direction`, since higher is better for vitamin D but worse for LDL. Keeping them on the server means doctors can change them without an app update. A bar against the range is also [easier to read](https://www.jmir.org/2024/1/e53993) than a number on its own.
2. **A list of reports.** The timeline and "your latest results are from March" need each report's date and type. Flags only carry the report ID.
3. **Booking.** Screens 04 and 05 need open slots and something like `POST /v1/me/bookings`. The retest also needs a "booked" state, so the app stops suggesting it.
4. **A cart endpoint.** Each suggestion has an `add_to_cart` action, but nothing on the server receives it yet.
