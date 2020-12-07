package dmh.iiser;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.pdf.PDFParser;
import org.apache.tika.sax.BodyContentHandler;

import org.xml.sax.SAXException;

public class PdfParse {

    public static void main(final String[] args) {
        try {
            BodyContentHandler handler = new BodyContentHandler();
            Metadata metadata = new Metadata();
            FileInputStream inputstream = new FileInputStream(new File("sales2014.pdf"));
            ParseContext pcontext = new ParseContext();

            //parsing the document using PDF parser
            PDFParser pdfparser = new PDFParser();
            pdfparser.parse(inputstream, handler, metadata, pcontext);

            //getting the content of the document
//            System.out.println("Contents of the PDF :" + handler.toString());

            FileWriter myObj = new FileWriter("output.txt");
//            if(myObj.createNewFile()){
//                System.out.println("file created: " + myObj.getName());
//            }else{
//                System.out.println("file already exists");
//            }

            myObj.write(handler.toString());

            //getting metadata of the document
            System.out.println("Metadata of the PDF:");
            String[] metadataNames = metadata.names();

            for (String name : metadataNames) {
                System.out.println(name + " : " + metadata.get(name));
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
    }
}
