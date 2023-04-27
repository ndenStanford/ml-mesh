package com.scienceminer.nerd.mention;

import com.scienceminer.nerd.disambiguation.NerdContext;
import com.scienceminer.nerd.service.NerdQuery;
import com.scienceminer.nerd.utilities.StringPos;
import com.scienceminer.nerd.utilities.Utilities;
import com.scienceminer.nerd.utilities.Stopwords;
import org.grobid.core.utilities.OffsetPosition;
import org.grobid.core.utilities.UnicodeUtil;
import org.grobid.core.analyzers.GrobidAnalyzer;
import org.grobid.core.lang.Language;
import org.grobid.core.layout.LayoutToken;
import org.grobid.core.utilities.Pair;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;

import java.io.*;
import java.util.*;
import java.util.prefs.PreferenceChangeEvent;
import java.util.stream.Collector;
import java.util.stream.Collectors;

import static org.hamcrest.CoreMatchers.*;
import static org.hamcrest.Matchers.greaterThan;
import static org.hamcrest.Matchers.hasSize;
import static org.junit.Assert.*;

public class ProcessTextTest {
    private ProcessText processText = null;

    static final String testText = "Other factors were also at play, said Felix Boni, head of research at " +
            "James Capel in Mexico City, such as positive technicals and economic uncertainty in Argentina, " +
            "which has put it and neighbouring Brazil's markets at risk.";

    @Before
    public void setUp() throws Exception {
        processText = ProcessText.getInstance();
    }

    @Test
    @Ignore("This test is for sentence segmention method.")
    public void testSentenceSegmentation() {
        // set the resource for the sentence segmentation since tokenizer need this resource
        InputStream inputFile = this.getClass().getResourceAsStream("dictionary-1.3.1.zip");

        //AbstractTokenizer tokenizer = EngineGetter.getTokenizer("en", inputFile);

        String text = "Austria invaded and fought the Serbian army at the Battle of Cer and Battle of Kolubara beginning on 12 August. \n\nThe army, led by general Paul von Hindenburg defeated Russia in a series of battles collectively known as the First Battle of Tannenberg (17 August – 2 September). But the failed Russian invasion, causing the fresh German troops to move to the east, allowed the tactical Allied victory at the First Battle of the Marne. \n\nUnfortunately for the Allies, the pro-German King Constantine I dismissed the pro-Allied government of E. Venizelos before the Allied expeditionary force could arrive. Beginning in 1915, the Italians under Cadorna mounted eleven offensives on the Isonzo front along the Isonzo River, northeast of Trieste.\\n\\n At the Siege of Maubeuge about 40000 French soldiers surrendered, at the battle of Galicia Russians took about 100-120000 Austrian captives, at the Brusilov Offensive about 325 000 to 417 000 Germans and Austrians surrendered to Russians, at the Battle of Tannenberg 92,000 Russians surrendered.\n\n After marching through Belgium, Luxembourg and the Ardennes, the German Army advanced, in the latter half of August, into northern France where they met both the French army, under Joseph Joffre, and the initial six divisions of the British Expeditionary Force, under Sir John French. A series of engagements known as the Battle of the Frontiers ensued. Key battles included the Battle of Charleroi and the Battle of Mons.";

        //processText.setTokenizer(tokenizer);
        List<Sentence> sentences = processText.sentenceSegmentation(text);

        assertThat(sentences, hasSize(9));

        Sentence sentence0 = sentences.get(0);
        assertThat(sentence0.getOffsetStart(),is(0));
        assertThat(sentence0.getOffsetEnd(),is(111));
        assertThat(text.substring(sentence0.getOffsetStart(), sentence0.getOffsetEnd()), is("Austria invaded and fought the Serbian army at the Battle of Cer and Battle of Kolubara beginning on 12 August."));

        Sentence sentence1 = sentences.get(1);
        assertThat(sentence1.getOffsetStart(),is(114));
        assertThat(sentence1.getOffsetEnd(),is(277));
        assertThat(text.substring(sentence1.getOffsetStart(), sentence1.getOffsetEnd()), is("The army, led by general Paul von Hindenburg defeated Russia in a series of battles collectively known as the First Battle of Tannenberg (17 August – 2 September)."));

        Sentence sentence2 = sentences.get(2);
        assertThat(sentence2.getOffsetStart(),is(278));
        assertThat(sentence2.getOffsetEnd(),is(433));
        assertThat(text.substring(sentence2.getOffsetStart(), sentence2.getOffsetEnd()), is("But the failed Russian invasion, causing the fresh German troops to move to the east, allowed the tactical Allied victory at the First Battle of the Marne."));

        Sentence sentence3 = sentences.get(3);
        assertThat(sentence3.getOffsetStart(),is(436));
        assertThat(sentence3.getOffsetEnd(),is(603));
        assertThat(text.substring(sentence3.getOffsetStart(), sentence3.getOffsetEnd()), is("Unfortunately for the Allies, the pro-German King Constantine I dismissed the pro-Allied government of E. Venizelos before the Allied expeditionary force could arrive."));

        Sentence sentence4 = sentences.get(4);
        assertThat(sentence4.getOffsetStart(),is(604));
        assertThat(sentence4.getOffsetEnd(),is(741));
        assertThat(text.substring(sentence4.getOffsetStart(), sentence4.getOffsetEnd()), is("Beginning in 1915, the Italians under Cadorna mounted eleven offensives on the Isonzo front along the Isonzo River, northeast of Trieste."));

    }

