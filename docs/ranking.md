# What we build next

**Thesis:** With a seed round targeted for Q1, I prioritised two things I expect investors at this stage to care about most: **revenue growth** and **retention**. Each feature needed to turn results into sales, bring members back, or make leaving harder. Features that don't move those numbers ranked lower.

| Rank | Feature | Why |
| --- | --- | --- |
| 1 | **Tests from your results** | The money feature. Every flagged marker becomes one clear call to action, one tap away. It turns results into follow-up test sales and grows revenue per member with zero acquisition spend. |
| 2 | **AI coach** | 	Members get answers about their own results at 2am and doctors stop fielding routine questions, only stepping in when medical judgement is needed. Also an easy story to tell investors, with [AI taking 61% of global VC in 2025](https://www.oecd.org/en/about/news/announcements/2026/02/ai-firms-capture-61-percent-of-global-venture-capital-in-2025.html). |
| 3 | **Smart reminders (with in-app booking)** | Closes the loop on #1. A nudge at the right moment turns a due retest into a visit on the calendar, instead of a follow-up that happens months late, or never. |
| 4 | **All your tests in one place** | The moat. Once a member's whole health history lives with us, leaving gets expensive, and lifetime value goes up. Ranks slightly lower because screening, genetics, imaging etc. each need their own data pipeline, which is heavy integration for results that come in once or twice a year. |
| 5 | **Wearables** | Good for daily engagement, but members already view this data in the companion app ([Oura users open theirs 3+ times a day](https://www.silicon.co.uk/press-release/oura-helping-millions-of-people-improve-their-health-surpasses-2-5-million-rings-sold)), and sleep and HRV don't clearly change what we recommend. Readings can also be patchy, so prompting earlier checks adds liability with no clear revenue. |
| 6 | **Doctor notes in the app** | Keeps everything in one place and gets health details off WhatsApp, which is a PDPA risk ([MOH already bars public hospital staff from sending sensitive medical information that way](https://www.moh.gov.sg/newsroom/use-of-whatsapp-by-healthcare-institutions-to-communicate-medical-information-and-records-to-patients/)). But it ranks last because the current setup works for now and this doesn't directly move revenue. It's easy to build, so it can be slotted in quickly once it's needed.|

# Why 'Tests from your results' ranked first

**For members.** Most people won't go through 100 biomarkers. They want to know what's off and what to do next, and right now the app doesn't tell them. Alex is a good example. His retest is 42 days overdue and he hasn't booked it. His latest results are from March, and he finished his vitamin D protocol but is still below optimal. He may not even know any of this. One screen could sort this out: a clear button to book the retest, the option to add a couple of tests to the same blood draw, and a suggestion to bring up vitamin D with his doctor.

**For the business.** Of the six, this is the most direct path to revenue. Flags turn into bookings, and since the retest is happening anyway, add-on tests are an easy extra on the same visit. Members who act on their results are also more likely to see them improve, and that's what gets them to renew. Revenue growth and retention are exactly what we'd want to show going into the raise.

**What I'd hold off on**

I wouldn't suggest tests based on uploads from other clinics yet. Same rule as scores: they're shown and marked as under review, but nothing gets suggested from them until the team has checked them.

I also wouldn't let AI pick the tests. Doctors set the rules and the app follows them, at least until there's enough trust and data to change that.

Pricing tricks can wait too. [Incentives do lift uptake of preventive care](https://hms.harvard.edu/news/spoonful-sugar), so promos and bundles are worth testing, and so is working out the cheapest mix of tests once more panels cover several markers. But none of it matters until the basic flow is working.

**What I'd add next**

First, I'd bring protocols into next steps, so it's not only about selling tests. Each flagged marker would show its linked protocol, e.g. LDL next to "30 g of fibre a day". If someone has finished a protocol and the marker is still flagged, the next step is a doctor consult, booked from the same screen as the tests. Alex finished his vitamin D protocol and his vitamin D is still moderate, so for him that's a consult on top of the retest. It's a second thing to sell, and it's the kind of care that makes the membership feel worth renewing.

Second, I'd make the flags smarter. Right now every moderate marker gets the same push. An improving one shouldn't look as urgent as a worsening one, and its test shouldn't be pre-selected, since pushing tests people don't need loses their trust fast. Beyond the trend, ranges should be sex-specific, related markers should be read together (high LDL and high ApoB are one heart-health story, not two flags), and context should count: ferritin can run high from inflammation, so a high ferritin next to a raised hs-CRP doesn't automatically mean an iron test.

Third, I'd be upfront about pending uploads. If a flag is affected by one, the app should say something like "your July result is being checked", and the team should get an alert when a review has waited too long. Alex's has been waiting almost four months.

Last, the app should know when the retest is booked, so it doesn't keep suggesting it.

**How I'd know it worked**

The first thing I'd watch is whether retests happen on time: more booked by the due date, and fewer days overdue on average.

Then conversion: how many flags end in a booked test, how many add-ons get added per visit, and what that adds up to in revenue per member each quarter.

The one that matters most for the raise is retention. I'd compare renewal rates for members who acted on a flag with those who didn't.
