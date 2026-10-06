"""Build the static evidence pages. Run from any directory with Python and Pillow."""
from html import escape
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAGES = [('innovation', 'Invention & Innovation'), ('inspiring', 'Inspiring Others'),
         ('consultancy', 'Consultancy'), ('influencer', 'Public Influence')]


def esc(value):
    return escape(str(value), quote=True)


def links(*items):
    return '<div class="links">' + ''.join(f'<a href="{esc(url)}">{esc(label)}</a>' for label, url in items) + '</div>'


def image(src, alt, eager=False):
    with Image.open(ROOT / src) as img:
        width, height = img.size
    return f'<img src="{esc(src)}" alt="{esc(alt)}" width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async">'


def evidence(title, issuer, caption, src, original=None, extra=(), photo=False, gallery=(), preview_class=''):
    original = original or src
    gallery_items = [{'src': src, 'href': original, 'title': title}]
    gallery_items.extend({'src': item_src, 'href': item_src, 'title': item_title} for item_title, item_src in gallery)
    gallery_data = f' data-gallery="{esc(json.dumps(gallery_items))}"' if gallery else ''
    gallery_count = f'<span class="media-count" aria-hidden="true">{len(gallery_items)} images</span>' if gallery else ''
    return f'''<article class="evidence">
<div class="document {'photo' if photo else ''} {esc(preview_class)}"><a href="{esc(original)}" data-preview="{esc(title)}"{gallery_data} aria-label="Enlarge {esc(title)}">{image(src, title)}{gallery_count}</a></div>
<div class="caption"><p class="eyebrow">{esc(issuer)}</p><h3>{esc(title)}</h3><p>{caption}</p>
{links(*extra, ('Original image' if original == src else 'Original document', original))}</div></article>'''


def cert(stem, title, issuer, caption, extra=(), gallery=()):
    base = ROOT / 'assets/certificates'
    thumbnails = list(base.glob(stem + '-thumb.*'))
    src = thumbnails[0] if thumbnails else base / (stem + '.jpg')
    original = base / (stem + '.pdf')
    if stem == 'georgia-tech-capstone-judge':
        original = base / 'georgia-tech-capstone-judge-certificate.pdf'
    if not original.exists():
        original = src
    return evidence(title, issuer, caption, str(src.relative_to(ROOT)), str(original.relative_to(ROOT)), extra, gallery=gallery)


def mentor_recognition():
    items = [
        ('adplist-top-50-data-engineering-mentor', 'Top 50 Data Engineering Mentor, April-June 2026'),
        ('adplist-top-50-data-engineering-mentor-jul-sep-2026', 'Top 50 Data Engineering Mentor, July-September 2026'),
        ('adplist-top-1-percent-mentor-2026', 'Top 1% Mentor in Engineering, September 2026'),
    ]
    documents = []
    for stem, title in items:
        original = f'assets/certificates/{stem}.pdf'
        thumb = f'assets/certificates/{stem}-thumb.png'
        documents.append(f'<div class="document"><a href="{original}" data-preview="{esc(title)}" aria-label="Enlarge {esc(title)}">{image(thumb, title)}</a></div>')
    return '<article class="evidence"><div class="paired-documents">' + ''.join(documents) + '</div><div class="caption"><p class="eyebrow">ADPList / 2026</p><h3>Mentoring recognition</h3><p>ADPList recognised my Data Engineering mentorship in both April-June and July-September 2026, and awarded Top 1% Mentor in Engineering recognition for September.</p>' + links(('Public mentor profile', 'https://adplist.org/mentors/jayakumar-ramalingam'), ('April-June certificate', f'assets/certificates/{items[0][0]}.pdf'), ('July-September certificate', f'assets/certificates/{items[1][0]}.pdf'), ('Top 1% certificate', f'assets/certificates/{items[2][0]}.pdf')) + '</div></article>'


def grid(*items):
    return '<div class="grid">' + ''.join(items) + '</div>'


def source(publisher, title, description, url, label='Publisher source'):
    return f'<article class="source"><p class="publisher">{esc(publisher)}</p><h3>{esc(title)}</h3><p>{description}</p>{links((label, url))}</article>'


