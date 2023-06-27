package com.scienceminer.nerd.service;

import com.scienceminer.nerd.disambiguation.DocumentContext;
import com.scienceminer.nerd.disambiguation.NerdContext;
import com.scienceminer.nerd.disambiguation.NerdEngine;
import com.scienceminer.nerd.disambiguation.NerdEntity;
import com.scienceminer.nerd.disambiguation.util.*;
import com.scienceminer.nerd.exceptions.QueryException;
import com.scienceminer.nerd.kb.Property;
import com.scienceminer.nerd.main.data.SoftwareInfo;
import com.scienceminer.nerd.mention.Mention;
import com.scienceminer.nerd.mention.ProcessText;
import com.scienceminer.nerd.utilities.Filter;
import com.scienceminer.nerd.utilities.Utilities;

import org.grobid.core.data.BibDataSet;
import org.grobid.core.data.BiblioItem;
import org.grobid.core.document.Document;
import org.grobid.core.document.DocumentPiece;
import org.grobid.core.document.DocumentSource;
import org.grobid.core.document.DocumentPointer;
import org.grobid.core.engines.Engine;
import org.grobid.core.engines.FullTextParser;
import org.grobid.core.engines.config.GrobidAnalysisConfig;
import org.grobid.core.engines.label.SegmentationLabels;
import org.grobid.core.engines.label.TaggingLabel;
import org.grobid.core.engines.label.TaggingLabels;
import org.grobid.core.engines.EngineParsers;
import org.grobid.core.factory.GrobidFactory;
import org.grobid.core.lang.Language;
import org.grobid.core.layout.LayoutToken;
import org.grobid.core.layout.LayoutTokenization;
import org.grobid.core.main.LibraryLoader;
import org.grobid.core.utilities.*;

import com.google.inject.Inject;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.InputStream;
import java.util.*;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.io.FileUtils;
import org.apache.commons.lang3.StringUtils;

import static com.scienceminer.nerd.utilities.StringProcessor.isAllUpperCase;
import static org.apache.commons.lang3.StringUtils.isNotBlank;
import static org.apache.commons.lang3.StringUtils.lowerCase;
import org.apache.commons.lang3.tuple.Pair;

public class NerdRestProcessFile {

    private static final Logger LOGGER = LoggerFactory.getLogger(NerdRestProcessFile.class);
    NerdRestProcessQuery nerdRestProcessQuery = new NerdRestProcessQuery();
    SoftwareInfo softwareInfo = SoftwareInfo.getInstance();

    @Inject
    public NerdRestProcessFile() {
    }

