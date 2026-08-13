# SOAPaDay App — Feature Analysis

> **Source:** Reverse-engineered from web bundle at `https://app.soapaday.com/`  
> **Date:** 2026-06-29  
> **Tech Stack:** Expo (React Native Web), GraphQL (Apollo), Supabase/Firebase auth, myChelper backend infrastructure

---

## 📱 App Overview

SOAPaDay is a **daily SOAP Bible study app** built with Expo, supporting both mobile (iOS/Android) and web. The app uses a tab-based navigation structure with deep linking support.

**Fonts:** Inter (UI), Merriweather (reading), Playfair Display (headings/accents)

---

## 🧭 Navigation Structure

### Tab Screens (`/(tabs)`)
The app uses a bottom-tab navigation pattern with these main sections:

| Tab | Screen | Purpose |
|-----|--------|---------|
| 🏠 **Home** | `BibleHomeScreen` | Daily verse, reading plans, quick access |
| 📖 **Bible** | `BibleReaderScreen` | Full Bible reader with translations |
| ✍️ **Journal** | `SoapEntryDetailScreen` | SOAP journaling (Scripture, Observation, Application, Prayer) |
| 👤 **Profile** | `ProfileScreen` | User stats, settings, progress |

### Stack Screens (Modal/Detail Flows)
- `LoginEmailScreen` — Email/password auth
- `VerifyCodeScreen` — Email verification
- `FilterScreen` — Bible search/book filters
- `SoapMethodGuideScreen` — SOAP method tutorial
- `ReadingPlansScreen` — Browse available plans
- `ReadingPlanDetailScreen` — Plan overview & enrollment
- `JourneyReaderScreen` — Guided reading experience

### Other Pages
- `PrayPage` — Dedicated prayer interface
- `BibleTranslationsPage` / `AvailableBibleTranslationsPage` — Translation selector
- `LanguagesPage` — App language settings
- `ConnectInboxPage` — Messages/inbox

---

## ✍️ Core Feature: SOAP Journaling

The heart of the app. Users create daily SOAP entries:

### SOAP Structure
1. **S**cripture — Selected Bible passage
2. **O**bservation — What do you notice?
3. **A**pplication — How does this apply to your life?
4. **P**rayer — Written prayer response

### Entry Management
- ✅ **Create** SOAP entry (`CreateSoapEntry` mutation)
- ✏️ **Update** existing entry (`UpdateSoapEntry` mutation)
- 🗑️ **Delete** entry (`DeleteSoapEntry` mutation)
- 📖 **View** entries by chapter (`MySoapEntriesForChapter` query)
- 📚 **List** all entries (`MySoapEntries` query)

---

## 📖 Bible Features

### Bible Reader
- Full Bible text with multiple translations
- Book/chapter navigation
- Verse-level granularity
- Search Bible verses (`SearchBibleVerses` query)

### Translations
- Multiple Bible versions available
- Language selection (`BibleLanguage`, `AvailableBibleLanguages`)
- Translation comparison

### Verse of the Day
- Daily curated verse (`VerseOfTheDay` query)
- Shareable format

---

## 📚 Reading Plans

### Plan Types
- Public reading plans (`SoapadayReadingPlans` query)
- Church-specific plans (`ChurchByUrl`, `HandleUserChurchProfile`)
- Thematic plans (likely: 30-day, 90-day, topical, etc.)

### Plan Management
- **Enroll** in a plan (`StartReadingPlan` mutation)
- **Pause** a plan (`PauseReadingPlan` mutation)
- **Resume** a plan (`ResumeReadingPlan` mutation)
- **Abandon** a plan (`AbandonReadingPlan` mutation)
- Track progress (`MyReadingPlanProgress` query)
- Day-by-day readings (`PublicReadingPlanDayReadings`, `PublicReadingPlanDayReadingsBatch`)
- Ensure day is ready (`EnsureReadingPlanDay` mutation)

### Progress Tracking
- Enrollment status (`MyReadingPlanEnrollments`, `MyReadingPlanEnrollment`)
- Completion tracking
- Batch reading support for efficiency

---

## 🔥 Streaks & Gamification

- **Daily streaks** (`MyStreak` query)
- Streak counting and display
- Progress visualization
- Badge/achievement system (references found in bundle)

---

## 👤 User Profile & Settings

### Authentication
- Email/password login (`LoginEmailScreen`)
- Email verification (`VerifyEmailWithCode`, `RegisterUserWithCode`)
- Account deletion (`DeleteSoapadayAccount` mutation)

### User Settings (`MySettings`, `UpsertMySettings`)
- Theme preferences (light/dark mode)
- Font selection
- Notification preferences
- Reading preferences

### Profile Features
- User profile management (`UpdateChurchPerson`)
- Church affiliation (`ChurchByUrl`, `HandleUserChurchProfile`)
- Reading stats and progress

---

## 🎨 Customization & Theming

