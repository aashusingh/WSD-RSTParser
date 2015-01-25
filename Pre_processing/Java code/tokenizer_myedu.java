package preprocessor_java;;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringReader;
import java.util.List;

import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;

public class tokenizer_myedu {

	public static void main(String[] args) throws IOException {
		// option #1: By sentence.
		// DocumentPreprocessor dp = new DocumentPreprocessor(arg);
		// for (List sentence : dp) {
		// System.out.println(sentence);
		// }
		// option #2: By token

		File dir = new File(
				"\\data\\");
		File[] directoryListing = dir.listFiles();
		if (directoryListing != null) {
			for (File child : directoryListing) {

				// Do something with child
		
				if (child.getName().substring(child.getName().lastIndexOf("."))
						.equals(".edus")) {
					PrintWriter out1 = new PrintWriter(
							"\\data\\"
									.concat(child
											.getName()
											.substring(
													0,
													child.getName()
															.lastIndexOf("."))
											.concat(".myedus")));
					String tokenText="";
					System.out.println(child.getName());
					BufferedReader br = new BufferedReader(
							new FileReader(child));
					String line;

					while ((line = br.readLine()) != null) {
						// process the line.

						PTBTokenizer ptbt = new PTBTokenizer(new StringReader(
								line), new CoreLabelTokenFactory(), "");
						System.out.println("");
						for (CoreLabel label; ptbt.hasNext();) {
							label = (CoreLabel) ptbt.next();
							if(!tokenText.equals("")){
								tokenText=tokenText.concat(" ");
							}
							tokenText=tokenText.concat(label.originalText());
							System.out.println(label);
						}
						tokenText=tokenText.concat("\n");
					}

					System.out.println(tokenText);
					out1.println(tokenText);
					out1.close();
				}
			}
		}
	}
}