package preprocessor_java;

//package stanford_pos_tagger;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Scanner;

import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;

public class pos_tagger {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		// creates a StanfordCoreNLP object, with POS tagging, lemmatization,
		// NER, parsing, and coreference resolution
		Properties props = new Properties();
		props.put("annotators", "tokenize, ssplit, pos");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

		// read some text in the text variable

		File dir = new File(
				"test_data\\");
		File[] directoryListing = dir.listFiles();
		if (directoryListing != null) {
			for (File child : directoryListing) {

				// Do something with child
				if (child.getName().substring(child.getName().lastIndexOf("."))
						.equals(".edus")) {
					System.out.println(child.getName());
					String text = new Scanner(child).useDelimiter("\\Z").next();
					PrintWriter out = new PrintWriter(
							"test_data\\"
									.concat(child
											.getName()
											.substring(
													0,
													child.getName()
															.lastIndexOf("."))
											.concat(".pos")));

					String posTagsForText = "";
					// create an empty Annotation just with the given text
					Annotation document = new Annotation(text);

					// run all Annotators on this text
					pipeline.annotate(document);

					// these are all the sentences in this document
					// a CoreMap is essentially a Map that uses class objects as
					// keys and has values with custom types
					List<CoreMap> sentences = document
							.get(SentencesAnnotation.class);

					for (CoreMap sentence : sentences) {
						// traversing the words in the current sentence
						// a CoreLabel is a CoreMap with additional
						// token-specific
						// methods
						for (CoreLabel token : sentence
								.get(TokensAnnotation.class)) {
							// this is the text of the token
							String word = token.get(TextAnnotation.class);
							// this is the POS tag of the token
							String pos = token
									.get(PartOfSpeechAnnotation.class);
							// this is the NER label of the token
							if (!posTagsForText.equals("")) {
								posTagsForText = posTagsForText.concat("\t");
							}
							posTagsForText = posTagsForText.concat(pos);
							String ne = token
									.get(NamedEntityTagAnnotation.class);
						}
						//posTagsForText = posTagsForText.concat("\n");

						// this is the parse tree of the current sentence
//						Tree tree = sentence.get(TreeAnnotation.class);

						// this is the Stanford dependency graph of the current
						// sentence
//						SemanticGraph dependencies = sentence
//								.get(CollapsedCCProcessedDependenciesAnnotation.class);
					}
					out.println(posTagsForText);
					out.close();
				}
			}
		}
	}
}
