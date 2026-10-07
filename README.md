# Personal Website

Open `index.html` in your browser to preview. The root HTML pages are already built and ready for the existing GitHub Pages repository.

## Where to edit

| File or folder | Purpose |
| --- | --- |
| `content/profile.json` | Name, position, Cambridge affiliations, focus, obfuscated contact email, homepage artwork, portrait and CV path |
| `content/publications.json` | All papers; add a record once and assign topics |
| `content/talks.json` | All talks, slides and related links; optionally generate homepage news |
| `content/news.json` | News dates, descriptive headlines and linked details; newest first |
| `content/navigation.json` | Research areas, courses, software and research-card image paths |
| `content/pages.json` | Page names and their editable source files |
| `content/pages/` | Readable HTML source for each research summary, biography, course and software page |
| `templates/base.html` | Shared page shell, navigation placement, footer and metadata |
| `assets/css/` and `assets/js/` | Design and interactive behavior |
| `assets/images/` | Profile portrait, homepage artwork, topic illustrations, publication thumbnails and research figures |
| `assets/media/research/` | Research videos, grouped by topic |
| `downloads/` | CV, presentations, posters, preprints, teaching material and software archives |
| `scripts/build.py` | Generates all root HTML pages and the sitemap; Python 3, no dependencies |
| `scripts/check.py` | Checks generated page links and publication records |

The generated root HTML files retain their original names so existing page URLs continue to work. Resource folders now use consistent lowercase names with hyphens. Edit the source files above, rather than generated HTML pages.

## Rebuild after an edit

```sh
python3 scripts/build.py
```

Run `python3 scripts/check.py` to check generated page links and publication records. The build script also validates talk IDs, required fields and dates. Then open `index.html` and check the affected pages. Commit/upload the source files and generated pages into the root of your `Maurice-Filo.github.io` repository when ready. No npm or application server is needed.

## Add a publication once

Add an object to `content/publications.json`:

```json
{
  "id": "paper-my-new-work",
  "title": "Your paper title",
  "url": "https://doi.org/your-doi",
  "authors": "Maurice Filo and collaborators",
  "venue": "Journal name, 2027",
  "year": 2027,
  "topics": ["Biomolecular Controllers", "Machine Learning"],
  "featured": true,
  "image": "assets/images/publications/my-new-paper.png",
  "links": [
    {"label": "Poster", "url": "downloads/posters/my-new-paper.pdf"}
  ]
}
```

Use a unique `id` and exact topic names from `navigation.json`. Rebuild: the paper appears in Publications and every tagged research page, plus the homepage when it is among the four newest featured papers. Within one year, array order controls ordering. Use `"image": ""` for papers without an image.

Existing placements within research summaries use `<div data-paper="paper-1"></div>`, which renders that central record. You do not need to insert this manually for new papers: tagged papers are appended under related publications.

## Add a talk once

Add a new object to the array in `content/talks.json`, separated from the previous object by a comma:

```json
{
  "id": "talk-my-new-seminar-2026",
  "title": "Your new talk title",
  "date": "2026-10-20",
  "venue": "Control Group Seminar, University of Cambridge",
  "venue_url": "https://www-control.eng.cam.ac.uk/",
  "location": "Cambridge, UK",
  "slides_url": "downloads/presentations/my-new-seminar.pdf",
  "paper_url": "",
  "video_url": "",
  "image": "assets/images/publications/my-paper.png",
  "group": "Conference & Invited Talks",
  "show_in_news": true
}
```

Place your slides at the exact referenced path and rebuild. The talk appears on Talks, and `show_in_news: true` adds its announcement to the homepage news automatically. You do not also enter the talk in `content/news.json`.

Optional fields can be omitted or left empty. Use `"show_in_news": false` to list a talk without a homepage announcement.

### Talk fields

| Field | Meaning |
| --- | --- |
| `id` | Required unique ID, using letters, numbers, hyphens, or underscores; also creates a direct anchor such as `Talks.html#talk-my-new-seminar-2026` |
| `title` | Required talk title |
| `date` | Required date: `YYYY-MM-DD`, `YYYY-MM`, or `YYYY`; incomplete historical dates are displayed with their original precision |
| `venue` | Required venue or event description |
| `venue_url` | Optional event or institution link |
| `location` | Optional city/country |
| `slides_url` | Optional slides link; the title also links to these slides |
| `paper_url` | Optional paper link |
| `video_url` | Optional video link |
| `image` | Optional thumbnail; use an empty string or omit it if not needed |
| `group` | Optional section heading; defaults to `Conference & Invited Talks` |
| `show_in_news` | Optional boolean, defaults to false; true generates homepage news |
| `news_headline` | Optional custom announcement headline; otherwise uses `Talk: <title>` |
| `notes_html` | Optional extra details in HTML, such as awards or a defense committee |
| `links` | Optional additional links, e.g. `[{"label": "Dissertation", "url": "https://…"}]` |

Talks are sorted newest first within each section. Sections follow the order in which they first occur in the sorted talks; talks on the same date follow array order. News combines manual entries and opted-in talks, sorts them by date, and retains the newest-five/earlier-updates layout. For sorting only, historical month-only/year-only dates use their first day; the displayed date does not invent a day.