def sources(*items):
    return '<div class="sources">' + ''.join(items) + '</div>'


def note(text):
    return f'<aside class="note">{text}</aside>'


def section(id, number, title, description, body):
    return f'<section class="section" id="{id}" aria-labelledby="{id}-title"><div class="section-head"><span class="section-number" aria-hidden="true">{number}</span><div><h2 id="{id}-title">{title}</h2><p>{description}</p></div></div>{body}</section>'


def facts(*items):
    return '<div class="facts">' + ''.join(f'<div class="fact"><strong>{value}</strong><span>{label}</span></div>' for value, label in items) + '</div>'


def page(slug, title, intro, sections, body, home=False):
    nav = '<a href="index.html">Home</a><a href="about.html">About</a>' + ''.join(f'<a href="{name}.html"' + (' aria-current="page"' if name == slug else '') + f'>{esc("Innovation" if name == "innovation" else label)}</a>' for name, label in PAGES)
    jump = '<nav class="page-index" aria-label="On this page">' + ''.join(f'<a href="#{id}">{label}</a>' for id, label in sections) + '</nav>' if sections else ''
    heading = '' if home else f'<div class="intro"><p class="eyebrow">Jayakumar Ramalingam / Professional portfolio</p><h1>{esc(title)}</h1><p>{intro}</p></div>'
    index = [p[0] for p in PAGES].index(slug) if slug in dict(PAGES) else -1
    onward = ''
    if index >= 0:
        next_name, next_title = PAGES[(index + 1) % 4]
        onward = f'<nav class="closing" aria-label="Continue reading"><a href="index.html">Portfolio overview</a><a href="{next_name}.html">{esc(next_title)} &rarr;</a></nav>'
    document = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet"><title>{esc(title)} | Jayakumar Ramalingam</title>