    @Test
    public void testAcronymsStringAllLower() {
        String input = "A graphical model or probabilistic graphical model (PGM) is a probabilistic model.";

        Map<Mention, Mention> acronyms = processText.acronymCandidates(input, new Language("en", 1.0));
        assertNotNull(acronyms);
        for (Map.Entry<Mention, Mention> entry : acronyms.entrySet()) {
            Mention base = entry.getValue();
            Mention acronym = entry.getKey();
            assertEquals(input.substring(acronym.getOffsetStart(), acronym.getOffsetEnd()).trim(), "PGM");
            assertEquals(base.getRawName(), "probabilistic graphical model");
        }
    }

    @Test
    @Ignore("Not yet finished")
    public void testAcronymCandidates() {
        String input = "We are working with Pulse Calculation Tarmac (P.C.T.) during our discovery on science";

        final Map<Mention, Mention> acronyms = processText.acronymCandidates(input, new Language("en"));

        assertThat(acronyms.keySet(), hasSize(1));
    }

    @Test
    public void testAcronymsTokensAllLower() {
        String input = "A graphical model or probabilistic graphical model (PGM) is a probabilistic model.";
        List<LayoutToken> tokens = GrobidAnalyzer.getInstance().tokenizeWithLayoutToken(input, new Language("en", 1.0));
        Map<Mention, Mention> acronyms = processText.acronymCandidates(tokens);
        assertThat(acronyms.entrySet(), hasSize(1));

        final ArrayList<Mention> keys = new ArrayList<>(acronyms.keySet());
        final Mention shortAcronym = keys.get(0);
        final Mention extendedAcronym = acronyms.get(shortAcronym);

        assertThat(extendedAcronym.getRawName(), is("probabilistic graphical model"));
        assertThat(input.substring(shortAcronym.getOffsetStart(), shortAcronym.getOffsetEnd()), is("PGM"));
    }

    @Test
    public void testAcronymsTokens() {
        String input = "Figure 4. \n" +
                "Canonical Correspondence Analysis (CCA) diagram showing the ordination of anopheline species along the\n" +
                "first two axes and their correlation with environmental variables. The first axis is horizontal, second vertical. Direction\n" +
                "and length of arrows shows the degree of correlation between mosquito larvae and the variables.";
        List<LayoutToken> tokens = GrobidAnalyzer.getInstance().tokenizeWithLayoutToken(input, new Language("en", 1.0));
        Map<Mention, Mention> acronyms = processText.acronymCandidates(tokens);

        assertNotNull(acronyms);
        for (Map.Entry<Mention, Mention> entry : acronyms.entrySet()) {
            Mention base = entry.getValue();
            Mention acronym = entry.getKey();

            assertEquals(input.substring(acronym.getOffsetStart(), acronym.getOffsetEnd()).trim(), "CCA");
            assertEquals(base.getRawName(), "Canonical Correspondence Analysis");

            assertThat(acronym.getOffsetStart(), is(46));
            assertThat(acronym.getOffsetEnd(), is(49));
        }
    }

