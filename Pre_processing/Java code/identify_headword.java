package preprocessor_java;

//package stanford_pos_tagger;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Scanner;
import java.util.Set;

import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.IndexedWord;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;

public class identify_headword {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		// creates a StanfordCoreNLP object, with POS tagging, lemmatization,
		// NER, parsing, and coreference resolution
		Properties props = new Properties();
		props.put("annotators", "tokenize, ssplit, pos, parse, lemma");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

		// read some text in the text variable
		ArrayList<String> wordArrayList = new ArrayList<String>();
		ArrayList<String> subwordArrayList = new ArrayList<String>();
		ArrayList<String> myeduList = new ArrayList<String>();
		Map<String, String> leduMap = new HashMap<String,String>();
		Map<String, Integer> geduMap = new LinkedHashMap<String, Integer>();
		Map<Integer, String> feduMap = new LinkedHashMap< Integer, String>();
		File dir = new File(
				"C:\\Users\\aashu\\Documents\\Github_New\\Project_RSTParser\\train_data\\dev_data\\dev_data\\");
		File[] directoryListing = dir.listFiles();
		if (directoryListing != null) {
			for (File child : directoryListing) {
				if (child.getName().substring(child.getName().lastIndexOf("."))
						.equals(".edus")) {
					feduMap.clear();geduMap.clear();
					System.out.println(child.getName());
					//					String text = new Scanner(child).useDelimiter("\\Z").next();
					Path path = Paths.get("C:\\Users\\aashu\\Documents\\Github_New\\Project_RSTParser\\train_data\\dev_data\\dev_data\\"
							.concat(child
									.getName()
									.substring(
											0,
											child.getName()
											.lastIndexOf("."))
											.concat(".mylasttry_dep")));
					//if( new File ())
					if (Files.exists(path)) {
						continue;
						  // file exist
						}
					PrintWriter out = new PrintWriter(
							"C:\\Users\\aashu\\Documents\\Github_New\\Project_RSTParser\\train_data\\dev_data\\dev_data\\"
							.concat(child
									.getName()
									.substring(
											0,
											child.getName()
											.lastIndexOf("."))
											.concat(".mylasttry_dep")));
					String fname = child.getName();
					int pos = fname.lastIndexOf(".");
					if (pos > 0) {
					    fname = fname.substring(0, pos);
					}

					String dep_temp = "\\train_data\\dev-documents\\" +fname;
					File process = new File(dep_temp);
					String txt_doc = new Scanner(process).useDelimiter("\\Z").next();
					//System.out.println(txt_doc);
					String temp_str = "";
					String buff_temp = "";
					int lcntr = 0, gcntr = 0;
					Map <String, String> headwords = new LinkedHashMap<String,String>();
					Map <String, String> localEDU = new LinkedHashMap<String,String>();
					Map<Integer, String> EDUmapping = new LinkedHashMap<Integer, String>();
					Scanner scanEDU = new Scanner(child);
					int initial=0;
					int counter = 1;
					while(scanEDU.hasNextLine()){
						String temp = scanEDU.nextLine().trim();
						headwords.put(temp, "");
						EDUmapping.put(counter,temp );
						counter ++;
					}
					
					Annotation document = new Annotation(txt_doc);
					pipeline.annotate(document);
					List<CoreMap> sentences = document.get(SentencesAnnotation.class);
					scanEDU = new Scanner(child);
					Scanner scanprev =  new Scanner(child);
					IndexedWord Iwrd = null;
					Set<IndexedWord> parent_wrdset = null;
					int initialEDU  = 1;
					for(CoreMap sentence: sentences) {
						localEDU.clear();
						SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
//						String trimmed = sentence.toString().trim();
//						int words_no = trimmed.isEmpty() ? 0 : trimmed.split("\\s+").length;
						String head = "";
						try{
						head = dependencies.getFirstRoot().toString();
						}
						catch(Exception e){
							
						}
						String tmp = "", tmp1 = "";
						int match = 0; int l = 0;
						for ( l = initialEDU; l<= EDUmapping.keySet().size();l++){
							
							String value = EDUmapping.get(l);
						//	System.out.println(value);
							for (String word : value.split(" ")) {
								tmp = tmp.concat(word);
							}
							for (String word : sentence.toString().trim().split("\\s+")) {
								tmp1 = tmp1.concat(word);
							}
						//	System.out.println(tmp1);
							if(tmp1.contains(tmp)){
								match = 1;
								localEDU.put(value, "");
							}
							else{
								if (match == 1) break;
							}
						}
						initialEDU = l;
						
						scanEDU = scanprev;
						for (String key : localEDU.keySet()) {
							if( key.contains(head.split("/")[0])){
								localEDU.put(key , head.split("/")[0]);
								headwords.put(key,head.split("/")[0] + " %%aashu");
								//feduMap.put(geduMap.get(key), (feduMap.get(geduMap.get(key)) + one_temp.split("/")[0]+" %%aashu"));
							}
						}
						

						for( String key : localEDU.keySet()){
							
							String buff_key = "";
							
							
								
						
							if(localEDU.get(key) ==  ""){
								String tot_buff = "";
								Annotation key_doc = new Annotation(key);
								pipeline.annotate(key_doc);
								List<CoreMap> tempsentences = key_doc
										.get(SentencesAnnotation.class);
								for( CoreMap tempsent : tempsentences){
								for (CoreLabel token : tempsent
										.get(TokensAnnotation.class)) {
									// this is the text of the token
									String word = token.get(TextAnnotation.class);
									buff_key = buff_key.concat(word).concat(" ");
							}
								}
								
								
								for(String word : buff_key.split(" ")) {
									try{
										Iwrd = dependencies.getNodeByWordPattern(word);
									}
									catch( java.util.regex.PatternSyntaxException e){
										
									}
									if (Iwrd == null) continue;
									parent_wrdset = dependencies.getParents(Iwrd);
									if (!parent_wrdset.isEmpty()){
										String buff = "";
										for (IndexedWord elem : parent_wrdset) {
											//System.out.println("elem = " + elem.toString());
											if(buff_key.contains(elem.toString().split("/")[0])) continue;
											buff = buff.concat(word+ " ");
										}
										if (buff != ".")
											tot_buff = tot_buff.concat(buff);
																			}
								}
								headwords.put((key), ( tot_buff+" "));
							}
						}
						
						myeduList.clear();
						wordArrayList.clear();
						leduMap.clear();
						
						


						
						
					}
//					for (int i=1;i < headwords.size(); i++){
//						out.println(headwords.get(i));
//					}
					for (String val : headwords.values()){
						out.println(val);
					}
//					out.println(feduMap.values().size());
					
					out.close();
					
					
				}
			}
			
		}
	}
}