<meta name="description" content="{esc(intro)}"><link rel="canonical" href="https://jrtechfolio.com/{slug}.html">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)} | Jayakumar Ramalingam"><meta property="og:description" content="{esc(intro)}">
<meta property="og:url" content="https://jrtechfolio.com/{slug}.html"><meta property="og:image" content="https://jrtechfolio.com/assets/profile/jay-full.jpeg">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="evidence.css?v=20261006"><link rel="stylesheet" href="shell.css?v=20261005b"><script defer src="navigation.js?v=20261005b"></script><script defer src="evidence.js?v=20261005d"></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="header"><div class="wrap"><div class="identity"><a class="brand" href="index.html"><span class="monogram" aria-hidden="true">JR</span>Jayakumar Ramalingam</a><small>Cloud architecture &amp; intelligent systems</small></div><nav class="primary" aria-label="Primary navigation">{nav}</nav></div></header>
<main id="main" class="wrap">{heading}{jump}{body}{onward}</main>
<footer class="footer"><div class="wrap"><p>&copy; 2026 Jayakumar Ramalingam</p><div><a href="https://www.linkedin.com/in/jayakumarramalingam/">LinkedIn</a><a href="https://orcid.org/0009-0007-9823-3097">ORCID</a><a href="https://github.com/jayakumar-ramalingam/">GitHub</a></div></div></footer>
<dialog id="evidence-viewer" aria-labelledby="viewer-title"><div class="viewer-head"><p id="viewer-title">Evidence</p><button class="close" type="button" aria-label="Close preview" title="Close preview">&times;</button></div><div class="viewer-image"><img alt=""></div><div class="viewer-actions"><div class="viewer-controls" hidden><button class="previous" type="button" aria-label="Previous image" title="Previous image">&#8592;</button><span class="viewer-count"></span><button class="next" type="button" aria-label="Next image" title="Next image">&#8594;</button></div><a class="viewer-link" href="#">Open original evidence</a></div></dialog>
</body></html>'''
    (ROOT / f'{slug}.html').write_text(document)


BDAI = 'https://ieeexplore.ieee.org/document/11655157'
IJSE = 'https://www.cscjournals.org/library/manuscriptinfo.php?mc=IJSE-200'
IJFMR = 'https://www.ijfmr.com/research-paper.php?id=84897'
BATCH = 'https://roundtable.ailovesdata.com/from-batch-to-streaming-a-reference-architecture-for-real-time-personalization'
OBS = 'https://www.dataversity.net/articles/why-observability-is-becoming-a-governance-layer-for-agentic-data-systems/'
DATA = 'https://datatech2026.sched.com/event/2N4eI/from-batch-to-streaming-data-architecture-for-context-aware-personalization'
KEYNOTE = 'https://scrs.in/conference/icdsa2026/speaker/talk/23115'
LAUNCH = 'https://investor.siriusxm.com/news-events/press-releases/detail/2012/siriusxm-unveils-next-generation-platform-bringing-fans'


def research_core():
    return grid(
        cert('bdai-2026-paper-presentation-certificate', 'Scalable Event-Driven Architecture for Machine Learning-Based Real-Time Personalization and Recommendation Systems', 'IEEE Xplore / BDAI 2026', 'Published research on event-driven personalisation. The presentation certificate is shown above; the indexed paper is available from IEEE Xplore.', [('IEEE Xplore paper', BDAI)]),
        cert('ijse-publication-certificate', 'Edge-to-Cloud Machine Learning Pipelines for Low-Latency Intelligent Systems', 'International Journal of Software Engineering / CSC Journals', 'Journal research on low-latency machine-learning pipelines across edge and cloud systems, with the publisher-issued certificate.', [('Journal article', IJSE)]))


innovation = section('platform', '01', 'Personalisation in production', 'SiriusXM streaming platform / 2022-2026',
    '<div class="text-columns"><div><h3>The "For You" serving component</h3><p>I designed, implemented and delivered recommendation serving that combines offline candidates with current listener context and request-time ranking. Stable interfaces allow models and recommendation sources to evolve independently.</p></div><div><h3>Experimentation and continued improvement</h3><p>I integrated set-level and page-level A/B experimentation into the serving flow and led subsequent performance optimisation.</p></div></div>'
    + facts(('3,000+', 'Requests per second sustained in production'), ('~40%', 'Lower end-to-end latency against the initial production baseline'), ('Set + page', 'Recommendation experimentation within one serving flow'))
    + note('Personal contribution and internal performance figures are supporter-verifiable. Public company sources below establish product launch and business context; they do not attribute those outcomes to an individual.'))
innovation += section('launch', '02', 'A publicly launched experience', 'Independent company records establish the product, its content and the scale of the business.', sources(
    source('SiriusXM / November 2023', 'The new streaming platform and "For You"', 'The launch announcement identifies "For You" as a customised landing page and describes always-on personalisation and curation.', LAUNCH, 'Official launch announcement'),
    source('SiriusXM / December 2023', 'More than 400 channels', 'The official rollout describes the breadth of channels and on-demand content available through the new app.', 'https://investor.siriusxm.com/news-events/press-releases/detail/2023/the-next-generation-of-siriusxm-begins-new-app-starts', 'Official app rollout'),
    source('SiriusXM / FY2025', 'Approximately 33 million subscribers', 'Year-end reporting provides company-wide subscriber context. This is business scale, not the number of users attributed to my services.', 'https://investor.siriusxm.com/sec-filings/all-sec-filings/content/0000908937-26-000003/siriq42025earningsrelease.htm', 'Official financial results')))
innovation += section('research', '03', 'Published technical research', 'Two publications develop the personalisation and machine-learning architecture described in this work.', research_core())
innovation += section('practice', '04', 'From production experience to practitioner guidance', 'A published reference architecture and public research records.', sources(
    source('AI Loves Data', 'From Batch to Streaming: A Reference Architecture for Real-Time Personalization', 'Explains how batch, streaming and request-time components fit together, making the architecture accessible to practitioners.', BATCH, 'Read the article'),
    source('ORCID', 'Jayakumar Ramalingam / 0009-0007-9823-3097', 'Research identity and publication record, alongside the publisher links above.', 'https://orcid.org/0009-0007-9823-3097', 'Research record')))
page('innovation', 'Invention & Innovation', 'Production personalisation, experimentation and the research that makes the approach reusable.', [('platform','Production work'),('launch','Public product evidence'),('research','Research'),('practice','Practitioner writing')], innovation)


inspiring = section('datatech', '01', 'DataTech: guidance recognised by the organiser', 'MinneAnalytics / Richfield, Minnesota / 15 May 2026', '<div class="wide-document">' +
    cert('datatech-2026-speaker-appreciation', 'From Batch to Streaming', 'John Hogue / DataTech Chair & Board Member', 'The letter confirms competitive speaker selection, engaged questions from senior data architects and analytics leaders, and positive responses to practical guidance on context-aware personalisation.', [('Official session', DATA)], gallery=[('At DataTech 2026', 'assets/events/datatech-event-photo.jpeg')]) + '</div>'
    + '<blockquote class="quote">"translate complex architectural concepts into actionable guidance for a working professional audience."<cite>John Hogue, DataTech 2026 Chair, recognition letter dated 26 May 2026</cite></blockquote>')
inspiring += section('ai4', '02', 'Ai4: The Cloud Playbook Was Written Before AI', 'Las Vegas / August 2026', '<div class="wide-document">' +
    evidence('Ai4 speaker listing', 'Ai4 / Organiser directory', 'The organiser directory names Jayakumar Ramalingam as a speaker. The session explored workload placement, workflow changes, shared capabilities and recovery for AI systems. A public attendee recap reports the organisers\' figure of more than 12,000 attendees from 100 countries; this is event reach, not session attendance. The preview includes the programme, event photo and speaker badge.', 'assets/events/ai4/ai4-speaker-directory.png', extra=[('Official speaker directory', 'https://ai4.io/speakers/'), ('Event attendance recap', 'https://www.wwt.com/blog/ai4-2026-recap-from-ai-experiments-to-ai-workloads')], gallery=[('Ai4 conference programme', 'assets/events/ai4/ai4-session-schedule.jpeg'), ('At Ai4 2026', 'assets/events/ai4/ai4-event-photo.jpeg'), ('Ai4 speaker badge', 'assets/events/ai4/ai4-speaker-badge.jpeg')]) + '</div>')
inspiring += section('guidance', '03', 'Shared engineering practice across teams', 'Pandora and SiriusXM / Organisational contribution',
    '<div class="text-columns"><div><h3>Pandora: a shared data-access framework</h3><p>In 2021, I developed and evolved a common data-access and caching framework used across playback continuity, recommendations, listening modes, listener history and collections. Working sessions addressed invalidation, retries, refresh and failure handling.</p></div><div><h3>SiriusXM: architecture decision practice</h3><p>I facilitated architecture reviews and published Architecture Decision Records covering alternatives and operational consequences. Engineers across several teams reused the reasoning to improve failure isolation, asynchronous processing and degradation behaviour.</p></div></div>'
    + note('Internal adoption, changed engineering practice and use by senior engineering leaders are supporter-verifiable. Confidential repositories, architecture records and production documents are not publicly reproduced.'))
inspiring += section('writing', '04', 'Making architectural reasoning available to others', 'Practitioner writing and community review', sources(
    source('DATAVERSITY', 'Why Observability Is Becoming a Governance Layer for Agentic Data Systems', 'Explains how decision provenance and governance should inform the design and review of autonomous data systems.', OBS, 'Read the article'),
    source('DevOps Institute / PeopleCert', 'The DevOps Standard', 'Contributed expertise and review feedback to the development of this vendor-neutral DevOps book. Acknowledged by name in the published book (PDF page 20).', 'https://www.peoplecert.org/devops-standard', 'Official book page')))
inspiring += section('mentoring', '05', 'ADPList mentoring recognition', 'Three independently issued recognitions in 2026.', '<div class="wide-document">' + mentor_recognition() + '</div>')
inspiring += section('recognition', '06', 'Professional recognition', 'An independent award for enterprise AI architecture.', '<div class="wide-document">' + cert('business-mint-enterprise-ai-architect-2026', 'Enterprise AI Architect of the Year 2026', 'Business Mint Nationwide Awards / 7 September 2026', 'Certificate of recognition in the Enterprise AI Architect category. This award provides professional context; the speaking, writing and mentoring records above document contributions to others.') + '</div>')
inspiring += section('memberships', '07', 'Professional society participation', 'Memberships and fellowships provide additional professional context.', grid(
    cert('ieee-senior-member-letter', 'IEEE Senior Member', 'IEEE', 'Letter recognising elevation to Senior Member grade.'),
    cert('iete-2026-fellow-certificate', 'IETE Fellow', 'Institution of Electronics and Telecommunication Engineers', 'Fellow membership recognition.'))
    + grid(cert('scrs-2026-distinguished-fellow-certificate', 'SCRS Distinguished Fellow', 'Soft Computing Research Society', 'Distinguished Fellow recognition.'),
           cert('sas-sefm-eminent-fellow-2026', 'SAS / SEFM Eminent Fellow', 'Scholars Academic and Scientific Society', 'Eminent Fellow recognition.'))
    + '<p class="note">Also an ACM member. Professional memberships provide context for participation in the community; the speaking and mentoring evidence above documents the contribution.</p>')
page('inspiring', 'Inspiring Others', 'Architectural guidance, professional speaking and mentoring, supported by organiser records and community recognition.', [('datatech','DataTech'),('ai4','Ai4'),('guidance','Engineering practice'),('writing','Writing'),('mentoring','Mentoring'),('recognition','Recognition'),('memberships','Memberships')], inspiring)


consultancy = section('home-depot', '01', 'Home Depot: merchandising modernisation', 'TCS / Offshore 2012-2015 / Onsite advisory and delivery 2015-2019',
    '<div class="text-columns"><div><h3>Recommendation adopted</h3><p>I assessed optimisation of existing applications, wholesale replacement and phased service decomposition. I recommended phased modernisation, integrated pricing workflows and event-driven distribution, with migration across Google Cloud and Pivotal Cloud Foundry.</p></div><div><h3>Technical delivery and outcome</h3><p>I provided technical delivery leadership across more than twenty offshore and ten onsite engineers. Pricing changes moved from more than a week to minutes, and shelf-label requests could be queued on demand. Business priorities and final approvals remained with Home Depot stakeholders.</p></div></div>'
    + '<div class="wide-document">' + cert('home-depot-appreciation', 'Appreciation for pricing support and technical expertise', 'Home Depot / TCS / 2016', 'The certificate names pricing support operations and expertise in Tomcat migration, report automation, Hadoop and Git migration. It documents recognition during the engagement; the wider modernisation outcomes are supporter-verifiable.') + '</div>')
consultancy += section('retail-context', '02', 'International retail and engineering context', 'Public sources describe the client environment, rather than attributing company-wide results to my work.', sources(
    source('The Home Depot / FY2015', 'Merchandising transformation', 'The official annual report describes assortment-planning and pricing tools by store and geography.', 'https://ir.homedepot.com/~/media/Files/H/HomeDepot-IR/documents/investor-packet/2015-10-k.pdf', 'Official annual report'),
    source('The Home Depot / 2019', 'One Home Depot', 'The transformation strategy provides context for interconnected retail operations across the United States, Canada and Mexico.', 'https://ir.homedepot.com/news-releases/2019/12-11-2019-110001607', 'Company announcement'),
    source('Google Cloud', 'Home Depot cloud transformation', 'Customer case study describing the use of cloud services in a large retail estate.', 'https://cloud.google.com/customers/the-home-depot', 'Customer case study'),
    source('Cloud Foundry Foundation', 'The engineering estate', 'Published context describes more than 2,500 developers, 1,600 production applications and services, and more than 1.5 billion monthly requests.', 'https://www.cloudfoundry.org/blog/cloud-foundry-power-user-the-home-depot-joins-foundation-as-gold-member/', 'Foundation article')))
consultancy += section('manheim', '03', 'Manheim: vehicle-data and auction workloads', 'Cox Automotive through Mastech Digital / 2019-2021',
    '<div class="text-columns"><div><h3>Selective serverless modernisation</h3><p>I assessed aggregation, processing and batching modules for auction-vehicle intake and appraisal. I recommended AWS Lambda for intermittent workloads, with warm-up mechanisms to mitigate cold-start latency and infrastructure as code for repeatable deployment.</p></div><div><h3>Adoption and extended responsibility</h3><p>The client adopted the recommendations. Targeted changes reduced idle infrastructure expenditure and made provisioning more consistent. Successful vehicle-data delivery led to an extension of my remit into vehicle-report generation.</p></div></div>'
    + sources(source('Manheim / Company press release', 'Manheim Express nationwide launch', 'The launch describes Manheim as a Cox Automotive business and the role of vehicle identification, valuation, build and history data in its marketplace.', 'https://www.prnewswire.com/news-releases/manheim-express-launches-nationwide--mobile-app-offers-dealers-fast-easy-and-self-service-way-to-list-and-sell-inventory-300685941.html', 'Launch announcement'),
              source('Cox Automotive', 'Connected data across the vehicle lifecycle', 'Company context for connecting consumer, vehicle and market information across automotive services.', 'https://www.coxautoinc.com/insights/connected-data-the-engine-that-powers-better-results/', 'Company source'))
    + note('The advisory recommendations, internal outcomes and extension of my remit are supporter-verifiable. The linked company sources establish the business context.'))
consultancy += section('scope', '04', 'Consultancy scope and continuity', 'Eleven years in supplier-side consultancy / 2010-2021', '<div class="timeline"><p><strong>2010-2012 / TCS</strong>Financial-services technology, including Morgan Stanley.</p><p><strong>2012-2015 / TCS for Home Depot</strong>Offshore engineering and specialist merchandising knowledge.</p><p><strong>2015-2019 / TCS for Home Depot</strong>Onsite stakeholder advice and technical delivery of merchandising modernisation.</p><p><strong>2019-2021 / Mastech Digital for Cox Automotive</strong>Vehicle-data services, selective serverless recommendations and vehicle-report generation.</p></div>' + note('Personal role, programme savings, delivery scale and operational improvements are based on my professional record and can be corroborated by supporters. Confidential client records are not reproduced.'))
page('consultancy', 'Consultancy', 'Adopted technical recommendations across retail merchandising and automotive data, with client recognition and public business context.', [('home-depot','Home Depot'),('retail-context','Retail context'),('manheim','Manheim'),('scope','Engagement history')], consultancy)


influence = section('speaking', '01', 'Keynote and conference speaking', 'Production AI architecture shared with research and practitioner audiences.', grid(
    cert('icdsa-2026-keynote-certificate', 'Event-Driven Intelligence: Architecting Real-Time AI Decision Systems at Scale', 'ICDSA 2026 / Keynote speaker', 'Keynote at the 7th International Conference on Data Science and Applications, addressing timely decisions and operational controls in production AI.', [('Official keynote programme', KEYNOTE)]),
    evidence('Ai4 2026: The Cloud Playbook Was Written Before AI', 'Ai4 2026 / Speaker', 'At Ai4 2026 in Las Vegas. The event-issued speaker badge and conference programme are available in the preview and document my session on workload placement, shared capabilities and recovery for AI systems.', 'assets/events/ai4/ai4-lead-photo.jpeg', extra=[('Official speaker directory', 'https://ai4.io/speakers/')], photo=True, preview_class='ai4-lead', gallery=[('Ai4 speaker badge', 'assets/events/ai4/ai4-speaker-badge.jpeg'), ('Ai4 conference programme', 'assets/events/ai4/ai4-session-schedule.jpeg')]))
    + grid(cert('datatech-2026-speaker-appreciation', 'From Batch to Streaming', 'MinneAnalytics DataTech / Featured speaker', 'The organiser confirms the session on context-aware personalisation, competitive selection and practitioner engagement. An event photograph is available in the preview.', [('Official session', DATA)], gallery=[('At DataTech 2026', 'assets/events/datatech-stage-photo.jpeg')]),
           evidence('Event-sourced multi-agent fault diagnosis', 'IEEE IEMCON 2026 / Paper presentation', 'Presented research on autonomous fault diagnosis and resilient self-healing in cloud-native microservices at the University of California, Berkeley. The preview also includes a conference photograph and delegate badge; no indexed proceedings claim is made here.', 'assets/events/iemcon/iemcon-presentation.jpeg', photo=True, gallery=[('At IEEE IEMCON 2026', 'assets/events/iemcon/iemcon-group-photo.jpeg'), ('IEMCON delegate badge', 'assets/events/iemcon/iemcon-delegate-badge.jpeg')])))
influence += section('committees', '02', 'Technical programme and peer-review service', 'Committee appointments and review records document research evaluation; they do not establish an event-organising or advisory-board role.', grid(
    cert('aiiot-2026-reviewer-certificate', 'World AI IoT Congress', 'AIIoT 2026 / TPC member and reviewer', 'The certificate recognises technical programme committee service and review of twelve papers.', [('Technical committee listing', 'https://worldaiiotcongress.org/technical-committee/')]),
    cert('2ai-2026-reviewer-certificate', 'Applied Artificial Intelligence', '2AI 2026 / Technical Program Committee', 'Recognition for peer review and technical evaluation of submitted manuscripts.', [('Conference organiser', 'https://2ai-conference.org/')]))
    + grid(cert('ngmse-2026-reviewer-certificate', 'Next-Generation Multimedia Services at the Edge', 'NGMSE / IEEE ISCC 2026', 'The certificate acknowledges review of four submitted manuscripts. Committee details are available from the workshop organiser.', [('Workshop programme and committee', 'https://sites.google.com/view/ngmse2026/home')]),
           source('UEMCON 2026', 'Technical programme committee', 'Committee service at the international conference on ubiquitous computing, electronics and mobile communication, recorded in my professional contribution history.', 'https://ieee-uemcon.org/', 'Conference organiser')))
influence += section('reviews', '03', 'Peer review across international conferences', 'More than fifty research papers reviewed, as recorded in my professional contribution history. Selected organiser-issued certificates are shown below.', grid(
    cert('r10-htc-2026-reviewer-certificate', 'IEEE Region 10 Humanitarian Technology Conference', 'R10-HTC 2026 / Reviewer', 'Organiser recognition of reviewing service.'),
    cert('isemantic-2026-reviewer-certificate', 'International Seminar on Application for Technology of Information and Communication', 'ISemantic 2026 / Reviewer', 'Certificate documenting peer-review contribution.'))
    + grid(cert('icetci-2026-reviewer-certificate', 'Emerging Techniques in Computational Intelligence', 'ICETCI 2026 / Reviewer', 'Recognition for technical review of conference submissions.'),
           cert('amlds-2026-reviewer-certificate', 'Applied Machine Learning and Data Science', 'AMLDS 2026 / Reviewer', 'Organiser acknowledgement of research evaluation.'))
    + note('My review record also includes IEEE GLOBECOM, IECON and IEEE BigData. The certificates above document selected engagements, rather than the total number of papers reviewed.'))
influence += section('judging', '04', 'Judging applied innovation', 'Award juries, university projects and hackathons.', grid(
    cert('stevie-2026-technology-excellence-jury-certificate', 'Stevie Awards for Technology Excellence', '2026 / Company & Organization Awards Jury', 'Jury recognition for evaluating entries in the technology excellence programme.'),
    cert('stevie-2026-international-business-awards-chair-certificate', 'International Business Awards', '2026 / New Product & Product Management Awards Jury', 'Certificate of appreciation for judging on the New Product & Product Management Awards Jury.'))
    + grid(cert('georgia-tech-capstone-judge', 'Georgia Tech Capstone Design Expo', 'Spring 2026 / Judge', 'Recognition for assessing senior design projects.'),
           cert('c-day-judging-certificate', 'Kennesaw State Computing Showcase', 'Spring 2026 / Judge', 'Certificate of appreciation for judging student projects.'))
    + '<div class="wide-document" style="margin-top:28px">' + cert('hackgt-13-judge-letter', 'HackGT 13: Seaside Market', 'HexLabs / Georgia Tech / September 2026', 'The organiser confirms my service as an official judge, evaluating projects and providing feedback at an event involving more than 1,000 students from universities around the world.') + '</div>'
    + sources(source('QS Reimagine Education', 'Awards judge', 'Public judging directory for the 2026 programme.', 'https://qsrea.evessiocloud.com/Reimagine2026/en/page/judges', 'Official judge directory'),
              source('AI Loves Data Miami', 'Enterprise AI evaluation', 'Public profile documenting participation as a judge of applied enterprise AI.', 'https://ailovesdata.com/miami/jayakumar-ramalingam/', 'Official judge profile')))
influence += section('writing', '05', 'Practitioner writing', 'Articles that make architecture, observability and operational trade-offs available beyond conference audiences.', sources(
    source('DATAVERSITY', 'Why Observability Is Becoming a Governance Layer for Agentic Data Systems', 'Decision provenance, governance and the observability required by autonomous systems.', OBS, 'Read article'),
    source('HackerNoon', 'Why AI Agents Need Event-Driven Architecture', 'Durable state, human approvals and reliable execution for production agent systems.', 'https://hackernoon.com/why-ai-agents-need-event-driven-architecture', 'Read article'),
    source('AI Loves Data', 'From Batch to Streaming: A Reference Architecture for Real-Time Personalization', 'A practitioner reference connecting batch pipelines, streaming signals and recommendation serving.', BATCH, 'Read article'),
    source('HackerNoon', 'Claude Managed Agents: Build a GitHub Repo Review Agent Without Running Infrastructure', 'A practical implementation guide for a repository-review agent.', 'https://hackernoon.com/claude-managed-agents-build-a-github-repo-review-agent-without-running-infrastructure', 'Read article')))
influence += section('publications', '06', 'Research publications', 'Three indexed IEEE conference papers and two journal articles.', research_core()
    + grid(cert('iwis-2026-paper-presentation-certificate', 'An Event-Driven Context-Aware Framework for Margin-Preserving Dynamic Pricing in High-Velocity Retail Commerce Systems', 'IEEE Xplore / IWIS 2026 / First author', 'Published work on context-aware retail pricing. The presentation certificate appears above.', [('IEEE Xplore paper', 'https://ieeexplore.ieee.org/document/11667738')]),
           cert('ijfmr-2025-ai-native-data-platforms-publication-certificate', 'Building AI-Native Data Platforms: From Data Lakes to Intelligent Decision Platforms', 'IJFMR / Journal publication / Co-author', 'Journal research examining the evolution of data platforms into intelligent decision systems.', [('Journal article', IJFMR)]))
    + '<div class="wide-document" style="margin-top:28px">' + cert('icosaas-2026-fraud-presentation-certificate', 'Beyond Rules-Based Fraud Detection: Explainable Graph AI for Streaming Retail Transactions', 'IEEE Xplore / ICOSAAS 2026 / Second author', 'Conference certificate documenting presentation of the co-authored fraud-detection paper. The publication is indexed by IEEE Xplore.', [('IEEE Xplore paper', 'https://ieeexplore.ieee.org/document/11648578')]) + '</div>'
    + note('The IEMCON presentation is documented in the speaking section above. Additional presented research covers a threat model for the Model Context Protocol. Neither presentation is labelled here as an indexed proceedings paper.'))
influence += section('media', '07', 'Independent media and interviews', 'Published commentary and conversations beyond authored technical articles.', sources(
    source('The New Stack', 'Agent memory and governance', 'Quoted analysis on governance risks associated with agent memory and offline processing.', 'https://thenewstack.io/anthropic-agent-memory-dreaming/', 'Published coverage'),
    source('The New Stack', 'Automated alignment and independent evaluation', 'Expert commentary on evaluating emerging automated alignment approaches.', 'https://thenewstack.io/claude-automated-alignment-research/', 'Published coverage'),
    source('DATAVERSITY / My Career in Data', 'Season 4, Episode 13: Jayakumar Ramalingam', 'A conversation about moving from software engineering into real-time data and AI, foundational learning, and practical experience.', 'https://www.dataversity.net/podcasts/my-career-in-data-season-4-episode-13-jayakumar-ramalingam-staff-software-engineer-and-cloud-architect/', 'Listen to the episode'),
    source('Authority Magazine', 'Professional interview', 'A published interview sharing perspectives on technology and digital engagement.', 'https://medium.com/authority-magazine/jayakumar-ramalingam-of-siriusxm-on-five-ways-to-leverage-instagram-to-dramatically-improve-your-ec9599d23a87', 'Read interview')))
page('influencer', 'Public Influence', 'Keynote speaking, international research evaluation, judging, publications and independent media recognition.', [('speaking','Speaking'),('committees','Committees'),('reviews','Peer review'),('judging','Judging'),('writing','Writing'),('publications','Research'),('media','Media')], influence)


print('Built the four evidence pages.')
