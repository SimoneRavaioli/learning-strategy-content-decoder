# Content Decoder

An internal tool for the Learning Strategy team. It analyzes supplied material through the Impactful Eight and Learning 2.0 reference lenses, then produces a practical strategic readout and downloadable report.

## GitHub Pages

The repository includes a static GitHub Pages version. Enable Pages from the repository's **Settings → Pages** screen, select **Deploy from a branch**, then choose **main** and **/(root)**.

The hosted version lets each user choose OpenAI or Anthropic and enter the corresponding API key. The key remains in that browser tab's memory, is sent directly to the selected provider, and is cleared on reload or close; it is never committed to GitHub. Paste text or upload a supported file, then run the diagnostic. Web links work only when the source website permits browser access.

## Shared deployment

The repository includes a `Dockerfile` for Cloud Run or another container host. Configure these values in the hosting service rather than committing them:

- `OPENAI_API_KEY` and optional `OPENAI_MODEL`; or
- `ANTHROPIC_API_KEY` and optional `ANTHROPIC_MODEL`.

When a server-side key is present, the browser connection form is hidden and users cannot replace the centrally managed connection. Protect the service with company identity access before sharing its URL. Submitted content is sent to the selected AI provider for analysis and is not persisted by this application.

Public deployments default to 10 analyses per client address per hour. Override this with `ANALYSIS_RATE_LIMIT`. Set `TRUST_PROXY_HEADERS=1` when the hosting platform supplies a trusted `X-Forwarded-For` header. Use a single instance for this lightweight in-memory guard and configure a provider spending limit.

### Cloud Run outline

1. Create a private Cloud Run service from this GitHub repository.
2. Store the provider key in Secret Manager and expose it as `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`.
3. Enable Identity-Aware Proxy and grant access to the Learning Strategy team group.
4. Set a maximum instance count and provider spending limit.
5. Share the authenticated service URL.

This is a local version of the supplied `content-decoder_3.html`. The HTML interface sends analysis and web page requests to the accompanying Python server, so the AI key stays outside the browser. Keep `content-decoder.html`, `content_decoder_server.py`, and `frameworks.json` together.

## Reference lenses

The lens names and definitions now follow the two supplied PDFs. `frameworks.json` is the shared source used by the AI prompt, interface, and PDF report labels. It contains faithful paraphrases with source page numbers, rather than the substitute categories in the original HTML.

- **The Impactful Eight 2026.pdf**, pages 1–3: Operational efficiency and effectiveness; The science of learning; Education and industry partnerships; Assessment lifecycle; Lifelong learning; Recognition of learning; Generative AI; Evidence-based design.
- **Learning 2.0: A teaching and learning vision for Instructure's strategy**, Melissa Loble, August 2026: five beliefs on page 5, three gaps on page 4, and supporting strategic context on pages 2–7. The four implementation pillars are context, not additional belief or Impactful Eight tags.

Open **Reference lenses and source pages** in the interface to inspect the definitions. Each matched Impactful Eight pillar includes its reference page and, when verified, an excerpt from the sample. Quote matching tolerates typographic and whitespace differences. Unverified excerpts are removed and the match is flagged for review, while the remaining analysis is retained. Highlighting indicates relevance rather than endorsement. Learning 2.0 gaps refer to the vision's named strategic gaps; they do not imply that the sample is deficient.

The app and local routes have been checked in a browser. A live OpenAI diagnostic completed successfully and its results were verified in the browser after API credits were added.

## Run

Open Terminal in this folder and start the app:

```sh
python3 content_decoder_server.py
```

Then open [http://127.0.0.1:8765/content-decoder.html](http://127.0.0.1:8765/content-decoder.html). In **AI connection**, choose OpenAI or Anthropic, enter your API key, and click **Save connection**. Then run the diagnostic. The key stays in the running server's memory, is never returned to the page, and is discarded when the server stops. The app clears the password field after saving. Keep the terminal running while using the page. The optional Model field overrides the default.

You can alternatively set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` before starting the server, with an optional `ANTHROPIC_MODEL` or `OPENAI_MODEL`. Diagnostics are disabled until a provider is configured. Saving a connection stores the settings; the provider checks the key when you run a diagnostic.

You can paste text, upload a supported file, or fetch a public HTML page. Word, PDF, spreadsheet, and CSV extraction use external JavaScript libraries, so those formats need internet access when the page loads. The PDF export is built in.

The PDF export uses an A4, print-friendly report layout with a title band, executive readout, matched-lens summary, evidence cards, a Learning 2.0 section, source references, running headers, and page numbers. Only matched lenses appear in the summary, which keeps the report concise and makes the highlighted categories unambiguous.

The Learning 2.0 section is a selective strategic readout for the Learning Strategy team. It returns one primary belief, at most one distinct supporting belief, up to two strategic gaps, a tension or challenge, and one strategic implication. It closes with three practical outputs: **Say** for a defensible narrative, **Study** for an evidence question, and **Build** for a concrete product or learning-experience proposal. Evidence excerpts are checked against the submitted sample.

The GitHub Pages version makes direct browser requests to the selected provider, so each user supplies a personal API key for the current tab. The local server version keeps the selected provider key outside the browser and is the safer basis for a shared internal deployment. Browser security still blocks retrieval from many third-party web pages. AI analysis requires a valid provider key and network access.