    /**
     * Parse a structured query in combination with a PDF file and return the corresponding
     * normalized enriched and disambiguated query object, where resulting entities include
     * position coordinates in the PDF.
     *
     * @param theQuery    the POJO query object
     * @param inputStream the PDF file as InputStream
     * @return a response query object containing the structured representation of
     * the enriched and disambiguated query.
     */
    public String processQueryAndPdfFile(String theQuery, final InputStream inputStream) {
        System.out.println(methodLogIn());
        File originFile = null;
        Engine engine = null;
        System.out.println(">> received query to process: " + theQuery);

        engine = GrobidFactory.getInstance().getEngine();
        originFile = IOUtilities.writeInputFile(inputStream);
        System.out.println(">> input PDF file saved locally...");

        GrobidAnalysisConfig config = new GrobidAnalysisConfig.GrobidAnalysisConfigBuilder().consolidateHeader(1).build();
        if (originFile == null || FileUtils.sizeOf(originFile) == 0) {
            throw new QueryException("The PDF file is empty or null", QueryException.FILE_ISSUE);
        }
        long start = System.currentTimeMillis();
        NerdQuery nerdQuery = NerdQuery.fromJson(theQuery);

        if (nerdQuery == null || isNotBlank(nerdQuery.getText()) || isNotBlank(nerdQuery.getShortText())) {
            throw new QueryException("Query with PDF shall not have the field text or shortText filled in.");
        }
        System.out.println(">> set query object...");

        Language lang = nerdQuery.getLanguage();
        if (nerdQuery.hasValidLanguage()) {
            lang.setConf(1.0);
            System.out.println(">> language provided in query: " + lang);
        } 

        /* the code for validation has been moved in nerdRestProcessQuery.markUserEnteredEntities() */

        // we assume for the moment that there are no entities originally set in the query
        // however, it would be nice to have them specified with coordinates and map
        // them to their right layout tokens when processing the PDF (as done for
        // instance in the project grobid-astro)

        // tuning the species only mention selection
        tuneSpeciesMentions(nerdQuery);

        //checking customisation
        NerdRestProcessQuery.processCustomisation(nerdQuery);

        //List<NerdEntity> entities = originalEntities;
        Document doc = null;
        DocumentContext documentContext = new DocumentContext();
        NerdQuery workingQuery = new NerdQuery(nerdQuery);

        DocumentSource documentSource =
                DocumentSource.fromPdf(originFile, config.getStartPage(), config.getEndPage());
        doc = engine.getParsers().getSegmentationParser().processing(documentSource, config);

        // test if we consider or not document structures when fishing entities
        if ((nerdQuery.getStructure() != null) && (nerdQuery.getStructure().equals("default") || nerdQuery.getStructure().equals("full"))) {
            List<LayoutToken> allTokens = doc.getTokenizations();
            if (allTokens != null) {
                if (lang == null) {
                    StringBuilder builder = new StringBuilder();
                    int nbTok = 0;
                    for(LayoutToken token : allTokens) {
                        if (nbTok == 1000)
                            break;
                        builder.append(token.getText());
                        nbTok++;
                    }

                    LanguageUtilities languageIdentifier = LanguageUtilities.getInstance();
                    synchronized (languageIdentifier) {
                        lang = languageIdentifier.runLanguageId(builder.toString(), 2000);
                    }

                    if (lang != null) {
                        workingQuery.setLanguage(lang);
                        nerdQuery.setLanguage(lang);
                    } else {
                        LOGGER.error("Language was not specified and there was not enough text to identify it. The process might fail. ");
                    }
                }

                List<NerdEntity> newEntities = processLayoutTokenSequence(allTokens, null, workingQuery);
                if (newEntities != null) {
                    System.out.println(newEntities.size() + " nerd entities");
                }
                nerdQuery.addNerdEntities(newEntities);
            }
        } else if ( (nerdQuery.getStructure() == null) || (nerdQuery.getStructure() != null && nerdQuery.getStructure().equals("grobid"))) {
            // we applied entirely GROBID article structuring

            // we process the relevant textual content of the document
            // for refining the process based on structures, we need to filter
            // segment of interest (e.g. header, body, annex) and possibly apply
            // the corresponding model to further filter by structure types

            // from the header, we are interested in title, abstract and keywords
            SortedSet<DocumentPiece> documentParts = doc.getDocumentPart(SegmentationLabels.HEADER);
            if (documentParts != null) {
                Pair<String,List<LayoutToken>> headerFeatured = engine.getParsers().getHeaderParser().getSectionHeaderFeatured(doc, documentParts);
                String header = headerFeatured.getLeft();
                //List<LayoutToken> tokenizationHeader =
                //        Document.getTokenizationParts(documentParts, doc.getTokenizations());
                List<LayoutToken> tokenizationHeader = headerFeatured.getRight();
                String labeledResult = null;

                if (StringUtils.isNotBlank(StringUtils.trim(header))) {
                    labeledResult = engine.getParsers().getHeaderParser().label(header);

                    BiblioItem resHeader = new BiblioItem();
                    resHeader.generalResultMapping(labeledResult, tokenizationHeader);

                    if (lang == null) {
                        BiblioItem resHeaderLangIdentification = new BiblioItem();
                        engine.getParsers().getHeaderParser().resultExtraction(labeledResult, 
                                tokenizationHeader, resHeaderLangIdentification);

                        lang = identifyLanguage(resHeaderLangIdentification, doc);
                        if (lang != null) {
                            workingQuery.setLanguage(lang);
                            nerdQuery.setLanguage(lang);
                        } else {
                            LOGGER.error("Language was not specified and there was not enough text to identify it. The process might fail. ");
                        }
                    }

                    // title
                    List<LayoutToken> titleTokens = resHeader.getLayoutTokens(TaggingLabels.HEADER_TITLE);
                    if (titleTokens != null) {
                        System.out.println("Process title... ");
                        System.out.println(LayoutTokensUtil.toText(titleTokens));

                        List<NerdEntity> newEntities = processLayoutTokenSequence(titleTokens, null, workingQuery);
                        if (newEntities != null) {
                            System.out.println(newEntities.size() + " nerd entities");
                        }
                        nerdQuery.addNerdEntities(newEntities);
                    }

                    // abstract
                    List<LayoutToken> abstractTokens = resHeader.getLayoutTokens(TaggingLabels.HEADER_ABSTRACT);
                    if (abstractTokens != null) {
                        System.out.println("Process abstract...");
                        //workingQuery.setEntities(null);
                        List<NerdEntity> newEntities = processLayoutTokenSequence(abstractTokens, null, workingQuery);
                        if (newEntities != null) {
                            System.out.println(newEntities.size() + " nerd entities");
                        }

                        nerdQuery.addNerdEntities(newEntities);
                    }

                    // keywords
                    List<LayoutToken> keywordTokens = resHeader.getLayoutTokens(TaggingLabels.HEADER_KEYWORD);
                    if (keywordTokens != null) {
                        System.out.println("Process keywords...");
                        //workingQuery.setEntities(null);
                        List<NerdEntity> newEntities = processLayoutTokenSequence(keywordTokens, null, workingQuery);
                        if (newEntities != null)
                            System.out.println(newEntities.size() + " nerd entities");
                        nerdQuery.addNerdEntities(newEntities);
                    }

                    // create document context from this first pass
                    documentContext.seed(nerdQuery.getEntities(), lang);
                    nerdQuery.setEntities(null);

                    // as alternative, we should use key phrase extraction and disambiguation on the whole document
                    // to seed the document context

                    // reprocess header fields with document context
                    if (titleTokens != null) {
                        //workingQuery.setEntities(null);
                        List<NerdEntity> newEntities = processLayoutTokenSequence(titleTokens, documentContext, workingQuery);
                        if (newEntities != null) {
                            System.out.println(newEntities.size() + " nerd entities");
                            for (NerdEntity entity : newEntities) {
                                System.out.println(entity.toString());
                            }
                        }
                        nerdQuery.addNerdEntities(newEntities);
                    }
                    if (abstractTokens != null) {
                        List<NerdEntity> newEntities = processLayoutTokenSequence(abstractTokens, documentContext, workingQuery);
                        nerdQuery.addNerdEntities(newEntities);
                    }
                    if (keywordTokens != null) {
                        List<NerdEntity> newEntities = processLayoutTokenSequence(keywordTokens, documentContext, workingQuery);
                        nerdQuery.addNerdEntities(newEntities);
                    }
                }
            }

            // we can process all the body, in the future figure and table could be the
            // object of more refined processing
            documentParts = doc.getDocumentPart(SegmentationLabels.BODY);
            if (documentParts != null) {
                System.out.println("Process body...");
                // full text processing
                Pair<String, LayoutTokenization> featSeg = FullTextParser.getBodyTextFeatured(doc, documentParts);
                if (featSeg != null) {
                    // if featSeg is null, it usually means that no body segment is found in the
                    // document segmentation
                    String bodytext = featSeg.getLeft();

                    LayoutTokenization tokenizationBody = featSeg.getRight();
                    String rese = null;
                    if ((bodytext != null) && (bodytext.trim().length() > 0)) {
                        rese = engine.getParsers().getFullTextParser().label(bodytext);

                        // get out the reference, figure, table and formula markers, plus the formula
                        // the rest can be processed by NERD
                        List<TaggingLabel> toProcess = Arrays.asList(TaggingLabels.PARAGRAPH, TaggingLabels.ITEM,
                                TaggingLabels.SECTION, TaggingLabels.FIGURE, TaggingLabels.TABLE);
                        List<LayoutTokenization> documentBodyTokens =
                                FullTextParser.getDocumentFullTextTokens(toProcess, rese, tokenizationBody.getTokenization());

                        if (documentBodyTokens != null) {
                            List<NerdEntity> newEntities =
                                    processLayoutTokenSequences(documentBodyTokens, documentContext, workingQuery);
                            nerdQuery.addNerdEntities(newEntities);
                        } else
                            System.out.println("no body part?!?");
                    } else {
                        System.out.println("Fulltext model: The input to the CRF processing is empty");
                    }
                }
            }
            System.out.println(nerdQuery.getEntities().size() + " nerd entities in NerdQuery");
            System.out.println(workingQuery.getEntities().size() + " nerd entities in workingQuery");
            // we process references if required
            if (nerdQuery.getMentions().contains(ProcessText.MentionMethod.grobid)) {
                List<BibDataSet> resCitations = engine.getParsers().getCitationParser().
                        processingReferenceSection(doc, engine.getParsers().getReferenceSegmenterParser(), 1);
                if ((resCitations != null) && (resCitations.size() > 0)) {
                    List<NerdEntity> newEntities = processCitations(resCitations, doc, workingQuery);
                    if (newEntities != null)
                        System.out.println(newEntities.size() + " citation entities");
                    nerdQuery.addNerdEntities(newEntities);
                }
            }
            System.out.println(nerdQuery.getEntities().size() + " nerd entities in NerdQuery");
            System.out.println(workingQuery.getEntities().size() + " nerd entities in workingQuery");
            // acknowledgement
            documentParts = doc.getDocumentPart(SegmentationLabels.ACKNOWLEDGEMENT);
            if (documentParts != null) {
                System.out.println("Process acknowledgement...");
                workingQuery.setEntities(null);
                List<NerdEntity> newEntities = processDocumentPart(documentParts, doc, documentContext, workingQuery);
                if (newEntities != null)
                    System.out.println(newEntities.size() + " nerd entities");
                nerdQuery.addNerdEntities(newEntities);
            }
            System.out.println(nerdQuery.getEntities().size() + " nerd entities in NerdQuery");
            System.out.println(workingQuery.getEntities().size() + " nerd entities in workingQuery");
            // we can process annexes
            documentParts = doc.getDocumentPart(SegmentationLabels.ANNEX);
            if (documentParts != null) {
                System.out.println("Process annex...");
                //workingQuery.setEntities(null);
                List<NerdEntity> newEntities = processDocumentPart(documentParts, doc, documentContext, workingQuery);
                if (newEntities != null)
                    System.out.println(newEntities.size() + " nerd entities");
                nerdQuery.addNerdEntities(newEntities);
            }
            System.out.println(nerdQuery.getEntities().size() + " nerd entities in NerdQuery");
            System.out.println(workingQuery.getEntities().size() + " nerd entities in workingQuery");
            // footnotes are also relevant
            documentParts = doc.getDocumentPart(SegmentationLabels.FOOTNOTE);
            if (documentParts != null) {
                System.out.println("Process footnotes...");
                //workingQuery.setEntities(null);
                List<NerdEntity> newEntities = processDocumentPart(documentParts, doc, documentContext, workingQuery);
                if (newEntities != null)
                    System.out.println(newEntities.size() + " nerd entities");
                nerdQuery.addNerdEntities(newEntities);
            }
        } else {
            // the value of the parameter structure is nto supported
            throw new QueryException("The value of the query parameter \"structure\" is not supported fot the PDF input: " + 
                nerdQuery.getStructure());
        }

        nerdQuery.setText(null);
        nerdQuery.setShortText(null);
        nerdQuery.setTokens(null);

        long end = System.currentTimeMillis();
        IOUtilities.removeTempFile(originFile);
        nerdQuery.setRuntime(end - start);
        // for metadata
        nerdQuery.setSoftware(softwareInfo.getName());
        nerdQuery.setVersion(softwareInfo.getVersion());
        nerdQuery.setDate(java.time.Clock.systemUTC().instant().toString());

        System.out.println("runtime: " + (end - start));
        if (CollectionUtils.isNotEmpty(nerdQuery.getEntities())) {
            Collections.sort(nerdQuery.getEntities(), new SortEntitiesBySelectionScore());
            System.out.println(nerdQuery.getEntities().size() + " nerd entities in NerdQuery");
        }

        System.out.println(methodLogOut());
        // TODO: output in the resulting json also page info from the doc object as in GROBID
        return nerdQuery.toJSONClean(doc);
    }


