import java.io.*;
import java.util.*;

public class OrganizeChamps {
    public static void main(String[] args) throws IOException{
        BufferedReader reader = new BufferedReader(new FileReader("listofchamps.txt"));
        String current = "";
        String total = "";
        while ((current = reader.readLine()) != null) {
            total += "\'";
            total += current;
            total += "\', ";
        }
        total = total.substring(0, total.length() - 2);
        PrintWriter writer = new PrintWriter("listofchamps.min", "UTF-8");
        writer.println(total);
        writer.close();
        System.out.println(total);
    }
}