    @Test
    public void testPropagateAcronyms_textSyncronisedWithLayoutTokens_shouldWork() {
        String input = "The Pulse Covariant Transmission (PCT) is a great deal. We are going to make it great again.\n " +
                "We propose a new methodology where the PCT results are improving in the gamma ray action matter.";
        final Language language = new Language("en");
        List<LayoutToken> tokens = GrobidAnalyzer.getInstance().tokenizeWithLayoutToken(input, language);

        NerdQuery aQuery = new NerdQuery();
        aQuery.setText(input);
        aQuery.setTokens(tokens);

        final HashMap<Mention, Mention> acronyms = new HashMap<>();
        Mention base = new Mention("Pulse Covariant Transmission");
        base.setOffsetStart(4);
        base.setOffsetEnd(32);
        final LayoutToken baseLayoutToken1 = new LayoutToken("Pulse");
        baseLayoutToken1.setOffset(4);
        final LayoutToken baseLayoutToken2 = new LayoutToken(" ");
        baseLayoutToken2.setOffset(9);
        final LayoutToken baseLayoutToken3 = new LayoutToken("Covariant");
        baseLayoutToken3.setOffset(10);
        final LayoutToken baseLayoutToken4 = new LayoutToken(" ");
        baseLayoutToken4.setOffset(19);
        final LayoutToken baseLayoutToken5 = new LayoutToken("Transmission");
        baseLayoutToken5.setOffset(20);
        final LayoutToken baseLayoutToken6 = new LayoutToken(" ");
        baseLayoutToken6.setOffset(21);

        Mention acronym = new Mention("PCT");
        acronym.setNormalisedName("Pulse Covariant Transmission");
        acronym.setOffsetStart(34);
        acronym.setOffsetEnd(37);
        acronym.setIsAcronym(true);
        final LayoutToken acronymLayoutToken = new LayoutToken("PCT");
        acronymLayoutToken.setOffset(34);
        acronym.setLayoutTokens(Arrays.asList(acronymLayoutToken));

        acronyms.put(acronym, base);

        final NerdContext nerdContext = new NerdContext();
        nerdContext.setAcronyms(acronyms);
        aQuery.setContext(nerdContext);

        final List<Mention> mentions = processText.propagateAcronyms(aQuery);
        assertThat(mentions, hasSize(1));
        assertThat(mentions.get(0).getRawName(), is("PCT"));
        assertThat(mentions.get(0).getOffsetStart(), is(133));
        assertThat(mentions.get(0).getOffsetEnd(), is(136));
        assertThat(mentions.get(0).getLayoutTokens(), is(Arrays.asList(tokens.get(53))));
//        assertThat(mentions.get(0).getBoundingBoxes(), hasSize(greaterThan(0)));
    }

    @Test
    public void testPropagateAcronyms_textNotSyncronisedWithLayoutTokens_shouldWork() {
        String input = "The Pulse Covariant Transmission (PCT) is a great deal. We are going to make it great again.\n " +
                "We propose a new methodology where the PCT results are improving in the gamma ray action matter.";
        final Language language = new Language("en");
        List<LayoutToken> tokens = GrobidAnalyzer.getInstance().tokenizeWithLayoutToken(input, language);
        tokens = tokens.stream()
                .map(layoutToken -> {
                    layoutToken.setOffset(layoutToken.getOffset() + 10);
                    layoutToken.setX(22.3);
                    layoutToken.setY(22.3);
                    layoutToken.setWidth(10);
                    layoutToken.setHeight(30);
                    return layoutToken;
                }).collect(Collectors.toList());

        NerdQuery aQuery = new NerdQuery();
        aQuery.setText(input);
        aQuery.setTokens(tokens);

        final HashMap<Mention, Mention> acronyms = new HashMap<>();
        Mention base = new Mention("Pulse Covariant Transmission");
        base.setOffsetStart(14);
        base.setOffsetEnd(42);
        final LayoutToken baseLayoutToken1 = new LayoutToken("Pulse");
        baseLayoutToken1.setOffset(4);
        final LayoutToken baseLayoutToken2 = new LayoutToken(" ");
        baseLayoutToken2.setOffset(9);
        final LayoutToken baseLayoutToken3 = new LayoutToken("Covariant");
        baseLayoutToken3.setOffset(10);
        final LayoutToken baseLayoutToken4 = new LayoutToken(" ");
        baseLayoutToken4.setOffset(19);
        final LayoutToken baseLayoutToken5 = new LayoutToken("Transmission");
        baseLayoutToken5.setOffset(20);
        final LayoutToken baseLayoutToken6 = new LayoutToken(" ");
        baseLayoutToken6.setOffset(21);

        Mention acronym = new Mention("PCT");
        acronym.setNormalisedName("Pulse Covariant Transmission");
        acronym.setOffsetStart(44);
        acronym.setOffsetEnd(47);
        acronym.setIsAcronym(true);
        final LayoutToken acronymLayoutToken = new LayoutToken("PCT");
        acronymLayoutToken.setOffset(44);
        acronym.setLayoutTokens(Arrays.asList(acronymLayoutToken));

        acronyms.put(acronym, base);

        final NerdContext nerdContext = new NerdContext();
        nerdContext.setAcronyms(acronyms);
        aQuery.setContext(nerdContext);

        final List<Mention> mentions = processText.propagateAcronyms(aQuery);
        assertThat(mentions, hasSize(1));
        assertThat(mentions.get(0).getRawName(), is("PCT"));
        assertThat(mentions.get(0).getOffsetStart(), is(143));
        assertThat(mentions.get(0).getOffsetEnd(), is(146));
        assertThat(mentions.get(0).getBoundingBoxes(), hasSize(greaterThan(0)));
        assertThat(mentions.get(0).getLayoutTokens(), is(Arrays.asList(tokens.get(53))));
    }