### Theme System
- **Light/Dark mode** support
- Custom color schemes
- Typography options (Inter, Merriweather, Playfair Display)
- `useThemedStyles`, `useAppTheme`, `useTheme` hooks

### Reading Experience
- Font size adjustment
- Line spacing
- Margin/padding controls
- Customizable reading environment

---

## 🔔 Notifications & Reminders

- Push notification support
- Daily reading reminders
- Streak maintenance alerts
- Schedule-based notifications
- Badge counts on app icon

---

## 💬 Social & Community Features

### Church Connection
- Church profile linking
- Church-specific reading plans
- Pastor/leader content distribution

### Sharing
- Share verses (native share sheet)
- Share SOAP entries as **4 PNG images** (one per SOAP section)
- Share reading progress
- Export functionality

### Testimonies
- Submit user testimonies (`SubmitUserTestimony` mutation)
- Approved testimonies feed (`ApprovedTestimonies` query)
- Community encouragement

### Messaging
- Inbox system (`PaginatedInbox` query, `ConnectInboxPage`)
- Direct messaging capability

---

## 📤 Share/Export Feature — Detailed

When sharing a SOAP entry, the app generates **4 PNG images** (1080×1350px each) — one for each SOAP section. These are designed as Instagram-friendly story/carousel posts.

### The 4 Share Images

| Slide | Content | Header | Body Style |
|-------|---------|--------|------------|
| **1. Scripture (S)** | The Bible verse text | "S" letter mark + "SCRIPTURE" label | Large scripture text (font: bodyReading, ~42px), reference in primary color, translation name below |
| **2. Observation (O)** | User's observation notes | "O" letter mark + "OBSERVATION" label | Body text (font: bodyUi, ~42px), italic placeholder if empty |
| **3. Application (A)** | User's application notes | "A" letter mark + "APPLICATION" label | Body text (font: bodyUi, ~42px), italic placeholder if empty |
| **4. Prayer (P)** | User's prayer | "P" letter mark + "PRAYER" label | Body text (font: bodyUi, ~42px), italic placeholder if empty. May include "Continue in SOAPaDay" banner |

### Visual Design

- **Canvas:** 1080×1350px (4:5 aspect ratio, Instagram-optimized)
- **Background:** App's current theme color (light/dark mode aware)
- **Padding:** 72px horizontal, 72px top, 96px bottom
- **Header row:** Letter mark (S/O/A/P) in primary color + section label in uppercase
- **Watermark (bottom):** "Journaled on SOAPaDay (Free & Ad-Free Bible Journal)" + "SOAPaDay.com"
- **Text handling:** Smart overflow with fade gradient, RTL support for Arabic
- **Empty states:** Italic "No response recorded" text instead of blank

### Technical Implementation
- Uses `html-to-image` library (`toPng`) for capture
- Hidden off-screen DOM elements rendered for capture
- Carousel preview modal with dot indicators
- Supports both light and dark themes
- Arabic localization with RTL layout support

---

## 🔍 Search & Discovery

- Bible verse search (`SearchBibleVerses`)
- Reading plan discovery
- Content filtering
- Sort options

---

## 💾 Data & Sync

### Offline Support
- Local caching
- Offline reading capability
- Sync when reconnected

### Data Export/Import
- Export journal entries
- Import functionality
- Print support
- PDF generation (limited)

---

## 🛠️ Technical Details

### API Layer
- **GraphQL** endpoint at `/graphql`
- Apollo Client for state management
- Queries and mutations for all CRUD operations

### Backend Infrastructure
- Connected to `mychelper.com` ecosystem
- `graphql.mychelper.com` — GraphQL API
- `images.mychelper.com` — Image CDN
- `giving.mychelper.com` — Giving/donations integration

### Auth
- Supabase/Firebase references found
- JWT-based session management
- Email verification flow

### State Management
- React hooks (useState, useEffect, useContext)
- Apollo Client cache
- Local persistence

---

## 🚀 Onboarding & UX

- Onboarding flow for new users
- SOAP method guide/tutorial
- Contextual help
- Smooth animations (spring, fade, slide transitions)
- Gesture support (swipe, scroll, tap)
- Loading states and skeleton screens
- Error handling with retry

---

## 🔗 External Integrations

- **App Store** — iOS download
- **Google Play** — Android download
- **BibleHub** — External Bible reference
- **Giving** — Donation processing via myChelper

---

## 📋 Feature Summary for Marketing

### Key Selling Points
1. **Simple SOAP framework** — Easy to start, hard to quit
2. **Multiple Bible translations** — Read in your preferred version
3. **Guided reading plans** — Structured spiritual growth
4. **Daily streaks** — Build consistent habits
5. **Beautiful journaling** — Aesthetic, distraction-free writing
6. **Church-connected** — Align with your community
7. **Cross-platform** — Mobile + web sync
8. **Offline capable** — Read anywhere
9. **Shareable** — Spread encouragement
10. **Customizable** — Make it yours with themes & fonts

---

*This document will be updated as the app evolves.*