    //TODO: we should move it downstream
    public static void tuneSpeciesMentions(NerdQuery nerdQuery) {
        if (nerdQuery.getMentions().contains(ProcessText.MentionMethod.species) &&
                nerdQuery.getMentions().size() == 1) {
            nerdQuery.addMention(ProcessText.MentionMethod.wikipedia);
            Filter speciesFilter = new Filter();
            Property speciesProperty = new Property();
            speciesProperty.setId("P225");
            speciesFilter.setProperty(speciesProperty);
            nerdQuery.setFilter(speciesFilter);
        }
    }

    public static Language identifyLanguage(BiblioItem resHeader, Document doc) {
        StringBuilder contentSample = new StringBuilder();
        if (resHeader.getTitle() != null) {
            contentSample.append(resHeader.getTitle());
        }
        if (resHeader.getAbstract() != null) {
            contentSample.append("\n");
            contentSample.append(resHeader.getAbstract());
        }
        if (resHeader.getKeywords() != null) {
            contentSample.append("\n");
            contentSample.append(resHeader.getKeywords());
        }
        if (contentSample.length() < 200) {
            // we can exploit more textual content to ensure that the language identification will be
            // correct
            SortedSet<DocumentPiece> documentBodyParts = doc.getDocumentPart(SegmentationLabels.BODY);
            if (documentBodyParts != null) {
                StringBuilder contentBuffer = new StringBuilder();
                for (DocumentPiece docPiece : documentBodyParts) {
                    DocumentPointer dp1 = docPiece.getLeft();
                    DocumentPointer dp2 = docPiece.getRight();

                    int tokens = dp1.getTokenDocPos();
                    int tokene = dp2.getTokenDocPos();
                    for (int i = tokens; i < tokene; i++) {
                        contentBuffer.append(doc.getTokenizations().get(i));
                        contentBuffer.append(" ");
                    }
                }
                contentSample.append(" ");
                contentSample.append(contentBuffer.toString());
            }
        }
        LanguageUtilities languageIdentifier = LanguageUtilities.getInstance();

        Language resultLang = null;
        synchronized (languageIdentifier) {
            resultLang = languageIdentifier.runLanguageId(contentSample.toString(), 2000);
        }

        return resultLang;
    }