    @Test
    public void testPropagateAcronyms_textNotSyncronisedWithLayoutTokens2_shouldWork() {
        String input = "The Pulse Covariant Transmission (P.C.T.) is a great deal. We are going to make it great again.\n " +
                "We propose a new methodology where the P.C.T. results are improving in the gamma ray action matter. " +
                "P.C.T. is good for you";
        final Language language = new Language("en");
        List<LayoutToken> tokens = GrobidAnalyzer.getInstance().tokenizeWithLayoutToken(input, language);
        tokens = tokens.stream()
                .map(layoutToken -> {
                    layoutToken.setOffset(layoutToken.getOffset() + 10);
                    return layoutToken;
                }).collect(Collectors.toList());

        NerdQuery aQuery = new NerdQuery();
        aQuery.setText(input);
        aQuery.setTokens(tokens);

        final HashMap<Mention, Mention> acronyms = new HashMap<>();
        Mention base = new Mention("Pulse Covariant Transmission");
        base.setOffsetStart(14);
        base.setOffsetEnd(42);
        final LayoutToken baseLayoutToken1 = new LayoutToken("Pulse");
        baseLayoutToken1.setOffset(4);
        final LayoutToken baseLayoutToken2 = new LayoutToken(" ");
        baseLayoutToken2.setOffset(9);
        final LayoutToken baseLayoutToken3 = new LayoutToken("Covariant");
        baseLayoutToken3.setOffset(10);
        final LayoutToken baseLayoutToken4 = new LayoutToken(" ");
        baseLayoutToken4.setOffset(19);
        final LayoutToken baseLayoutToken5 = new LayoutToken("Transmission");
        baseLayoutToken5.setOffset(20);
        final LayoutToken baseLayoutToken6 = new LayoutToken(" ");
        baseLayoutToken6.setOffset(21);

        Mention acronym = new Mention("P.C.T.");
        acronym.setNormalisedName("Pulse Covariant Transmission");
        acronym.setOffsetStart(44);
        acronym.setOffsetEnd(47);
        acronym.setIsAcronym(true);
        final LayoutToken acronymLayoutToken1 = new LayoutToken("P");
        acronymLayoutToken1.setOffset(44);
        final LayoutToken acronymLayoutToken2 = new LayoutToken(".");
        acronymLayoutToken2.setOffset(45);
        final LayoutToken acronymLayoutToken3 = new LayoutToken("C");
        acronymLayoutToken3.setOffset(46);
        final LayoutToken acronymLayoutToken4 = new LayoutToken(".");
        acronymLayoutToken4.setOffset(47);
        final LayoutToken acronymLayoutToken5 = new LayoutToken("T");
        acronymLayoutToken5.setOffset(48);
        final LayoutToken acronymLayoutToken6 = new LayoutToken(".");
        acronymLayoutToken6.setOffset(49);

        acronym.setLayoutTokens(Arrays.asList(acronymLayoutToken1, acronymLayoutToken2,
                acronymLayoutToken3, acronymLayoutToken4, acronymLayoutToken5, acronymLayoutToken6));

        acronyms.put(acronym, base);

        final NerdContext nerdContext = new NerdContext();
        nerdContext.setAcronyms(acronyms);
        aQuery.setContext(nerdContext);

        final List<Mention> mentions = processText.propagateAcronyms(aQuery);
        assertThat(mentions, hasSize(2));
        assertThat(mentions.get(0).getRawName(), is("P.C.T."));
        assertThat(mentions.get(0).getOffsetStart(), is(146));
        assertThat(mentions.get(0).getOffsetEnd(), is(152));
//        assertThat(mentions.get(0).getBoundingBoxes(), hasSize(greaterThan(0)));
        assertThat(mentions.get(0).getLayoutTokens(), hasSize(6));

        assertThat(mentions.get(1).getRawName(), is("P.C.T."));
        assertThat(mentions.get(1).getOffsetStart(), is(207));
        assertThat(mentions.get(1).getOffsetEnd(), is(213));
//        assertThat(mentions.get(1).getBoundingBoxes(), hasSize(greaterThan(0)));
        assertThat(mentions.get(1).getLayoutTokens(), hasSize(6));
    }


