# -*- coding: utf-8

ROLES = (('contributor', 'contributor'),
         ('administrator', 'administrator'))

ORGANISATION_TYPES_DATA = ('Administration', 'Academic', 'Business', 'NGO')
ORGANISATION_TYPES = [(i, i) for i in ORGANISATION_TYPES_DATA]
ORGANISATION_TYPES += (('Other', 'Other, please describe below'), )

LANGUAGES = (
    ('BG', 'Bulgarian'),
    ('CS', 'Czech'),
    ('DA', 'Danish'),
    ('DE', 'German'),
    ('EL', 'Greek'),
    ('EN', 'English'),
    ('ES', 'Spanish'),
    ('ET', 'Estonian'),
    ('FI', 'Finnish'),
    ('FR', 'French'),
    ('GA', 'Irish'),
    ('H', 'Hungarian'),
    ('IS', 'Icelandic'),
    ('IT', 'Italian'),
    ('LB', 'Luxembourgish'),
    ('LT', 'Lithuanian'),
    ('LV', 'Latvian'),
    ('MT', 'Maltese'),
    ('NL', 'Dutch'),
    ('NO', 'Norwegian'),
    ('PL', 'Polish'),
    ('PT', 'Portuguese'),
    ('RM', 'Rhaeto-Romance'),
    ('RO', 'Romanian'),
    ('SK', 'Slovak'),
    ('SL', 'Slovenian'),
    ('SV', 'Swedish'),
    ('TR', 'Turkish'),
)

RESOURCE_TYPES = (
    ('literature', 'Literature'),
    ('tool', 'Tool'),
    ('event', 'Event'),
    ('website', 'Website'),
    ('maps', 'Maps'),
)

ORIGIN_DATA = ('Science/academic organisation',
               'Policy/governmental organisation',
               'Science-policy interface',
               'Field practitioner/Manager',)
ORIGIN = [(i, i) for i in ORIGIN_DATA]

STATUS = (
    ('Draft', 'Draft'),
    ('Final', 'Final'),
    ('I don\'t know', 'I don\'t know'),
)

AVAILABILITY = (
    ('Free of charge', 'Free of charge'),
    ('With costs', 'With costs'),
    ('I don\'t know', 'I don\'t know'),
)

YES_NO = (
    ('0', 'No'),
    ('1', 'Yes'),
)

SPATIAL_SCALE = (
    ('International', 'International'),
    ('National', 'National'),
    ('Regional', 'Regional'),
    ('Local', 'Local'),
    ('Required', 'Required'),
)

COUNTRIES = (
    ('AL', 'Albania'),
    ('AT', 'Austria'),
    ('BA', 'Bosnia-Herzegovina'),
    ('BE', 'Belgium'),
    ('BG', 'Bulgaria'),
    ('CH', 'Switzerland'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('DE', 'Germany'),
    ('DK', 'Denmark'),
    ('EE', 'Estonia'),
    ('ES', 'Spain'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GB', 'United Kingdom'),
    ('GR', 'Greece'),
    ('HR', 'Croatia'),
    ('HU', 'Hungary'),
    ('IE', 'Ireland'),
    ('IS', 'Iceland'),
    ('IT', 'Italy'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('LV', 'Latvia'),
    ('ME', 'Montenegro'),
    ('MK', 'Macedonia (FYR)'),
    ('MT', 'Malta'),
    ('NL', 'Netherlands'),
    ('NO', 'Norway'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('RO', 'Romania'),
    ('RS', 'Serbia'),
    ('SE', 'Sweden'),
    ('SI', 'Slovenia'),
    ('SK', 'Slovakia'),
    ('TR', 'Turkey'),
)

CONTENT_DATA = (
    'Theoretical material for ecosystem assessment (methods, concepts, guidance)',
    'Analytical material (Ecosystem assessment case-studies)',
    'Communication material on ecosystem assessment (maps)',
    'Policy document (Strategies, Directives)',
    'Produce/Evaluate data (measured, observed, modelled)',
    'Produce maps',
    'Mandatory reporting to EU or international body',)
CONTENT = [(i, i) for i in CONTENT_DATA]

KEY_ELEMENTS_DATA = (
    'Setting the assessment process (incl. governance, stakeholder engagement, funding, communication, ...)',
    'Conceptual framework',
    'Biophysical baseline of ecosystems and their services (mapping and assessment of state & trends)',
    'Valuation of ecosystem services (links between ecosystem services and human well-being)',
    'Scenario development and analyses',
    'Policy analyses or response options',)
KEY_ELEMENTS = [(i, i) for i in KEY_ELEMENTS_DATA]

FEEDBACK_DATA = (
    'You have been using this document for your own work on ecosystem assessment',
    'You were involved in reviewing the document',
    'You commissioned this document',
    'You were involved in the production of the document (author of a paper, organiser of an event...)',
)
FEEDBACK = [(i, i) for i in FEEDBACK_DATA]

ECOSYSTEM_ISSUES_DATA = (
    'State & trends of Ecosystems',
    'State & trends of Ecosystem services',
    'Restoration',
    'Compensation & no net loss',
)
ECOSYSTEM_ISSUES = [(i, i) for i in ECOSYSTEM_ISSUES_DATA]

ECOSYSTEM_METHODS_DATA = (
    'Indicators',
    'Mapping',
    'Natural capital accounting',
    'Valuation of ecosystem services',
    'Scenario',
    'Policy analyses',
)
ECOSYSTEM_METHODS = [(i, i) for i in ECOSYSTEM_METHODS_DATA]

ECOSYSTEM_TYPES_DATA = (
    'Urban',
    'Cropland',
    'Grassland',
    'Woodland and forest',
    'Heathland and shrub',
    'Sparsely vegetated land',
    'Wetlands',
    'Rivers and lakes',
    'Marine',
)
ECOSYSTEM_TYPES = [(i, i) for i in ECOSYSTEM_TYPES_DATA]