    /**
     * Generate a global context for a document
     */
    public static NerdContext getGlobalContext(NerdQuery query) {
        // TODO
        return null;
    }

    private List<NerdEntity> processLayoutTokenSequences(List<LayoutTokenization> layoutTokenizations,
                                                         NerdContext documentContext,
                                                         NerdQuery workingQuery) {
        // text of the selected segment
        List<NerdEntity> resultingEntities = new ArrayList<>();

        ProcessText processText = ProcessText.getInstance();
        NerdEngine disambiguator = NerdEngine.getInstance();

        for (LayoutTokenization layoutTokenization : layoutTokenizations) {
            List<LayoutToken> layoutTokens = layoutTokenization.getTokenization();

            workingQuery.setEntities(null);
            workingQuery.setText(null);
            workingQuery.setShortText(null);
            workingQuery.setTokens(layoutTokens);
            workingQuery.setContext(documentContext);

            try {
                // ner
                List<Mention> nerEntities = processText.process(workingQuery);

                // TODO: this should not be done at this place for all segments (this is quite costly), 
                // but before when dealing with explicit HEADER_TITLE, or by passing a parameter indicating 
                // that the token sequence is a title - or better a possibly full upper case sequence, 
                // because this is probably relevant to more than just title 
                if (isTitle(layoutTokens) && needToLowerCase(layoutTokens)) {
                    for (Mention nerEntity : nerEntities) {
                        nerEntity.setNormalisedName(lowerCase(nerEntity.getRawName()));
                    }
                }

                // inject explicit acronyms
                nerEntities = processText.acronymCandidates(workingQuery, nerEntities);

                workingQuery.setAllEntities(nerEntities);

                if (workingQuery.getEntities() != null) {

                    // sort the entities
                    //Collections.sort(workingQuery.getEntities());
                    Collections.sort(workingQuery.getEntities(), new SortEntitiesBySelectionScore());
                    // disambiguate and solve entity mentions
                    List<NerdEntity> disambiguatedEntities = disambiguator.disambiguate(workingQuery);
                    workingQuery.setEntities(disambiguatedEntities);
                    for (NerdEntity entity : workingQuery.getEntities()) {
                        entity.setNerdScore(entity.getNer_conf());
                    }
                }

                resultingEntities.addAll(workingQuery.getEntities());
                // update document context
                if (documentContext != null)
                    ((DocumentContext) documentContext).update(workingQuery);

            } catch (Exception e) {
                LOGGER.error("An unexpected exception occurs when processing layout tokens. ", e);
            }
        }
        workingQuery.setEntities(resultingEntities);
        return workingQuery.getEntities();
    }