    @Test
    public void testAcronymsStringMixedCase() {
        String input = "Cigarette smoke (CS)-induced airway epithelial senescence has been implicated in " +
                "the pathogenesis of chronic obstructive pulmonary disease (COPD).";

        Map<Mention, Mention> acronyms = processText.acronymCandidates(input, new Language("en", 1.0));
        assertNotNull(acronyms);
        for (Map.Entry<Mention, Mention> entry : acronyms.entrySet()) {
            Mention base = entry.getValue();
            Mention acronym = entry.getKey();
//System.out.println("acronym: " + input.substring(acronym.start, acronym.end) + " / base: " + base.getRawName());
            if (input.substring(acronym.getOffsetStart(), acronym.getOffsetEnd()).trim().equals("CS")) {
                assertEquals(base.getRawName(), "Cigarette smoke");
            } else {
                assertEquals(input.substring(acronym.getOffsetStart(), acronym.getOffsetEnd()).trim(), "COPD");
                assertEquals(base.getRawName(), "chronic obstructive pulmonary disease");
            }
        }
    }

    @Test
    public void testAcronymsTokensMixedCase() {
        String input = "Cigarette smoke (CS)-induced airway epithelial senescence has been implicated in " +
                "the pathogenesis of chronic obstructive pulmonary disease (COPD).";
        List<LayoutToken> tokens = GrobidAnalyzer.getInstance().tokenizeWithLayoutToken(input, new Language("en", 1.0));
        Map<Mention, Mention> acronyms = processText.acronymCandidates(tokens);
        assertNotNull(acronyms);
        for (Map.Entry<Mention, Mention> entry : acronyms.entrySet()) {
            Mention base = entry.getValue();
            Mention acronym = entry.getKey();
//System.out.println("acronym: " + input.substring(acronym.start, acronym.end) + " / base: " + base.getRawName());
            if (input.substring(acronym.getOffsetStart(), acronym.getOffsetEnd()).trim().equals("CS")) {
                assertEquals(base.getRawName(), "Cigarette smoke");
            } else {
                assertEquals(input.substring(acronym.getOffsetStart(), acronym.getOffsetEnd()).trim(), "COPD");
                assertEquals(base.getRawName(), "chronic obstructive pulmonary disease");
            }
        }
    }

    //@Test
    public void testDICECoefficient() throws Exception {
        String mention = "Setophaga ruticilla";
        Double dice = ProcessText.getDICECoefficient(mention, "en");
        System.out.println(mention + ": " + dice);

        mention = "Setophaga";
        dice = ProcessText.getDICECoefficient(mention, "en");
        System.out.println(mention + ": " + dice);

        mention = "ruticilla";
        dice = ProcessText.getDICECoefficient(mention, "en");
        System.out.println(mention + ": " + dice);

        mention = "bird";
        dice = ProcessText.getDICECoefficient(mention, "en");
        System.out.println(mention + ": " + dice);

        mention = "washing machine";
        dice = ProcessText.getDICECoefficient(mention, "en");
        System.out.println(mention + ": " + dice);

        mention = "washing";
        dice = ProcessText.getDICECoefficient(mention, "en");
        System.out.println(mention + ": " + dice);

        mention = "machine";
        dice = ProcessText.getDICECoefficient(mention, "en");
        System.out.println(mention + ": " + dice);
    }

    /*@Test
    public void testProcessSpecies() throws Exception {
        List<Mention> entities = processText.processSpecies("The mouse is here with us, beware not to be too aggressive.",
                new Language("en"));

        assertThat(entities, hasSize(1));
    }*/