Existing manual announcements for an opted-in talk are suppressed when they match its slides link, or its event link in the same month. You can also put `"talk_id": "your-talk-id"` on a manual news entry to associate it explicitly. Opting out leaves existing manual news untouched.

Keep valid JSON: double quotes, commas between objects, no trailing comma, and lowercase `true`/`false` without quotes.

The 13 existing talks were converted to JSON with their resource links and additional details preserved. `content/pages/talks.html` is no longer read; you may keep it as a backup or delete it. Its entry in `content/pages.json` is ignored, and Talks remains in the sitemap even without that entry. Talks is also available directly in the main navigation.

## Add news

Prepend a record in `content/news.json`:

```json
{
  "date": "1 Jan 2027",
  "datetime": "2027-01-01",
  "headline": "A clear, descriptive headline",
  "html": "Details with an optional <a href=\"downloads/presentations/new-talk.pdf\">link</a>."
}
```

Manual news and talks with `show_in_news: true` are combined and sorted by date. The newest five are shown immediately; earlier news appears under “Earlier updates.” For a talk announcement, edit only `content/talks.json`; use `content/news.json` for other updates. `datetime` is optional for older entries without a precise day. Use valid JSON, with double quotes and no trailing commas.

## Add a research area, course, or software tool

1. Add its name to `topics`, `courses`, or `software` in `content/navigation.json`.
2. Create its readable HTML source in `content/pages/`.
3. Register the page in `content/pages.json`:

   ```json
   "New Course": {"file": "pages/new-course.html", "title": "New Course"}
   ```

4. Add its resources to the matching `downloads/` or `assets/` folder, then rebuild.

Overview cards, the detail page, and its sitemap entry are generated automatically. For a research-card illustration, add the page name and image path under `topic_images` in navigation.json. Talks use `content/talks.json`; their page is generated separately. Adding a talk does not create a publication record.

Page sources support profile placeholders such as `{{role}}`, `{{institution}}`, and `{{email_display}}`. These take their values from `profile.json`, keeping your current affiliations consistent on the homepage, Contact, About and footer.

## Cambridge updates and email

Your current position is Assistant Professor in the Department of Engineering, University of Cambridge, Information Engineering Division, Control Group. The news records your appointment on 1 September 2026 and your Fellowship of Gonville and Caius College on 5 October 2026, with official institutional links. Historical ETH appointments and teaching remain in the biography and earlier news.

The Cambridge address appears as `mf916 [at] cam [dot] ac [dot] uk`, without a mailto link or complete plain-text address. This discourages simple address scrapers; it cannot prevent every bot. The old ETH email is removed from the delivered website.

## Artwork

The homepage banner is `assets/images/site/research-hero.webp`. Its palette is teal, forest green, ivory and warm amber. The revised image emphasizes control-system feedback loops, phase-space trajectories and AI neural-network connections, with synthetic biology as a smaller supporting motif. It is conceptual artwork, not a scientific diagram.

The supplied new portrait is at `assets/images/profile/portrait.jpg`. Its background was changed to the website ivory (`#f8f9f5`), preserving the person, clothes, expression and framing.

Both raster edits used the built-in image generation tool. Edit prompts:

- Portrait: “Replace ONLY the light blue background with a uniform soft ivory matching website background hex #f8f9f5. Preserve the person's identity, facial features, expression, hair, skin, jacket, shirt, pose, lighting and crop exactly. Natural meticulous hair edges; no retouching of the person, no text, no vignette. Output same portrait aspect ratio.”
- Banner: “Keep the elegant teal/forest green/ivory palette, warm amber accents, refined scientific editorial style, soft depth, panoramic composition. Shift subject balance so control systems and AI dominate: make graceful feedback loops with clear directional arrows, connected control blocks and phase-space trajectories prominent across left and center; enlarge the neural network lattice across the right half. Reduce synthetic biology to a small subtle DNA/molecular motif along the far left, remove the dominant giant cellular spheres. Harmonize all elements into a beautiful coherent image. No text, labels, people or logos. Conceptual science art, not a precise scientific diagram.”

Five simple SVG research-card illustrations live in `assets/images/topics/`. The biomolecular controllers illustration now combines chemical species and reaction arrows with a genetic circuit backbone, promoter, coding regions and terminator. These are decorative concepts rather than a claim about a particular biochemical mechanism. The other cards show a cochlear spiral, neural network, uncertain trajectories and optimal path.

## Validation

Checks cover the build, internal HTML links, available image paths, ETH email removal, both appointment entries and their links, five illustrated research cards, and propagation of a new publication from one source record. Original research summaries, teaching material, talks, theses and publication records are retained. Downloaded resource contents were not verified during the original build. Publication search, intersecting year/topic filters, empty results, and mobile-menu state passed scripted interaction checks. The talks update was checked for all 13 migrated talks and every original link, rendering without the old HTML source, the active Talks navigation item, adding a new talk to both Talks and homepage news, duplicate-announcement suppression, opting out of news, empty lists, and errors for invalid dates or duplicate IDs. Talk cards reuse the existing publication-card styling, including custom thumbnail-size CSS. No automated browser visual checks were performed; review desktop and mobile appearance locally before publishing.