    protected boolean isTitle(List<LayoutToken> layoutTokens) {
        int count = 0;
        int total = 0;
        for (LayoutToken layoutToken : layoutTokens) {
            if (!TextUtilities.delimiters.contains(layoutToken.getText())) {
                if (layoutToken.getLabels().contains(TaggingLabels.HEADER_TITLE)) {
                    count++;
                }
                total++;
            }
        }

        return count == total;
    }

    private boolean needToLowerCase(List<LayoutToken> layoutTokens) {
        if (isAllUpperCase(LayoutTokensUtil.toText(layoutTokens))) {
            return true;
        } else {
            int count = 0;
            int total = 0;
            for (LayoutToken token : layoutTokens) {
                final String tokenText = token.getText();
                if (!TextUtilities.fullPunctuations.contains(tokenText)) {
                    total++;

                    if (tokenText.length() == 1) {
                        if (TextUtilities.isAllUpperCase(tokenText)) {
                            count++;
                        }
                    } else if (tokenText.length() > 1) {
                        if (Character.isUpperCase(tokenText.charAt(0))
                                && TextUtilities.isAllLowerCase(tokenText.substring(1, tokenText.length()))) {
                            count++;
                        }
                    }
                }
            }
            if (count == total) {
                return true;
            }
        }
        return false;
    }

