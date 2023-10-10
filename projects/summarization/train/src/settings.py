"""Settings."""

# Standard Library
import os
from typing import List

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
)


# --- settings classes
class TrackedSumModelSpecs(TrackedModelSpecs):
    """Tracked summarization model specs."""

    project: str = "onclusive/summarization"
    model = "SUM-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):
    """Inputs."""

    sample_documents: List[str] = ["Sky News announces slate of special programming for the appointment of the UK's new Prime Minister.\nSky News' political programming will expand ahead of a momentous week in UK politics with the impending announcement of the new Prime Minister. Sky News' key political programmes will return to bring audiences in-depth discussion and analysis of all the latest news with live coverage from Downing Street and Westminster.\nHead of Sky News, John Ryley:\n'This is a momentous week in British politics, where a new Prime Minister will take on an in-tray bursting with crunch decisions. Sky News will be live in Westminster and hearing from voters in key constituencies to bring our audiences the latest news, and analyse the impact this new government will have on households across the UK.'\nSky News' slate of dedicated political programming will kick off from 8.30 am on Sunday 4th September with Sophy Ridge on Sunday, focusing on the impending result of the Conservative Party leadership election.\nOn Monday 5th, Tuesday 6th and Wednesday 7th September, Sky News will bring live coverage to audiences from Downing Street and Westminster as power is handed over from outgoing Prime Minister, Boris Johnson to his successor, either Liz Truss or Rishi Sunak.\nSophy Ridge's The Take will return on Wednesday 7th September and on Thursday 8th September Beth Rigby Interviews… will also return to explore the result of the leadership election.\nOther special programming on Sky News will cover the key moments for the new Prime Minster in their first days in office, including their first meeting with her Majesty the Queen on Tuesday - during which they'll seek permission to form a government - and their first major statement as Prime Minister from the steps of Downing Street. With millions of households across the UK asking questions about the cost-of-living crisis, this moment will be pivotal for the new Prime Minister and Sky News will bring audiences the full story on-air, online, on our app, and via our podcasts.\nThe first Prime Minister's Questions will also be broadcast live from the House of Commons on Sky News on Wednesday 7th September. This will be the first time that the new PM faces Labour's leader across the despatch box, and they will be expected to face questions about future government policy including the possible timing of a general election.\nCoverage of all these events will be available on the Sky News Politics Hub and will continue throughout September and October from the Labour and Conservative Party Conferences from 25th-28th September and 2nd-5th October respectively. Sky News will also be hosting pop-up radio stations at both party conferences.",
                                   "Elle est toujours là et inquiète de plus en plus les dirigeants d'entreprise. Selon la dernière vague du baromètre mensuel OpinionWay-BDO-Challenges, l'inflation est la préoccupation numéro un, à hauteur de 65%, contre 53% en septembre. Très loin devant les autres thématiques, « l'environnement » plongeant par exemple de 11 % à 3 %. Il est vrai qu'à 5,6% le rythme annuel de l'indice des prix à la consommation reste soutenu, même s'il est près de deux fois moins important qu'en Allemagne ou au Royaume-Uni. Car le danger vient bien de l'international, l'indice de confiance en l'économie mondiale tombant à 27 %, contre 33 % pour la France, toujours dans une perspective à six mois. Dans un contexte conjoncturel aussi instable, il n'est guère étonnant que les dirigeants d'entreprise mettent en veilleuse leurs intentions d'embauches, qui plongent de 9 points (voir graphique). Un chiffre à relativiser, rappelle OpinionWay, en raison « d'effets de saisonnalité ». A noter que les inquiétudes concernant la pénurie de main-d'oeuvre et la « grande démission » s'estompent. Peut-être parce que les entreprises se sont décidées à augmenter les salaires, 90% d'entre elles s'étant résolues à adopter des « actions sociales », un taux qui grimpe même à 100% pour la partie de l'échantillon dont le chiffre d'affaires annuel est de 100 millions d'euros ou plus. Toujours selon OpinionWay, « la tendance est à la perte de confiance » des dirigeants d'entreprise vis-à-vis de l'environnement économique. Mais « ils restent sereins visà-vis de l'avenir proche de leur société ». C'est tout le paradoxe, puisque l'indicateur de « confiance dans votre entreprise » est à la hausse, à 79 %, retrouvant ses niveaux du mois de juin. L'Insee, qui traque aussi le moral patronal avec un indice synthétique du climat des affaires, a annoncé le 22 septembre qu'il avait légèrement baissé, tout en restant « encore audessus de sa moyenne de longue période ». Exception notable, le secteur du BTP où « le climat des affaires se stabilise à un niveau très élevé ». L'instabilité macroéconomique n'est de toute façon pas un frein pour l'ambition entrepreneuriale. Bien au contraire. Ils sont désormais 29 % à considérer un « potentiel de développement à l'international », contre 22 % le mois précédent. Le Royaume-Uni, par exemple, offre de belles opportunités d'acquisition en raison de la faiblesse de la livre sterling. P.-H. M.   P.-H. M.",
                                   "Ermittlungen gegen Bar-Mitarbeiterin Würzburg - Nachdem ein Mann in der Würzburger Disco „Odeon' schwere Brandverletzungen erlitten hat, ermittelt die Polizei gegen eine Disco-Mitarbeiterin. Sie soll als geplante Showaktion brennende Getränke auf der Bartheke ausgebracht haben, sagte ein Polizeisprecher am Donnerstag. Zeitgleich werde geklärt, ob es noch andere Verantwortliche gebe. Die Flammen waren am frühen Samstagmorgen auf den Mann übergesprungen. Er erlitt schwere Verletzungen im Gesicht und am Oberkörper. Nach Polizeiangaben wurde er inzwischen aus dem Krankenhaus entlassen.",
                                   "Isdin logra evitar una sanción de la CNMC G. Trindade. Barcelona El laboratorio de cosmética Isdin ha llegado a un acuerdo con la Comisión Nacional del Mercado y la Competencia (CNMC) para cerrar un expediente sancionador sobre prácticas restrictivas en la venta por Internet. De esta forma, la compañía catalana, propiedad a partes iguales de Puig y Esteve, evitará una sanción económica. La CNMC comunicó la incoación de un expediente a Isdin por la fijación de precios en la reventa en Internet de productos de protección solar en noviembre de 2020. En concreto, el regulador señaló que la empresa barcelonesa estaba desincentivando el comercio electrónico de determinados productos por parte de los distribuidores minoristas y revendedores. Tras el acuerdo, el regulador vigilará el cumplimiento de las medidas durante un periodo de tres años. Isdin se ha comprometido a mejorar su política de comunicación de precios a sus distribuidores, a fomentar su cultura interna de cumplimiento de la normativa de competencia y a garantizar que el personal de su departamento comercial no tenga acceso a determinada información relacionada con precios de venta de las farmacias.",
                                   "Tossuderia, curiositat, tenacitat, no témer el fracàs, envoltar-se d'un bon equip, aprofitar les oportunitats... El doctor Pere-Joan Cardona va donar un munt de consells als nois i noies que, ahir al migdia, van omplir la sala d'actes de la FUB, on va avançar que el seu probiòtic antituberculosi està a punt per poder sortir al mercat. S'hi van presentar tres dels millors projectes de la 7a Mostra de Treballs de Recerca i Crèdits de Síntesi de l'Escola Joviat. Cardona és doctor en Medicina i especialista en Microbiologia Clínica; cap de la Unitat de Tuberculosi Experimental de l'Institut Germans Trias i Pujol; professor associat de la UAB i inventor de la vacuna contra la tuberculosi Ruti -aturada per manca de finançament- i del probiòtic Nyaditum resae (NR), que té per objectiu immunitzar el cos contra la malaltia acostumant-lo a ella. L'investigador manresà va repassar amb la seva trajectòria -amb els èxits i també amb les patacades- els ingredients per excel·lir en la matèria que cadascú decideix triar. Va parlar del llibre que li va obrir els ulls al món de la recerca, El microscopi, quan estudiava a l'institut Lluís de Peguera; de la seva admiració pel descobridor de la penicil·lina, del laboratori que va muntar a casa seva i de les mostres que treia del Cardener per analitzar-les. L'atzar ha fet que sigui en aquest mateix riu on va recollir el micobacteri ambiental amb què ha formulat el complement dietètic esmentat abans, 'un producte que pràcticament ja es pot portar al mercat'. Un exemple de tenacitat, tenint en compte que l'aturada de la Ruti hauria ensorrat més d'una i de dues persones.",
                                   "Capodanno 'amaro' per un quarantenne modenese, libero professionista, e un operaio 36enne di Nonantola. I due - controllati dai carabinieri verso le 17 di ieri a Modena, in via Nonantolana, a bordo di una Golf - sono stati trovati in possesso di 28 grammi di cocaina, suddivisi in tre involucri di cellophane. Sono stati arrestati per detenzione ai fini di spaccio di stupefacenti e portati in carcere."
                                  ]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SumSettings(TrackedParams):
    """Summarization settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SumModelParams(TrackedParams):
    """summarization model settings."""

    sum_settings: SumSettings = SumSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class SumModelParamsEn(SumModelParams):
    """English Summarization model settings."""

    huggingface_model_reference: str = "Yale-LILY/brio-cnndm-uncased"
        
        
class SumModelParamsFrDe(SumModelParams):
    """French/German Summarization model settings."""

    huggingface_model_reference: str = "ctu-aic/mbart25-multilingual-summarization-multilarge-cs"

        
class SumModelParamsEs(SumModelParams):
    """Spanish Summarization model settings."""

    huggingface_model_reference: str = "knkarthick/MEETING_SUMMARY"


class SumModelParamsCa(SumModelParams):
    """Catalan Summarization model settings."""

    huggingface_model_reference: str = "ELiRF/NASCA"


class SumModelParamsIt(SumModelParams):
    """Italian Summarization model settings."""

    huggingface_model_reference: str = "morenolq/bart-it-fanpage"


class TrackedSumModelCard(TrackedModelCard):
    """The model cards for the model of the multilingual Summarization ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params_en: SumModelParamsEn = SumModelParamsEn()
    model_params_frde: SumModelParamsFrDe = SumModelParamsFrDe()
    model_params_es: SumModelParamsEs = SumModelParamsEs()
    model_params_ca: SumModelParamsCa = SumModelParamsCa()
    model_params_it: SumModelParamsIt = SumModelParamsIt()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "sum_model_artifacts")
    logging_level: str = "INFO"

    en_model_subdirectory: str = "/en_sum"
    frde_model_subdirectory: str = "/frde_sum"
    es_model_subdirectory: str = "/es_sum"
    ca_model_subdirectory: str = "/ca_sum"
    it_model_subdirectory: str = "/it_sum"
    
    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"