    /*@Test
    public void testProcessSpecies2() {
        if (processText == null) {
            System.err.println("text processor was not properly initialised!");
        }
        try {
            List<Mention> entities = processText.processSpecies("Morphological variation in hybrids between Salmo marmoratus and alien Salmo species in the Volarja stream, Soca River basin, Slovenia", 
                new Language("en"));

            assertThat(entities, hasSize(1));
        } catch(Exception e) {
            e.printStackTrace();
        }
    }*/


    @Test
    public void testParagraphSegmentation() {
        // create a dummy super long text to be segmented
        List<LayoutToken> tokens = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            if (i == 250) {
                tokens.add(new LayoutToken("\n"));
            }
            if (i == 500) {
                tokens.add(new LayoutToken("\n"));
                tokens.add(new LayoutToken("\n"));
            }
            tokens.add(new LayoutToken("blabla"));
            tokens.add(new LayoutToken(" "));
        }

        List<List<LayoutToken>> segments = ProcessText.segmentInParagraphs(tokens);
        assertThat(segments, hasSize(12));
    }

    @Test
    public void testGetSequenceMatch_singleTokenAcronym_shouldWork() throws Exception {

        String text = "We are proving that the PCT is working fine. PCT will work just fine.";

        final List<LayoutToken> tokens = GrobidAnalyzer.getInstance().tokenizeWithLayoutToken(text);

        final LayoutToken pct = new LayoutToken("PCT");
        pct.setOffset(24);
            final List<LayoutToken> sequenceMatch = processText.getSequenceMatch(tokens, 19, Arrays.asList(pct));
        assertThat(sequenceMatch, hasSize(1));
        assertThat(sequenceMatch.get(0), is(tokens.get(19)));
    }

    @Test
    public void testGetSequenceMatch_multiTokenAcronym_shouldWork() throws Exception {

        String text = "We are proving that the P.C.T. is working fine. P.C.T. will work just fine.";

        final List<LayoutToken> tokens = GrobidAnalyzer.getInstance().tokenizeWithLayoutToken(text);

        final LayoutToken acronymLayoutToken1 = new LayoutToken("P");
        acronymLayoutToken1.setOffset(24);
        final LayoutToken acronymLayoutToken2 = new LayoutToken(".");
        acronymLayoutToken2.setOffset(25);
        final LayoutToken acronymLayoutToken3 = new LayoutToken("C");
        acronymLayoutToken3.setOffset(26);
        final LayoutToken acronymLayoutToken4 = new LayoutToken(".");
        acronymLayoutToken4.setOffset(27);
        final LayoutToken acronymLayoutToken5 = new LayoutToken("T");
        acronymLayoutToken5.setOffset(28);
        final LayoutToken acronymLayoutToken6 = new LayoutToken(".");
        acronymLayoutToken6.setOffset(29);

        List<LayoutToken> layoutTokenAcronym = Arrays.asList(acronymLayoutToken1, acronymLayoutToken2,
                acronymLayoutToken3, acronymLayoutToken4, acronymLayoutToken5, acronymLayoutToken6);

        final List<LayoutToken> sequenceMatch = processText.getSequenceMatch(tokens, 24, layoutTokenAcronym);
        assertThat(sequenceMatch, hasSize(6));
        assertThat(sequenceMatch.get(0), is(tokens.get(24)));
    }

    @Test
    public void testParagraphSegmentationMonolithic() {
        // create a dummy super long text to be segmented
        List<LayoutToken> tokens = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            tokens.add(new LayoutToken("blabla"));
            tokens.add(new LayoutToken(" "));
        }

        List<List<LayoutToken>> segments = ProcessText.segmentInParagraphs(tokens);
        assertThat(segments, hasSize(9));
    }

    @Test
    @Ignore("This test is failing")
    public void testNGram_old_oneGram_shouldWork() throws Exception {
        final String input = "this is it.";

        final List<StringPos> result = processText.ngrams(input, 1, new Language("en"));
        System.out.println(result);

        assertThat(result, hasSize(6));
        assertThat(result.get(0), is(new StringPos("this", 0)));
        assertThat(result.get(1), is(new StringPos(" ", 4)));
        assertThat(result.get(2), is(new StringPos("is", 5)));
        assertThat(result.get(3), is(new StringPos(" ", 7)));
    }

    @Test
    @Ignore("This test is failing too")
    public void testNGram_old_biGram_shouldWork() throws Exception {
        final String input = "this is it.";

        final List<StringPos> result = processText.ngrams(input, 2, new Language("en"));
//        System.out.println(result);

        assertThat(result, hasSize(15));
        assertThat(result.get(0), is(new StringPos("this", 0)));
        assertThat(result.get(1), is(new StringPos("this ", 0)));
        assertThat(result.get(2), is(new StringPos("this is", 0)));
        assertThat(result.get(3), is(new StringPos(" ", 4)));
    }

    @Test
    public void testNGram_LayoutTokens_oneGram_shouldWork() throws Exception {
        final String input = "this is it.";

        final List<LayoutToken> inputLayoutTokens = GrobidAnalyzer.getInstance()
                .tokenizeWithLayoutToken(input, new Language("en"));

        final List<StringPos> result = processText.ngrams(inputLayoutTokens, 1);
        System.out.println(result);

        assertThat(result, hasSize(6));
        assertThat(result.get(0), is(new StringPos("this", 0)));
        assertThat(result.get(1), is(new StringPos(" ", 4)));
        assertThat(result.get(2), is(new StringPos("is", 5)));
        assertThat(result.get(3), is(new StringPos(" ", 7)));
    }

    @Test
    @Ignore("This test is not testing anything")
    public void testNGram_twoGram_shouldWork() throws Exception {
        final String input = "this is it.";

        final List<StringPos> old = processText.ngrams(input, 2, new Language("en"));
        Collections.sort(old);
        old.remove(4);
        System.out.println(old);

        final List<StringPos> newd = processText.ngrams(GrobidAnalyzer.getInstance().tokenizeWithLayoutToken(input), 2);
        Collections.sort(newd);
        System.out.println(newd);
    }

    @Test
    @Ignore("This test is not testing anything")
    public void extractMentionsWikipedia() throws Exception {
        final String input = "this is it.";

        final Language language = new Language("en");
        final List<LayoutToken> inputLayoutTokens = GrobidAnalyzer.getInstance()
                .tokenizeWithLayoutToken(input, language);

        System.out.println(processText.extractMentionsWikipedia(inputLayoutTokens, language, null));

        //System.out.println(processText.extractMentionsWikipedia(input, language, null));
    }

    @Test
    public void segmentWithDoubleEOL() {
        final String input = "This is really not it. \n\nBut here this is it.";
        final Language language = new Language("en");
        List<OffsetPosition> segments = processText.segment(input, null, 25, language);
        assertThat(segments.size(),is(2));
        assertThat(segments.get(0).end,is(23));
    }

    @Test
    public void segmentWithSingleEOL() {
        final String input = "This is really not it. \nBut here this is it. \nAnd here again, it.";
        final Language language = new Language("en");
        List<OffsetPosition> segments = processText.segment(input, null, 25, language);
        assertThat(segments.size(),is(3));
        assertThat(segments.get(0).end,is(23));
    }

    @Test
    public void segmentWithSentences() {
        final String input = "This is really not it. But here this is it. And here again, this is it.";
        final Language language = new Language("en");
        List<OffsetPosition> segments = processText.segment(input, null, 25, language);
        assertThat(segments.size(),is(3));
        assertThat(segments.get(0).end,is(22));
    }

    @Test
    public void segmentWithEOLAndSentences() {
        final String input = "This is really not it. \nBut here this is it. And here again, this is it.";
        final Language language = new Language("en");
        List<OffsetPosition> segments = processText.segment(input, null, 25, language);
        assertThat(segments.size(),is(3));
        assertThat(segments.get(0).end,is(23));
    }

    @Test
    public void segmentWithWeird() {
        final String input = "This is really not it. \nBut here \nthis is it. \n \n \n And here again, this is it.";
        final Language language = new Language("en");
        List<OffsetPosition> segments = processText.segment(input, null, 25, language);
        /*System.out.println(input);
        for(OffsetPosition pos : segments) {
            System.out.println("" + pos.start + ", " + pos.end);
        }
        for(OffsetPosition pos : segments) {
            System.out.println("" + pos.start + ", " + pos.end);
            System.out.println(input.substring(pos.start, pos.end));
        }*/
        assertThat(segments.size(),is(4));
        assertThat(segments.get(0).end,is(23));
    }

    @Test
    public void segmentTooLongSentence() {
        final String input = "This is really not it but here, this is it and here again, this is it.";
        final Language language = new Language("en");
        List<OffsetPosition> segments = processText.segment(input, null, 25, language);
        assertThat(segments.size(),is(3));
        assertThat(segments.get(0).end,is(18));
    }

    @Test
    public void testSegmentZh() throws Exception {
        String input = "天津市由于处于海河流域下游的九河下梢，自古便建有大量各式各样的桥梁。自从2002年起，天津市开始对海河进行综合开发以后，除对原有桥梁进行修缮、提升和改造之外，还邀请英国、美国、日本等多个国家的桥梁建筑设计公司共同对天津海河的桥梁进行设计并新建了一批具有景观作用的桥梁，使得天津市区内的海河上游，平均不到0.8千米就有一座桥梁，在改善交通的同时也提升了海河的景观。现在天津海河上的“一桥一景”已经成为天津著名的旅游景观。";
        input = UnicodeUtil.normaliseText(input);

        final List<LayoutToken> inputLayoutTokens = GrobidAnalyzer.getInstance()
                .tokenizeWithLayoutToken(input, new Language("zh"));

        final List<StringPos> result = processText.ngrams(inputLayoutTokens, 1);
        System.out.println(result);

        assertThat(result, hasSize(134));
        assertThat(result.get(0), is(new StringPos("天津市", 0)));
        assertThat(result.get(1), is(new StringPos("由于", 3)));
        assertThat(result.get(2), is(new StringPos("处于", 5)));
        assertThat(result.get(3), is(new StringPos("海河", 7)));
    }

    @Test
    public void testSegmentJa() throws Exception {
        String input = "レゲエ (reggae) は狭義においては1960年代後半ジャマイカで成立し、1980年代前半まで流行した4分の4拍子の第2・第4拍目をカッティング奏法で刻むギター、各小節の3拍目にアクセントが置かれるドラム、うねるようなベースラインを奏でるベースなどの音楽的特徴を持つポピュラー音楽である。広義においてはジャマイカで成立したポピュラー音楽全般のことをいう。 ";
        input = UnicodeUtil.normaliseText(input);

        final List<LayoutToken> inputLayoutTokens = GrobidAnalyzer.getInstance()
                .tokenizeWithLayoutToken(input, new Language("ja"));

        final List<StringPos> result = processText.ngrams(inputLayoutTokens, 1);
        System.out.println(result);

        assertThat(result, hasSize(94));
        assertThat(result.get(0), is(new StringPos("レゲエ", 0)));
        assertThat(result.get(1), is(new StringPos(" ", 3)));
        assertThat(result.get(2), is(new StringPos("(", 4)));
        assertThat(result.get(3), is(new StringPos("reggae", 5)));
    }

    @Test
    public void testMentionsZh() throws Exception {
        String input = "天津市由于处于海河流域下游的九河下梢，自古便建有大量各式各样的桥梁。";
        input = UnicodeUtil.normaliseText(input);

        final List<LayoutToken> inputLayoutTokens = GrobidAnalyzer.getInstance()
                .tokenizeWithLayoutToken(input, new Language("zh"));

        List<Mention> mentions = processText.processWikipedia(inputLayoutTokens, new Language("zh"),  3);

        /*System.out.println("nb mentions: " + mentions.size());
        for(Mention mention : mentions) {
            System.out.println(mention.getRawName());
        }*/

        assertThat(mentions.size(), is(71));
    }

    @Test
    public void testMentionsJa() throws Exception {
        String input = "レゲエ (reggae) は狭義においては1960年代後半ジャマイカで成立し、1980年代前半まで流行した4分の4拍子の第2・";
        input = UnicodeUtil.normaliseText(input);

        final List<LayoutToken> inputLayoutTokens = GrobidAnalyzer.getInstance()
                .tokenizeWithLayoutToken(input, new Language("ja"));

        List<Mention> mentions = processText.processWikipedia(inputLayoutTokens, new Language("ja"), 3);

        /*System.out.println("nb mentions: " + mentions.size());
        for(Mention mention : mentions) {
            System.out.println(mention.getRawName());
        }*/

        assertThat(mentions.size(), is(103));
    }

    @Test
    public void testFrenchStopWord() throws Exception {
        String input = "l’avocat";
        Stopwords stopwords = Stopwords.getInstance();
        assertThat(stopwords.startsWithStopword(input, "fr"), is(true));
        assertThat(stopwords.endsWithStopword(input, "fr"), is(false));
    }

}