    private List<NerdEntity> processLayoutTokenSequence(List<LayoutToken> layoutTokens,
                                                        NerdContext documentContext,
                                                        NerdQuery workingQuery) {
        List<LayoutTokenization> layoutTokenizations = new ArrayList<>();
        layoutTokenizations.add(new LayoutTokenization(layoutTokens));
        return processLayoutTokenSequences(layoutTokenizations, documentContext, workingQuery);
    }

    private List<NerdEntity> processDocumentPart(SortedSet<DocumentPiece> documentParts,
                                                 Document doc,
                                                 NerdContext documentContext,
                                                 NerdQuery workingQuery) {
        List<LayoutToken> tokenizationParts = Document.getTokenizationParts(documentParts, doc.getTokenizations());
        return processLayoutTokenSequence(tokenizationParts, documentContext, workingQuery);
    }

    private List<NerdEntity> processCitations(List<BibDataSet> resCitations,
                                              Document doc,
                                              NerdQuery workingQuery) {
        return NerdEngine.getInstance().solveCitations(resCitations);
    }

    public static String methodLogIn() {
        return ">> " + NerdRestProcessFile.class.getName() + "." +
                Thread.currentThread().getStackTrace()[1].getMethodName();
    }

    public static String methodLogOut() {
        return "<< " + NerdRestProcessFile.class.getName() + "." +
                Thread.currentThread().getStackTrace()[1].getMethodName();
    }

}
